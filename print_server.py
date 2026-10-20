#!/usr/bin/env python3
"""
Photo booth print server.

Runs on a Mac (or Linux / Raspberry Pi with CUPS) on the same Wi-Fi as the iPad
and the Canon SELPHY CP1300. It:
  * serves the booth (index.html) to the iPad over https (Safari only allows the camera on https pages)
  * receives each finished 4x6 sheet and prints it silently with `lp`
  * keeps a copy of every sheet in ./strips/

Usage:
    python3 print_server.py                  # auto-detects the Selphy
    python3 print_server.py --printer NAME   # pick a specific printer queue
    python3 print_server.py --dry-run        # save strips but don't print (for testing)
    python3 print_server.py --list           # show printers and their paper sizes, then exit

No extra Python packages are needed.
"""
import argparse
import datetime
import http.server
import json
import pathlib
import re
import socket
import ssl
import subprocess
import sys
import threading

HERE = pathlib.Path(__file__).resolve().parent
STRIPS = HERE / "strips"
CERT = HERE / "booth-cert.pem"
KEY = HERE / "booth-key.pem"
MAX_UPLOAD = 25 * 1024 * 1024

ARGS = None
PRINTER = None
MEDIA_OPT = None
LOCK = threading.Lock()
COUNT = 0


# ---------------------------------------------------------------- helpers
def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "timed out"


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def list_printers():
    code, out = run(["lpstat", "-e"])
    names = [l.strip() for l in out.splitlines() if l.strip()] if code == 0 else []
    if not names:  # older CUPS
        code, out = run(["lpstat", "-p"])
        names = re.findall(r"^printer (\S+)", out, re.M)
    return names


def pick_printer(hint):
    names = list_printers()
    if hint:
        if hint in names:
            return hint
        for n in names:
            if hint.lower() in n.lower():
                return n
        return None
    for n in names:
        if re.search(r"selphy|cp1300|cp13", n, re.I):
            return n
    code, out = run(["lpstat", "-d"])
    m = re.search(r":\s*(\S+)\s*$", out.strip())
    return m.group(1) if m else (names[0] if names else None)


def page_sizes(printer):
    code, out = run(["lpoptions", "-p", printer, "-l"])
    for line in out.splitlines():
        key = line.split("/", 1)[0].split(":", 1)[0].strip()
        if key in ("PageSize", "media"):
            vals = line.split(":", 1)[1].split()
            return key, [v.lstrip("*") for v in vals]
    return None, []


def pick_media(printer, forced):
    if forced:
        return forced
    key, vals = page_sizes(printer)
    if not key:
        return None
    for pat in (r"postcard", r"4x6", r"100x148", r"101\.6x152"):
        for v in vals:
            if re.search(pat, v, re.I) and not re.search(r"double|duplex", v, re.I):
                return f"{key}={v}"
    return None


def ensure_cert(ip):
    if CERT.exists() and KEY.exists():
        return
    print("Creating a self-signed certificate for https …")
    base = ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
            "-keyout", str(KEY), "-out", str(CERT), "-days", "825",
            "-subj", "/CN=photobooth"]
    code, out = run(base + ["-addext", f"subjectAltName=IP:{ip},DNS:localhost"])
    if code != 0:
        code, out = run(base)
    if code != 0:
        sys.exit("Could not create a certificate with openssl:\n" + out)


def queue_length():
    if not PRINTER:
        return 0
    code, out = run(["lpstat", "-o", PRINTER])
    return len([l for l in out.splitlines() if l.strip()]) if code == 0 else 0


def print_file(path, copies):
    cmd = ["lp", "-d", PRINTER, "-n", str(copies), "-o", f"print-scaling={ARGS.scaling}"]
    if MEDIA_OPT:
        cmd += ["-o", MEDIA_OPT]
    cmd += [str(path)]
    return run(cmd)


# ---------------------------------------------------------------- server
class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "PhotoBooth/1.0"

    def log_message(self, fmt, *a):
        sys.stderr.write("%s  %s\n" % (datetime.datetime.now().strftime("%H:%M:%S"), fmt % a))

    def cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Copies")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def send_json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.cors()
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        files = {"/": ("index.html", "text/html; charset=utf-8"),
                 "/index.html": ("index.html", "text/html; charset=utf-8"),
                 "/sw.js": ("sw.js", "text/javascript"),
                 "/manifest.json": ("manifest.json", "application/manifest+json"),
                 "/icon.png": ("icon.png", "image/png"),
                 "/logo.png": ("logo.png", "image/png"),
                 "/fonts/Inter-Regular.woff": ("fonts/Inter-Regular.woff", "font/woff"),
                 "/fonts/Inter-Medium.woff": ("fonts/Inter-Medium.woff", "font/woff"),
                 "/fonts/Inter-SemiBold.woff": ("fonts/Inter-SemiBold.woff", "font/woff")}
        if path in files:
            name, ctype = files[path]
            body = (HERE / name).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/status":
            self.send_json(200, {"ok": True, "printer": PRINTER, "media": MEDIA_OPT,
                                 "dry_run": ARGS.dry_run, "printed": COUNT, "queue": queue_length()})
        else:
            self.send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        global COUNT
        if self.path.split("?", 1)[0] != "/print":
            return self.send_json(404, {"ok": False, "error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            n = 0
        if n <= 0 or n > MAX_UPLOAD:
            return self.send_json(400, {"ok": False, "error": "bad upload size"})
        data = self.rfile.read(n)
        if not (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n"):
            return self.send_json(400, {"ok": False, "error": "not an image"})
        try:
            copies = max(1, min(5, int(self.headers.get("X-Copies", "1"))))
        except ValueError:
            copies = 1
        ext = ".png" if data[:4] == b"\x89PNG" else ".jpg"
        with LOCK:
            COUNT += 1
            stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            path = STRIPS / f"strip-{stamp}-{COUNT:04d}{ext}"
            path.write_bytes(data)
            if ARGS.dry_run:
                print(f"  saved {path.name} (dry run, not printed)")
                return self.send_json(200, {"ok": True, "file": path.name, "queue": 0, "dry_run": True})
            code, out = print_file(path, copies)
        if code != 0:
            print("  PRINT FAILED:", out.strip())
            return self.send_json(500, {"ok": False, "error": out.strip() or "lp failed"})
        print(f"  printing {path.name} x{copies}: {out.strip()}")
        self.send_json(200, {"ok": True, "file": path.name, "queue": queue_length()})


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    global ARGS, PRINTER, MEDIA_OPT
    ap = argparse.ArgumentParser(description="Photo booth print server")
    ap.add_argument("--printer", help="printer queue name (default: auto-detect Selphy)")
    ap.add_argument("--media", help='paper option to pass to lp, e.g. "PageSize=Postcard"')
    ap.add_argument("--scaling", default="fill", choices=["fill", "fit", "auto", "none"],
                    help="how the 4x6 image is scaled onto the paper (default: fill = borderless)")
    ap.add_argument("--port", type=int, default=8443)
    ap.add_argument("--no-https", action="store_true", help="serve plain http (camera will NOT work on iPad)")
    ap.add_argument("--dry-run", action="store_true", help="save strips but don't print")
    ap.add_argument("--list", action="store_true", help="list printers and paper sizes, then exit")
    ARGS = ap.parse_args()

    if ARGS.list:
        names = list_printers()
        if not names:
            print("No printers found. Add the SELPHY in System Settings › Printers & Scanners first.")
        for n in names:
            key, vals = page_sizes(n)
            print(f"{n}\n   {key}: {' '.join(vals) if vals else '(none reported)'}")
        return

    STRIPS.mkdir(exist_ok=True)
    if not ARGS.dry_run:
        PRINTER = pick_printer(ARGS.printer)
        if not PRINTER:
            sys.exit("No printer found. Add the SELPHY in System Settings › Printers & Scanners, "
                     "or run with --list to see queue names, or --dry-run to test without printing.")
        MEDIA_OPT = pick_media(PRINTER, ARGS.media)

    ip = local_ip()
    httpd = Server(("0.0.0.0", ARGS.port), Handler)
    scheme = "http"
    if not ARGS.no_https:
        ensure_cert(ip)
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(CERT, KEY)
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
        scheme = "https"

    print("\n  ✦ Photo booth print server ✦")
    print(f"  Printer : {PRINTER or '(dry run — not printing)'}")
    print(f"  Paper   : {MEDIA_OPT or '(printer default — set Postcard as default if prints look wrong)'}")
    print(f"  Strips  : {STRIPS}")
    print(f"\n  On the iPad, open:  {scheme}://{ip}:{ARGS.port}/")
    if scheme == "https":
        print("  (Safari will warn the certificate isn't trusted the first time — tap Show Details › visit this website)")
    print("\n  Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nBye ♡")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Loopback-only preview, with Pages-style extensionless routes and custom 404s."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if any(part.startswith('.') for part in Path(path).parts):
            self.send_error(404)
            return
        super().do_GET()

    def translate_path(self, path):
        target = Path(super().translate_path(path))
        if not target.exists() and not target.suffix and target.with_suffix('.html').is_file():
            return str(target.with_suffix('.html'))
        return str(target)

    def list_directory(self, path):
        self.send_error(404)
        return None

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            content = (ROOT / '404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            if self.command != 'HEAD': self.wfile.write(content)
        else:
            super().send_error(code, message, explain)


if __name__ == '__main__':
    print('Preview: http://127.0.0.1:8765', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8765), partial(Handler, directory=str(ROOT))).serve_forever()

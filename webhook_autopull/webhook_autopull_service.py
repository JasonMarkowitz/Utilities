#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import subprocess
import os

# Config
PSK = ''

PORT = 8000
ALLOWED_DIRS = {
    "dir1": "/var/www/htdocs/dir/",
    # Add more mappings as needed
}

ALLOWED_KEYS = {
    "defaultkey": "id_rsa",
    # Add more keys as needed
}

class GitPullHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        psk = self.headers.get('X-PSK')
        if psk != PSK:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden\n")
            return

        query = parse_qs(urlparse(self.path).query)
        dir_key = query.get("dir", [None])[0]
        key_id = query.get("key", [None])[0]

        if dir_key not in ALLOWED_DIRS:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid or missing 'dir' parameter\n")
            return

        if key_id not in ALLOWED_KEYS:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid or missing 'key' parameter\n")
            return

        git_dir = ALLOWED_DIRS[dir_key]
        ssh_key_path = ALLOWED_KEYS[key_id]

        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key_path} -o IdentitiesOnly=yes -o StrictHostKeyChecking=no"

        try:
            result = subprocess.run(
                ["git", "-C", git_dir, "pull"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=True
            )
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Git pull successful\n")
            self.wfile.write(result.stdout)
        except subprocess.CalledProcessError as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Git pull failed\n")
            self.wfile.write(e.stderr)

    def do_GET(self):
        self.send_response(405)
        self.end_headers()
        self.wfile.write(b"GET not allowed\n")

def run():
    server = HTTPServer(('127.0.0.1', PORT), GitPullHandler)
    print(f"Listening on port {PORT}...")
    server.serve_forever()

if __name__ == '__main__':
    run()


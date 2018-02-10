#!/usr/bin/env python2
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json, subprocess

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        try:
            data_dict = json.loads(post_data)
        except Exception as e:
            self.wfile.write('{"status": "error"}')
            return
        print (data_dict) # <-- Print post data
        if u'key' in data_dict:
            if data_dict[u'key'] == u'mysecretkey':
                subprocess.call(["touch", "for_slave/touch_me_to_promote_to_me_master"])
                self.wfile.write('{"status": "ok"}')
            else:
                self.wfile.write('{"status": "error"}')
        else:
            self.wfile.write('{"status": "error"}')

def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

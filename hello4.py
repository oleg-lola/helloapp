#!/home/oleg/.local/bin/python3_virt/bin/python3
"""
Very simple HTTP server in python.
Usage::
    ./hello-server.py [<port>]
version: 2.0
"""
import http.server
import signal
import sys
from os import listdir
from os.path import isfile, join
from os import curdir, sep
import os
import pathlib

target_folder = os.getenv('CREDENTIALS_FOLDER', 'creds')
get_num = 0


def get_credentials(target_folder):
    try:
        path = pathlib.Path(__file__).parent / target_folder
        files = [f for f in listdir(path) if isfile(join(path, f))]
        credentials = {}
        for file in files:
            with open(curdir + sep + target_folder + sep + file, 'r') as procfile:
                content = procfile.read().replace('\n', '')
                procfile.close()
                credentials[file] = content
    except IOError:
        print("Invalid target folder!")
        exit(101)
    return credentials

class SERVER(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_header('Server', 'Not your fkn bussines')
        self.end_headers()

    def do_GET(self):
        global get_num
        get_num += 1
        templ_string = "Hello to you {} times, mr. Anderson! Here is your credentials: {}"
        content = templ_string.format(get_num, get_credentials(target_folder))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self._set_headers()
        self.wfile.write(content.encode())

    def do_HEAD(self):
        self._set_headers()
        self.wfile.write("Stop doing this")


def signal_handler(sig, frame):
    print ("\nStopped.")
    sys.exit(0)


def run(server_class=http.server.HTTPServer, handler_class=SERVER, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    signal.signal(signal.SIGINT, signal_handler)
    print ('HTTP server started')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

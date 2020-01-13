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

get_num = 0


class SERVER(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_header('Server', 'Not your fkn bussines')
        self.end_headers()

    def do_GET(self):
        global get_num
        get_num += 1
        templ_string = 'Hello to you {} times, mr. Andersen!'
        content = templ_string.format(get_num)
        print (content)
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

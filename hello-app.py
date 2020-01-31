#!/home/oleg/.local/bin/python3_virt/bin/python3
"""
Very simple HTTP server in python.
Usage::
    ./hello-server.py [<port>]
"""
import http.server
import signal
import sys
from os import listdir
from os.path import isfile, join
from os import curdir, sep
import os
import pathlib
import redis


target_folder = os.getenv('CREDENTIALS_FOLDER', 'creds')
redis_host = os.getenv('redis_host', 'redis')
# redis_host = os.getenv('redis_host', '127.0.0.1')
get_num = 0
use_redis = False
redis_pool = None
app_version = '1.5'


def redis_init(redis_host):
    print("PID %d: initializing redis pool..." % os.getpid())
    try:
        global redis_pool
        redis_pool = redis.ConnectionPool(host=redis_host, port=6379, db=0)
        # redis_conn = redis.Redis(host=redis_host, port=6379, db=0)
        redis_conn = redis.Redis(connection_pool=redis_pool)
        if redis_conn.ping():
            print('Redis is used and Connected!')
            return True
    except Exception as ex:
        print('Error:', ex, 'Redis is not used!')
        return False


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
        if use_redis:
            red_con = redis.Redis(connection_pool=redis_pool)
            if red_con.get("get_count") is None:
                get_num += 1
                red_con.set("get_count", get_num)
            else:
                get_num = int(red_con.get("get_count")) + 1
                red_con.set("get_count", get_num)
        else:
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
    print("\nStopped.")
    sys.exit(0)


def run(server_class=http.server.HTTPServer, handler_class=SERVER, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    signal.signal(signal.SIGINT, signal_handler)
    global use_redis
    use_redis = redis_init(redis_host)
    print('HTTP server started')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv
    if argv[1] == '--version':
        print(app_version)
        sys.exit(0)
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

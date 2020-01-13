#!/home/oleg/.local/bin/python3_virt/bin/python3
"""
Very simple HTTP server in python.
Usage::
    ./hello-server.py [<port>]
version: 2.0
"""

import os
import redis


target_folder = os.getenv('CREDENTIALS_FOLDER', 'creds')
# redis_host = os.getenv('redis_host', 'redis')
redis_host = os.getenv('redis_host', '127.0.0.1')
get_num = 0
use_redis = False
redis_pool = None


def redis_init(redis_host):
    print("PID %d: initializing redis pool..." % os.getpid())
    try:
        global redis_pool
        redis_pool = redis.ConnectionPool(host=redis_host, port=6379, db=0, decode_responses=True)
        # redis_conn = redis.Redis(host=redis_host, port=6379, db=0)
        redis_conn = redis.Redis(connection_pool=redis_pool)
        if redis_conn.ping():
            print ('Connected!')
            return True
    except Exception as ex:
        print ('Error:', ex)
        return False


use_redis = redis_init(redis_host)
print(use_redis)


#global get_num
red_con = redis.Redis(connection_pool=redis_pool)
print (red_con.get("get_count"))
if use_redis:
    if red_con.get("get_count") is None:
        get_num += 1
        red_con.set("get_count", get_num)
    else:
        get_num = int(red_con.get("get_count")) + 1
        red_con.set("get_count", get_num)
else:
    get_num += 1

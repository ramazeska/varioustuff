# Here be misc funcs and tiny -> little helpers
# maybe someday they'll grow and be a helper class
import base64
import os
import re
import socket


def decodestring(string):
    # decode password
    return base64.b64decode(string).decode('utf-8').strip('\n')


def myenv():
    run_env = os.getenv('RUN_ENV')
    if run_env is None:
        run_env = 'dev'
    return run_env


def match_pattern(pattern, string):
    if type(pattern) == list:
        for pt in pattern:
            if re.match(pt, string):
                return True
        return False
    elif type(pattern) == str:
        if re.match(pattern, string):
            return True
        return False
    return False


def url_ok(url):
    '''
    @param url: expect string in host:port format
    '''
    try:
        host = url.split(':')[0]
        port = int(url.split(':')[1])
        socket.gethostbyname(host)
        socket.create_connection((host, port), 2)
        return url
    except Exception as e:
        print('Url validation failed:', e)
        return False

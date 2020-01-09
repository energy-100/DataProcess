'''
Using ping to scan
'''
import os
import re
import time
import thread


def host_scanner(ip):
    p = os.popen('ping -c 2 ' + ip)
    string = p.read()
    pattern = 'Destination Host Unreachable'
    if re.search(pattern, string) is not None:
        print
        '[*]From ' + ip + ':Destination Host Unreachable!' + time.asctime(time.localtime(time.time()))
        return False
    else:
        print
        '[-]From ' + ip + ':Recived 64 bytes!' + time.asctime(time.localtime(time.time()))
        return True


if __name__ == '__main__':
    print
    'This script is only use as model,function:scanner(ip)!'

'''
'Kernel IP routing table\nDestination     Gateway         Genmask         Flags Metric Ref    Use Iface\n
0.0.0.0         172.16.0.254    0.0.0.0         UG    100    0        0 enp3s0f1\n
172.16.0.0      0.0.0.0         255.255.255.0   U     100    0        0 enp3s0f1\n'
'''

import re
import os
import time
from macSearch import *


def find_Gateway():
    p = os.popen('route -n')
    route_table = p.read()
    pattern = '(0\.0\.0\.0)(\s+)((\d+\.){1,3}(\d+))(\s+)(0\.0\.0\.0)'
    result = re.search(pattern, route_table)
    if result is not None:
        # print '[-]Gateway is located on:' + result.group(3)+'...'+time.asctime( time.localtime(time.time()) )
        table = getMac()
        ip = table[0][0]
        mac = table[1][ip]
        return (ip, mac)
    else:
        # print '[*]arpATC.find_Gateway:result is None!'
        # print '[*]Gateway is no found!'
        return


if __name__ == '__main__':
    print
    '[-]Looking for Gateway...' + time.asctime(time.localtime(time.time()))
    gateway = find_Gateway()
    if gateway is not None:
        print
        '[-]Gateway is located on:' + gateway[0] + '(' + gateway[1] + ')' + '...' + time.asctime(
            time.localtime(time.time()))
    else:
        print
        '[*]Gateway is no found!' + gateway[0] + time.asctime(time.localtime(time.time()))

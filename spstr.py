import re
from datetime import datetime
a="2019- 9-24   9:24:24: 355"

jj="2019- 9-24   9:24:24: 355"
jjj="2019- 9-24   9:26:24: 357"
list=re.split('[- :]\s*',jjj)
# list2=re.split('[- :]\s*',"2019- 9-24   9:26:22: 605 .")
list2=re.split('[- :]\s*',jj)
print(list)
print(list2)
data1=list[0]+"-"+list[1]+"-"+list[2]+"-"+list[3]+"-"+list[4]+"-"+list[5]+"."+list[6]
data2=list2[0]+"-"+list2[1]+"-"+list2[2]+"-"+list2[3]+"-"+list2[4]+"-"+list2[5]+"."+list2[6]
# data2=list2[0]+"-"+list2[1]+"-"+list2[2]+"-"+list2[3]+"-"+list2[4]+"-"+list2[5]

b=datetime.strptime(data1,'%Y-%m-%d-%H-%M-%S.%f')
c=datetime.strptime(data2,'%Y-%m-%d-%H-%M-%S.%f')
print(b)
print(c)
e=(b-c).seconds/60
# print(c.second)
# print(e)
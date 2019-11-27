
import re
# a=[1,2,3,4,5,6,7,8,9]
# print(a)
# a.pop(2)
# print(a)
datapar='56.253'
a=re.search("\d{1,2}\.\d{1,3}",datapar).group(0)
print(a)
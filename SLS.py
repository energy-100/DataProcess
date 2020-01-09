import matplotlib
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
# x=set()
# x.add(1)
# x.add(2)
# x.add(3)
# x.add(3)
# print(x)
# xx=[0,1,5,4,8,5,4,8,7,5,9,4,4,8,2,5]

# def fun1(x, s1, s2, s3):
#     # return s1 * ((1 + (x / s2)) ** (-s3)) + s4
#     return s1+s2 * x + s3*(x**2)
#
# a=[3175,3128,3067,2969,2842,2626,2411,2195]
# b=[7950,8910,9880,10850,11830,12780,13750,14720]
# xfit = np.linspace(2195.0,3175.0, 1000).tolist()
# print(xfit)
# popt, pcov = curve_fit(fun1, a, b,maxfev=500000000)
#
# yfit=[]
# for i in xfit:
#     yfit.append(fun1(i, popt[0], popt[1], popt[2]))
# plt.plot(xfit,yfit)
# plt.scatter(a,b)
# print(popt)
# print(yfit)
# plt.show()

# print([str(i*0.1) for i in range(1,10)])

# x=[1,2,3,1,4,5,6,7,8,5,4]
# y=[1,2,3,1,4,5,6,7,8,5,4]
a={"a",1,"b",2}
# c="b"
# a[c]=3
print(a)
# print(list(zip(x,y)))


class A():
    def __init__(self,x1=["name"],x2={"1","2"}):
        self.x1=x1
        self.x2=x2

if __main__""

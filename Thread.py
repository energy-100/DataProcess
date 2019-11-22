import os
import re
import numpy as np
import xlrd
import xlwt
from scipy.optimize import curve_fit
from datetime import datetime
from xlutils.copy import copy
import copy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class DataRead(QThread):
    sinOut1 = pyqtSignal(str)
    sinOut2 = pyqtSignal(int)
    sinOutvisible = pyqtSignal(bool)
    setonedata=pyqtSignal(str,list)
    def __init__(self,path,parent=None):
        super(DataRead, self).__init__(parent)
        # self.working = True
        self.path=""

    # def __del__(self):
        #线程状态改变与线程终止
        # self.working = False
        # self.wait()
    def run(self):
        #在函数里激发信号
        # while self.working == True:
        self.data.readfiles(self.path,self.sinOut1,self.sinOut2,self.sinOutvisible)
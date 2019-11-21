
import os
import re
import numpy as np
import xlrd
import xlwt
from scipy.optimize import curve_fit
from datetime import datetime
from xlutils.copy import copy
import copy

class dataclass():
    def __init__(self, parent=None):
        self.filepath=""
        self.outpath=""
        self.filename=""
        self.Max=0
        self.Min=0
        self.paras=[]
        self.Interval=0     #每个点的间隔

        self.ACQ_Time=""
        self.ACQ_TimeMinuteCount=""
        self.Project=""
        self.Name=""
        self.Part=""
        self.Operator=""
        self.Desc=""
        self.Excited_Peroid=""
        self.Excited_Time=""
        self.Acq_Delay_Time=""
        self.Gate_Time=""
        self.Count_Num_per_gate=""
        self.Repeat_Times=""            #重复次数
        self.Acq_Gate_Times=""
        self.Interval_per_Gate=""
        self.Channel_Number=""
        # ----------data1--------------
        # 原始数据
        self.Raw_Data1=[]
        #预处理后的数据
        self.Pro_Data1_X = []
        self.Pro_Data1=[]
        # 裁剪数据
        self.Cut_Data1_X=[]
        self.Cut_Data1 = []
        self.Cut_Data1fit_X = []
        self.Cut_Data1fit = []
        #----------data2--------------
        #原始数据
        self.Raw_Data2 = []
        #预处理后的数据
        self.Pro_Data2_X = []
        self.Pro_Data2 = []
        #裁剪数据
        self.Cut_Data2_X=[]
        self.Cut_Data2 = []
        self.Cut_Data2fit_X = []
        self.Cut_Data2fity = []




class dataread():
    def __init__(self,progressBar,statusBar):
        self.progressBar=progressBar
        self.statusBar=statusBar
        self.filelist = dict()
        self.maxCol = 0
        self.filenames=[]
        self.dirList = []
        self.filepath=""
    def readfiles(self,filepath):  #存入数据
        self.progressBar.setVisible(True)
        self.statusBar().showMessage("正在进行数据转换...")
        self.progressBar.setValue(0)
        files = os.listdir(filepath)
        #排除隐藏文件和文件夹
        for f in files:
            if (os.path.isdir(filepath + '/' + f)):
                # 排除隐藏文件夹。因为隐藏文件夹过多
                if (f[0] == '.'):
                    pass
                else:
                    # 添加非隐藏文件夹
                    self.dirList.append(f)
            if (os.path.isfile(filepath + '/' + f)):
                # 添加文件
                if(os.path.splitext(f)[1]==".txt"):
                    self.filenames.append(f)
        p=1
        print(self.filenames)

        for f in self.filenames:
            self.statusBar().showMessage("正在转换 " + str(p) + "/" + str(len(self.filenames)))
            data=dataclass()
            data.filepath=filepath
            datarow = open(filepath + '/' + f)  #读取的整个原始文件数据
            datarowlines = datarow.readlines()      #读取的整个原始文件的数据，按行分割
            datapar=[]                          #真正的每行数据数组
            for line in datarowlines:
                linenew=line.strip()
                if (linenew!=""):
                    datapar.append(linenew)
            # self.ACQ_Time=re.search("(\d{4}-\d{1,2}-\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\s*\d{1,3})",datapar[1])
            temptime=re.search("\d{4}-\s*\d{1,2}-\s*\d{1,2}\s*\d{1,2}:\s*\d{1,2}:\s*\d{1,2}:\s*\d{1,3}",datapar[1]).group(0)
            timelist = re.split('[- :]\s*', temptime)
            # print(timelist)
            timestr=timelist[0] + "-" + timelist[1] + "-" + timelist[2] + "  " + timelist[3] + ":" + timelist[4] + ":" + timelist[5]+"."+timelist[6]
            data.ACQ_Time=datetime.strptime(timestr,'%Y-%m-%d  %H:%M:%S.%f')
            data.Project=datapar[2].strip(datapar[2].split(": ")[0]).strip(": ")
            data.Name=datapar[3].strip(datapar[3].split(": ")[0]).strip(": ")
            data.part=datapar[4].strip(datapar[4].split(": ")[0]).strip(": ")
            data.Operator=datapar[5].strip(datapar[5].split(": ")[0]).strip(": ")
            data.Desc=datapar[6].strip(datapar[6].split(": ")[0]).strip(": ")
            data.Excited_Peroid=int(datapar[9].strip(datapar[9].split(": ")[0]).strip(": "))
            data.Excited_Time=int(datapar[10].strip(datapar[10].split(": ")[0]).strip(": "))
            data.Acq_Delay_Time=int(datapar[11].strip(datapar[11].split(": ")[0]).strip(": "))
            data.Gate_Time=int(datapar[12].strip(datapar[12].split(": ")[0]).strip(": "))
            data.Count_Num_per_gate=int(datapar[13].strip(datapar[13].split(": ")[0]).strip(": "))
            data.Repeat_Times=int(datapar[14].strip(datapar[14].split(": ")[0]).strip(": "))
            data.Acq_Gate_Times=int(datapar[15].strip(datapar[15].split(": ")[0]).strip(": "))
            data.Interval_per_Gate=int(datapar[16].strip(datapar[16].split(": ")[0]).strip(": "))
            data.Channel_Number=int(datapar[17].strip(datapar[17].split(": ")[0]).strip(": "))
            # print(data.ACQ_Time)
            #计算时间，以分钟为单位
            # minutecount=0
            # timelist=re.split('[- :]\s*',data.ACQ_Time)
            # data1 =timelist[0] + "-" + timelist[1] + "-" + timelist[2] + " " + timelist[3] + ":" + timelist[4] + ":" + timelist[5]
            #
            # year=(float(timelist[0])-2019)*364*24*60
            # mouth=(float(timelist[1])-1)*30.5*24*60
            # day=  (float(timelist[2])-1)*24*
            # print(data)

            datanum=int(data.Repeat_Times*data.Count_Num_per_gate)
            data.Pro_Data1=np.zeros(data.Acq_Gate_Times*data.Count_Num_per_gate).tolist()
            # [0 for i in range(data.Acq_Gate_Times*data.Count_Num_per_gate)]
            # print(data.Gate_Time)
            # print("len(data.Raw_Data1)",len(data.Pro_Data1))
            # print("data.Count_Num_per_gate*data.Gate_Time",data.Count_Num_per_gate*data.Gate_Time)


            for i in range(19,19+datanum):
                data.Raw_Data1.append(int(datapar[i]))
            if(data.Channel_Number=="2"):
                for i in range(19+datanum+1,19+datanum+1+datanum):
                    data.Raw_Data2.append(int(datapar[i]))
            # print(len(data.Raw_Data1))
            # print(len(data.Raw_Data2))

            dScale = data.Count_Num_per_gate * 1000/(data.Gate_Time *data.Repeat_Times)
            for i in range(int(data.Acq_Gate_Times)):
                for j in range(int(data.Count_Num_per_gate)):
                    ncps=0
                    for k in range(int(data.Repeat_Times)):
                        ncps += data.Raw_Data1[k * data.Count_Num_per_gate + j+i*datanum]
                    data.Pro_Data1[j * data.Acq_Gate_Times + i] = ncps * dScale
            data.Interval=float(data.Gate_Time)/len(data.Pro_Data1)
            for i in range(len(data.Pro_Data1)):
                data.Pro_Data1_X.append(i*data.Interval)
            # print(data.Pro_Data1)
            data.Max=np.max(data.Pro_Data1)
            data.Min=np.min(data.Pro_Data1)

            #复制原始数据到Cut
            data.Cut_Data1=copy.deepcopy(data.Pro_Data1)
            data.Cut_Data1_X=copy.deepcopy(data.Pro_Data1_X)
            if(len(data.Cut_Data1)>self.maxCol):
                self.maxCol=len(data.Cut_Data1)
            # print("data.Cut_Data1",data.Cut_Data1)
            self.filelist[f]=data

            # print(self.filelist[f].Pro_Data1)
            self.progressBar.setValue(p/len(self.filenames)*100)

            p+=1
        self.progressBar.setVisible(False)
        self.statusBar().showMessage("数据转换成功！")

    def writeXls(self,outpath):
        print(self.filelist)
        workbook = xlwt.Workbook()  # 新建一个工作簿
        sheet = workbook.add_sheet("预处理后的数据")  # 在工作簿中新建一个表格
        i=1
        sheet.write(0, 0, "文件名")
        sheet.write(0, 1, "MAX")
        sheet.write(0, 2, "MIN")
        # for i in range(3,len(value.Pro_Data1)+3):
        #     sheet.write(0, i, i)

        for key,value in self.filelist.items():
            j=0
            sheet.write(i, 0, key)  # 像表格中写入数据（对应的行和列）
            sheet.write(i, 1, value.Max)  # 像表格中写入数据（对应的行和列）
            sheet.write(i, 2, value.Min)  # 像表格中写入数据（对应的行和列）
            for j in range(3,len(value.Pro_Data1)+3):
                sheet.write(i, j, value.Pro_Data1[j-3])  # 像表格中写入数据（对应的行和列）
                j+=1
            i+=1
        print(outpath)
        print(not (os.path.exists(outpath)))
        print(os.path.exists(outpath))
        if( not (os.path.exists(outpath))):
            os.makedirs(outpath)
        try:
            workbook.save(outpath+"/预处理后的数据.xls")  # 保存工作簿
        except Exception as a:
            print(a)
        print("xls格式表格写入数据成功！")

    def Fitting(self,filename=""):
        def getIndexes(y_predict, y_data):
            y_predict = np.array(y_predict)
            y_data = np.array(y_data)
            n = y_data.size
            # SSE为和方差
            SSE = ((y_data - y_predict) ** 2).sum()
            # MSE为均方差
            MSE = SSE / n
            # RMSE为均方根,越接近0，拟合效果越好
            RMSE = np.sqrt(MSE)

            # 求R方，0<=R<=1，越靠近1,拟合效果越好
            u = y_data.mean()
            SST = ((y_data - u) ** 2).sum()
            SSR = SST - SSE
            R_square = SSR / SST
            return SSE, MSE, RMSE, R_square

        def fun1(x, s1, s2, s3, s4):
            return s1 * ((1 + (x / s2)) ** (-s3)) + s4

        if(filename==""):
            self.progressBar.setVisible(True)
            p=1

            for datakey in self.filelist:
                self.statusBar().showMessage("正在拟合 " + str(p) + "/" + str(len(self.filenames)))
                data=self.filelist[datakey]
                try:
                    popt, pcov = curve_fit(fun1, data.Pro_Data1_X, data.Pro_Data1,maxfev=500000)
                except Exception as a:
                    print(a)
                data.paras=popt
                data.Cut_Data1fit_X = np.linspace(data.Pro_Data1_X[0], data.Pro_Data1_X[-1], 1000).tolist()
                data.Cut_Data1fit = fun1(data.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
                print(data.Cut_Data1fit)
                self.progressBar.setValue(p / len(self.filenames) * 100)
                p=p+1
        self.progressBar.setVisible(False)
        self.statusBar().showMessage("数据拟合成功！")











if __name__ == '__main__':
    a=dataread()
    a.readfiles("C:/Users/ENERGY/Desktop/工作文件/test")
    a.writeXls("C:/Users/ENERGY/Desktop/工作文件/test")







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
        self.paras=dict()
        # self.paras["双曲线拟合"]=[-1,-1,-1,-1]
        # self.paras["指数拟合"]=[-1,-1,-1]
        # self.paras["双曲线积分拟合"]=[-1,-1,-1,-1]
        # self.paras["指数积分拟合"]=[-1,-1,-1]
        self.paras["双曲线拟合"]=["","","",""]
        self.paras["指数拟合"]=["","",""]
        self.paras["双曲线积分拟合"]=["","","",""]
        self.paras["指数积分拟合"]=["","",""]
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
        self.Pro_mal1=[]    #每个数据点的子数据矩阵
        self.Pro_Data1_X = []
        self.Pro_Data1=[]
        # 裁剪数据
        self.cutstartnum1=0
        self.cutendnum1=0       #最后一个数据点的序号
        self.Cut_Data1_X=[]
        self.Cut_Data1 = []
        self.Cut_Data1fit_X = []
        self.Cut_Data1fit = []
        #----------data2--------------
        #原始数据
        self.Raw_Data2 = []

        #预处理后的数据
        self.Pro_mal2 = []
        self.Pro_Data2_X = []
        self.Pro_Data2 = []
        #裁剪数据
        self.cutstartnum2=0
        self.cutendnum2=0
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
        # print(self.filenames)

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
                    ncpslist=[]
                    for k in range(int(data.Repeat_Times)):
                        ncps += data.Raw_Data1[k * data.Count_Num_per_gate + j+i*datanum]
                        ncpslist.append(data.Raw_Data1[k * data.Count_Num_per_gate + j+i*datanum])
                    data.Pro_mal1.append(ncpslist)
                    data.Pro_Data1[j * data.Acq_Gate_Times + i] = ncps * dScale
            data.Interval=float(data.Gate_Time)/len(data.Pro_Data1)
            # print("data.Interval",data.Interval)
            for i in range(len(data.Pro_Data1)):
                data.Pro_Data1_X.append(round(i*data.Interval,5))
            # print(data.Pro_Data1)
            data.Max=np.max(data.Pro_Data1)
            data.Min=np.min(data.Pro_Data1)
            data.cutendnum1=len(data.Pro_Data1)-1
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
            self.statusBar().showMessage("完成！")
        self.progressBar.setVisible(False)
        self.statusBar().showMessage("数据转换成功！")

    def writeXls(self,outpath):

        #_________颜色样式__________________
        style1 = xlwt.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']  # 设置单元格背景色为黄色
        style1.pattern = pattern
        #_________颜色样式__________________
        style2 = xlwt.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['green']  # 设置单元格背景色为黄色
        style2.pattern = pattern
        #_________颜色样式__________________
        style3 = xlwt.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['red']  # 设置单元格背景色为黄色
        style3.pattern = pattern

        # _________颜色样式__________________
        style4 = xlwt.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # 设置单元格背景色为黄色
        style4.pattern = pattern

        print(self.filelist)
        workbook = xlwt.Workbook()  #表

        sheetpars = workbook.add_sheet("参数数据")  #参数数据表
        Prodata = workbook.add_sheet("预处理后的数据")  #预处理后的数据表
        cutdata= workbook.add_sheet("裁剪后后的数据")  #预处理后的数据表
        inf =   workbook.add_sheet("文件信息")  #预处理后的数据表
        datamat = workbook.add_sheet("子数据矩阵")  # 子数据矩阵表

        filenamelen=self.countlen(list(self.filelist.keys()))
        Prodata.write(0, 0, "文件名")
        cutdata.write(0, 0, "文件名")
        # for i in range(len(self.filelist.)):
        #     Prodata.write(0, i+1, str(i+1))
        #     cutdata.write(0, i+1, str(i+1))

        sheetpars.write(0, 0, "文件名")
        sheetpars.write(0, 1, "Max")
        sheetpars.write(0, 2, "Min")
        sheetpars.write(0, 3, "ACQ_Time")
        sheetpars.write(0, 4, "(双曲线)I_0")
        sheetpars.write(0, 5, "(双曲线)τ")
        sheetpars.write(0, 6, "(双曲线)Γ")
        sheetpars.write(0, 7, "(双曲线)D")
        sheetpars.write(0, 8, "(指数)I_0")
        sheetpars.write(0, 9, "(指数)τ")
        sheetpars.write(0, 10, "(指数)D")
        sheetpars.write(0, 11, "(双曲线积分)I_0")
        sheetpars.write(0, 12, "(双曲线积分)τ")
        sheetpars.write(0, 13, "(双曲线积分)Γ")
        sheetpars.write(0, 14, "(双曲线)D")
        sheetpars.write(0, 15, "(指数积分)I_0")
        sheetpars.write(0, 16, "(指数积分)τ")
        sheetpars.write(0, 17, "(指数)D")

        sheetpars.col(0).width=filenamelen*256
        sheetpars.col(3).width=28*256
        for i in range(4,18):
            sheetpars.col(i).width = self.countlen("(双曲线积分)I_0") * 256

        i = 1
        for key,value in self.filelist.items():
            sheetpars.write(i, 0, key)  # 像表格中写入数据（对应的行和列）
            sheetpars.write(i, 1, value.Max)  # 像表格中写入数据（对应的行和列）
            sheetpars.write(i, 2, value.Min)  # 像表格中写入数据（对应的行和列）
            sheetpars.write(i, 3, value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f'))  # 像表格中写入数据（对应的行和列）
            j=4
            for para in value.paras["双曲线拟合"]:
                print(para)
                if(para!=""):
                    para=round(para,3)
                sheetpars.write(i, j, str(para), style=style1)
                j+=1
            for para in value.paras["指数拟合"]:
                print(para)
                if (para != ""):
                    para = round(para, 3)
                sheetpars.write(i, j, str(para), style=style2)
                j+=1
            for para in value.paras["双曲线积分拟合"]:
                if (para != ""):
                    para = round(para, 3)
                sheetpars.write(i, j, str(para), style=style3)
                print(para)
                j+=1
            for para in value.paras["指数积分拟合"]:
                if (para != ""):
                    para = round(para, 3)
                sheetpars.write(i, j, str(para), style=style4)
                print(para)
                j+=1


            #保存预处理后的数据
            Prodata.write(i, 0, key)
            Prodata.col(0).width = filenamelen * 256
            z=1
            for spot in value.Pro_Data1:
                Prodata.write(i, z, str(spot))
                z+=1

            # 保存预剪切后的数据
            cutdata.write(i, 0, key)
            cutdata.col(0).width = filenamelen * 256
            z = 1
            print(value.cutstartnum1)
            print(value.cutendnum1 + 1)
            for spot in value.Pro_Data1[value.cutstartnum1:value.cutendnum1+1]:
                cutdata.write(i, z, str(spot))
                z += 1
            i += 1

        # 文件信息
        inf.write(0, 0, "文件名")
        inf.write(0, 1, "ACQ_Time")
        inf.write(0, 2, "Project")
        inf.write(0, 3, "Name")
        inf.write(0, 4, "Part")
        inf.write(0, 5, "Operator")
        inf.write(0, 6, "Desc")
        inf.write(0, 7, "Excited_Peroid(ms)")
        inf.write(0, 8, "Excited_Time(ms)")
        inf.write(0, 9, "Acq_Delay_Time(ms)")
        inf.write(0, 10, "Gate_Time(ms)")
        inf.write(0, 11, "Count_Num_per_gate")
        inf.write(0, 12, "Repeat_Times")
        inf.write(0, 13, "Acq_Gate_Times")
        inf.write(0, 14, "Interval_per_Gate(ms)")
        inf.write(0, 15, "Channel_Number")
        print(type(inf))

        inf.col(0).width=self.countlen(list(self.filelist.keys()))*256
        inf.col(1).width = 28* 256
        inf.col(2).width = self.countlen("Project")* 256
        inf.col(3).width = self.countlen("Name  ")* 256
        inf.col(4).width = self.countlen("Part  ")* 256
        inf.col(5).width = self.countlen("Operator")* 256
        inf.col(6).width = self.countlen("Desc ")* 256
        inf.col(7).width = self.countlen("Excited_Peroid(ms)")* 256
        inf.col(8).width = self.countlen("Excited_Time(ms)")* 256
        inf.col(9).width = self.countlen("Acq_Delay_Time(ms)")* 256
        inf.col(10).width = self.countlen("Gate_Time(ms)")* 256
        inf.col(11).width = self.countlen("Count_Num_per_gate")* 256
        inf.col(12).width = self.countlen("Repeat_Times")* 256
        inf.col(13).width = self.countlen("Acq_Gate_Times")* 256
        inf.col(14).width = self.countlen("Interval_per_Gate(ms)")* 256
        inf.col(15).width = self.countlen("Channel_Number")* 256




        # for i in range(0,16):
            # inf.col(i).width=256*(len(inf.cell(0,i).value.encode('utf-8').encode()))
            # print(len(inf.cell(0,i).value.encode('utf-8').encode()))




        i=1
        for key, value in self.filelist.items():
            inf.write(i, 0,str(key))
            inf.write(i, 1,str(value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
            inf.write(i, 2,str(value.Project))
            inf.write(i, 3,str(value.Name))
            inf.write(i, 4,str(value.Part))
            inf.write(i, 5,str(value.Operator))
            inf.write(i, 6,str(value.Desc))
            inf.write(i, 7,str(round(value.Excited_Peroid,2)))
            inf.write(i, 8,str(round(value.Excited_Time,2)))
            inf.write(i, 9,str(round(value.Acq_Delay_Time,2)))
            inf.write(i, 10,str(round(value.Gate_Time,2)))
            inf.write(i, 11,str(round(value.Count_Num_per_gate,2)))
            inf.write(i, 12,str(round(value.Repeat_Times,2)))
            inf.write(i, 13,str(round(value.Acq_Gate_Times,2)))
            inf.write(i, 14,str(round(value.Interval_per_Gate,2)))
            inf.write(i, 15,str(round(value.Channel_Number,2)))
            i+=1




        print(outpath)
        print(not (os.path.exists(outpath)))
        print(os.path.exists(outpath))
        if( not (os.path.exists(outpath+ "/预处理后的数据.xls"))):
            if( not os.path.exists(outpath)):
                os.makedirs(outpath)
            # os.mknod(outpath+"/预处理后的数据.xls")
            workbook.save(outpath + "/预处理后的数据.xls")  # 保存工作簿
            self.statusBar().showMessage("数据保存成功！(首次保存，已创建目录及文件)")
        else:
            try:
                os.remove(outpath+"/预处理后的数据.xls")
            except Exception as a:
                self.statusBar().showMessage("保存失败！(文件被占用，请关闭关闭文件后重试)")
                print(a)
            else:
                workbook.save(outpath+"/预处理后的数据.xls")  # 保存工作簿
                print("xls格式表格写入数据成功！")
                self.statusBar().showMessage("数据保存成功！(数据文件存在，已覆盖原数据文件)")





    def Fitting(self,funtype,filename=""):

        param_bounds1 = ([0, 0, 0, 0], [999999999, 999999999, 999999999, 999999999])
        param_bounds2 = ([0, 1, 0 ], [999999999, 9999999999, 9999999999])
        param_bounds3 = ([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf])
        param_bounds4 = ([0, 0, 0 ], [np.inf, np.inf, np.inf])


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
            # return s1 * ((1 + (x / s2)) ** (-s3)) + s4
            return s1 * (np.power((1 + (x / s2))  , -s3)) + s4

        def fun2(x, s1, s2, s3):
            return s1 * (np.exp(-(x/ s2))) +s3

        def fun3(x, s1, s2, s3, s4):
            temp1spot = (1 / (1 + np.asarray(x) / s2)) ** (s3 - 1)
            temp2spot = (1 / (1 + (np.asarray(x) + TimeSpan) / s2)) ** (s3 - 1)
            yfitspot = s1 * s2 * (1 / (s3 - 1)) * (temp1spot - temp2spot) + s4 * TimeSpan

        def fun4(x, s1, s2, s3):
            temp1spot = np.exp(-np.asarray(x) / s2)
            temp2spot = np.exp(-(np.asarray(x) + TimeSpan) / s2)
            yfitspot = s1 * s2 * (temp1spot - temp2spot) + s3 * TimeSpan



        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)
        if(filename==""):

            p=1
            for key,value in self.filelist.items():

                x=value.Pro_Data1_X[value.cutstartnum1:value.cutendnum1+1]
                y=value.Pro_Data1[value.cutstartnum1:value.cutendnum1+1]


                # print("x:",x)
                # print("y:",y)
                value.Cut_Data1fit_X = np.linspace(value.Pro_Data1_X[value.cutstartnum1],value.Pro_Data1_X[value.cutendnum1], 1000).tolist()
                if(funtype==1):
                    self.statusBar().showMessage("正在进行双曲线拟合 " + str(p) + "/" + str(len(self.filenames)))
                    popt, pcov = curve_fit(fun1, x, y,maxfev=500000,bounds=param_bounds1)
                    value.paras["双曲线拟合"]=popt
                    value.Cut_Data1fit = fun1(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
                elif(funtype==2):
                    # print(key)
                    self.statusBar().showMessage("正在进行指数拟合 " + str(p) + "/" + str(len(self.filenames)))
                    #
                    # print(x)
                    # print(y)
                    try:
                        popt, pcov = curve_fit(fun2, x, y,maxfev=50000000,bounds=param_bounds2)
                    except Exception as a:
                        print(a)
                    value.paras["指数拟合"] = popt
                    value.Cut_Data1fit = fun2(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
                elif(funtype==3):
                    self.statusBar().showMessage("正在进行双曲线积分拟合 " + str(p) + "/" + str(len(self.filenames)))
                    popt, pcov = curve_fit(fun3, x, y,maxfev=500000,bounds=param_bounds3)
                    value.paras["双曲线积分拟合"] = popt
                    value.Cut_Data1fit = fun3(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
                elif(funtype==4):
                    self.statusBar().showMessage("正在进行指数积分拟合 " + str(p) + "/" + str(len(self.filenames)))
                    popt, pcov = curve_fit(fun4, x, y,maxfev=500000,bounds=param_bounds4)
                    value.paras["指数积分拟合"] = popt
                    value.Cut_Data1fit = fun4(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])




                # print(value.Cut_Data1fit)
                self.statusBar().showMessage("正在拟合"+str(p)+"/"+str(len(self.filelist))+"  "+key)
                print("正在拟合",str(p))
                self.progressBar.setValue(p / len(self.filenames) * 100)
                p=p+1
        else:
            try:
                value = self.filelist[filename]
            except Exception as a:
                print("2222222")
                print(a)
            TimeSpan = value.Gate_Time
            x = value.Pro_Data1_X[value.cutstartnum1:value.cutendnum1 + 1]
            y = value.Pro_Data1[value.cutstartnum1:value.cutendnum1 + 1]
            value.Cut_Data1fit_X = np.linspace(value.Pro_Data1_X[value.cutstartnum1],value.Pro_Data1_X[value.cutendnum1], 1000).tolist()
            try:
                if (funtype == 1):
                    # print(value)
                    # print(x)
                    # print(y)
                    popt, pcov = curve_fit(fun1, x, y, maxfev=500000, bounds=param_bounds1)
                    value.paras["双曲线拟合"] = popt
                    value.Cut_Data1fit = fun1(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
                elif (funtype == 2):
                    # print(value)
                    # print(x)
                    # print(y)
                    popt, pcov = curve_fit(fun2, x, y, maxfev=500000, bounds=param_bounds2)
                    value.paras["指数拟合"] = popt
                    value.Cut_Data1fit = fun2(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])
                elif (funtype == 3):
                    popt, pcov = curve_fit(fun3, x, y, maxfev=500000, bounds=param_bounds3)
                    value.paras["双曲线积分拟合"] = popt
                    value.Cut_Data1fit = fun3(value.Cut_Data1fit_X, popt[0], popt[1], popt[2], popt[3])
                elif (funtype == 4):
                    popt, pcov = curve_fit(fun4, x, y, maxfev=500000, bounds=param_bounds4)
                    value.paras["指数积分拟合"] = popt
                    value.Cut_Data1fit = fun4(value.Cut_Data1fit_X, popt[0], popt[1], popt[2])

                popt, pcov = curve_fit(fun1, x, y, maxfev=500000, bounds=param_bounds1)
            except Exception as a:
                print(a)
        self.progressBar.setValue(100)
        self.progressBar.setVisible(False)
        self.statusBar().showMessage(filename+"文件数据拟合成功！")

    def cutdata(self,numstart,numend,filename):

        # 单文件
        print(filename)
        if (filename != "批量裁剪"):
            index = filename.find("]")
            title = filename[(index + 1):]
            self.filelist[title].cutstartnum1=numstart
            self.filelist[title].cutendnum1=len(self.filelist[title].Pro_Data1)-numend-1
            # print("numstart",self.filelist[title].cutstartnum1)
            # print("numend",self.filelist[title].cutendnum1)
            self.statusBar().showMessage(
                "已经移除 " + filename + " 文件的前" + str(numstart) + "后" + str(numend)+"个数据点,并更新数据的区间内最值")
            self.countparas(title)


        #批处理
        else:
            # self.filelist[filename].cutstartnum1=numstart
            # self.filelist[filename].cutendnum1=len(self.filelist[filename].Pro_Data1)-numend-1
            p = 1
            for key, value in self.filelist.items():
                value.cutstartnum1=numstart
                value.cutendnum1=len(self.filelist[key].Pro_Data1)-numend-1
                # for i in range(numstart):
                #     value.Cut_Data1_X.pop(0)
                #     value.Cut_Data1.pop(0)
                p += 1

                # value.Max = np.max(value.Cut_Data1)
                # value.Min = np.min(value.Cut_Data1)
                self.countparas(key)
            self.statusBar().showMessage("已经移除所有文件的前" + str(numstart) + "后" + str(numend)+"个数据点,并更新数据的区间内最值")


    def countparas(self,filename):
        numstart=self.filelist[filename].cutstartnum1
        numend=self.filelist[filename].cutendnum1
        self.filelist[filename].Max = np.max(self.filelist[filename].Pro_Data1[numstart:numend+1])
        self.filelist[filename].Min = np.min(self.filelist[filename].Pro_Data1[numstart:numend+1])



    def countlen(self,x):
        if type(x)==list:
            max=0
            for str in x:
               if (len(str.encode())>max):
                   max=len(str.encode())
            return max+1
        else:
            return len(x.encode())+1






if __name__ == '__main__':
    a=dataread()
    a.readfiles("C:/Users/ENERGY/Desktop/工作文件/test")
    a.writeXls("C:/Users/ENERGY/Desktop/工作文件/test")






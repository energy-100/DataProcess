import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from Mydemo import*
from dataread import*
from PyQt5 import QtCore
class main (QMainWindow):
    def __init__(self, parent=None):
        self.inpath=""
        self.outpath=""
        self.imagenName=''

        super(main, self).__init__(parent)
        self.setWindowTitle('人体延迟发光数据画图软件 V2.0')
        self.setWindowIcon(QIcon('xyjk.png'))
        self.setFont(QFont("Microsoft YaHei", 12))
        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        self.statusBar().addPermanentWidget(self.progressBar)

        self.resize(900, 600)
        self.tab=QTabWidget()
        self.grid = QGridLayout(self)
        self.figure = Mydemo(width=10, height=2, dpi=100)
        self.grid.addWidget(self.figure, 0, 3, 4, 12)

        self.label1=QLabel("文件列表：")
        self.grid.addWidget(self.label1, 2, 0, 1, 3)

        self.label2 = QLabel("转换后的列表(右键选择复制类型)：")
        self.grid.addWidget(self.label2, 4, 0, 1, 10)

        self.label3 = QLabel("数据子矩阵：")
        # self.grid.addWidget(self.label3, 4, 10, 1, 5)

        self.Table1=QListWidget()
        self.grid.addWidget(self.Table1, 3, 0, 1, 3)

        self.Table2=QTableWidget()
        self.Table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table2.horizontalHeader().sectionClicked.connect(self.Table2HorizontalHeaderClick)
        self.Table2.verticalHeader().sectionClicked.connect(self.Table2VerticalHeaderClick)
        self.Table2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Table2.customContextMenuRequested.connect(self.generateMenu2)
        self.grid.addWidget(self.Table2, 5, 0, 1, 10)


        self.Table3=QTableWidget()
        self.Table3.horizontalHeader().sectionClicked.connect(self.Table3HorizontalHeaderClick)
        self.Table3.verticalHeader().sectionClicked.connect(self.Table3VerticalHeaderClick)
        self.Table3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.grid.addWidget(self.Table3, 5, 10, 1, 5)

        self.Table4=QTableWidget()
        # self.Table4.horizontalHeader().sectionClicked.connect(self.Table4HorizontalHeaderClick)
        # self.Table4.verticalHeader().sectionClicked.connect(self.Table4VerticalHeaderClick)
        self.Table4.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.grid.addWidget(self.Table3, 5, 10, 1, 5)

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.Table4, "拟合参数列表")
        self.tabWidget.addTab(self.Table3, "数据子矩阵")

        self.grid.addWidget(self.tabWidget, 4, 10, 2, 5)

        self.readfileButton=QPushButton("读取并转换")
        self.grid.addWidget(self.readfileButton,0,0,1,1)
        self.readfileButton.clicked.connect(lambda: self.readfileButtonclicked())

        self.inLineEdit = QLineEdit(self)
        self.inLineEdit.returnPressed.connect(lambda: self.inLineEditfinished())
        self.grid.addWidget(self.inLineEdit, 0, 1, 1, 2)


        self.outfileButton=QPushButton("输出文件夹")
        self.grid.addWidget(self.outfileButton,1,0,1,1)
        self.outfileButton.clicked.connect(lambda: self.outfileButtonclicked())

        self.outLineEdit = QLineEdit(self)
        self.outLineEdit.returnPressed.connect(lambda: self.outLineEditfinished())
        self.grid.addWidget(self.outLineEdit, 1, 1, 1, 2)

        self.cutButton = QPushButton("数据裁剪")
        self.grid.addWidget(self.cutButton, 6, 7, 1, 1)
        self.cutButton.clicked.connect(lambda: self.cutButtonlicked())




        self.fitButton = QPushButton("数据拟合")
        self.grid.addWidget(self.fitButton, 7, 8, 1, 1)
        self.fitButton.clicked.connect(lambda: self.fitButtonlicked())



        self.saveImageButton=QPushButton("保存图片")
        self.grid.addWidget(self.saveImageButton,6,13,1,1)
        self.saveImageButton.clicked.connect(lambda: self.saveImageButtonlicked())

        self.savefileButton=QPushButton("保存数据")
        self.grid.addWidget(self.savefileButton,6,14,1,1)
        self.savefileButton.clicked.connect(lambda: self.savefileButtonclicked())

        self.savefilesonButton = QPushButton("保存子矩阵")
        self.grid.addWidget(self.savefilesonButton, 7, 14, 1, 1)
        self.savefilesonButton.clicked.connect(lambda: self.savefilesonButtonclicked())

        self.cutstartlabel = QLabel("删除数据个数(前):")
        self.cutstartlabel.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.cutstartlabel, 6, 0, 1, 1)

        self.cutendlabel = QLabel("删除数据个数(后):")
        self.cutendlabel.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.cutendlabel, 6, 2, 1, 1)

        self.cutlabel = QLabel("裁剪模式:")
        self.cutlabel.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.cutlabel, 6, 4, 1, 1)


        self.cuttypeComboBox = QComboBox()
        self.cuttypeComboBox.addItems(
            ["批量裁剪"])
        # self.cuttypeComboBox.setCurrentIndex(0)
        # self.cuttypeComboBox.currentIndexChanged.connect(lambda: self.ChangedcuttypeComboBox())
        self.grid.addWidget(self.cuttypeComboBox, 6, 5, 1, 2)


        self.fitlabel = QLabel("拟合模式:")
        self.fitlabel.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.fitlabel, 7, 0, 1, 1)

        self.fitComboBox = QComboBox()
        self.fitComboBox.addItems(
            ["批量拟合"])
        # self.fitComboBox.setCurrentIndex(0)
        # self.fitComboBox.currentIndexChanged.connect(lambda: self.ChangedfitComboBox())
        self.grid.addWidget(self.fitComboBox, 7, 1, 1, 2)

        ComBoxlist=[str(i) for i in range(0,101)]
        # ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
        #  "20"]
        self.cutComboBoxstart = QComboBox()
        self.cutComboBoxstart.addItems(ComBoxlist)
        self.cutComboBoxstart.setCurrentIndex(0)
        # self.cutComboBoxstart.currentIndexChanged.connect(lambda: self.ChangedcutComboBoxstart())
        self.grid.addWidget(self.cutComboBoxstart, 6, 1, 1, 1)

        self.cutComboBoxend = QComboBox()
        self.cutComboBoxend.addItems(ComBoxlist)
        self.cutComboBoxend.setCurrentIndex(0)
        # self.cutComboBoxend.currentIndexChanged.connect(lambda: self.ChangedcutComboBoxend())
        self.grid.addWidget(self.cutComboBoxend, 6, 3, 1, 1)

        #函数拟合符复选框
        self.cb1 = QCheckBox('双曲',self)
        self.grid.addWidget(self.cb1, 7, 3, 1, 1)
        self.cb2 = QCheckBox('指数',self)
        self.grid.addWidget(self.cb2, 7, 4, 1, 1)
        self.cb3 = QCheckBox('双曲积分',self)
        self.grid.addWidget(self.cb3, 7, 5, 1, 1)
        self.cb4 = QCheckBox('指数积分',self)
        self.grid.addWidget(self.cb4, 7, 6, 1, 1)

        self.cb1ComboBoxstart = QComboBox()
        self.cb1ComboBoxstart.addItems(["trf", "dogbox"])
        # self.cb1ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        self.grid.addWidget(self.cb1ComboBoxstart, 8, 3, 1, 1)

        self.cb2ComboBoxstart = QComboBox()
        self.cb2ComboBoxstart.addItems(["trf", "dogbox"])
        # self.cb2ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        self.grid.addWidget(self.cb2ComboBoxstart, 8, 4, 1, 1)

        self.cb3ComboBoxstart = QComboBox()
        self.cb3ComboBoxstart.addItems(["trf", "dogbox"])
        # self.cb3ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        self.grid.addWidget(self.cb3ComboBoxstart, 8, 5, 1, 1)

        self.cb4ComboBoxstart = QComboBox()
        self.cb4ComboBoxstart.addItems(["trf", "dogbox"])
        # self.cb4ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        self.grid.addWidget(self.cb4ComboBoxstart, 8, 6, 1, 1)

        self.widget=QWidget()
        self.widget.setLayout(self.grid)
        self.tab.addTab(self.widget,"数据预处理")
        self.setCentralWidget(self.tab)
        self.data=""




    def readfileButtonclicked(self):
        self.data = dataread(self.progressBar, self.statusBar)
        self.statusBar().showMessage("正在选择文件夹...")
        path = QFileDialog.getExistingDirectory(self, "请选择数据文件的根目录")
        # path = "C:/Users/ENERGY/Desktop/工作文件/test"
        # path = "C:/Users/ENERGY/Desktop/工作文件/lhy"
        if path=="":
            self.statusBar().showMessage("未选择文件夹！")
        elif(path==self.inpath):
            self.statusBar().showMessage("读取文件夹位置未改变！")
        else:
            self.data.readfiles(path)
            self.statusBar().showMessage("文件读取成功，正在加载数据！")
            keys=self.data.filelist
            self.Table1.addItems(keys)
            self.inLineEdit.blockSignals(True)
            self.inLineEdit.setText(path)
            self.inLineEdit.blockSignals(False)
            self.inpath=path
            self.outpath=path+"/预处理后的数据"
            self.outLineEdit.blockSignals(True)
            self.outLineEdit.setText(self.outpath)
            self.outLineEdit.blockSignals(False)
            i=0
            self.Table2.setRowCount(len(self.data.filelist))
            # self.Table2.setColumnCount(self.data.maxCol+4)
            self.Table2.setColumnCount(4)
            t2=["文件名","Max","Min","ACQ_Time"]
            # for z in range(self.data.maxCol):
                # t2.append(str(z))
            print(t2)
            print("正在写入标题")
            self.Table2.setHorizontalHeaderLabels(t2)
            print(self.data.maxCol)
            print("输出数据")
            for key in self.data.filelist:
                # print("迭代",i)
                # print(self.data.filelist[key].Cut_Data1)
                self.Table2.setItem(i,0,QTableWidgetItem(key))
                self.Table2.setItem(i,1,QTableWidgetItem(str(self.data.filelist[key].Max)))
                self.Table2.setItem(i,2,QTableWidgetItem(str(self.data.filelist[key].Min)))
                self.Table2.setItem(i,3,QTableWidgetItem(self.data.filelist[key].ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
                # print()

                # for j in range(len(self.data.filelist[key].Cut_Data1)):
                #     self.Table2.setItem(i, j+4, QTableWidgetItem(str(int(self.data.filelist[key].Cut_Data1[j]))))
                    # print(self.data.filelist[key].Cut_Data1[j])
                    # j+=1
                i+=1
            self.statusBar().showMessage("已读取并转换"+str(len(self.data.filelist))+"个数据！")


    def outfileButtonclicked(self):
        self.statusBar().showMessage("正在输出文件夹...")
        path = QFileDialog.getExistingDirectory(self, "请选择数据文件的根目录")
        # path = "C:/Users/ENERGY/Desktop/工作文件/test"
        if path!="":
            self.outpath=path+"/预处理后的数据"
            self.outLineEdit.setText(self.outpath)

    def inLineEditfinished(self):
        path=self.inLineEdit.text()
        if(not(os.path.exists(path))):
            self.statusBar().showMessage("文件夹不存在，请重新输入！")
        elif (path == self.inpath):
            self.statusBar().showMessage("读取文件夹位置未改变！")
        else:
            self.data.readfiles(path)
            keys=self.data.filelist
            self.Table1.addItems(keys)
            self.inLineEdit.setText(path)
            self.outpath=path+"/预处理后的数据/"
            self.outLineEdit.setText(self.outpath)
            i=0
            self.Table2.setRowCount(len(self.data.filelist))
            self.Table2.setColumnCount(self.data.maxCol+3)
            t2=["文件名","Max","Min"]
            for z in range(self.data.maxCol):
                t2.append(str(z))
            print(t2)
            self.Table2.setHorizontalHeaderLabels(t2)

            print(self.data.maxCol)

            for key in self.data.filelist:
                # print(self.data.filelist[key].Cut_Data1)
                self.Table2.setItem(i,0,QTableWidgetItem(key))
                self.Table2.setItem(i,1,QTableWidgetItem(str(self.data.filelist[key].Max)))
                self.Table2.setItem(i,2,QTableWidgetItem(str(self.data.filelist[key].Min)))
                for j in range(len(self.data.filelist[key].Cut_Data1)):
                    self.Table2.setItem(i, j+3, QTableWidgetItem(str(self.data.filelist[key].Cut_Data1[j])))
                    # print(self.data.filelist[key].Cut_Data1[j])
                    j+=1
                i+=1


    def outLineEditfinished(self):
        path = self.outLineEdit.text()
        if (not(os.path.exists(path))):
            self.statusBar().showMessage("路径不存在，输出时将自动创建文件夹！")

        elif(os.path.exists(path+"/预处理后的数据.xls")):
            self.outpath=path
            self.statusBar().showMessage("文件已存在，若不想覆盖文件请更改文件保存路径")
        else:
            self.outpath=path+"/预处理后的数据.xls"
            self.statusBar().showMessage("已更改输出文件路径！")

    def Table2HorizontalHeaderClick(self,index):
        if((index!=3)and(index!=0)):
            print(index)
            print(self.Table2.horizontalHeaderItem(index).text())
            # if(index==1):
            row=[]
            x=[]
            # self.Table3.setRowCount(self.Table2.rowCount())
            # self.Table3.setColumnCount(1)
            # self.Table3.setHorizontalHeaderLabels([self.Table2.horizontalHeaderItem(index).text()])
            for i in range(self.Table2.rowCount()):
                try:
                    row.append(float(self.Table2.item(i,index).text()))
                except Exception as a:
                    print(a)
                # self.Table3.setItem(i,0,QTableWidgetItem(self.Table2.item(i,index).text()))
            # for i in range(len(row)):
            #         x.append(i)
            for time in self.data.filelist:
                x.append(self.data.filelist[time].ACQ_Time)
            print(x)
            self.plotfeature(x,row,"所选数据文件第"+self.Table2.horizontalHeaderItem(index).text()+"列变化折线图")

    def Table2VerticalHeaderClick(self,index):
        print(index)
        # len(self.filelist[title].Pro_Data1) - numend - 1
        print(self.data.filelist[self.Table2.item(index,0).text()].cutstartnum1)
        print(len(self.data.filelist[self.Table2.item(index,0).text()].Pro_Data1) -self.data.filelist[self.Table2.item(index,0).text()].cutendnum1-1)
        self.cutComboBoxstart.setCurrentIndex(self.data.filelist[self.Table2.item(index,0).text()].cutstartnum1)
        self.cutComboBoxend.setCurrentIndex(len(self.data.filelist[self.Table2.item(index,0).text()].Pro_Data1) -self.data.filelist[self.Table2.item(index,0).text()].cutendnum1-1)

        self.cuttypeComboBox.clear()
        self.cuttypeComboBox.addItems(["["+str(index+1)+"]"+self.Table2.item(index,0).text(),"批量裁剪"])
        self.fitComboBox.clear()
        self.fitComboBox.addItems(["["+str(index+1)+"]"+self.Table2.item(index,0).text(),"批量拟合"])
        filename=self.Table2.item(index, 0).text()
        x=self.data.filelist[filename].Pro_Data1_X
        y=self.data.filelist[filename].Pro_Data1

        self.Table3.setRowCount(1+len(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1[0]))
        self.Table3.setColumnCount(len(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1))
        for i in range(len(self.data.filelist[filename].Pro_Data1)):
            self.Table3.setItem(0, i, QTableWidgetItem(str(self.data.filelist[filename].Pro_Data1[i])))

        for i in range(len(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1)):
            for j in range(len(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1[i])):
                self.Table3.setItem(j+1, i, QTableWidgetItem(str(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1[i][j])))


        # self.Table3.setRowCount(1)
        # self.Table3.setColumnCount(self.Table2.columnCount())
        # coltitle=[]
        #
        # for i in range(self.Table2.columnCount()):
        #     coltitle.append(self.Table2.horizontalHeaderItem(i).text())
        #     self.Table3.setItem(0,i,QTableWidgetItem(self.Table2.item(index,i).text()))
        # self.Table3.setHorizontalHeaderLabels(coltitle)

        numstart=self.data.filelist[self.Table2.item(index,0).text()].cutstartnum1
        numend=self.data.filelist[self.Table2.item(index,0).text()].cutendnum1
        title=self.Table2.item(index,0).text()+"点"+str(numstart)+"到点"+str(numend+1)+"数据折线图"
        self.plotdata(filename,title)

    def Table3HorizontalHeaderClick(self,index):
        print(index)
        # print(self.Table2.horizontalHeaderItem(index).text())
        # if(index==1):
        row = []
        x = []
        for i in range(1,self.Table3.rowCount()):
            row.append(float(self.Table3.item(i, index).text()))
        self.plotfeature(x, row, "第" + str(index+1) + "个数据点重复测试数值变化图")

    def Table3VerticalHeaderClick(self,index):
        print(index)
        # print(self.Table2.horizontalHeaderItem(index).text())
        # if(index==1):
        row = []
        x = []
        for i in range(0, self.Table3.columnCount()):
            row.append(float(self.Table3.item(index,i).text()))
        self.plotfeature(x, row, "重复测试中每个点的第" + str(index + 1) + "次测量值变化图")


    def ChangedcutComboBoxstart(self,index):
        print()



    def savefileButtonclicked(self):
        if(self.Table2.rowCount()>0):
            self.data.writeXls(self.outpath)
        else:
            self.statusBar().showMessage(
                "请添加数据文件！")

    def savefilesonButtonclicked(self):
        self.data.writesondataXls(self.outpath)

    def saveImageButtonlicked(self):
        if(self.imagenName!=""):
            self.figure.axes.get_figure().savefig(self.outpath+ "/" + self.imagenName+".png")
            self.statusBar().showMessage(
                "图片成功保存到" + self.outpath+ "/" + self.imagenName+".png")
        else:
            self.statusBar().showMessage(
                "无图片！")

    def fitButtonlicked(self):
        title=""
        if(self.fitComboBox.currentText()!="批量拟合"):
            # self.statusBar().showMessage("开始进行批量数据拟合...")
            index=self.fitComboBox.currentText().find("]")
            title=self.fitComboBox.currentText()[(index+1):]
            print(title)
        if(self.cb1.isChecked()):
            self.data.Fitting(1,self.cb1ComboBoxstart.currentText(),title)
        if(self.cb2.isChecked()):
            self.data.Fitting(2,self.cb2ComboBoxstart.currentText(),title)
        if (self.cb3.isChecked()):
            self.data.Fitting(3, self.cb3ComboBoxstart.currentText(),title)
        if (self.cb4.isChecked()):
            self.data.Fitting(4, self.cb4ComboBoxstart.currentText(),title)

        self.Table2.clear()
        self.Table2.setRowCount(len(self.data.filelist))
        self.Table2.setColumnCount(4+14)
        i=0
        title2=["文件名","Max","Min","ACQ_Time","(双曲线)I_0", "(双曲线)τ", "(双曲线)Γ", "(双曲线)D","(指数)I_0", "(指数)τ", "(指数)D","(双曲线积分)I_0", "(双曲线积分)τ", "(双曲线积分)Γ", "(双曲线)D","(指数积分)I_0", "(指数积分)τ", "(指数)D"]
        self.Table2.setHorizontalHeaderLabels(title2)
        for key,value in self.data.filelist.items():
            row=[]
            for para in value.paras["双曲线拟合"]:
                row.append(para)
            for para in value.paras["指数拟合"]:
                row.append(para)
            for para in value.paras["双曲线积分拟合"]:
                row.append(para)
            for para in value.paras["指数积分拟合"]:
                row.append(para)
            self.Table2.setItem(i, 0, QTableWidgetItem(key))
            self.Table2.setItem(i, 1, QTableWidgetItem(str(value.Max)))
            self.Table2.setItem(i, 2, QTableWidgetItem(str(value.Min)))
            self.Table2.setItem(i, 3,
                                QTableWidgetItem(value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
            j=4
            for para in row:
                if(para!=""):
                    self.Table2.setItem(i,j,QTableWidgetItem(str(round(para,2))))
                else:
                    self.Table2.setItem(i, j, QTableWidgetItem(str(para)))
                j+=1
            i+=1


        # 若不是批量拟合，只改变一行数据
        if (self.fitComboBox.currentText() != "批量拟合"):
            index = self.fitComboBox.currentText().find("]")
            self.plotdata(self.fitComboBox.currentText()[(index + 1):])


    def cutButtonlicked(self):
        self.data.cutdata(int(self.cutComboBoxstart.currentText()),int(self.cutComboBoxend.currentText()),self.cuttypeComboBox.currentText())
        if (self.cuttypeComboBox.currentText()!="批量裁剪"):

            index=self.cuttypeComboBox.currentText().find("]")
            title=self.cuttypeComboBox.currentText()[(index+1):]
            find = self.Table2.findItems(title,QtCore.Qt.MatchExactly)
            row = find[0].row()

            print(title)
            self.Table2.setItem(row,1,QTableWidgetItem(str(self.data.filelist[title].Max)))
            self.Table2.setItem(row,2,QTableWidgetItem(str(self.data.filelist[title].Min)))
            self.plotdata(title)
        else:
            count=len(self.data.filelist)
            self.Table2.clear()
            self.Table2.setRowCount(len(self.data.filelist))
            self.Table2.setColumnCount(4)
            t2=["文件名","Max","Min","ACQ_Time"]
            for z in range(self.data.maxCol):
                t2.append(str(z))
            print(t2)
            print("正在写入标题")
            self.Table2.setHorizontalHeaderLabels(t2)
            p=1
            for key in self.data.filelist:
                self.Table2.setItem(p-1,0,QTableWidgetItem(key))
                self.Table2.setItem(p-1, 1, QTableWidgetItem(str(self.data.filelist[key].Max)))
                self.Table2.setItem(p-1, 2, QTableWidgetItem(str(self.data.filelist[key].Min)))
                self.Table2.setItem(p-1, 3, QTableWidgetItem(self.data.filelist[key].ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
                p+=1










    def generateMenu2(self, pos):
        row_num = -1
        # fittype = QListWidgetItem(self.listwidget2.currentItem()).text()
        # filename = QListWidgetItem(self.listwidget1.currentItem()).text()
        rowlabel = str(self.Table2.currentIndex().row() + 1)
        collabel = str(self.Table2.horizontalHeaderItem(self.Table2.currentIndex().column()).text())
        # collabel=self.listwidget3.takeHorizontalHeaderItem(self.listwidget3.currentIndex().column()).text()
        currtext = self.Table2.currentItem().text()

        for i in self.Table2.selectionModel().selection().indexes():
            row_num = i.row()

        if row_num < self.Table2.rowCount():
            menu = QMenu()
            # item1 = menu.addAction("复制单元格["+rowlabel+","+collabel+"]"+currtext)
            item1 = menu.addAction("复制单元格内容：" + currtext)
            item2 = menu.addAction("复制第" + rowlabel + "组参数(带文件名)")
            item3 = menu.addAction('提取每组参数中的"' + collabel+'"列(带列名)')
            item4 = menu.addAction("复制第" + rowlabel + "组参数")
            item5 = menu.addAction('提取每组参数中的"' + collabel+'"列')
            action = menu.exec_(self.Table2.mapToGlobal(pos))
            if action == item1:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.Table2.currentItem().text())
                self.statusBar().showMessage(
                    '已复制："' + currtext + '"')
            elif action == item2:
                clipboard = QApplication.clipboard()
                text = ""
                ind = self.Table2.currentIndex().row()
                for j in range(self.Table2.columnCount()):
                    text += self.Table2.item(ind, j).text() + ","
                clipboard.setText(text)
                self.statusBar().showMessage('已复制:"' + self.Table2.item(self.Table2.currentIndex().row(),0).text()+ "的参数与数据(带文件名)")

            elif action == item3:
                clipboard = QApplication.clipboard()
                text = ""
                ind = self.Table2.currentIndex().column()
                text +=collabel+","
                for i in range(self.Table2.rowCount()):
                    text += self.Table2.item(i, ind).text() + ","
                clipboard.setText(text)
                self.statusBar().showMessage("已提取每组参数中的" + collabel + "列特征(带列名)")
            elif action == item4:
                clipboard = QApplication.clipboard()
                text = ""
                ind = self.Table2.currentIndex().row()
                for j in range(1,self.Table2.columnCount()):
                    text += self.Table2.item(ind, j).text() + ","
                clipboard.setText(text)
                self.statusBar().showMessage(
                    '已复制:"' + self.Table2.item(self.Table2.currentIndex().row(), 0).text() + "的参数与数据")
            elif action == item5:
                clipboard = QApplication.clipboard()
                text = ""
                ind = self.Table2.currentIndex().column()
                for i in range(self.Table2.rowCount()):
                    text += self.Table2.item(i, ind).text() + ","
                clipboard.setText(text)
                self.statusBar().showMessage("已提取每组参数中的" + collabel + "列特征")
            else:
                return

    def plotfeature(self,x,y,title="",xlabel="t",ylabel="cps"):
        if(x==[]):
            x=range(1,len(y)+1)
        print(x)
        print(y)
        self.imagenName =title
        self.figure.fig.canvas.draw_idle()
        self.figure.axes.clear()

        self.figure.axes.plot(x,y)
        self.figure.axes.scatter(x,y, alpha=0.5)
        self.figure.axes.set_ylabel(ylabel)
        self.figure.axes.set_xlabel(xlabel)
        self.figure.axes.set_title(title)
        # self.figure.axes.xlim(x[0], x[-1])
        self.figure.axes.legend()

    def plotdata(self,filename,title="",xlabel="t",ylabel="cps"):
        numstart=self.data.filelist[filename].cutstartnum1
        numend=self.data.filelist[filename].cutendnum1
        self.imagenName =title
        self.figure.fig.canvas.draw_idle()
        self.figure.axes.clear()


        # self.figure.axes.plot(self.data.filelist[filename].Cut_Data1_X,self.data.filelist[filename].Cut_Data1)

        #原始曲线
        self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[0:numstart+1],self.data.filelist[filename].Pro_Data1[0:numstart+1],"--",color="green")#前半段
        self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[numstart:numend+1],self.data.filelist[filename].Pro_Data1[numstart:numend+1],color="blue") #中段
        self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[numend:],self.data.filelist[filename].Pro_Data1[numend:],"--",color="green")#后半段段

        self.figure.axes.scatter(self.data.filelist[filename].Pro_Data1_X,self.data.filelist[filename].Pro_Data1, alpha=0.3)
        self.figure.axes.plot(self.data.filelist[filename].Cut_Data1fit_X, self.data.filelist[filename].Cut_Data1fit,color="red")
        # self.figure.axes.scatter(self.data.filelist[filename].Cut_Data1_X,self.data.filelist[filename].Cut_Data1, alpha=0.3)
        self.figure.axes.set_ylabel(ylabel)
        self.figure.axes.set_xlabel(xlabel)
        self.figure.axes.set_title(title)
        self.figure.axes.legend()























if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())



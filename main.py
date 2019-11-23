import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Mydemo import*
from dataread import*
from PyQt5 import QtCore
class main (QMainWindow):
    def __init__(self, parent=None):
        self.inpath=""
        self.outpath=""
        self.imagenName=''

        super(main, self).__init__(parent)
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

        self.label3 = QLabel("提取的列表：")
        self.grid.addWidget(self.label3, 4, 10, 1, 5)

        self.Table1=QListWidget()
        self.grid.addWidget(self.Table1, 3, 0, 1, 3)

        self.Table2=QTableWidget()
        self.Table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Table2.horizontalHeader().sectionClicked.connect(self.Table2HorizontalHeaderClick)
        self.Table2.verticalHeader().sectionClicked.connect(self.Table2VerticalHeaderClick)
        self.Table2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Table2.customContextMenuRequested.connect(self.generateMenu2)
        self.grid.addWidget(self.Table2, 5, 0, 1, 10)

        self.Table3=QTableWidget()
        self.grid.addWidget(self.Table3, 5, 10, 1, 5)




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

        self.cutButton = QPushButton("裁剪")
        self.grid.addWidget(self.cutButton, 7, 4, 1, 1)
        self.cutButton.clicked.connect(lambda: self.cutButtonlicked())

        self.fitButton = QPushButton("数据拟合")
        self.grid.addWidget(self.fitButton, 6, 5, 1, 1)
        self.fitButton.clicked.connect(lambda: self.fitButtonlicked())



        self.saveImageButton=QPushButton("保存图片")
        self.grid.addWidget(self.saveImageButton,6,14,1,1)
        self.saveImageButton.clicked.connect(lambda: self.saveImageButtonlicked())

        self.savefileButton=QPushButton("保存数据")
        self.grid.addWidget(self.savefileButton,7,14,1,1)
        self.savefileButton.clicked.connect(lambda: self.savefileButtonlicked())


        self.cutlabel = QLabel("请选择开始数据点:")
        self.cutlabel.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.cutlabel, 6, 0, 1, 1)

        self.cutlabel = QLabel("请选择结束数据点:")
        self.cutlabel.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.cutlabel, 7, 0, 1, 1)

        self.cutlabel = QLabel("请选择裁剪类型:")
        self.cutlabel.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.cutlabel, 6, 2, 1, 1)

        self.cuttypeComboBox = QComboBox()
        self.cuttypeComboBox.addItems(
            ["批量裁剪"])
        # self.cuttypeComboBox.setCurrentIndex(0)
        # self.cuttypeComboBox.currentIndexChanged.connect(lambda: self.ChangedcuttypeComboBox())
        self.grid.addWidget(self.cuttypeComboBox, 6, 3, 1, 2)

        self.cutComboBoxstart = QComboBox()
        self.cutComboBoxstart.addItems(
            ["0","1", "2","3", "4","5", "6","7", "8","9", "10","11", "12","13", "14","15", "16","17", "18","19", "20"])
        self.cutComboBoxstart.setCurrentIndex(0)
        # self.cutComboBoxstart.currentIndexChanged.connect(lambda: self.ChangedcutComboBoxstart())
        self.grid.addWidget(self.cutComboBoxstart, 6, 1, 1, 1)
        
        self.cutComboBoxend = QComboBox()
        self.cutComboBoxend.addItems(
            ["0","1", "2","3", "4","5", "6","7", "8","9", "10","11", "12","13", "14","15", "16","17", "18","19", "20"])
        self.cutComboBoxend.setCurrentIndex(0)
        # self.cutComboBoxend.currentIndexChanged.connect(lambda: self.ChangedcutComboBoxend())
        self.grid.addWidget(self.cutComboBoxend, 7, 1, 1, 1)

        self.widget=QWidget()
        self.widget.setLayout(self.grid)
        self.tab.addTab(self.widget,"数据预处理")
        self.setCentralWidget(self.tab)
        self.data=dataread(self.progressBar,self.statusBar)

    def readfileButtonclicked(self):
        self.statusBar().showMessage("正在选择文件夹...")
        path = QFileDialog.getExistingDirectory(self, "请选择数据文件的根目录")
        # path = "C:/Users/ENERGY/Desktop/工作文件/test"
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
        if(index!=3):
            print(index)
            print(self.Table2.horizontalHeaderItem(index).text())
            # if(index==1):
            row=[]
            x=[]
            self.Table3.setRowCount(self.Table2.rowCount())
            self.Table3.setColumnCount(1)
            self.Table3.setHorizontalHeaderLabels([self.Table2.horizontalHeaderItem(index).text()])
            for i in range(self.Table2.rowCount()):
                try:
                    row.append(float(self.Table2.item(i,index).text()))
                except Exception as a:
                    print(a)
                self.Table3.setItem(i,0,QTableWidgetItem(self.Table2.item(i,index).text()))
            # for i in range(len(row)):
            #         x.append(i)
            for time in self.data.filelist:
                x.append(self.data.filelist[time].ACQ_Time)
            print(x)
            self.plotfeature(x,row,"所选数据文件第"+self.Table2.horizontalHeaderItem(index).text()+"列变化折线图")

    def Table2VerticalHeaderClick(self,index):
        print(index)
        self.cuttypeComboBox.clear()
        self.cuttypeComboBox.addItems(["["+str(index+1)+"]"+self.Table2.item(index,0).text(),"批量裁剪"])
        filename=self.Table2.item(index, 0).text()
        x=self.data.filelist[filename].Pro_Data1_X
        y=self.data.filelist[filename].Pro_Data1
        # try:
        #     # print(self.Table2.verticalHeaderItem(index).text())
        # except Exception as a:
        #     print(a)
        # if(index==1):
        self.Table3.setRowCount(1)
        self.Table3.setColumnCount(self.Table2.columnCount())
        coltitle=[]

        # for i in range(self.Table2.columnCount()):
        for i in range(4):
            coltitle.append(self.Table2.horizontalHeaderItem(i).text())
            self.Table3.setItem(0,i,QTableWidgetItem(self.Table2.item(index,i).text()))
        self.Table3.setHorizontalHeaderLabels(coltitle)

        # print(x)
        # print(y)
        self.plotdata(filename)

    def ChangedcutComboBoxstart(self,index):
        print()



    def savefileButtonlicked(self):
        if(self.Table2.rowCount()>0):
            self.data.writeXls(self.outpath)
        else:
            self.statusBar().showMessage(
                "请添加数据文件！")

    def saveImageButtonlicked(self):
        if(self.imagenName!=""):
            self.figure.axes.get_figure().savefig(self.outpath+ "/" + self.imagenName+".png")
            self.statusBar().showMessage(
                "图片成功保存到" + self.outpath+ "/" + self.imagenName+".png")
        else:
            self.statusBar().showMessage(
                "无图片！")

    def fitButtonlicked(self):
        self.data.Fitting()


    def cutButtonlicked(self):
        self.data.cutdata(int(self.cutComboBoxstart.currentText()),int(self.cutComboBoxend.currentText()),self.cuttypeComboBox.currentText()[3:])
        if (self.cuttypeComboBox.currentText()!="批量裁剪"):
            find = self.Table2.findItems(self.cuttypeComboBox.currentText()[3:],QtCore.Qt.MatchExactly)
            row = find[0].row()
            self.Table2.setItem(row,1,QTableWidgetItem(str(self.data.filelist[self.cuttypeComboBox.currentText()[3:]].Max)))
            self.Table2.setItem(row,2,QTableWidgetItem(str(self.data.filelist[self.cuttypeComboBox.currentText()[3:]].Min)))
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
                # strr=""
                # strr+="正在裁剪"+str(p)+"/"+str(count)+"  "+key
                # print(strr)
                # self.statusBar().showMessage(strr)
                self.Table2.setItem(p-1,0,QTableWidgetItem(key))
                self.Table2.setItem(p-1, 1, QTableWidgetItem(str(self.data.filelist[key].Max)))
                self.Table2.setItem(p-1, 2, QTableWidgetItem(str(self.data.filelist[key].Min)))
                self.Table2.setItem(p-1, 3, QTableWidgetItem(self.data.filelist[key].ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
                p+=1
            self.statusBar().showMessage(
                "已移除所有文件中的前十个数据点！(同时更新数据最大值，最小值)")










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

        self.figure.axes.plot(self.data.filelist[filename].Cut_Data1fit_X,self.data.filelist[filename].Cut_Data1fit,color="red")
        # self.figure.axes.plot(self.data.filelist[filename].Cut_Data1_X,self.data.filelist[filename].Cut_Data1)

        #原始曲线
        self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[0:numstart+1],self.data.filelist[filename].Pro_Data1[0:numstart+1],"--",color="green")#前半段
        self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[numstart:numend+1],self.data.filelist[filename].Pro_Data1[numstart:numend+1],color="blue") #中段
        self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[numend:],self.data.filelist[filename].Pro_Data1[numend:],"--",color="green")#后半段段

        self.figure.axes.scatter(self.data.filelist[filename].Pro_Data1_X,self.data.filelist[filename].Pro_Data1, alpha=0.3)
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



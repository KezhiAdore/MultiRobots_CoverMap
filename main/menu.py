from PySide2.QtWidgets import QApplication, QMessageBox,QFileDialog,QGridLayout
from PySide2.QtUiTools import QUiLoader
import numpy as np
import pyqtgraph as pg
import mapmaker
import simulation
import time


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        loader=QUiLoader()
        loader.registerCustomWidget(pg.PlotWidget)
        self.ui = QUiLoader().load('main.ui')
        self.ui.Simulation.clicked.connect(self.simulator)
        self.ui.Make_map.clicked.connect(self.makemap)
        self.ui.Robot_num.setValue(50)
        self.ui.Map_filename_read.setText('map1.txt')
        self.ui.Alpha.setValue(0.1)
        self.ui.Len.setValue(10)
        self.ui.Total_time.setValue(1)
        self.ui.Cover_ratio.setValue(0.99)
        self.ui.Map_xlen.setValue(100)
        self.ui.Map_ylen.setValue(100)
        self.ui.progressBar.setRange(0,100)
        self.ui.progressBar.setValue(0)
        self.ui.Coverage_time.setBackground('w')
        self.ui.Coverage_time.setYRange(min=0,max=1000)
        self.curve = self.ui.Coverage_time.getPlotItem().plot(pen=pg.mkPen('r', width=1))


    def makemap(self):
        xlen=int(self.ui.Map_xlen.text())
        ylen=int(self.ui.Map_ylen.text())
        filename=self.ui.Map_filename_write.text()
        maker=mapmaker.Makemap(xlen,ylen,filename)
        maker.run()


    def simulator(self):
        robot_num=self.ui.Robot_num.value()
        filename=self.ui.Map_filename_read.text()
        algorithm=self.choose_model(self.ui.Algorithm.currentText())
        alpha=self.ui.Alpha.value()
        length=self.ui.Len.value()
        total_time=self.ui.Total_time.value()
        is_window=self.is_windowed(self.ui.Window.currentText())
        cover_ratio=self.ui.Cover_ratio.value()
        self.ui.progressBar.setRange(0,total_time)
        if algorithm==4 or algorithm==5:
            parameter=[alpha,length]
        else:
            parameter=[alpha,0]
        result=[]
        for i in range(total_time):
            tmp=simulation.main(robot_num,algorithm,parameter,(100,100),filename,cover_ratio,is_window)
            result.append(tmp)
            np_result=np.array(result)
            self.ui.Num_now.clear()
            self.ui.Num_now.insertPlainText(str(i+1))
            self.ui.Time_now.clear()
            self.ui.Time_now.insertPlainText(str(tmp))
            self.ui.progressBar.setValue(i+1)
            print((i+1)/total_time)
            self.ui.Mean.clear()
            self.ui.Mean.insertPlainText(str(np.mean(np_result)))
            self.ui.Stander.clear()
            self.ui.Stander.insertPlainText(str(np.std(np_result)))
        self.ui.Coverage_time.setYRange(min=0,max=1000)
        self.curve.setData([j for j in range(1,i+2)],result)



    def choose_model(tmp,algorithm):
        models=['直接轮盘赌','基本黄蜂群算法','启发式黄蜂群','深度优先搜索','栈限长dfs','队列限长dfs']
        if algorithm in models:
            for i in range(6):
                if models[i]==algorithm:
                    return i

    def is_windowed(tmp,Window):
        if Window=='是':
            return 60
        else:
            return 0


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
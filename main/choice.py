from PySide2.QtWidgets import QApplication, QMessageBox,QFileDialog
from PySide2.QtUiTools import QUiLoader
import yaml
import mapmaker

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = QUiLoader().load('main.ui')
        # self.ui.Simulation.clicked.connect(test.run)
        self.ui.Make_map.clicked.connect(self.makemap)
        # self.filepath,_=QFileDialog.getOpenFileName(self.ui,"选择地图文件")
        # if self.filepath != '':
        #     self.data=self.get_yaml_data(self.filepath)

    def makemap(self):
        xlen=int(self.ui.Map_xlen.text())
        ylen=int(self.ui.Map_ylen.text())
        filename=self.ui.Map_filename.text()
        maker=mapmaker.Makemap(xlen,ylen,filename)
        maker.run()

    def get_yaml_data(stat,yaml_file):
        #打开读取配置文件
        file = open(yaml_file, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()
        #将数据转化为字典
        data = yaml.load(file_data)
        return data

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
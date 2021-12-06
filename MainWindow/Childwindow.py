import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

from MainWindow.dialog import Ui_Dialog


class MyDialog(QDialog, Ui_Dialog):
    mySignal = pyqtSignal(str)  # 定义信号量

    def __init__(self):
        super(MyDialog, self).__init__()
        self.setupUi(self)
        self.tijiao.clicked.connect(self.getData)

    def getData(self):

        self.para_Json = {
            "zaibo_freq": self.zaibo_freq.text(),
            "zaibo_power": self.zaibo_power.text(),
            "tiaozhi_amp": self.tiaozhi_amp.text(),
            "tiaozhi_bias": self.tiaozhi_bias.text(),
            "wave": '',
            "distance": self.distance.text(),
            "rotate_a": self.rotate_a.text(),
            "rotate_v": self.rotate_v.text(),
            "water_temp": self.water_temp.text(),
            "hight": self.hight.text(),
            "width": self.widith.text()
        }
        if self.zhengxianbo.isChecked():
            self.para_Json['wave'] = "正弦波"
        if self.juxingbo.isChecked():
            self.para_Json['wave'] = "矩形波"
        if self.zhengbanbo.isChecked():
            self.para_Json['wave'] = "正半波"
        self.mySignal.emit(str(self.para_Json))
        self.close()
        # print(self.para_Json)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MyDialog()
    ui.show()
    sys.exit(app.exec_())

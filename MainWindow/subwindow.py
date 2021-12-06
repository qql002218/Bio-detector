import numpy as np
import sys
import matplotlib
import csv
import pandas as pd

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from pylab import *

# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QTimer
import sys
import os

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect


class App(QWidget):
    def __init__(self, parent=None):
        # 父类初始化方法
        super(App, self).__init__(parent)
        self.initUI()
        self.center()

    def initUI(self):
        self.setWindowTitle('数据可视化')
        self.setFixedSize(800, 600)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        # 几个QWidgets

        self.startBtn = QPushButton('开始')
        self.endBtn = QPushButton('结束')
        self.saveBtn = QPushButton('保存')
        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
        self.saveBtn.clicked.connect(self.save)
        # 时间模块
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        # 图像模块
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        hanglayout = QHBoxLayout()
        hanglayout.addWidget(self.startBtn)
        hanglayout.addWidget(self.endBtn)
        hanglayout.addWidget(self.saveBtn)
        # 垂直布局
        layout = QVBoxLayout()
        layout.addLayout(hanglayout)

        layout.addWidget(self.canvas)
        self.setLayout(layout)
        ##颜色矩阵
        self.COLORS = ['aliceblue',
                       'aqua',
                       'black',
                       'blanchedalmond',
                       'blue',
                       'blueviolet',
                       'brown',
                       'burlywood',
                       'cadetblue',
                       'chartreuse',
                       'chocolate',
                       'coral',
                       'cornflowerblue',
                       'cornsilk',
                       'crimson',
                       'cyan',
                       'darkblue',
                       'darkcyan',
                       'darkgoldenrod',
                       'darkgray',
                       'darkgreen',
                       'darkkhaki',
                       'darkmagenta',
                       'darkolivegreen',
                       'darkorange',
                       'darkorchid',
                       'darkred',
                       'darksalmon']

        # 数组初始化
        self.data = {}  # 画图所需要的data,这里是字典格式的数据串

    def center(self, screenNum=0):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.normalGeometry2 = QRect((screen.width() - size.width()) / 2 + screen.left(),
                                     (screen.height() - size.height()) / 2,
                                     size.width(), size.height())
        self.setGeometry((screen.width() - size.width()) / 2 + screen.left(),
                         (screen.height() - size.height()) / 2,
                         size.width(), size.height())

    def save(self):

        self.i = 0
        plt.savefig(f"{self.path}/辐照小鼠运动距离图线.png")
        file_name = os.path.join(self.path, "辐照小鼠运动距离.csv")

        fileHeader = []
        maxlen = 0
        for key in self.data.keys():
            fileHeader.append(key)
            maxlen = max(maxlen, len(self.data[key][0]))
        df = pd.DataFrame(columns=fileHeader)
        for key in self.data.keys():
            temp = []
            for i in range(len(self.data[key][0])):
                temp.append((self.data[key][0][i], self.data[key][1][i]))
            fill = maxlen - len(temp) #DataFrame需要列的行数相同，所以在这里计算短的列需要加多少个空行
            # temp = zip(temp)
            temp.extend(fill*['']) #在此进行补行
            df[key] = temp
        df.to_csv(file_name, mode='a', encoding='gbk')
        # csvfile = open(file_name, 'wt', newline='')
        # writer = csv.writer(csvfile, delimiter=",")
        # header = []  # 第一行,tracker_id
        # for key in self.data.keys():
        #     header.append(key)
        # writer.writerow(header)
        # data = []
        #
        # for key in self.data.keys():
        #     temp = []
        #     for i in range(len(self.data[key][0])):
        #         temp.append((self.data[key][0][i], self.data[key][1][i]))
        #     temp = zip(temp)
        #     data.append(temp)
        # result = pd.DataFrame(columns=key, data=data)
        # result.to_csv(file_name, encoding='gbk')

    def showTime(self):
        # shuju=np.random.random_sample()*10#返回一个[0,1)之间的浮点型随机数*10
        # shuju_2=np.random.random_sample()*10#返回一个[0,1)之间的浮点型随机数*10
        # self.x.append(shuju)#数组更新
        # self.xx.append(shuju_2)
        ax = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        # ax = self.figure.add_subplot(111)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['left'].set_position(('data', 0))
        ax.clear()
        # print(self.data.keys())
        # print('-------------------------')
        plt.xlabel("实验时间(second)")
        plt.ylabel("小鼠运动距离(cm)")
        plt.title("小鼠辐照实时运动距离曲线图")
        for key in self.data.keys():
            ax.plot(self.data.get(key)[0], self.data.get(key)[1], label='tracker_id_{}'.format(key), linestyle='-',
                    color=self.COLORS[int(key)])
            print(self.COLORS[int(key)])
        # ax.plot(self.people_num_list, label="people_num", linestyle=':', color="g")
        # ax.plot(self.cars_num_list, label="cars_num", color="b", linestyle='--')
        # ax.plot(self.motors_num_list, label="motors_num", color="r", linestyle='-.')

        self.figure.legend()

        plt.grid(True)
        self.canvas.draw()

    # 启动函数
    def startTimer(self):
        # 设置计时间隔并启动
        self.timer.start(1000)  # 每隔一秒执行一次绘图函数 showTime
        self.startBtn.setEnabled(False)  # 开始按钮变为禁用
        self.endBtn.setEnabled(True)  # 结束按钮变为可用

    def endTimer(self):
        self.timer.stop()  # 计时停止
        self.startBtn.setEnabled(True)  # 开始按钮变为可用
        self.endBtn.setEnabled(False)  # 结束按钮变为可用

    def getData(self, data):
        # 对data 进行处理过滤
        if len(data) == 1:
            self.path = data[0]
            # print(self.path)
        for j in range(1, len(data)):
            if len(data[j]) != 0:
                temp = data[j]
                xdata = [temp[i][0] / 20 for i in range(len(temp))]
                ydata = [temp[i][1] for i in range(len(temp))]
                self.data['{}'.format(j)] = [xdata, ydata]
                # print(f'track id :{j} : {xdata}')
                # print(f'track id :{j} : {ydata}')
                # print('-----------------------------------------------------------------------')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app.exec_())

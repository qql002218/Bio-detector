import json
import os
import time
import csv
import pandas as pd

# def main():
#     current_dir = os.path.abspath('.')
#     file_name = os.path.join(current_dir, "csss.csv")
#     csvfile = open(file_name, 'wt', newline='')  # encoding='utf-8'
#     data = []
#     header = []
#     data = {'1': [[1, 2, 3, 4, 5], [11, 12, 34, 55, 66]]}
#
#     for key in data.keys():
#         header.append(key)
#         temp = []
#         for i in range(len(data[key][0])):
#             temp.append((data[key][0][i], data[key][1][i]))
#
#     writer = csv.writer(csvfile, delimiter=",")
#
#     writer.writerow(header)
#     writer.writerows(zip(temp))
#
#     csvfile.close()
#
# def main():
#     file_name = 'csss.csv'
#     data = {'1': [[1, 2, 3, 4, 5], [11, 12, 34, 55, 66]]}
#     zz = []
#     for key in data.keys():
#         temp = []
#         for i in range(len(data[key][0])):
#             temp.append((data[key][0][i], data[key][1][i]))
#         temp = zip(temp)
#         zz.append(temp)
#     result = pd.DataFrame({''.format(key): temp})
#
#     result.to_csv(file_name, encoding='gbk')
#
#
# if __name__ == '__main__':
#     main()


# import csv
# import pandas as pd
#
# # 文件头，一般就是数据名
#
# ss ={}
# data = {'1': [[1, 2, 3, 4, 5], [11, 12, 34, 55, 66]],
#         '2': [[12, 22, 32, 42, 52,99], [11, 12, 34, 55, 66,222]]
#         }
# fileHeader = []
# maxlen = 0
# for key in data.keys():
#     fileHeader.append(key)
#     maxlen= max(maxlen,len(data[key][0]))
# print(maxlen)
# df =pd.DataFrame(columns=fileHeader)
# for key in data.keys():
#     temp = []
#     for i in range(len(data[key][0])):
#         temp.append((data[key][0][i], data[key][1][i]))
#     print(temp)
#     # temp = zip(temp)
#     fill = maxlen - len(temp)
#     print(fill)
#     temp.extend(fill*[''])
#     df[key] = temp
# df.to_csv('Experiments.csv', mode='a', encoding='gbk')

# temp = ['a']
# temp.append('c')
# print(temp)

# import matplotlib.pyplot as plt
# def autolabel(rects):
#     for rect in rects:
#         height = rect.get_height()
#         plt.text(rect.get_x()+rect.get_width()/2.- 0.2, 1.03*height, '%s' % int(height))
#
#
# name_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
# num_list = [33, 44, 53, 16, 11, 17, 17, 10]

# autolabel(plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list))
#
# plt.show()
# a =['a']
# print(type(a[0]))
# s = '/home/qiao/PycharmProjects/PythonLearning/LogFile/11-22/zz-pppp'
# slist = s.split('/')[-1].split('-')[-1]
#
# print(slist)

import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import font_manager
#
# # 设置中文字体
# my_font = font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/ukai.ttc")
#
# x = ["战狼2", "速度与激情8", "功夫瑜伽", "西游伏妖篇", "变形金刚5：最后的骑士", "摔跤吧！爸爸", "加勒比海盗5：死无对证", "金刚：骷髅岛", "极限特工：终极回归", "生化危机6：终章",
#      "乘风破浪", "神偷奶爸3", "智取威虎山", "大闹天竺", "金刚狼3：殊死一战", "蜘蛛侠：英雄归来", "悟空传", "银河护卫队2", "情圣", "新木乃伊", ]
#
# y = [56.01, 26.94, 17.53, 16.49, 15.45, 12.96, 11.8, 11.61, 11.28, 11.12, 10.49, 10.3, 8.75, 7.55, 7.32, 6.99, 6.88,
#      6.86, 6.58, 6.23]
#
# # 设置图形大小
# plt.figure(figsize=(18, 10),dpi=80)
#
# # 绘制条形图
# plt.bar(range(len(x)), y, width=0.8)  # width表示条形粗细
# # 绘制条形图 （横向条形图）
# # plt.barh(range(len(x)), y, height=0.3, color="orange")  # 横向条形图中height表示条形粗细
#
# # 设置x轴刻度
# plt.xticks(range(len(x)), x, fontproperties=my_font)
# # plt.yticks(range(len(x)), x, fontproperties=my_font)  # barh()绘制横向条形图时，设置的是y轴刻度
#
# # 保存图片
# # plt.savefig("./movie.png")
#
# plt.show()
#
# import json
#
# prices = {
#      'ACME': 45.23,
#      'AAPL': 612.78,
#      'IBM': 205.55,
#      'HPQ': 37.20,
#      'FB': 10.75,
#      '名字':'你好'
# }
# prices['sb'] =1
#
# with open('price.json', 'w+',encoding='utf-8') as f:
#      json.dump(prices, f,ensure_ascii=False,indent = 4)
#      f.close()
from PyQt5 import QtCore, QtWidgets
import sys

##########################################
# ui界面设置
# class Ui_MainWindow(object):
#
#      def setupUi(self, MainWindow):
#           # 主窗口参数设置
#           MainWindow.setObjectName("MainWindow")
#           MainWindow.resize(848, 721)
#           self.centralwidget = QtWidgets.QWidget(MainWindow)
#           self.centralwidget.setObjectName("centralwidget")
#
#           # 设置按键参数
#           self.file = QtWidgets.QPushButton(self.centralwidget)
#           self.file.setGeometry(QtCore.QRect(57, 660, 175, 28))
#           self.file.setObjectName("file")
#           self.file.setStyleSheet("background-color:rgb(111,180,219)")
#           self.file.setStyleSheet(
#                "QPushButton{background-color:rgb(111,180,219)}"  # 按键背景色
#                "QPushButton:hover{color:green}"  # 光标移动到上面后的前景色
#                "QPushButton{border-radius:6px}"  # 圆角半径
#                "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
#           )
#
#           # 设置显示窗口参数
#           self.fileT = QtWidgets.QPushButton(self.centralwidget)
#           self.fileT.setGeometry(QtCore.QRect(300, 660, 480, 28))
#           self.fileT.setObjectName("file")
#           self.fileT.setStyleSheet("background-color:rgb(111,180,219)")
#           self.fileT.setStyleSheet(
#                "QPushButton{background-color:rgb(111,180,219)}"  # 按键背景色
#                "QPushButton:hover{color:green}"  # 光标移动到上面后的前景色
#                "QPushButton{border-radius:6px}"  # 圆角半径
#                "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
#           )
#
#           # 主窗口及菜单栏标题栏设置
#           MainWindow.setCentralWidget(self.centralwidget)
#           self.menubar = QtWidgets.QMenuBar(MainWindow)
#           self.menubar.setGeometry(QtCore.QRect(0, 0, 848, 26))
#           self.menubar.setObjectName("menubar")
#           MainWindow.setMenuBar(self.menubar)
#           self.statusbar = QtWidgets.QStatusBar(MainWindow)
#           self.statusbar.setObjectName("statusbar")
#           MainWindow.setStatusBar(self.statusbar)
#
#           self.retranslateUi(MainWindow)
#           QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#           ################button按钮点击事件回调函数################
#
#           self.file.clicked.connect(self.msg)
#
#      def retranslateUi(self, MainWindow):
#           _translate = QtCore.QCoreApplication.translate
#           MainWindow.setWindowTitle(_translate("MainWindow", "Deecamp_Eurus"))
#           self.file.setText(_translate("MainWindow", "选择文件"))
#           self.fileT.setText(_translate("MainWindow", ""))
#
#      #########选择图片文件夹#########
#
#      def msg(self, Filepath):
#           m = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
#           self.fileT.setText(m)
#
#
# #########主函数入口 #########
#
# if __name__ == '__main__':
#      app = QtWidgets.QApplication(sys.argv)
#
#      mainWindow = QtWidgets.QMainWindow()
#
#      ui = Ui_MainWindow()
#
#      ui.setupUi(mainWindow)
#
#      mainWindow.show()
#
#      sys.exit(app.exec_())
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from resWindow import Ui_MainWindow

import sys


class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.vid = ''
        self.img = ''
        self.setupUi(self)
        self.sld_video_pressed = False
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.widget)  # 视频播放输出的widget，就是上面定义的
        self.btn_open.clicked.connect(self.msg)  # 打开视频文件按钮
        self.btn_play.clicked.connect(self.playVideo)  # play
        self.btn_stop.clicked.connect(self.pauseVideo)  # pause
        self.player.positionChanged.connect(self.changeSlide)  # change Slide
        self.sld_video.setTracking(False)
        self.sld_video.sliderReleased.connect(self.releaseSlider)
        self.sld_video.sliderPressed.connect(self.pressSlider)
        self.sld_video.sliderMoved.connect(self.moveSlider)
        self.pushButton.clicked.connect(self.openVideoFile)

    def moveSlider(self, position):
        if self.player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            self.lab_video.setText(str(round(position, 2)) + '%')

    def msg(self, Filepath):  # 选择文件夹
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 选择路径/并进行存储
        self.path = m  # 把路径进行存储
        for root, dirs, files in os.walk(self.path):
            for f in files:
                lastfix = f.split('.')[-1]
                if lastfix == 'png':
                    self.img = m + '/' + f
                if lastfix == 'mp4' or 'avi':
                    self.vid = m + '/' + f
                if lastfix == 'json':
                    json_path = m + '/' + f
                    with open(json_path, 'r') as f:
                        self.json = json.load(f)
                    print(self.json)
        print(self.vid)
        print(self.img)
        self.fileDir.setText(m)

    def pressSlider(self):
        self.sld_video_pressed = True
        print("pressed")

    def releaseSlider(self):
        self.sld_video_pressed = False

    def changeSlide(self, position):
        if not self.sld_video_pressed:  # 进度条被鼠标点击时不更新
            self.vidoeLength = self.player.duration() + 0.1
            self.sld_video.setValue(round((position / self.vidoeLength) * 100))
            self.lab_video.setText(str(round((position / self.vidoeLength) * 100, 2)) + '%')

    def openVideoFile(self):
        # self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.vid)))
        self.movieImage = QImage(self.img)
        self.qimage_2.setPixmap(QPixmap.fromImage(self.movieImage).scaled(self.qimage_2.size(), Qt.KeepAspectRatio,
                                                                          Qt.SmoothTransformation))
        ####实验信息填报
        self.zaibo_freq_2.setText(self.json['zaibo_freq'])
        self.zaibo_power_2.setText(self.json['zaibo_power'])
        self.tiaozhi_amp_2.setText(self.json['tiaozhi_amp'])
        self.tiaozhi_bias_2.setText(self.json['tiaozhi_bias'])
        self.lineEdit.setText(self.json['wave'])
        self.distance.setText(self.json['distance'])
        self.rotate_a.setText(self.json['rotate_a'])
        self.rotate_v.setText(self.json['rotate_v'])
        self.water_temp.setText(self.json['water_temp'])
        self.hight.setText(self.json['hight'])
        self.hight_2.setText(self.json['width'])
        if self.json['exp'] =='平衡木实验':
            # self.checkBox.checkState(True)
            pass
        self.textBrowser.setText(self.json['result'])
        if self.btn_preVId.isChecked():
            print('原始视频')
        if self.btn_chuliVid.isChecked():
            print('处理视频')

        self.player.play()  # 播放视频

    def playVideo(self):
        self.player.play()

    def pauseVideo(self):
        self.player.pause()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vieo_gui = myMainWindow()
    vieo_gui.show()
    sys.exit(app.exec_())

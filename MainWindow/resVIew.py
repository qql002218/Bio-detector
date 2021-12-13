from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from qtpy import QtWidgets

from resultview import Ui_MainWindow
import json
import os
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
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "/home/qiao/PycharmProjects/PythonLearning/LogFile/")  # 选择路径/并进行存储
        self.path = m  # 把路径进行存储
        for root, dirs, files in os.walk(self.path): ##这块写复杂了
            for f in files:
                lastfix = f.split('.')[-1]
                if lastfix == 'png':
                    self.img = m + '/' + f
                if lastfix == 'avi':
                    # self.vid = m + '/' + f
                    pass
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
            path = self.path+'/MyoutputVid-pre.avi'
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.player.play()
            print('原始视频')
        if self.btn_chuliVid.isChecked():
            path = self.path + '/MyoutputVid-lst.avi'
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.player.play()

            print('处理视频')

    def playVideo(self):
        self.player.play()

    def pauseVideo(self):
        self.player.pause()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vieo_gui = myMainWindow()
    vieo_gui.show()
    sys.exit(app.exec_())

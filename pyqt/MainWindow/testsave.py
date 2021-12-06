import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import QTimer,QCoreApplication
from PyQt5.QtGui import QPixmap
import cv2
import qimage2ndarray
import time
import os
import paramiko

class CamShow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CamShow, self).__init__(parent)
        self.setupUi(self)
        self.PreSliders()
        self.PrepWidgets()
        self.PreCamera()
        self.PrepParameters()
        self.CallBackFunctions()
        self.Timer = QTimer()
        self.Timer.timeout.connect(self.TimerOutFun)




    def PreSliders(self): ##滑动条的值连接
        self.rslid.valueChanged.connect(self.redspinBox.setValue)
        self.redspinBox.valueChanged.connect(self.rslid.setValue)

        self.gsld.valueChanged.connect(self.greenspinBox.setValue)
        self.greenspinBox.valueChanged.connect(self.gsld.setValue)

        self.bsld.valueChanged.connect(self.bluespinBox.setValue)
        self.bluespinBox.valueChanged.connect(self.bsld.setValue)

    def PrepWidgets(self):#初始化的时候 要将所有的按键设置为不可用，否则后期会紊乱
        self.sshbtn.setEnabled(True)
        self.savebtn.setEnabled(False)
        self.stopbtn.setEnabled(False)
        # self.startbtn.setEnabled(False)


        self.bsld.setEnabled(False)
        self.gsld.setEnabled(False)
        self.rslid.setEnabled(False)

        self.bluespinBox.setEnabled(False)
        self.redspinBox.setEnabled(False)
        self.greenspinBox.setEnabled(False)
        self.checkBox.setEnabled(False)


    def PreCamera(self): #摄像头初始化
        try:
            self.camera = cv2.VideoCapture(0)
            self.MsgText.clear()
            self.MsgText.setText('摄像头未连接')

        except Exception as e:
            self.MsgText.clear()
            self.MsgText.append(str(e))

    def PrepParameters(self):
        self.RecordFlag = 0
        self.RecordPath = '/usr/home/qiao//PycharmProjects/PythonLearning/pyqt/video'
        self.Filepath.setText(self.RecordPath)
        self.Image_num = 0
        self.R = 1
        self.G = 1
        self.B = 1
    def SSHconnect(self):

        user_name = 'qql'
        host_port = 22
        password ='002218'
        self.host_ip = self.sshlinetext.text()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.host_ip, host_port, user_name, password)
            self.MsgText.setText('Connection to {} success to established!'.format(self.host_ip))
            self.sshlinetext.setEnabled(False)
            self.sshbtn.setEnabled(False)
        except Exception:
            self.MsgText.setText('Connection is falure to established! Try again')
            self.sshlinetext.setText('')
            self.ssh.close()


        # print(out)
        # if out is null:
        #     self.MsgText.setText('Connection is falure to established! Try again')
        #     self.ssh.close()
        # else:
        #     self.MsgText.setText('Connection to {} success to established!'.format(self.host_ip))
        #     self.sshbtn.setEnabled(False)
        # 关闭连接
        # ssh.close()

        # self.MsgText.setText('Connection to {} success to established!'.format(self.host_ip))
        # self.sshbtn.setEnabled(False)
        #




    def StartCam(self):
        self.startbtn.setEnabled(False)
        self.stopbtn.setEnabled(True)
        self.rslid.setEnabled(True)
        self.gsld.setEnabled(True)
        self.bsld.setEnabled(True)
        self.checkBox.setEnabled(True)

        self.redspinBox.setEnabled(True)
        self.greenspinBox.setEnabled(True)
        self.bluespinBox.setEnabled(True)
        self.Timer.start(1) #开启计时器，计时器连接到了TimerOutFun函数，1ms轮训
        self.timelb = time.clock()
        self.MsgText.setPlainText('<-------------------摄像头已打开---------------------->')

    def StopCamera(self):
        if self.stopbtn.text() == '暂停':
            self.stopbtn.setText('继续')
            self.savebtn.setText('保存')
            self.Timer.stop()
            self.MsgText.setPlainText('摄像已暂停')
        elif self.stopbtn.text() == '继续':
            self.stopbtn.setText('暂停')
            self.savebtn.setText('录像')
            self.Timer.start(1)
            self.MsgText.setPlainText('摄像已继续')

    def TimerOutFun(self):
        success,frame = self.camera.read(0)
        if success:
            self.Img = self.ColorAdjust(frame)
            self.Display()
            self.Image_num +=1
            if self.RecordFlag:
                self.video_writer.write(self.Img)
            if self.Image_num % 10 == 9:
                frame_rate = 10 / (time.clock() - self.timelb)
                self.lcdNumber.display(frame_rate)
                self.timelb = time.clock()
        else:
            self.MsgText.clear()
            self.MsgText.setPlainText('摄像头故障')

    def SetGray(self):
        if self.checkBox.isChecked():
            self.rslid.setEnabled(False)
            self.gsld.setEnabled(False)
            self.bsld.setEnabled(False)
            self.redspinBox.setEnabled(False)
            self.greenspinBox.setEnabled(False)
            self.bluespinBox.setEnabled(False)
        else:
            self.rslid.setEnabled(True)
            self.gsld.setEnabled(True)
            self.bsld.setEnabled(True)
            self.redspinBox.setEnabled(True)
            self.greenspinBox.setEnabled(True)
            self.bluespinBox.setEnabled(True)

    def Display(self):
        if self.checkBox.isChecked():
            img = cv2.cvtColor(self.Img,cv2.COLOR_BGR2GRAY)
        else:
            img = cv2.cvtColor(self.Img,cv2.COLOR_BGR2RGB) #更换颜色通道
        qimg = qimage2ndarray.array2qimage(img)
        self.ImgDIsplay.setPixmap(QPixmap(qimg))
        self.ImgDIsplay.show()

    def SetR(self):
        R = self.rslid.value()
        self.R = R / 255

    def SetG(self):
        G = self.gsld.value()
        self.G = G / 255

    def SetB(self):
        B = self.bsld.value()
        self.B = B / 255


    def ColorAdjust(self,img):
        try:
            B = img[:, :, 0]
            G = img[:, :, 1]
            R = img[:, :, 2]
            B = B * self.B
            G = G * self.G
            R = R * self.R
            img1 = img
            img1[:, :, 0] = B
            img1[:, :, 1] = G
            img1[:, :, 2] = R
            return img1
        except Exception as e:
            self.MsgText.setPlainText(str(e))
    def SetFilePath(self):
        dirname = QFileDialog.getExistingDirectory(self, "浏览", '.')
        if dirname:
            self.FilePathLE.setText(dirname)
            self.RecordPath = dirname + '/'



    def CallBackFunctions(self):
        # self.Filepathbtn_2.clicked.connect(self.SetFilePath)
        self.startbtn.clicked.connect(self.StartCam)

        self.stopbtn.clicked.connect(self.StopCamera)
        self.checkBox.stateChanged.connect(self.SetGray)
        self.sshbtn.clicked.connect(self.SSHconnect)
        # self.savebtn.clicked.connect(self.RecordCamera)
        # self.exitbtn.clicked.connect(self.ExitApp)
        self.bsld.valueChanged.connect(self.SetB)
        self.gsld.valueChanged.connect(self.SetG)
        self.rslid.valueChanged.connect(self.SetR)











if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CamShow()
    ui.show()
    sys.exit(app.exec_())

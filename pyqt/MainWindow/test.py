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
import socket

class CamShow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CamShow, self).__init__(parent)
        self.msg = '欢迎使用BIO-viewer系统 author by：qiao \n'
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
        # self.savebtn.setEnabled(False)
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
            self.msg +='摄像头未连接 \n'
            self.MsgText.setText(self.msg)

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
        self.localhost = os.popen("ifconfig wlp0s20f3 |grep inet |head -n 1 |awk '{print $2}'").read().replace('\n','')
        self.host_ip = self.sshlinetext.text()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.host_ip, host_port, user_name, password)
            self.msg +='Connection to {} success to established! \n'.format(self.host_ip)
            self.MsgText.setText(self.msg)
            self.sshlinetext.setEnabled(False)
            self.sshbtn.setEnabled(False)

        except Exception:
            self.msg +='Connection is falure to established! Try again \n'
            self.MsgText.setText(self.msg)
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

    def reciveVId(self):

        # IP地址'0.0.0.0'为等待客户端连接
        address = ('10.192.16.116', 9008)
        # 建立socket对象，参数意义见https://blog.csdn.net/rebelqsp/article/details/22109925
        # socket.AF_INET：服务器之间网络通信
        # socket.SOCK_STREAM：流式socket , for TCP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将套接字绑定到地址, 在AF_INET下,以元组（host,port）的形式表示地址.
        self.s.bind(address)
        # 开始监听TCP传入连接。参数指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。
        self.s.listen(1)

        # 接受TCP连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。addr是连接客户端的地址。
        # 没有连接则等待有连接
        conn, addr = self.s.accept()
        print('connect from:' + str(addr))
        print(conn)
        size = (640, 480)
        # videowriter = cv2.VideoWriter('recive.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), 10, size)
        while 1:
            length = recvall(conn, 16)  # 获得图片文件的长度,16代表获取长度
            stringData = recvall(conn, int(length))  # 根据获得的文件长度，获取图片文件
            data = numpy.frombuffer(stringData, numpy.uint8)  # 将获取到的字符流数据转换成1维数组
            self.Img = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 将数组解码成图像
            self.Display()
            # cv2.imwrite("./MainWindow.jpg", decimg)
            # videowriter.write(decimg)
            # cv2.imshow('SERVER', decimg)  # 显示图像
            # cv2.waitKey(1)

            # end = time.time()
            # seconds = end - start
            # fps = 1 / seconds;
            # conn.send(bytes(str(int(fps)), encoding='utf-8'))
            # k = cv2.waitKey(10)&0xff
            # if k == 27:
            #    break
        s.close()
    def sendvideo(self):
        stdin, stdout, stderr = self.ssh.exec_command("python3 /home/qql/Desktop/MainWindow/sendvideo.py")
        out = stdout.readlines()
        err = stderr.readlines()
        print(err, out)




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
        self.savebtn.clicked.connect(self.reciveVId)
        self.exitbtn.clicked.connect(self.sendvideo)
        self.bsld.valueChanged.connect(self.SetB)
        self.gsld.valueChanged.connect(self.SetG)
        self.rslid.valueChanged.connect(self.SetR)











if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CamShow()
    ui.show()
    sys.exit(app.exec_())

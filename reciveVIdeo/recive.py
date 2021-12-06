import qimage2ndarray
from PyQt5.QtGui import QPixmap
import threading
from reviveVideo import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import sys
import cv2
import time
import sys
from detector import Detector
from MainWindow.gongju import torch
from udp import ChatRoomPlus
import paramiko
from timeit import default_timer as timer
import os
import numpy
from socket import *
from PyQt5.QtWidgets import QApplication, QMainWindow

class recieve(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(recieve, self).__init__()
        self.setupUi(self)
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.exitbtn.clicked.connect(self.stop)
        self.startbtn.clicked.connect(self.open)


    def open(self):
        th = threading.Thread(target=self.start, daemon=True)
        th.start()
    def stop(self):  # 连接中断，线程需要信号量
        self.stopEvent.set()

    def start(self):
        # 全局参数配置
        self.encoding = "utf-8"  # 使用的编码方式
        self.recvbroadcastPort = 10101  # 广播端口
        self.recvSocket = socket(AF_INET, SOCK_DGRAM)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.recvSocket.bind(('', self.recvbroadcastPort))

        det = Detector()
        dic = [(148, 110),(549, 361)]

        torchDet = torch('rect', dic, det)

        print("UDP接收器启动成功...")
        while 1:
            # 接收数据格式：(data, (ip, port))
            recvData, addr = self.recvSocket.recvfrom(400000)
            recvData = np.frombuffer(recvData, dtype=np.uint8)
            if recvData[0]:
                decimg = cv2.imdecode(recvData, 1)
                decimg = torchDet.torchdetect(decimg)
                # print("imshow........")
            img = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(img)
            self.Image.setPixmap(QPixmap(qimg))
            if self.stopEvent.is_set():
                sendData = '1'
                self.stopEvent.clear()
                self.recvSocket.sendto(sendData.encode("utf-8"), ('10.192.44.57', 10102))
                print("线程已经结束")
                break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = recieve()
    ui.show()
    sys.exit(app.exec_())
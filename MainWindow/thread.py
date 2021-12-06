
'''
导入深度学习模块
'''
import qimage2ndarray
from PyQt5.QtGui import QPixmap
import threading
from videosave import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import sys
import cv2
import time
import sys
from timeit import default_timer as timer
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from timeit import default_timer as timer

ROOT_DIR = os.path.abspath("../../../PycharmProjects")
sys.path.append(os.path.join(ROOT_DIR, "keras-yolo3-master/"))  #模型存放路径
import yolo


class CamShow(QMainWindow, Ui_MainWindow):
    """docstring for Mywine"""

    def __init__(self):
        super(CamShow, self).__init__()
        self.setupUi(self)

        self.startbtn.clicked.connect(self.open)
        self.recivebtn.clicked.connect(self.stop)

        self.stopEvent = threading.Event()
        self.stopEvent.clear()


    def open(self):
        self.vid = cv2.VideoCapture(0)
        th = threading.Thread(target=self.Display)
        th.start()


    def stop(self):
        self.stopEvent.set()

    def Display(self):
        start = timer()
        self.temp = yolo.YOLO()
        end = timer()



        print(end -start)
        while self.vid.isOpened():
            success, frame = self.vid.read()
            image = Image.fromarray(frame)
            image = self.temp.detect_image(image)
            result = np.asarray(image)
            img = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)  # 更换颜色通道
            qimg = qimage2ndarray.array2qimage(img)
            self.image.setPixmap(QPixmap(qimg))
            # self.image.show()


            if self.stopEvent.is_set():
                self.stopEvent.clear()
                self.image.clear()
                self.cam.release()
                break
        self.temp.close_session()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CamShow()
    ui.show()
    sys.exit(app.exec_())

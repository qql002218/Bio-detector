
import multiprocessing
from collections import deque
import qimage2ndarray
from PyQt5.QtGui import QPixmap, QTextCursor
import threading
from MainWindow.video import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication
from MainWindow.Childwindow import MyDialog
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import sys
import cv2
import time
import sys
import paramiko
from timeit import default_timer as timer
import os
import numpy
from socket import *
from PyQt5.QtWidgets import QApplication, QMainWindow

from MainWindow.gongju import DrawLineWidget, cv2ImgAddText, torch
from detector import Detector

# ROOT_DIR = os.path.abspath("../../../PycharmProjects")
# sys.path.append(os.path.join(ROOT_DIR, "keras-yolo3-master/"))  # 模型存放路径
# import yolo


from pyqt.login.log import LogFile

class CamShow(QMainWindow, Ui_MainWindow):
    """docstring for Mywine"""

    receiveLogSignal = pyqtSignal(str)  # 为msgbox设置信号
    logQueue = multiprocessing.SimpleQueue()  # 将信息存入进一个阻塞队列

    def __init__(self):
        super(CamShow, self).__init__()
        self.setupUi(self)

        self.startbtn.clicked.connect(self.open)
        self.sendbtn.clicked.connect(self.send)
        self.stopbtn.clicked.connect(self.stop)
        self.sshbutton.clicked.connect(self.SSH)
        self.stopEvent = threading.Event()
        self.exitbtn.clicked.connect(self.exit)

        self.stopEvent.clear()
        self.time = time.strftime("%Y-%m-%d", time.localtime())
        path = '/home/qiao/PycharmProjects/PythonLearning/LogFile/{}/{}.txt'.format(self.time, self.time)
        self.logFile = open(path, 'a')
        #########
        self.receiveLogSignal.connect(lambda log: self.logOutput(log))
        self.logOutputThread = threading.Thread(target=self.receiveLog, daemon=True)
        self.logOutputThread.start()
        #########
        self.check.clicked.connect(self.openMyDialog)
        ########
        self.flag = False  # 标定是否完成的标志
        self.fixbtn.clicked.connect(self.fix)
        ##
        self.yolobtn.clicked.connect(self.pytorchstart)

    def receiveLog(self):
        while True:
            data = self.logQueue.get()
            if data:
                self.receiveLogSignal.emit(data)
            else:
                continue

    def fix(self):
        '''
        标定：截取一张图片，按图片上的水印进行操作，并且获取划线 或感兴趣区域的坐标值，同时在后续检测中进行区域划分
        '''
        # draw_line_widget=DrawLineWidget(self.frametemp)
        self.clone = self.frametemp
        self.frametemp = cv2ImgAddText(self.frametemp, "按下l键，进行分割线划定" + '\n' + "按下d键，进行区域框划定", 10, 40, (0, 0, 139), 20)
        # cv2ImgAddText(self.frametemp, "按下d键，进行区域框划定", 10, 60, (0, 0, 139), 20)
        while True:
            cv2.imshow('image', self.frametemp)
            key = cv2.waitKey(1)
            # Close program with keyboard 'q'
            if key == ord('l'):
                temp = cv2ImgAddText(self.clone, "开始进行划线操作", 10, 40, (0, 0, 139), 20)
                draw_line_widget = DrawLineWidget(temp, key='draw_line')
                self.logQueue.put('开始进行标定，划线操作 \n')
                break
            if key == ord('d'):
                temp = cv2ImgAddText(self.clone, "开始进行划框操作", 10, 40, (0, 0, 139), 20)
                draw_line_widget = DrawLineWidget(temp, key='draw_rect')
                self.logQueue.put('开始进行标定，画框操作 \n')
                break
        while True:
            cv2.imshow('image', draw_line_widget.show_image())
            key = cv2.waitKey(1)
            # Close program with keyboard 'q'
            if key == ord('q'):
                self.fixdata = draw_line_widget.getData()
                if self.fixdata.get('line') is not None:
                    self.logQueue.put(
                        '标定工作完成，操作为划线操作，起点：{}，终点{} \n'.format(self.fixdata.get('line')[0], self.fixdata.get('line')[1]))
                else:
                    self.logQueue.put(
                        '标定工作完成，操作为画框操作，右上角：{}，左下角{} \n'.format(self.fixdata.get('rect')[0],
                                                                self.fixdata.get('rect')[1]))
                self.flag = True
                cv2.destroyAllWindows()
                break

    def logOutput(self, log):
        # 获取当前系统时间
        self.time = self.gettime()
        log = self.time + '------->:' + log
        # 写入日志文件
        self.logFile.write(log)
        # 　界面日志打印
        self.msgbox.moveCursor(QTextCursor.End)
        self.msgbox.insertPlainText(log)
        self.msgbox.ensureCursorVisible()  # 自动滚屏

    def gettime(self):  # 获得时间的方法
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def SSH(self):
        """
        ssh方法
        """
        user_name = 'qiaoge'  # 远端服务器名字
        host_port = 22
        password = 'qiaoge'  # 密码
        dest_ip = self.sshiptext.text()  # 文本行获得远端连接IP
        dest_ip = '10.192.44.57'
        print(dest_ip)
        self.ssh = paramiko.SSHClient()  # 用paramiko建立客户端
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(dest_ip, host_port, user_name, password)  # ssh连接
            self.logQueue.put('SSH远程连接操作: host:{0} 连接成功 \n'.format(dest_ip))

            # self.msgbox.ensureCursorVisible()
            self.sshiptext.setEnabled(False)
            self.sshbutton.setEnabled(False)

        except Exception as e:
            self.sshiptext.setText('')
            self.logfile.write('SSH远程连接操作: host:{} 连接失败 \n'.format(dest_ip))

    def exit(self):
        self.logQueue.put('系统退出')
        try:
            self.logFile.close()
        except Exception as e:
            print(e)
        finally:
            QCoreApplication.quit()

    def open(self):  # 开启接收，while循环，中间方法

        th = threading.Thread(target=self.recive, daemon=True)
        th.start()

    def send(self):  # 开始发送 中间方法
        th2 = threading.Thread(target=self.sendstart, daemon=True)
        th2.start()

    def yolostart(self):
        th3 = threading.Thread(target=self.yolodetect, daemon=True)
        th3.start()

    def pytorchstart(self):
        th4 = threading.Thread(target=self.torchdetect, daemon=True)
        th4.start()

    def torchdetect(self):
        self.recvSocket = socket(AF_INET, SOCK_DGRAM)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.recvSocket.bind(('', 10101))
        det = Detector()
        flag = 'rect' if self.fixdata.get('line') is None else 'line'
        self.torchDet = torch(flag, self.fixdata.get(flag), det)
        self.logQueue.put('torch 模型已经load成功... \n')

        while 1:
            # 接收数据格式：(data, (ip, port))
            recvData, addr = self.recvSocket.recvfrom(400000)
            recvData = np.frombuffer(recvData, dtype=np.uint8)
            if recvData[0]:
                decimg = cv2.imdecode(recvData, 1)
                decimg = self.torchDet.torchdetect(decimg)
                # print("imshow........")
            img = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(img)
            self.image.setPixmap(QPixmap(qimg))
            if self.stopEvent.is_set():
                sendData = '1'
                self.stopEvent.clear()
                self.recvSocket.sendto(sendData.encode("utf-8"), ('10.192.44.57', 10102))
                print("线程已经结束")
                break


    # def yolodetect(self):
    #     # self.temp = yolo.YOLO()
    #     self.logQueue.put('模型已经load成功... \n')
    #
    #     self.localhost = os.popen("ifconfig wlp0s20f3 |grep inet |head -n 1 |awk '{print $2}'").read().replace('\n', '')
    #     address = (self.localhost, 9008)
    #     self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.s.bind(address)
    #     self.s.listen(1)
    #     self.logQueue.put('客户端开始接收数据... \n')
    #
    #     def recvall(sock, count):
    #         buf = b''  # buf是一个byte类型
    #         while count:
    #             # 接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
    #             newbuf = sock.recv(count)
    #             if not newbuf: return None
    #             buf += newbuf
    #             count -= len(newbuf)
    #         return buf
    #
    #     conn, addr = self.s.accept()
    #     self.logQueue.put('连接已建立, connect from {},图像显示! \n'.format(str(addr)))
    #     print('connect from:' + str(addr))
    #     print(conn)
    #
    #     while 1:
    #         start = time.time()  # 用于计算帧率信息
    #         length = recvall(conn, 16)  # 获得图片文件的长度,16代表获取长度
    #         stringData = recvall(conn, int(length))  # 根据获得的文件长度，获取图片文件
    #         data = numpy.frombuffer(stringData, numpy.uint8)  # 将获取到的字符流数据转换成1维数组
    #         decimg = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 将数组解码成图像
    #         end = time.time()
    #         seconds = end - start
    #         fps = round(1 / seconds, 2)
    #         conn.send(bytes(str(int(fps)), encoding='utf-8'))
    #         decimg = cv2.putText(decimg, "FPS:{}".format(fps), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    #
    #         if self.flag is True:
    #             if self.fixdata.get('line') is not None:
    #                 decimg = Image.fromarray(decimg)
    #                 image = self.temp.detect_image(decimg)
    #                 decimg = np.asarray(image)
    #                 cv2.line(decimg, self.fixdata.get('line')[0], self.fixdata.get('line')[1], (36, 255, 12), 2)
    #
    #             else:
    #                 decimg = Image.fromarray(decimg)
    #                 image = self.temp.detect_image(decimg)
    #                 decimg = np.asarray(image)
    #                 cv2.rectangle(decimg, self.fixdata.get('rect')[0], self.fixdata.get('rect')[1], (36, 255, 12), 2)
    #         img = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
    #
    #         qimg = qimage2ndarray.array2qimage(img)
    #         self.image.setPixmap(QPixmap(qimg))
    #         if self.stopEvent.is_set():
    #             self.stopEvent.clear()
    #             self.frametemp = decimg
    #             print("线程已经结束")
    #             break

    def sendstart(self):
        """
        远端登录ssh，执行发送命令
        """
        stdin, stdout, stderr = self.ssh.exec_command(
            "python3 /home/qiaoge/test/udp.py {hostip}".format(hostip=self.localhost),timeout=3)  # localhost 绑定
        self.logQueue.put('服务器开始发送数据... \n')
        # out = stdout.readlines()
        # err = stderr.readlines()
        # print(err, out)

    def stop(self):  # 连接中断，线程需要信号量
        self.stopEvent.set()

    def recive(self):
        self.localhost = os.popen("ifconfig wlp0s20f3 |grep inet |head -n 1 |awk '{print $2}'").read().replace('\n', '')
        self.encoding = "utf-8"  # 使用的编码方式
        self.recvbroadcastPort = 10101  # 广播端口
        self.recvSocket = socket(AF_INET, SOCK_DGRAM)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.recvSocket.bind(('', self.recvbroadcastPort))

        self.logQueue.put('客户端开始接收数据...\n')
        while 1:
            # 接收数据格式：(data, (ip, port))
            recvData, addr = self.recvSocket.recvfrom(400000)
            recvData = np.frombuffer(recvData, dtype=np.uint8)
            if recvData[0]:
                decimg = cv2.imdecode(recvData, 1)
                # print("imshow........")
            img = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(img)
            self.image.setPixmap(QPixmap(qimg))
            if self.stopEventssh.py.is_set():
                sendData = '1'
                self.stopEvent.clear()
                self.recvSocket.sendto(sendData.encode("utf-8"), ('10.192.44.57', 10102))
                self.frametemp = img
                command = "ps -aux |grep udp | head -n 1 |awk 'print $2"
                _,out,_=self.ssh.exec_command(f"{command}")
                print(out.readlines())
                print("线程已经结束")
                break


    def openMyDialog(self):
        my = MyDialog()
        my.mySignal.connect(self.getDialogSignal)
        my.exec_()

    def getDialogSignal(self, connect):
        para = eval(connect)
        pre = ''
        info_2 = ''
        if self.balance.isChecked():
            pre = '开始进行 平衡木实验\n'
            info_2 = ''
        if self.rolate.isChecked():
            pre = '开始进行 转棒实验\n'
            info_2 = '转速：{} r/min 加速度：{} r/min2'.format(para.get('rotate_v'), para.get('rotate_a'))
        if self.track.isChecked():
            pre = '开始进行 辐照跟踪实验 \n'
            info_2 = '运动区域:长 {} m 宽{}m'.format(para.get('hight'), para.get('width'))
        if self.swim.isChecked():
            pre = '开始进行 游泳实验\n'
            info_2 = '水温 {} 摄氏度'.format(para.get('water_temp'))

        info = '******硬件参数****** \n' \
               '载波参数\n' \
               '载波频率:{0}GHz  载波幅值:{1}V\n' \
               '调制参数\n' \
               '幅值：{2}V 偏置：{3}V 波形:{4}\n' \
               '******环境参数****** \n' \
               '辐照距离：{5} m\n'.format(para.get("zaibo_freq"), para.get("zaibo_power"), para.get("tiaozhi_amp"),
                                     para.get("tiaozhi_bias"), para.get("wave"), para.get("distance"))

        info = pre + info + info_2
        self.logQueue.put(info)
        self.testinfo.setText(info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CamShow()
    ui.show()
    sys.exit(app.exec_())

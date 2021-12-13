import math
import multiprocessing
from collections import deque
import qimage2ndarray
from PyQt5.QtGui import QPixmap, QTextCursor
import threading

from MainWindow.subwindow import App
from resVIew import myMainWindow
from MainWindow.video import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication, QDateTime, QTimer
from MainWindow.Childwindow import MyDialog  # 对话框，主要是试验参数的选取

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
from pyqt.login.log import LogFile
import json


# ROOT_DIR = os.path.abspath("../../../PycharmProjects")
# sys.path.append(os.path.join(ROOT_DIR, "keras-yolo3-master/"))  # 模型存放路径
# import yolo


class CamShow(QMainWindow, Ui_MainWindow):
    """docstring for Mywine"""

    receiveLogSignal = pyqtSignal(str)  # 为msgbox设置信号
    logQueue = multiprocessing.SimpleQueue()  # 将信息存入进一个阻塞队列
    subWinSignal = pyqtSignal(list)  # 为数据可视化设置list 信号

    def __init__(self):
        super(CamShow, self).__init__()
        self.setupUi(self)

        self.startbtn.clicked.connect(self.open)
        self.sendbtn.clicked.connect(self.send)
        self.stopbtn.clicked.connect(self.stop)
        self.sshbutton.clicked.connect(self.SSH)
        self.stopEvent = threading.Event()
        self.exitbtn.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.expEnd)
        self.btn_openVid.clicked.connect(self.resultView)

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
        self.flag = False  # 标定是否完成标定的标志
        self.fixbtn.clicked.connect(self.fix)
        ##
        self.yolobtn.clicked.connect(self.pytorchstart)
        ##时间戳 系统时间label相关
        self.timer = QTimer()
        self.timer.timeout.connect(self.showtime)
        self.starttimer()
        #数据回放窗口
        self.resview = myMainWindow()
        # 子窗口和父窗口通信
        self.sub_win = App()
        # 可视化数据
        self.dataViewbtn.clicked.connect(self.visualizeData)
        self.sub_data = ''
        self.subWinSignal.connect(lambda log2: self.sub_win.getData(log2))
        self.subWinThread = threading.Thread(target=self.subWinFunc, daemon=True)
        self.subWinThread.start()

    def subWinFunc(self):
        while True:
            time.sleep(0.5)
            if self.sub_data != '':
                self.subWinSignal.emit(self.sub_data)

    def visualizeData(self):
        self.sub_win.show()
    #数据回放窗口展示
    def resultView(self):
        self.resview.show()

    def expEnd(self):  # 实验结束应该做的事
        self.stopEvent.set()
        command = "ps -aux |grep udp | head -n 1 |awk '{print $2}'"
        _, out, _ = self.ssh.exec_command(f"{command}")
        pid = out.readlines()[0].replace('/n', '')
        self.ssh.exec_command(f"kill {pid}")
        time.sleep(0.5)
        self.expResinfo.setText(self.resinfo)




    ##主窗口的 系统时间相关
    def showtime(self):
        time = QDateTime.currentDateTime()  # 获取当前时间
        timedisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")  # 格式化一下时间
        self.label_time.setText(timedisplay)

    def starttimer(self):
        self.timer.start(1000)

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
        # dest_ip = '10.192.61.97'
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
        time1 = time.strftime("%H:%M:%S", time.localtime())
        exp = self.exptemp
        path = '/home/qiao/PycharmProjects/PythonLearning/LogFile/{}/{}-{}'.format(
            time.strftime("%Y-%m-%d", time.localtime()), time1, exp)
        if not os.path.exists(path):
            os.mkdir(path)  # 创建实验文件夹
        file_path = path + '/实验报告'
        os.system("touch {}".format(file_path))  # 创建实验报告

        json_path = path + 'json数据.json'


        logFile = open(file_path, 'a')
        logFile.write(self.info)
        logFile.close()


        # videowriter = cv2.VideoWriter(path+'/实验视频.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), 20, (741,491))

        saveflag = True if self.savevidBox.isChecked() else False
        if saveflag:
            videowriter = cv2.VideoWriter(path + '/MyoutputVid-pre.avi', cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 20,
                                      (741, 491))
            videowriter2 = cv2.VideoWriter(path + '/MyoutputVid-lst.avi', cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 20,
                                      (741, 491))
        # print('save flag is{}'.format(saveflag))
        self.recvSocket = socket(AF_INET, SOCK_DGRAM)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.recvSocket.bind(('', 10101))
        det = Detector()
        flag = 'rect' if self.fixdata.get('line') is None else 'line'
        if flag is 'rect':
            x = self.fixdata.get(flag)[1][0] - self.fixdata.get(flag)[0][0]
            y = self.fixdata.get(flag)[1][1] - self.fixdata.get(flag)[0][1]
            width = int(self.para.get('width'))
            hight = int(self.para.get('hight'))
            px_convert = round(math.sqrt((width / x) ** 2 + ((hight / y) ** 2)), 2)
            # print(f'px_convert:{px_convert}')  #坐标值换算
            # print(f'x:{x}')
            # print(f'y:{y}')
            # print(f'widith:{width}')
            # print(f'hight:{hight}')
            self.torchDet = torch(flag, self.fixdata.get(flag), det, px_convert)
        else:
            self.torchDet = torch(flag, self.fixdata.get(flag), det, 0) #划线操作 px_convert 可以缺省
        self.logQueue.put('模型已加载完毕...\n')
        self.sub_data=[path]
        # self.sub_data.append(self.exptemp)
        #这块注意时序问题，点击实验开始按钮，data signal emit ，其长度为2，包含路径信息 和实验名称


        while 1:
            # 接收数据格式：(data, (ip, port))
            recvData, addr = self.recvSocket.recvfrom(400000)
            recvData = np.frombuffer(recvData, dtype=np.uint8)
            if recvData[0]:
                decimg = cv2.imdecode(recvData, 1)
                if saveflag:
                    videowriter.write(decimg)
                decimg = self.torchDet.torchdetect(decimg)
                if saveflag:
                    videowriter2.write(decimg)
                # print("imshow........")
            img = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(img)

            self.sub_data = self.torchDet.data
            # for j in range(1,len(self.sub_data)):
            #     if len(self.sub_data[j]) != 0:
            #         print(f'track id :{j} : {self.sub_data[j]}')
            # print('--------------------------------------------------------')
            self.image.setPixmap(QPixmap(qimg))
            if self.stopEvent.is_set():
                sendData = '1'
                self.stopEvent.clear()
                # self.recvSocket.sendto(sendData.encode("utf-8"), ('10.192.44.57', 10102))
                print("线程已经结束")
                if saveflag:
                    videowriter.release()
                    videowriter2.release()
                self.logQueue.put('{}实验结束\n'.format(self.exptemp))
                break
        logFile = open(file_path, 'a')
        logFile.write('------------实验结果-------------\n')
        info = ''
        if flag is 'rect':
            for j in range(1,len(self.sub_data)):
                if len(self.sub_data[j]) != 0:
                    temp = self.sub_data[j]
                    result = temp[len(temp)-1][1]
                    info=info+'traker_{} 老鼠，运动距离为 {} cm\n'.format(j,result)
            logFile.write(info)

        if flag is 'line':
            for i in range(len(self.sub_data)):
                if len(self.sub_data[i]) != 0:
                    info = info+'tracker_{}老鼠，在{}中坚持时间为{}s\n'.format(i,self.exptemp,self.sub_data[i])
            logFile.write(info)
        self.resinfo = info
        self.para['result'] = self.resinfo
        jaso_path = path+'/record.json'
        with open(jaso_path, 'w+',encoding='utf-8') as f: #将最后的结果进行存储成json 格式
            json.dump(self.para,f,ensure_ascii=False,indent = 4)
            print("加载入文件完成...")
            f.close()

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
    #         decimg = cv2.putText(decimg, "FPS:{}".format(fps), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)    #
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
            "python3 /home/qiaoge/test/udp.py {hostip}&".format(hostip=self.localhost))  # localhost 绑定
        self.logQueue.put('服务器开始发送数据... \n')
        # out = stdout.readlines()
        # err = stderr.readlines()
        # print(err, out)

    def stop(self):  # 连接中断，线程需要信号量
        self.stopEvent.set()
        command = "ps -aux |grep udp | head -n 1 |awk '{print $2}'"
        _, out, _ = self.ssh.exec_command(f"{command}")
        pid = out.readlines()[0].replace('/n', '')
        self.ssh.exec_command(f"kill {pid}")
        print(pid)

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
            start = time.time()
            recvData, addr = self.recvSocket.recvfrom(400000)
            recvData = np.frombuffer(recvData, dtype=np.uint8)
            if recvData[0]:
                decimg = cv2.imdecode(recvData, 1)
                # print("imshow........")
            end = time.time()
            seconds = end - start
            fps = round(1 / seconds, 2)
            decimg = cv2.putText(decimg, "FPS:{}".format(fps), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            img = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(img)
            self.image.setPixmap(QPixmap(qimg))
            if self.stopEvent.is_set():
                sendData = '1'
                self.stopEvent.clear()
                self.recvSocket.sendto(sendData.encode("utf-8"), ('10.192.44.57', 10102))
                self.frametemp = decimg
                print("线程已经结束")
                self.logQueue.put('远程视频联通测试结束，标定照片已保存....\n')
                break

    def openMyDialog(self):
        my = MyDialog()
        my.mySignal.connect(self.getDialogSignal)
        my.exec_()

    def getDialogSignal(self, connect):
        self.para = eval(connect)
        self.exptemp = ''
        pre = ''
        info_2 = ''
        if self.balance.isChecked():
            self.exptemp = '平衡木实验'
            pre = '开始进行 平衡木实验\n'
            info_2 = ''
        if self.rolate.isChecked():
            self.exptemp = '转棒实验'
            pre = '开始进行 转棒实验\n'
            info_2 = '转速：{} r/min 加速度：{} r/min2\n'.format(self.para.get('rotate_v'), self.para.get('rotate_a'))
        if self.track.isChecked():
            self.exptemp = '辐照跟踪实验'
            pre = '开始进行 辐照跟踪实验 \n'
            info_2 = '运动区域:长 {} cm 宽{} cm \n'.format(self.para.get('hight'), self.para.get('width'))
        if self.swim.isChecked():
            self.exptemp = '游泳实验'
            pre = '开始进行 游泳实验\n'
            info_2 = '水温 {} 摄氏度'.format(self.para.get('water_temp'))

        info = '******硬件参数****** \n' \
               '载波参数\n' \
               '载波频率:{0}GHz  载波幅值:{1}V\n' \
               '调制参数\n' \
               '幅值：{2}V 偏置：{3}V 波形:{4}\n' \
               '******环境参数****** \n' \
               '辐照距离：{5} m\n'.format(self.para.get("zaibo_freq"), self.para.get("zaibo_power"),
                                     self.para.get("tiaozhi_amp"),
                                     self.para.get("tiaozhi_bias"), self.para.get("wave"), self.para.get("distance"))
        self.para['exp'] = self.exptemp


        self.info = pre + info + info_2
        # self.json ={ '实验名称':self.exptemp,"载波频率":self.para.get("zaibo_freq"),'载波幅值':self.para.get("zaibo_power"),'幅值':self.para.get("tiaozhi_amp"),
        #              '偏置':self.para.get("tiaozhi_bias"),'波形':self.para.get("wave"),'辐照距离':self.para.get("distance"),'转棒转速':self.para.get('rotate_v'),
        #              '转棒加速度':self.para.get('rotate_a'),'运动区域长':self.para.get('hight'),'运动区域宽':self.para.get('width')
        # }
        self.logQueue.put(f'----------------------{self.exptemp}实验开始---------------------\n')
        self.logQueue.put('系统参数设定完毕...\n')
        self.testinfo.setText(self.info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CamShow()
    ui.show()
    sys.exit(app.exec_())

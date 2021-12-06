import cv2
from socket import *
from time import ctime, sleep
import threading
import numpy as np


class ChatRoomPlus:
    def __init__(self):
        # 全局参数配置
        self.encoding = "utf-8"  # 使用的编码方式
        self.recvbroadcastPort = 10101  # 广播端口
        self.sendbroadcastPort = 10102

        # 创建广播接收器
        self.recvSocket = socket(AF_INET, SOCK_DGRAM)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.recvSocket.bind(('', self.recvbroadcastPort))

        # 创建广播发送器
        self.sendSocket = socket(AF_INET, SOCK_DGRAM)
        self.sendSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.sendData=None
        # 其他
        self.threads = []

    def send(self):
        """发送广播"""
        self.sendData = "1"
        print("UDP发送器启动成功...")
        while True:

            self.sendSocket.sendto(self.sendData.encode(self.encoding), ('10.192.44.57', self.sendbroadcastPort))
            #print("【%s】%s:%s" % (ctime(), "我", self.sendData))

            #sleep(1)
        self.sendSocket.close()

    def recv(self):
        """接收广播"""

        print("UDP接收器启动成功...")
        cv2.namedWindow('img')
        while True:
            # 接收数据格式：(data, (ip, port))
            recvData, addr = self.recvSocket.recvfrom(400000)
            recvData = np.frombuffer(recvData, dtype=np.uint8)
            if recvData[0]:
                imde = cv2.imdecode(recvData, 1)
                print("imshow........")
                cv2.imshow('img', imde)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    self.sendData="0"
                    break

           # sleep(1)
        self.recvSocket.close()
        cv2.destroyAllWindows()



    def start(self):
        """启动线程"""

        t1 = threading.Thread(target=self.recv)
        t2 = threading.Thread(target=self.send)
        self.threads.append(t1)
        self.threads.append(t2)

        for t in self.threads:
            t.setDaemon(True)
            t.start()

        while True:
            pass


if __name__ == "__main__":
    demo = ChatRoomPlus()
    demo.start()
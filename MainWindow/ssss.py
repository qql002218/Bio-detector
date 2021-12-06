import cv2
from socket import *
from time import ctime, sleep
import threading


class ChatRoomPlus:
    def __init__(self):
        # 全局参数配置
        self.encoding = "utf-8"  # 使用的编码方式
        self.recvbroadcastPort = 10102   # 广播端口
        self.sendbroadcastPort = 10101
        # 创建广播接收器
        self.recvSocket = socket(AF_INET, SOCK_DGRAM)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.recvSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.recvSocket.bind(('', self.recvbroadcastPort))
        self.recvData=None

        # 创建广播发送器
        self.sendSocket = socket(AF_INET, SOCK_DGRAM)
        self.sendSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)



        # 其他
        self.threads = []

    def send(self):
        """发送广播"""
        cap = cv2.VideoCapture('ex2.mp4')
        # cap.set(3, 224)
        # cap.set(4, 224)
        print("UDP发送器启动成功...")

        while True:
            print(self.recvData)
            if self.recvData == b'1':
                ret, fra = cap.read()
                if ret:
                    print(ret)
                    _, sendData = cv2.imencode('.jpg', fra)
                    print(sendData.size)
                    print(fra.size)
                    self.sendSocket.sendto(sendData, ('255.255.255.255', self.sendbroadcastPort))

            sleep(1)
        self.sendSocket.close()
        cap.release()

    def recv(self):
        """接收广播"""

        print("UDP接收器启动成功...")
        while True:
            # 接收数据格式：(data, (ip, port))
            self.recvData, addr = self.recvSocket.recvfrom(1024)

            # print("【%s】[%s : %s] : %s" % (ctime(), self.recvData[1][0], self.recvData[1][1], self.recvData[0].decode(self.encoding)))

            #sleep(1)
        self.recvSocket.close()

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
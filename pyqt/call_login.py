#导入程序运行必须模块
import datetime
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
import time

from PyQt5.QtWidgets import QApplication, QMainWindow
#导入designer工具生成的login模块
from login import test, log
import pymysql
from MainWindow.ssh import CamShow
import pyqt.login.resource_rc #重要！！！！！ 增加配置好的resource文件


class MyMainForm(QMainWindow, test.Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.login_btn.clicked.connect(self.check)
        # 添加退出按钮信号和槽。调用close函数
        self.quit_btn.clicked.connect(self.close)



    def check(self):
        # 利用line Edit控件对象text()函数获取界面输入
        username = self.username.text()
        password = self.password.text()
        print('用户名: {name}---> 密码：{password}'.format(name= username,password=password))
        conn = pymysql.connect(user='root', password='123', database="test", charset="utf8")
        cur = conn.cursor()
        res = cur.execute("select passwd from user where name = '{na}' and passwd = '{pd}';".format(na=username,pd =password))
        if res ==0:
            self.username.setText('用户或密码错误')
            self.password.setText('')

        else:

            conn.close()
            logfile = log.LogFile()
            file = open(logfile.getLogFile(), 'a')
            msg = '用户：{} 于 {} 系统登录 \n'.format(username,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            file.write(msg)
            file.close()
            self.toMainWindow()


    def toMainWindow(self):
        self.ui1 = CamShow()
        self.ui1.show()

        self.close()


if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
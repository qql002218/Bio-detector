# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1344, 813)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(300, 50, 741, 491))
        self.image.setFrameShape(QtWidgets.QFrame.Box)
        self.image.setText("")
        self.image.setObjectName("image")
        self.msgbox = QtWidgets.QTextEdit(self.centralwidget)
        self.msgbox.setGeometry(QtCore.QRect(300, 580, 741, 171))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msgbox.sizePolicy().hasHeightForWidth())
        self.msgbox.setSizePolicy(sizePolicy)
        self.msgbox.setFrameShape(QtWidgets.QFrame.Box)
        self.msgbox.setObjectName("msgbox")
        self.exitbtn = QtWidgets.QPushButton(self.centralwidget)
        self.exitbtn.setGeometry(QtCore.QRect(1230, 710, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.exitbtn.setFont(font)
        self.exitbtn.setObjectName("exitbtn")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 30, 281, 381))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(0, 120, 67, 17))
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 150, 241, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.check = QtWidgets.QPushButton(self.layoutWidget)
        self.check.setObjectName("check")
        self.gridLayout.addWidget(self.check, 0, 1, 1, 1)
        self.yolobtn = QtWidgets.QPushButton(self.layoutWidget)
        self.yolobtn.setObjectName("yolobtn")
        self.gridLayout.addWidget(self.yolobtn, 2, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)
        self.rolate = QtWidgets.QCheckBox(self.layoutWidget)
        self.rolate.setObjectName("rolate")
        self.gridLayout.addWidget(self.rolate, 1, 0, 1, 1)
        self.track = QtWidgets.QCheckBox(self.layoutWidget)
        self.track.setObjectName("track")
        self.gridLayout.addWidget(self.track, 2, 0, 1, 1)
        self.swim = QtWidgets.QCheckBox(self.layoutWidget)
        self.swim.setObjectName("swim")
        self.gridLayout.addWidget(self.swim, 3, 0, 1, 1)
        self.balance = QtWidgets.QCheckBox(self.layoutWidget)
        self.balance.setObjectName("balance")
        self.gridLayout.addWidget(self.balance, 0, 0, 1, 1)
        self.fixbtn = QtWidgets.QPushButton(self.layoutWidget)
        self.fixbtn.setObjectName("fixbtn")
        self.gridLayout.addWidget(self.fixbtn, 1, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(21, 31, 256, 68))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sshiptext = QtWidgets.QLineEdit(self.layoutWidget1)
        self.sshiptext.setObjectName("sshiptext")
        self.horizontalLayout.addWidget(self.sshiptext)
        self.sshbutton = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sshbutton.setFont(font)
        self.sshbutton.setObjectName("sshbutton")
        self.horizontalLayout.addWidget(self.sshbutton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startbtn = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.startbtn.setFont(font)
        self.startbtn.setObjectName("startbtn")
        self.horizontalLayout_2.addWidget(self.startbtn)
        self.sendbtn = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sendbtn.setFont(font)
        self.sendbtn.setObjectName("sendbtn")
        self.horizontalLayout_2.addWidget(self.sendbtn)
        self.stopbtn = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stopbtn.setFont(font)
        self.stopbtn.setObjectName("stopbtn")
        self.horizontalLayout_2.addWidget(self.stopbtn)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.savevidBox = QtWidgets.QCheckBox(self.groupBox)
        self.savevidBox.setGeometry(QtCore.QRect(20, 350, 141, 23))
        self.savevidBox.setObjectName("savevidBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(470, 10, 351, 41))
        font = QtGui.QFont()
        font.setFamily("Noto Sans CJK SC")
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1120, 720, 101, 20))
        self.label_3.setObjectName("label_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 420, 281, 331))
        self.groupBox_2.setObjectName("groupBox_2")
        self.testinfo = QtWidgets.QLabel(self.groupBox_2)
        self.testinfo.setGeometry(QtCore.QRect(0, 30, 281, 291))
        self.testinfo.setFrameShape(QtWidgets.QFrame.Box)
        self.testinfo.setText("")
        self.testinfo.setObjectName("testinfo")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 321, 20))
        self.label_4.setObjectName("label_4")
        self.label_time = QtWidgets.QLabel(self.centralwidget)
        self.label_time.setGeometry(QtCore.QRect(1040, 0, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_time.setFont(font)
        self.label_time.setText("")
        self.label_time.setObjectName("label_time")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(300, 550, 67, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.dataViewbtn = QtWidgets.QPushButton(self.centralwidget)
        self.dataViewbtn.setGeometry(QtCore.QRect(1050, 80, 121, 41))
        self.dataViewbtn.setObjectName("dataViewbtn")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1050, 130, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(1060, 260, 241, 401))
        self.textEdit.setObjectName("textEdit")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1060, 237, 81, 20))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1344, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.exitbtn.setText(_translate("MainWindow", "退出"))
        self.groupBox.setTitle(_translate("MainWindow", "系统设置"))
        self.label.setText(_translate("MainWindow", "功能选项"))
        self.check.setText(_translate("MainWindow", "功能选定"))
        self.yolobtn.setText(_translate("MainWindow", "开始实验"))
        self.pushButton_2.setText(_translate("MainWindow", "实验结束"))
        self.rolate.setText(_translate("MainWindow", "转棒实验"))
        self.track.setText(_translate("MainWindow", "辐照运动跟踪"))
        self.swim.setText(_translate("MainWindow", "游泳实验"))
        self.balance.setText(_translate("MainWindow", "平衡木实验"))
        self.fixbtn.setText(_translate("MainWindow", "标定"))
        self.sshiptext.setPlaceholderText(_translate("MainWindow", "请输入服务器ip"))
        self.sshbutton.setText(_translate("MainWindow", "ssh连接"))
        self.startbtn.setText(_translate("MainWindow", "绑定接收"))
        self.sendbtn.setText(_translate("MainWindow", "远端发送"))
        self.stopbtn.setText(_translate("MainWindow", "暂停"))
        self.savevidBox.setText(_translate("MainWindow", "保存实验视频"))
        self.label_2.setText(_translate("MainWindow", "BIO Viewer 生物辐照检测系统"))
        self.label_3.setText(_translate("MainWindow", "Author by:115 "))
        self.groupBox_2.setTitle(_translate("MainWindow", "实验信息"))
        self.label_4.setText(_translate("MainWindow", " Enhancements and suggestions are welcome！ "))
        self.label_6.setText(_translate("MainWindow", "消息框"))
        self.dataViewbtn.setText(_translate("MainWindow", "数据可视化"))
        self.pushButton.setText(_translate("MainWindow", "打开视频"))
        self.label_5.setText(_translate("MainWindow", "实验结果"))

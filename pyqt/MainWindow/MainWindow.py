# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1062, 819)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.setUI = QtWidgets.QFrame(self.centralwidget)
        self.setUI.setGeometry(QtCore.QRect(0, 50, 381, 621))
        self.setUI.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setUI.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setUI.setObjectName("setUI")
        self.gridLayout = QtWidgets.QGridLayout(self.setUI)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.setUI)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout.addWidget(self.frame_2, 2, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.setUI)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gLab = QtWidgets.QLabel(self.frame_4)
        self.gLab.setObjectName("gLab")
        self.gridLayout_2.addWidget(self.gLab, 2, 0, 1, 1)
        self.rLab = QtWidgets.QLabel(self.frame_4)
        self.rLab.setObjectName("rLab")
        self.gridLayout_2.addWidget(self.rLab, 1, 0, 1, 1)
        self.gsld = QtWidgets.QSlider(self.frame_4)
        self.gsld.setMaximum(255)
        self.gsld.setOrientation(QtCore.Qt.Horizontal)
        self.gsld.setObjectName("gsld")
        self.gridLayout_2.addWidget(self.gsld, 2, 1, 1, 1)
        self.greenspinBox = QtWidgets.QSpinBox(self.frame_4)
        self.greenspinBox.setMaximum(255)
        self.greenspinBox.setObjectName("greenspinBox")
        self.gridLayout_2.addWidget(self.greenspinBox, 2, 3, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.frame_4)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 2)
        self.redspinBox = QtWidgets.QSpinBox(self.frame_4)
        self.redspinBox.setMaximum(255)
        self.redspinBox.setObjectName("redspinBox")
        self.gridLayout_2.addWidget(self.redspinBox, 1, 3, 1, 1)
        self.bLab = QtWidgets.QLabel(self.frame_4)
        self.bLab.setObjectName("bLab")
        self.gridLayout_2.addWidget(self.bLab, 4, 0, 1, 1)
        self.bsld = QtWidgets.QSlider(self.frame_4)
        self.bsld.setMaximum(255)
        self.bsld.setOrientation(QtCore.Qt.Horizontal)
        self.bsld.setObjectName("bsld")
        self.gridLayout_2.addWidget(self.bsld, 4, 1, 1, 1)
        self.bluespinBox = QtWidgets.QSpinBox(self.frame_4)
        self.bluespinBox.setMaximum(255)
        self.bluespinBox.setObjectName("bluespinBox")
        self.gridLayout_2.addWidget(self.bluespinBox, 4, 3, 1, 1)
        self.rslid = QtWidgets.QSlider(self.frame_4)
        self.rslid.setMaximum(255)
        self.rslid.setOrientation(QtCore.Qt.Horizontal)
        self.rslid.setObjectName("rslid")
        self.gridLayout_2.addWidget(self.rslid, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_4, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.setUI)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 67, 17))
        self.label_2.setObjectName("label_2")
        self.Filepath = QtWidgets.QLineEdit(self.frame)
        self.Filepath.setGeometry(QtCore.QRect(80, 20, 211, 25))
        self.Filepath.setObjectName("Filepath")
        self.Filepathbtn = QtWidgets.QPushButton(self.frame)
        self.Filepathbtn.setGeometry(QtCore.QRect(298, 20, 41, 25))
        self.Filepathbtn.setObjectName("Filepathbtn")
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
        self.dispUI = QtWidgets.QFrame(self.centralwidget)
        self.dispUI.setGeometry(QtCore.QRect(400, 50, 651, 621))
        self.dispUI.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dispUI.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dispUI.setObjectName("dispUI")
        self.startbtn = QtWidgets.QPushButton(self.dispUI)
        self.startbtn.setGeometry(QtCore.QRect(70, 20, 89, 25))
        self.startbtn.setObjectName("startbtn")
        self.stopbtn = QtWidgets.QPushButton(self.dispUI)
        self.stopbtn.setGeometry(QtCore.QRect(210, 20, 89, 25))
        self.stopbtn.setObjectName("stopbtn")
        self.savebtn = QtWidgets.QPushButton(self.dispUI)
        self.savebtn.setGeometry(QtCore.QRect(350, 20, 89, 25))
        self.savebtn.setObjectName("savebtn")
        self.exitbtn = QtWidgets.QPushButton(self.dispUI)
        self.exitbtn.setGeometry(QtCore.QRect(490, 20, 89, 25))
        self.exitbtn.setObjectName("exitbtn")
        self.ImgDIsplay = QtWidgets.QLabel(self.dispUI)
        self.ImgDIsplay.setGeometry(QtCore.QRect(26, 66, 581, 471))
        self.ImgDIsplay.setFrameShape(QtWidgets.QFrame.Box)
        self.ImgDIsplay.setText("")
        self.ImgDIsplay.setObjectName("ImgDIsplay")
        self.label = QtWidgets.QLabel(self.dispUI)
        self.label.setGeometry(QtCore.QRect(220, 560, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lcdNumber = QtWidgets.QLCDNumber(self.dispUI)
        self.lcdNumber.setGeometry(QtCore.QRect(320, 560, 121, 41))
        self.lcdNumber.setObjectName("lcdNumber")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(0, 670, 1051, 91))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.MsgText = QtWidgets.QTextEdit(self.frame_3)
        self.MsgText.setObjectName("MsgText")
        self.gridLayout_3.addWidget(self.MsgText, 0, 0, 1, 1)
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 10, 911, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ssh_label = QtWidgets.QLabel(self.layoutWidget)
        self.ssh_label.setObjectName("ssh_label")
        self.horizontalLayout.addWidget(self.ssh_label)
        self.sshlinetext = QtWidgets.QLineEdit(self.layoutWidget)
        self.sshlinetext.setObjectName("sshlinetext")
        self.horizontalLayout.addWidget(self.sshlinetext)
        self.sshbtn = QtWidgets.QPushButton(self.layoutWidget)
        self.sshbtn.setObjectName("sshbtn")
        self.horizontalLayout.addWidget(self.sshbtn)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1062, 28))
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
        self.gLab.setText(_translate("MainWindow", "G"))
        self.rLab.setText(_translate("MainWindow", "R"))
        self.checkBox.setText(_translate("MainWindow", "GRAY"))
        self.bLab.setText(_translate("MainWindow", "B"))
        self.label_2.setText(_translate("MainWindow", "????????????"))
        self.Filepathbtn.setText(_translate("MainWindow", "???"))
        self.startbtn.setText(_translate("MainWindow", "??????"))
        self.stopbtn.setText(_translate("MainWindow", "??????"))
        self.savebtn.setText(_translate("MainWindow", "??????"))
        self.exitbtn.setText(_translate("MainWindow", "??????"))
        self.label.setText(_translate("MainWindow", "????????????"))
        self.ssh_label.setText(_translate("MainWindow", "SSH??????"))
        self.sshlinetext.setPlaceholderText(_translate("MainWindow", "?????????????????????ip??????"))
        self.sshbtn.setText(_translate("MainWindow", "??????"))

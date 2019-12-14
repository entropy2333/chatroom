import json
import time
import base64
import socket
import threading
# import hashlib
from utils import *
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class chatroom_mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(chatroom_mainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowModality(QtCore.Qt.WindowModal)
        mainWindow.setMinimumSize(970, 710)
        mainWindow.setMaximumSize(970, 710)
        mainWindow.setStyleSheet('#mainWindow{border-image:url(bg2.jpg)}')

        self.centralWidget = QWidget(mainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.label = QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 70, 220, 50))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label.setStyleSheet('font-size:20px;font-family:微软雅黑')

        self.label_1 = QLabel(self.centralWidget)
        self.label_1.setGeometry(QtCore.QRect(230, 70, 100, 40))
        self.label_1.setTextFormat(QtCore.Qt.AutoText)
        self.label_1.setObjectName("label_1")
        self.label_1.setStyleSheet('font-size:20px;font-family:微软雅黑')

        self.label_2 = QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(80, 0, 220, 70))
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet('font-size:20px;font-family:微软雅黑')

        self.label.setStyleSheet('font-size:20px;font-family:微软雅黑')
        self.label_1.setStyleSheet('font-size:20px;font-family:微软雅黑')
        self.label_2.setStyleSheet('font-size:20px;font-family:微软雅黑')

        # self.pixmap = QPixmap('1.jpeg')
        # self.pixmap.rect()
        # self.pixmap.setGeometry(QtCore.QRect(10, 5, 80, 80))
        
        self.list = QListWidget(self.centralWidget)
        self.list.setGeometry(0, 120, 220, 580)
        self.list.setVerticalScrollBarPolicy(2)

        self.list.addItem("Jack")
        self.list.addItem("Lily")
        self.list.addItem("Lucy")
        self.list.addItem("Rob")
        self.list.setStyleSheet('font-size:28px;font-family:微软雅黑;border-width:0px;border-style:solid')

        self.pushButton = QPushButton(self.centralWidget)
        self.pushButton.setGeometry(860, 670, 80, 30)
        # self.pushButton.clicked.connect(self.send_msg)
        self.pushButton.setStyleSheet('font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')

        self.pushButton_1 = QPushButton(self.centralWidget)
        self.pushButton_1.setGeometry(760, 670, 80, 30)
        self.pushButton_1.setStyleSheet('font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')
        # self.pushButton_1.clicked.connect(self.send_img)

        self.textEdit = QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(220, 545, 750, 115)
        self.textEdit.setStyleSheet('font-size:16px;font-family:微软雅黑;border-width:0px;border-style:solid')

        self.stackedwidget = QStackedWidget(self.centralWidget)
        self.stackedwidget.setGeometry(QtCore.QRect(220, 115, 750, 430))
        # self.stackedwidget.connectNotify

        for i in range(self.list.count()):
            text = self.list.item(i).text()
            log = QTextEdit(self.centralWidget)
            log.setGeometry(230, 35, 730, 500)
            log.setText(text)
            log.setVerticalScrollBarPolicy(2)
            log.setReadOnly(True)
            self.stackedwidget.addWidget(log)
            log.setStyleSheet('font-size:16px;font-family:微软雅黑;border-width:0px;border-style:solid')

        # self.stackedwidget.setCurrentIndex(1)
        # self.list.setCurrentIndex(1)
        
        mainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(mainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "hello world"))
        # self.log.setText(_translate("MainWindow", "聊天记录"))
        self.label.setText(_translate("mainWindow", "好友列表"))
        self.label_1.setText(_translate("mainWindow", "好友昵称"))
        self.label_2.setText(_translate("mainWindow", "Jack"))
        self.pushButton.setText(_translate("mainWindow", "发送"))
        self.pushButton_1.setText(_translate("mainWindow", "图片"))
        self.textEdit.setPlaceholderText(_translate("mainWindow", "请输入消息"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = chatroom_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
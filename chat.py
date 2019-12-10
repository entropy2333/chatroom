import json
import time
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
        self.logs = {}
        self.client_socket = None
        super(chatroom_mainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        # self.init_info(self)

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowModality(QtCore.Qt.WindowModal)
        mainWindow.setMinimumSize(970, 710)
        mainWindow.setMaximumSize(970, 710)

        self.centralWidget = QWidget(mainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.label = QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 75, 80, 20))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")

        self.label_1 = QLabel(self.centralWidget)
        self.label_1.setGeometry(QtCore.QRect(235, 5, 100, 20))
        self.label_1.setTextFormat(QtCore.Qt.AutoText)
        self.label_1.setObjectName("label_1")

        self.label_2 = QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 5, 80, 20))
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")

        # self.pixmap = QPixmap('1.jpeg')
        # self.pixmap.rect()
        # self.pixmap.setGeometry(QtCore.QRect(10, 5, 80, 80))
        
        self.list = QListWidget(self.centralWidget)
        self.list.setGeometry(5, 100, 220, 600)
        self.list.setVerticalScrollBarPolicy(2)
        self.list.addItem("Jack")
        self.list.addItem("Lily")
        self.list.addItem("Lucy")
        self.list.addItem("Rob")
        self.list.currentRowChanged.connect(self.switchlog)
        
        self.pushButton = QPushButton(self.centralWidget)
        self.pushButton.setGeometry(880, 710, 80, 30)
        self.pushButton.clicked.connect(self.send_msg)

        self.textEdit = QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(230, 580, 730, 120)
        
        self.stackedwidget = QStackedWidget(self.centralWidget)
        self.stackedwidget.setGeometry(QtCore.QRect(230, 35, 730, 500))

        for i in range(self.list.count()):
            text = self.list.item(i).text()
            log = QTextEdit(self.centralWidget)
            log.setGeometry(230, 35, 730, 500)
            log.setText(text)
            log.setVerticalScrollBarPolicy(2)
            log.setReadOnly(True)
            self.stackedwidget.addWidget(log)
        
        # self.log = QTextEdit(self.centralWidget)
        # self.log.setGeometry(230, 35, 730, 500)
        # self.log.setVerticalScrollBarPolicy(2)
        # self.log.setReadOnly(True)
        
        mainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(mainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "hello word"))
        # self.log.setText(_translate("MainWindow", "聊天记录"))
        self.label.setText(_translate("MainWindow", "好友列表"))
        self.label_1.setText(_translate("MainWindow", "好友昵称"))
        self.label_2.setText(_translate("MainWindow", "我"))
        self.pushButton.setText(_translate("MainWindow", "发送"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "请输入消息"))
    
    def send_msg(self):
        index = self.stackedwidget.currentIndex()
        nickname = self.list.item(index).text()
        content = self.textEdit.toPlainText()
        if not content:
            QMessageBox.information(self, "error", "发送内容不能为空，请重新输入")
        else:
            req = {
                "op": 3,
                "args": {
                    "src_nickname": 'Jack',
                    "dst_nickname": nickname,
                    "content": content
                }
            }
            if send_func(self.client_socket, req):
                self.textEdit.setPlainText('')
            else:
                QMessageBox.information(self, "error", "发送失败")

    def recv_msg(self):
        while True:
            recv_content = recv_func(self.client_socket)
            if recv_content['op'] == 3:
                src_nickname = recv_content['args']['src_nickname']
                dst_nickname = recv_content['args']['dst_nickname']
                content = recv_content['args']['content']
                log = self.stackedwidget.currentWidget()
                # 将鼠标指针移至末尾
                cursor = log.textCursor()
                cursor.movePosition(QtGui.QTextCursor.End)
                log.setTextCursor(cursor)
                log.insertPlainText('\n'+src_nickname+':')
                log.insertPlainText('\n\t'+content)
            else:
                pass
    
    def send_hearbeat(self):
        req = {
            'op': 5,
            'args': {
                'account': 'Jack',
                'check_alive': True
            }
        }
        if not send_func(self.client_socket, req):
            QMessageBox.information(self, "error", "与服务器失去连接")
        time.sleep(10)

    def switchlog(self, i):
        self.stackedwidget.setCurrentIndex(i)
        
    def init_info(self):
        # send_thread = threading.Thread(target=self.send_msg)
        # send_thread.start()
        recv_thread = threading.Thread(target=self.recv_msg)
        recv_thread.start()
    
    def run(self):
        init_thread = threading.Thread(target=self.init_info)
        init_thread.start()

        heartbeat = threading.Thread(target=self.send_hearbeat)
        heartbeat.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = chatroom_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
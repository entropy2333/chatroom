import json
import time
import socket
import hashlib
from utils import *
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class register_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(register_MainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(386, 127)
        MainWindow.setWindowIcon(QIcon('logo.png'))
        MainWindow.setStyleSheet('#MainWindow{border-image:url(register.jpg)}')

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 20, 150, 30))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 50, 150, 30))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(70, 80, 150, 30))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.lineEdit.setStyleSheet('font-size:18px;font-family:微软雅黑;'+
                    'border-width:1px;border-style:solid;border-color:#d1d1d1;border-radius:3px;')
        self.lineEdit_2.setStyleSheet('font-size:18px;font-family:微软雅黑;'+
                    'border-width:1px;border-style:solid;border-color:#d1d1d1;border-radius:3px;')
        self.lineEdit_3.setStyleSheet('font-size:18px;font-family:微软雅黑;'+
                    'border-width:1px;border-style:solid;border-color:#d1d1d1;border-radius:3px;')

        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(30, 25, 40, 20))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(30, 55, 40, 20))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(30, 85, 40, 20))
        self.label_3.setObjectName("label_3")

        self.label.setStyleSheet('font-size:18px;font-family:微软雅黑;')
        self.label_2.setStyleSheet('font-size:18px;font-family:微软雅黑;')
        self.label_3.setStyleSheet('font-size:18px;font-family:微软雅黑;')

        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 50, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet('font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')
        # self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        # self.pushButton_2.setGeometry(QtCore.QRect(250, 60, 75, 23))
        # self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton.clicked.connect(self.commit)
        # self.pushButton_2.clicked.connect(self.cancel)

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "注册"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入帐号"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "请输入昵称"))
        self.label.setText(_translate("MainWindow", "帐号"))
        self.label_2.setText(_translate("MainWindow", "密码"))
        self.label_3.setText(_translate("MainWindow", "昵称"))
        self.pushButton.setText(_translate("MainWindow", "提交"))
        # self.pushButton_2.setText(_translate("MainWindow", "取消"))

    def commit(self):
        account = self.lineEdit.text()
        passwd = self.lineEdit_2.text()
        nickname = self.lineEdit_3.text()
        if not account or not passwd or not nickname:
            QMessageBox.information(self, "info", "请填写信息")
            return 
        # md5 = hashlib.md5()
        # md5.update(password.encode())
        # password = md5.hexdigest()
        req = {
            "op": 'register',
            "args": {
                "account": account,
                "password": passwd
            }
        }
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP_PORT = ('127.0.0.1', 8888)
        client_socket.connect(IP_PORT)
        send_func(client_socket, req)
        recv_content = recv_func(client_socket)
        
        if recv_content['op'] == 'register':
            if recv_content['args']['check_flag']:
                QMessageBox.information(self, "info", "注册成功")
            else:
                QMessageBox.information(self, "info", "注册失败")
        else:
            QMessageBox.information(self, "info", "服务器未响应")
        
        client_socket.close()
        
    # def cancel(self):
    #     # MainWindow.show()
    #     ui_register.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui_register = register_MainWindow()
    ui_register.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

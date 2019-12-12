import json
import socket
# import hashlib
from chat import *
from utils import *
from register import *
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.client_socket = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        # MainWindow.resize(386, 127)
        # 尺寸与Background.jpg相关
        MainWindow.setMaximumSize(386, 127)
        MainWindow.setMinimumSize(386, 127)
        MainWindow.setWindowIcon(QIcon('logo.png'))
        MainWindow.setStyleSheet('background-image:url(Background.jpg)')

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName('centralWidget')

        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(250, 20, 100, 20))
        self.lineEdit.setText('')
        self.lineEdit.setObjectName('lineEdit')

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 50, 100, 20))
        self.lineEdit_2.setText('')
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName('lineEdit_2')

        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(200, 20, 30, 20))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName('label')

        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(200, 50, 30, 20))
        self.label_2.setObjectName('label_2')
        
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 90, 75, 23))
        self.pushButton.setObjectName('pushButton')

        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 90, 75, 23))
        self.pushButton_2.setObjectName('pushButton_2')

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)

        MainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', '登陆程序'))
        self.lineEdit.setPlaceholderText(_translate('MainWindow', '请输入帐号'))
        self.lineEdit_2.setPlaceholderText(_translate('MainWindow', '请输入密码'))
        self.label.setText(_translate('MainWindow', '帐号'))
        self.label_2.setText(_translate('MainWindow', '密码'))
        self.pushButton.setText(_translate('MainWindow', '登陆'))
        self.pushButton_2.setText(_translate('MainWindow', '注册'))

    def login(self):
        '''
        登陆
        '''
        account = self.lineEdit.text()
        passwd = self.lineEdit_2.text()
        # md5 = hashlib.md5()
        # md5.update(password.encode())
        # password = md5.hexdigest()
        req = {
            'op': 1,
            'args': {
                'account': account,
                'passwd': passwd
            }
        }
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            IP_PORT = ('127.0.0.1', 8888)
            self.client_socket.connect(IP_PORT)
            # self.client_socket.settimeout(0.2)
            send_func(self.client_socket, req)
            recv_content = recv_func(self.client_socket)
            if recv_content['op'] == 1:
                if recv_content['args']['check_flag']:
                    # login success
                    ui_chatroom.user_info = recv_content['args']['user_info']
                    ui_chatroom.user_list = recv_content['args']['user_list']
                    ui_chatroom.client_socket = ui.client_socket
                    ui_chatroom.show()
                    ui_chatroom.run()
                    MainWindow.close()
            else:
                # login error
                self.client_socket.close()
                QMessageBox.information(self, 'info', '登陆出错')
        except Exception as e:
            QMessageBox.information(self, 'info', '登陆出错')
            self.client_socket.close()
            # self.lineEdit.setFocus()
    
    def register(self):
        '''
        注册
        '''
        
        ui_register.setWindowModality(Qt.ApplicationModal)
        ui_register.show()
        # MainWindow.close()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui_chatroom = chatroom_mainWindow()
    ui_register = register_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
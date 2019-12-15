import os
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

    def __init__(self, client_socket, user_list, user_info, users_online):
        # self.logs = {}
        self.client_socket = client_socket
        self.user_list = user_list
        self.user_info = user_info
        self.users_online = users_online
        super(chatroom_mainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        # self.init_info(self)

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

        self.label_1 = QLabel(self.centralWidget)
        self.label_1.setGeometry(QtCore.QRect(230, 70, 100, 40))
        self.label_1.setTextFormat(QtCore.Qt.AutoText)
        self.label_1.setObjectName("label_1")

        self.label_2 = QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(80, 0, 220, 70))
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")

        self.label.setStyleSheet('font-size:20px;font-family:微软雅黑')
        self.label_1.setStyleSheet('font-size:20px;font-family:微软雅黑')
        self.label_2.setStyleSheet('font-size:20px;font-family:微软雅黑')

        # self.pixmap = QPixmap('1.jpeg')
        # self.pixmap.rect()
        # self.pixmap.setGeometry(QtCore.QRect(10, 5, 80, 80))
        
        self.list = QListWidget(self.centralWidget)
        self.list.setGeometry(0, 120, 220, 580)
        self.list.setVerticalScrollBarPolicy(2)

        for user in self.user_list:
            self.list.addItem(user)

        # self.list.addItem("Jack")
        # self.list.addItem("Lily")
        # self.list.addItem("Lucy")
        # self.list.addItem("Rob")

        self.list.currentRowChanged.connect(self.switchlog)
        self.list.setStyleSheet('font-size:28px;font-family:微软雅黑;border-width:0px;border-style:solid')

        self.pushButton = QPushButton(self.centralWidget)
        self.pushButton.setGeometry(860, 670, 80, 30)
        self.pushButton.clicked.connect(self.send_msg)
        self.pushButton.setStyleSheet('font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')

        self.pushButton_1 = QPushButton(self.centralWidget)
        self.pushButton_1.setGeometry(760, 670, 80, 30)
        self.pushButton_1.clicked.connect(self.send_img)
        self.pushButton_1.setStyleSheet('font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')

        self.textEdit = QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(220, 545, 750, 115)
        self.textEdit.setStyleSheet('font-size:16px;font-family:微软雅黑;border-width:0px;border-style:solid')

        self.stackedwidget = QStackedWidget(self.centralWidget)
        self.stackedwidget.setGeometry(QtCore.QRect(220, 115, 750, 430))

        for i in range(self.list.count()):
            text = self.list.item(i).text()
            log = QTextEdit(self.centralWidget)
            log.setGeometry(230, 35, 730, 500)
            log.setText(text)
            log.setVerticalScrollBarPolicy(2)
            log.setReadOnly(True)
            self.stackedwidget.addWidget(log)
            log.setStyleSheet('font-size:16px;font-family:微软雅黑;border-width:0px;border-style:solid')

        mainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        # self.stackedwidget.setCurrentIndex(1)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "hello world"))
        # self.log.setText(_translate("MainWindow", "聊天记录"))
        self.label.setText(_translate("MainWindow", "好友列表"))
        self.label_1.setText(_translate("MainWindow", "好友昵称"))
        self.label_2.setText(_translate("MainWindow", self.user_info[2]))
        self.pushButton.setText(_translate("MainWindow", "发送"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "请输入消息"))
    
    def send_msg(self):
        '''
        发送消息
        '''
        index = self.stackedwidget.currentIndex()
        dst_nickname = self.list.item(index).text()
        content = self.textEdit.toPlainText()
        time = time_func()
        if not content:
            QMessageBox.information(self, "error", "发送内容不能为空，请重新输入")
        else:
            self.textEdit.setPlainText('')
            log = self.stackedwidget.currentWidget()
            # 将鼠标指针移至末尾
            cursor = log.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            log.setTextCursor(cursor)
            log.insertPlainText('\n' + self.user_info[2] + '  ' + time)
            log.insertPlainText('\n  ' + content)
            # 发给自己，直接打印
            if dst_nickname == self.user_info[2]:
                return 
            req = {
                "op": 'send_msg',
                "args": {
                    "src_info": self.user_info,
                    "dst_nickname": dst_nickname,
                    "content": content,
                    'time': time
                }
            }
            send_func(self.client_socket, req)
            # else:
            #     QMessageBox.information(self, "error", "发送失败")

    def scaled_img(self, img_path):
        '''
        将图片按一定比例缩放
        
        Arguments:
            img_path {str} -- 图片路径
        
        Returns:
            QTextImageFormat -- 图片
        '''
        img = QImageReader(img_path).read()
        image = QTextImageFormat()
        image.setName(img_path)
        width = img.width()
        height = img.height()
        ratio = width / height
        scale = max(750/width, 430/height)
        if scale < 1:
            width, height = width * 0.4 * scale, height * 0.4 * scale
        if scale > 5:
            width, height = width * 2, height * 2
        image.setWidth(width)
        image.setHeight(height)
        return image

    def send_img(self):
        '''
        发送图片并显示到聊天界面
        '''
        index = self.stackedwidget.currentIndex()
        dst_nickname = self.list.item(index).text()
        img_path = QFileDialog().getOpenFileName(self, 'Open File', './') # type: tuple
        img_path = img_path[0] # type: str
        # 未选定图片，路径为空
        if not img_path:
            return 
        img_name = img_path.split('/')[-1] # type: str
        time = time_func()
        img = self.scaled_img(img_path)
        # img = QTextImageFormat()
        # img.setName(img_path)
        log = self.stackedwidget.currentWidget()
        # 将鼠标指针移至末尾
        cursor = log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        log.setTextCursor(cursor)
        log.insertPlainText('\n' + self.user_info[2] + '  ' + time + '\n  ')
        cursor.insertImage(img)
        # 发送给自己，直接打印
        if dst_nickname == self.user_info[2]:
            return
        with open (img_path, 'rb') as f:
            content = f.read() # type: bytes
            img_str = base64.encodebytes(content).decode('utf-8') # type: str
        req = {
            'op': 'send_img',
            'args': {
                "src_info": self.user_info,
                "dst_nickname": dst_nickname,
                'img_name': img_name,
                'img_str': img_str,
                'time': time
            }
        }
        send_func(self.client_socket, req)

    def refresh_user(self):
        pass
        # users = []
        # for i in range(self.list.count()):
        #     users.append(self.list.item(i).text())
        # for user in self.user_list:
        #     if user not in self.users_online:
        #         self.list.item(user.index()).setBackround(QColor('red'))
        #     else:
        #         self.list.item(user.index()).setBackround(QColor('green'))

    def recv_msg(self):
        '''
        接收消息并打印
        '''
        while True:
            try:
                recv_content = recv_func(self.client_socket)
                if recv_content['op'] == 'send_msg':
                    src_nickname = recv_content['args']['src_nickname']
                    dst_nickname = recv_content['args']['dst_nickname']
                    time = recv_content['args']['time']
                    if src_nickname == dst_nickname:
                        pass
                    content = recv_content['args']['content']
                    index = self.user_list.index(src_nickname)
                    self.switchlog(index)
                    # self.list.setCurrentIndex(index)
                    log = self.stackedwidget.currentWidget()
                    # 将鼠标指针移至末尾
                    cursor = log.textCursor()
                    cursor.movePosition(QtGui.QTextCursor.End)
                    log.setTextCursor(cursor)
                    log.insertPlainText('\n' + src_nickname + '  ' + time)
                    log.insertPlainText('\n  ' + content)

                elif recv_content['op'] == 'send_img':
                    src_nickname = recv_content['args']['src_nickname']
                    dst_nickname = recv_content['args']['dst_nickname']
                    tiem = recv_content['args']['time']
                    if src_nickname == dst_nickname:
                        pass
                    img_name = recv_content['args']['img_name']
                    img_str = recv_content['args']['img_str']
                    img_data = base64.b64decode(img_str)
                    img_path = os.path.join(os.path.dirname(__file__), 'image_cache', img_name)
                    with open (img_path, 'wb+') as f:
                        f.write(img_data)

                    img = self.scaled_img(img_path)
                    # img = QTextImageFormat()
                    # img.setName(img_path)
                    index = self.user_list.index(src_nickname)
                    self.switchlog(index)
                    # self.list.setCurrentIndex(index)
                    # 将鼠标指针移至末尾
                    log = self.stackedwidget.currentWidget()
                    cursor = log.textCursor()
                    cursor.movePosition(QtGui.QTextCursor.End)
                    log.setTextCursor(cursor)
                    log.insertPlainText('\n' + src_nickname + '  ' + time + '\n')
                    cursor.insertImage(img)

                elif recv_content['op'] == 'new_user':
                    self.users_online = recv_content['args']['users_online']
                    time = recv_content['args']['time']
                    self.refresh_user()
                else:
                    pass
            except Exception as e:
                pass

    def switchlog(self, i):
        self.stackedwidget.setCurrentIndex(i)
    
    def run(self):
        recv_thread = threading.Thread(target=self.recv_msg)
        recv_thread.start()
        # self.recv_msg()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = chatroom_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
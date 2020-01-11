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
        self.user_list.insert(0, 'Group')
        self.user_info = user_info
        self.users_online = users_online
        super(chatroom_mainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowModality(QtCore.Qt.WindowModal)
        mainWindow.setMinimumSize(970, 710)
        mainWindow.setMaximumSize(970, 710)
        mainWindow.setStyleSheet('#mainWindow{border-image:url(img/bg2.png)}')

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
        
        self.list = QListWidget(self.centralWidget)
        self.list.setGeometry(0, 120, 220, 580)
        self.list.setVerticalScrollBarPolicy(2)

        for user in self.user_list:
            self.list.addItem(user)

        self.list.currentRowChanged.connect(self.switchlog)
        self.list.setStyleSheet('font-size:28px;font-family:微软雅黑;border-width:0px;border-style:solid')

        self.pushButton = QPushButton(self.centralWidget)
        self.pushButton.setGeometry(860, 670, 80, 30)
        self.pushButton.clicked.connect(self.send_msg)
        self.pushButton.setStyleSheet('font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')

        self.pushButton_1 = QPushButton(self.centralWidget)
        self.pushButton_1.setGeometry(260, 545, 40, 35)
        self.pushButton_1.clicked.connect(self.send_img)
        self.pushButton_1.setToolTip('发送图片')
        self.pushButton_1.setToolTipDuration(1000)
        self.pushButton_1.setStyleSheet('border-image:url(img/pic.png);font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')

        self.pushButton_2 = QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(300, 545, 50, 35)
        self.pushButton_2.clicked.connect(self.send_file)
        self.pushButton_2.setToolTip('发送文件')
        self.pushButton_2.setToolTipDuration(1000)
        self.pushButton_2.setStyleSheet('border-image:url(img/file.png);font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')

        self.pushButton_3 = QPushButton(self.centralWidget)
        self.pushButton_3.setGeometry(220, 545, 40, 35)
        self.pushButton_3.clicked.connect(self.show_emoji)
        self.pushButton_3.setToolTip('发送表情包')
        self.pushButton_3.setToolTipDuration(1000)
        self.pushButton_3.setStyleSheet('border-image:url(img/emoji.png);font-size:18px;font-family:等线;color:#ecf8ff;background:#00a3ff;border-radius:5px')

        self.textEdit = QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(220, 580, 750, 85)
        self.textEdit.setFocus()
        self.textEdit.setStyleSheet('font-size:16px;font-family:微软雅黑;border-width:1px;border-style:solid;border-color:#CCCCCC')

        self.stackedwidget = QStackedWidget(self.centralWidget)
        self.stackedwidget.setGeometry(QtCore.QRect(220, 115, 750, 430))

        for i in range(self.list.count()):
            text = self.list.item(i).text()
            log = QTextEdit(self.centralWidget)
            log.setGeometry(230, 35, 730, 500)
            log.setText(text)
            log.setVerticalScrollBarPolicy(2)
            log.setReadOnly(True) # 设置为只读模式，以防用户修改
            self.stackedwidget.addWidget(log)
            log.setStyleSheet('font-size:16px;font-family:微软雅黑;border-width:1px;border-style:solid;border-color:#CCCCCC')

        self.table = QTableWidget(self.centralWidget)
        self.table.setGeometry(220, 380, 150, 150)
        self.table.setColumnCount(4)
        self.table.setRowCount(4)
        self.table.setColumnWidth(0, 36)
        self.table.setColumnWidth(1, 36)
        self.table.setColumnWidth(2, 36)
        self.table.setColumnWidth(3, 36)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        for i in range(16):
            row = i // self.table.rowCount()
            column = i % self.table.columnCount()
            icon = QLabel(self.centralWidget)
            icon.setMargin(4)
            movie = QMovie(self.centralWidget)
            movie.setScaledSize(QSize(28, 28))
            movie.setFileName('emoji/{}.gif'.format(i))
            movie.start()
            icon.setMovie(movie)
            self.table.setCellWidget(row, column, icon)
        self.table.setHidden(True)
        self.table.cellClicked.connect(self.send_emoji)

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
        # self.pushButton_1.setText(_translate("MainWindow", "图片"))
        # self.pushButton_2.setText(_translate("MainWindow", "文件"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "请输入消息"))
    
    def show_emoji(self):
        self.table.setHidden(False)

    def send_emoji(self, row, column):
        emoji_name = str(4*row+column) + '.gif'
        emoji_path = 'emoji/' + emoji_name
        index = self.stackedwidget.currentIndex()
        dst_nickname = self.list.item(index).text()
        if not emoji_path:
            return 
        time = time_func()
        log = self.stackedwidget.currentWidget()
        # 将鼠标指针移至末尾
        cursor = log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        log.setTextCursor(cursor)
        log.insertPlainText('\n' + self.user_info[2] + '  ' + time + '\n')
        html = "<img src={}>".format(emoji_path)
        log.insertHtml(html)
        cursor.movePosition(QtGui.QTextCursor.End)
        self.table.setHidden(True)
        # 发送给自己，直接打印
        if dst_nickname == self.user_info[2]:
            return

        with open (emoji_path, 'rb') as f:
            content = f.read() # type: bytes
            emoji_str = base64.encodebytes(content).decode('utf-8') # type: str
        req = {
            'op': 'send_img',
            'args': {
                "src_info": self.user_info,
                "dst_nickname": dst_nickname,
                'img_name': emoji_name,
                'img_str': emoji_str,
                'time': time
            }
        }
        send_func(self.client_socket, req)

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
            return 
        self.textEdit.setPlainText('') # 发送完消息清空消息框
        log = self.stackedwidget.currentWidget() # 获取当前控件
        # 将鼠标指针移至末尾
        cursor = log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        log.setTextCursor(cursor)
        log.insertPlainText('\n' + self.user_info[2] + '  ' + time + '\n')
        log.insertPlainText(content)
        cursor.movePosition(QtGui.QTextCursor.End)
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
        if width == 0 or height == 0:
            return 0
        scale = max(750/width, 430/height)
        if scale < 1:
            width, height = width * 0.4 * scale, height * 0.4 * scale
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
        try:
            img = self.scaled_img(img_path)
            log = self.stackedwidget.currentWidget()
            # 将鼠标指针移至末尾
            cursor = log.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            log.setTextCursor(cursor)
            log.insertPlainText('\n' + self.user_info[2] + '  ' + time + '\n')
            cursor.insertImage(img)
            cursor.movePosition(QtGui.QTextCursor.End)
        except Exception as e:
            QMessageBox.information(self, "error", "请选择正确格式的图片")
            return 
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

    def send_file(self):
        '''
        发送文件并显示到聊天界面
        '''
        index = self.stackedwidget.currentIndex()
        dst_nickname = self.list.item(index).text()
        file_path = QFileDialog().getOpenFileName(self, 'Open File', './') # type: tuple
        file_path = file_path[0] # type: str
        # 未选定图片，路径为空
        if not file_path:
            return 
        file_name = file_path.split('/')[-1] # type: str
        time = time_func()
        # img = self.scaled_img(img_path)
        # img = QTextImageFormat()
        # img.setName(img_path)
        log = self.stackedwidget.currentWidget()
        # 将鼠标指针移至末尾
        cursor = log.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        log.setTextCursor(cursor)
        log.insertPlainText('\n' + self.user_info[2] + '  ' + time + '\n')
        log.insertPlainText(file_name)
        cursor.movePosition(QtGui.QTextCursor.End)
        # cursor.insertImage(img)
        # 发送给自己，直接打印
        if dst_nickname == self.user_info[2]:
            return
        with open (file_path, 'rb') as f:
            content = f.read() # type: bytes
            file_str = base64.encodebytes(content).decode('utf-8') # type: str
        req = {
            'op': 'send_file',
            'args': {
                "src_info": self.user_info,
                "dst_nickname": dst_nickname,
                'file_name': file_name,
                'file_str': file_str,
                'time': time
            }
        }
        send_func(self.client_socket, req)

    def refresh_user(self, online, offline):
        '''
        刷新用户列表，在线用户为绿色，离线用户为灰色
        
        Arguments:
            online {set} -- 在线用户
            offline {set} -- 离线用户
        '''
        for user in online:
            index = self.user_list.index(user)
            self.list.item(index).setBackground(QColor('#C1FFC1'))
        for user in offline:
            index = self.user_list.index(user)
            self.list.item(index).setBackground(QColor('#C7C7C7'))

    def recv_msg(self):
        '''
        接收消息并显示
        '''
        try:
            while True:            
                recv_content = recv_func(self.client_socket)
                if recv_content['op'] == 'send_msg':
                    src_nickname = recv_content['args']['src_nickname']
                    dst_nickname = recv_content['args']['dst_nickname']
                    time = recv_content['args']['time']
                    content = recv_content['args']['content']

                    index = self.user_list.index(src_nickname)
                    if src_nickname == self.user_info[2]:
                        continue
                    if dst_nickname == 'Group':
                        index = 0
                    self.switchlog(index)
                    log = self.stackedwidget.currentWidget()
                    # 将鼠标指针移至末尾
                    cursor = log.textCursor()
                    cursor.movePosition(QtGui.QTextCursor.End)
                    log.setTextCursor(cursor)
                    log.insertPlainText('\n' + src_nickname + '  ' + time + '\n')
                    log.insertPlainText(content)
                    cursor.movePosition(QtGui.QTextCursor.End)

                elif recv_content['op'] == 'send_img':
                    src_nickname = recv_content['args']['src_nickname']
                    dst_nickname = recv_content['args']['dst_nickname']
                    time = recv_content['args']['time']
                    img_name = recv_content['args']['img_name']
                    img_str = recv_content['args']['img_str']

                    img_data = base64.b64decode(img_str)
                    dir_path = os.path.join(os.path.dirname(__file__), 'image_cache')
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                    img_path = os.path.join(dir_path, img_name)
                    with open (img_path, 'wb+') as f:
                        f.write(img_data)

                    img = self.scaled_img(img_path)
                    index = self.user_list.index(src_nickname)
                    if src_nickname == self.user_info[2]:
                        continue
                    if dst_nickname == 'Group':
                        index = 0
                    self.switchlog(index)
                    # 将鼠标指针移至末尾
                    log = self.stackedwidget.currentWidget()
                    cursor = log.textCursor()
                    cursor.movePosition(QtGui.QTextCursor.End)
                    log.setTextCursor(cursor)
                    log.insertPlainText('\n' + src_nickname + '  ' + time + '\n')
                    cursor.insertImage(img)
                    cursor.movePosition(QtGui.QTextCursor.End)
                
                elif recv_content['op'] == 'send_file':
                    src_nickname = recv_content['args']['src_nickname']
                    dst_nickname = recv_content['args']['dst_nickname']
                    time = recv_content['args']['time']
                    file_name = recv_content['args']['file_name']
                    file_str = recv_content['args']['file_str']

                    file_data = base64.b64decode(file_str)
                    dir_path = os.path.join(os.path.dirname(__file__), 'file_cache')
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                    file_path = os.path.join(dir_path, file_name)
                    with open (file_path, 'wb+') as f:
                        f.write(file_data)

                    index = self.user_list.index(src_nickname)
                    if src_nickname == self.user_info[2]:
                        continue
                    if dst_nickname == 'Group':
                        index = 0
                    self.switchlog(index)
                    # 将鼠标指针移至末尾
                    log = self.stackedwidget.currentWidget()
                    cursor = log.textCursor()
                    cursor.movePosition(QtGui.QTextCursor.End)
                    log.setTextCursor(cursor)
                    log.insertPlainText('\n' + src_nickname + '  ' + time + '\n')
                    log.insertPlainText('收到文件：{}，并保存在{}'.format(file_name, dir_path))
                    cursor.movePosition(QtGui.QTextCursor.End)
                    # cursor.insertImage(img)

                elif recv_content['op'] == 'new_user':
                    users_online = recv_content['args']['users_online']
                    time = recv_content['args']['time']
                    users_online.append('Group')
                    users = set(self.user_list)
                    online = set(users_online)
                    offline = users - online
                    self.refresh_user(online, offline)
                else:
                    pass
        except Exception as e:
            self.client_socket.close()
            QMessageBox.information(self, "error", "与服务器失去连接")
            self.close()

    def switchlog(self, i):
        self.stackedwidget.setCurrentIndex(i)
    
    def run(self):
        recv_thread = threading.Thread(target=self.recv_msg)
        recv_thread.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = chatroom_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
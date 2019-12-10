import socket
import threading
import json
import sys
import hashlib
from PyQt5.QtWidgets import (QWidget, QGridLayout, 
    QPushButton, QLabel, QLineEdit, QApplication)


class Client(QWidget):
    """
    客户端
    """

    def __init__(self):
        """
        构造
        """
        super().__init__()
        self.init_UI()
        # self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.__id = None
        # self.__nickname = None
        # self.__username = None
        # self.__password = None

    def init_UI(self):

        grid = QGridLayout()
        self.setLayout(grid)
        
        self.label_username = QLabel('用户名:')
        self.label_password = QLabel('密码:')
        self.edit_username = QLineEdit()
        self.edit_password = QLineEdit()
        self.button_login = QPushButton('登陆')
        self.button_register = QPushButton('注册')

        self.button_login.clicked.connect(self.jump_UI)
        # self.button_login.clicked.connect(self.login)
        # self.button_register.clicked.connect(self.register)

        # button_login.resize(button_login.sizeHint())
        # button_register.resize(button_register.sizeHint())

        grid.addWidget(self.label_username, 0, 0)
        grid.addWidget(self.edit_username, 0, 1)
        grid.addWidget(self.label_password, 1, 0)
        grid.addWidget(self.edit_password, 1, 1)
        grid.addWidget(self.button_login, 2, 0)
        grid.addWidget(self.button_register, 2, 1)
        
        self.move(300, 150)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Chat')
        self.show()

    
    def jump_UI(self):
        
        pass
    
    def __receive_message_thread(self):
        """
        接受消息线程
        """
        while True:
            # noinspection PyBroadException
            try:
                buffer = self.__socket.recv(1024).decode()
                obj = json.loads(buffer)
                print('[' + str(obj['sender_nickname']) + '(' + str(obj['sender_id']) + ')' + ']', obj['message'])
            except Exception:
                print('[Client] 无法从服务器获取数据')

    def __send_message_thread(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        self.__socket.send(json.dumps({
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())

    def start(self):
        """
        启动客户端
        """
        self.__socket.connect(('127.0.0.1', 8888))

    def login(self, args):
        """
        登录聊天室
        :param args: 参数
        """
        self.__username = self.edit_username.text()
        self.__password = self.edit_password.text()

        req = {
            "op": 1,
            "args": {
                "uname": self.__username,
                "password": self.__password
            }
        }

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP_Port = tuple(eval(json.load(open("IP_address.json", encoding='utf-8'))['server_IP']))
        client_socket.connect(IP_Port)

        m = hashlib.md5()
        req_md5 = m.update(req['args']['password'])
        req['args']['password'] = m.hexdigest().upper()
        req = json.dumps(req).encode()
        len_req = str(len(req)).ljust(15).encode()
        # 发送文件大小
        client_socket.send(len_req)
        client_socket.send(req)
        # nickname = args.split(' ')[0]

        # 将昵称发送给服务器，获取用户id
        self.__socket.send(json.dumps({
            'type': 'login',
            'nickname': nickname
        }).encode())
        # 尝试接受数据
        # noinspection PyBroadException
        try:
            buffer = self.__socket.recv(1024).decode()
            obj = json.loads(buffer)
            if obj['id']:
                self.__nickname = nickname
                self.__id = obj['id']
                print('[Client] 成功登录到聊天室')

                # 开启子线程用于接受数据
                thread = threading.Thread(target=self.__receive_message_thread)
                thread.setDaemon(True)
                thread.start()
            else:
                print('[Client] 无法登录到聊天室')
        except Exception:
            print('[Client] 无法从服务器获取数据')

    def register():
        pass

    def send(self, args):
        """
        发送消息
        :param args: 参数
        """
        message = args
        # 显示自己发送的消息
        print('[' + str(self.__nickname) + '(' + str(self.__id) + ')' + ']', message)
        # 开启子线程用于发送数据
        thread = threading.Thread(target=self.__send_message_thread, args=(message, ))
        thread.setDaemon(True)
        thread.start()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
    # def do_help(self, arg):
    #     """
    #     帮助
    #     :param arg: 参数
    #     """
    #     command = arg.split(' ')[0]
    #     if command == '':
    #         print('[Help] login nickname - 登录到聊天室，nickname是你选择的昵称')
    #         print('[Help] send message - 发送消息，message是你输入的消息')
    #     elif command == 'login':
    #         print('[Help] login nickname - 登录到聊天室，nickname是你选择的昵称')
    #     elif command == 'send':
    #         print('[Help] send message - 发送消息，message是你输入的消息')
    #     else:
    #         print('[Help] 没有查询到你想要了解的指令')

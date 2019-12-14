import os
import json
import time
import queue
import socket
import sqlite3
import threading
from utils import *

class Server():
    
    def __init__(self):
        # self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.__socket = None
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(('', 8888))
        self.__socket.listen(8)
        self.__client_sockets = dict()
        self.__db_file = os.path.join(os.path.dirname(__file__), 'test.db')
        # self.con = threading.Condition()
        self.__msg_queue = queue.Queue()
        self.__lock = threading.Lock()
        self.init_db()
        # self.__connections = list()
        # self.__nicknames = list()
             
    def init_db(self):
        '''
        初始化数据库\n
        数据库文件为test.db，若不存在会在当前目录创建
        '''
        if os.path.isfile(self.__db_file):
            os.remove(self.__db_file)    
        conn = sqlite3.connect(self.__db_file)
        cur = conn.cursor()
        cur.execute(r'create table user(account varchar(20) primary key, passwd varchar(20), nickname varchar(20), status varchar(10))')
        # 插入记录:
        cur.execute(r"insert into user values ('admin', '123456', 'Jack', 'offline')")
        cur.execute(r"insert into user values ('admin2', '123456', 'Lily', 'offline')")
        cur.close()
        conn.commit()
        conn.close()        
        
        print('Database initialization completed!')

    def add_user(self, account, passwd, nickname):
        '''
        向数据库中添加新用户
        
        Arguments:
            account {str} -- 账号
            passwd {str} -- 密码
            nickname {str} -- 昵称
        
        Returns:
            bool -- 添加成功为True，用户已存在为False
        '''
        if self.user_in_table(account):
            return False
        else:
            conn = sqlite3.connect(self.__db_file)
            cur = conn.cursor()
            # 插入记录:
            cur.execute(r"insert into user values (%s, %s, %s, 'offline')' %(account, passwd, nickname)")
            cur.close()
            conn.commit()
            conn.close()
            return True

    def user_in_table(self, account):
        '''
        检查指定的用户是否在数据库中
        
        Arguments:
            account {str} -- 用户账号
        
        Returns:
            bool -- 用户在表中则返回True，不在则False
        '''
        conn = sqlite3.connect(self.__db_file)
        cur = conn.cursor()
        cur.execute('select * from user where account=?', (account, ))
        rows = cur.fetchone()
        cur.close()
        conn.commit()
        if rows:
            return True
        else:
            return False

    def get_user_info(self, account=None):
        '''
        根据账号返回用户信息，account为空时返回所有用户
        
        Arguments:
            account {str} -- 账号
        
        Returns:
            tuple/list  -- 用户信息
        '''
        conn = sqlite3.connect(self.__db_file)
        cur = conn.cursor()
        if not account:
            cur.execute('select * from user')
            rows = cur.fetchall()
        else:
            cur.execute('select * from user where account=?', (account, ))
            rows = cur.fetchone()
        cur.close()
        conn.commit()
        if rows:
            return rows
        else:
            return None

    def get_user_account(self, nickname):
        '''
        根据昵称返回用户信息
        
        Arguments:
            nickname {str} -- 用户昵称
        
        Returns:
            str -- 用户账号
        '''
        conn = sqlite3.connect(self.__db_file)
        cur = conn.cursor()
        cur.execute('select * from user where nickname=?', (nickname, ))
        rows = cur.fetchone()
        cur.close()
        conn.commit()
        if rows:
            return rows
        else:
            return None

    def check_passwd(self, account, passwd):
        '''
        检查用户账号与密码是否匹配
        
        Arguments:
            account {str} -- 用户账号
            passwd {str} -- 用户密码
        
        Returns:
            bool -- 匹配为True，反之为False
        '''
        if not self.user_in_table(account):
            return False
        conn = sqlite3.connect(self.__db_file)
        cur = conn.cursor()
        cur.execute('select * from user where account=?', (account, ))
        rows = cur.fetchone()
        cur.close()
        conn.commit()
        if rows[1] == passwd:
            return True
        else:
            return False
    
    def msg_to_queue(self, recv_content, client_socket):
        '''
        将服务器接收的消息存到队列中
        
        Arguments:
            recv_content {str} -- 接收的内容
            client_socket {socket} -- 客户端套接字
        '''
        self.__lock.acquire()
        try:
            self.__msg_queue.put((recv_content, client_socket))
        finally:
            self.__lock.release()

    def users_online(self):
        '''
        返回所有在线的用户
        
        Returns:
            list -- list of tuples: [(account, passwd, nickname, status),]
        '''
        return list(self.__client_sockets.keys())

    def send_msg(self):
        '''
        从队列中获取消息并发送
        '''
        while True:
            if not self.__msg_queue.empty():
                recv_content, client_socket = self.__msg_queue.get()
                # 客户端发起登陆请求
                if recv_content['op'] == 'login':
                    account = recv_content['args']['account']
                    passwd = recv_content['args']['passwd']
                    time = recv_content['args']['time']
                    user_info = self.get_user_info(account)
                    if user_info and passwd == user_info[1] and user_info not in self.__client_sockets:
                        print('{} New Connection from: {}'.format(time, client_socket.getpeername()))
                        user_list = []
                        for user in self.get_user_info():
                            user_list.append(user[2])
                        resp = {
                            'op': 'login',
                            'args': {
                                'check_flag':  True,
                                'user_info': user_info,
                                'user_list': user_list,
                                'time': time_func()
                            }
                        }
                        # 动态维护在线用户
                        self.__client_sockets[user_info] = client_socket
                        send_func(client_socket, resp)
                        # 为新用户开一个线程监听消息  
                        recv_thread = threading.Thread(target=self.recv_msg_thread,args=(client_socket,))
                        recv_thread.start()
                        users_online = []
                        for user in self.users_online():
                            users_online.append(user[2])
                        # 新用户登陆成功 则通知所有在线用户
                        resp = {
                            'op': 'refresh',
                            'args': {
                                'users_online': users_online,
                                'time': time_func()
                            }
                        }
                        self.msg_to_queue(resp, client_socket)
                    else:
                        print('{} Failed Connection from: {}'.format(time, client_socket.getpeername()))
                        resp = {
                                'op': 'login',
                                'args': {
                                    'check_flag': False,
                                    'error_info': '',
                                    'time': time_func()
                                }
                            }
                        if not user_info:
                            resp['args']['error_info'] = 'user not exists'
                        elif not passwd == user_info[1]:
                            resp['args']['error_info'] = "account and password don't match"
                        elif user_info in self.__client_sockets:
                            resp['args']['error_info'] = "user already logins"
                        else:
                            resp['args']['error_info'] = "unexpected error happens"
                        send_func(client_socket, resp)

                # 客户端发起注册请求
                elif recv_content['op'] == 'register':
                    account = recv_content['args']['account']
                    passwd = recv_content['args']['passwd']
                    nickname = recv_content['args']['nickname']
                    if self.add_user(account, passwd, nickname):
                        print('{} Add new user successfully! account: {} nickname: {}'.format(time, account, nickname))
                        resp = {
                            'op': 'register',
                            'args': {
                                'check_flag':  True,
                                'time': time_func()
                            }
                        }
                        send_func(client_socket, resp)
                    else:
                        print('{} Fail to add new user：user already exists'.format(time))
                        resp = {
                            'op': 'register',
                            'args': {
                                'check_flag':  False,
                                'error_info': 'user already exists',
                                'time': time_func()
                            }
                        }
                        send_func(client_socket, resp)
                
                # 客户端发起私聊请求
                elif recv_content['op'] == 'send_msg':
                    src_info = recv_content['args']['src_info']
                    dst_nickname = recv_content['args']['dst_nickname']
                    content = recv_content['args']['content']
                    # src = self.get_user_account(src_nickname)
                    dst_info = self.get_user_account(dst_nickname)
                    resp = {
                            'op': 'send_msg',
                            'args': {
                                'src_nickname': src_info[2],
                                'dst_nickname': dst_info[2],
                                'content': content,
                                'time': time_func()
                            }
                        }
                    send_func(self.__client_sockets[dst_info], resp)
                    print('{} sender: {}, receiver: {}, content: {}'.format(time, src_info[2], dst_info[2], content))
                
                # 客户端发起私聊请求
                elif recv_content['op'] == 'send_img':
                    src_info = recv_content['args']['src_info']
                    dst_nickname = recv_content['args']['dst_nickname']
                    img_name = recv_content['args']['img_name']
                    img_str = recv_content['args']['img_str']
                    # src = self.get_user_account(src_nickname)
                    dst_info = self.get_user_account(dst_nickname)
                    resp = {
                            'op': 'send_img',
                            'args': {
                                'src_nickname': src_info[2],
                                'dst_nickname': dst_info[2],
                                'img_name': img_name,
                                'img_str': img_str,
                                'time': time_func()
                            }
                        }
                    send_func(self.__client_sockets[dst_info], resp)
                    print('{} sender: {}, receiver: {}, img: {}'.format(time, src_info[2], dst_info[2], content))

                # 新用户加入，刷新在线用户
                elif recv_content['op'] == 'refresh':
                    for client_socket in list(self.__client_sockets.values()):
                        resp = {
                            'op': 'new_user',
                            'args': {
                                'users_online': recv_content['args']['users_online'],
                                'time': time_func()
                            }
                        }
                        send_func(client_socket, resp)
    
    def login_thread(self):
        '''
        用户登陆线程，接收新的客户端连接
        '''

        while True:
            print('Waiting for connection....')
            client_socket, client_addr = self.__socket.accept()
            # print 'New connection from : %s' % str(addr)
            recv_content = recv_func(client_socket)
            self.msg_to_queue(recv_content, client_socket)

    def recv_msg_thread(self, client_socket):
        '''
        服务器监听消息的线程
        
        Arguments:
            client_socket {socket} -- 客户端套接字
        '''
        try:
            while True:
                recv_content = recv_func(client_socket)
                self.msg_to_queue(recv_content, client_socket)
            client_socket.close()
        except:
            print('Connnetion with {} lost!'.format(client_socket.getpeername()))
            self.__client_sockets.pop(list(self.__client_sockets.keys())[list(self.__client_sockets.values()).index(client_socket)])
            client_socket.close()
            pass # To be modified
    
    def run(self):
        '''
        启动线程
        '''
        login_thread = threading.Thread(target=self.login_thread)
        login_thread.start()
        send_thread = threading.Thread(target=self.send_msg)
        send_thread.start()

if __name__ == '__main__':
    Server().run()
    
    
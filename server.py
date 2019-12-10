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
        self.__socket = None
        self.__client_sockets = dict()
        self.__db_file = os.path.join(os.path.dirname(__file__), 'test.db')
        # self.con = threading.Condition()
        # self.msg_queue = queue.Queue()
        self.init_db()
        # self.__connections = list()
        # self.__nicknames = list()
             
    def init_db(self):
        '''
        初始化数据库
        '''
        # 连接到SQLite数据库
        # 数据库文件是test.db
        # 如果文件不存在，会自动在当前目录创建:
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
        
        print('数据库初始化完毕！')

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
            print('用户添加失败：用户已存在')
            return False
        else:
            conn = sqlite3.connect(self.__db_file)
            cur = conn.cursor()
            # 插入记录:
            cur.execute(r"insert into user values (%s, %s, %s, 'offline')" %(account, passwd, nickname))
            cur.close()
            conn.commit()
            conn.close()
            print('用户添加成功')
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

    def get_user_account(self, nickname):
        '''
        根据昵称返回用户账号
        
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
            return rows[0]
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
    
    def recv_msg_thread(self, client_socket):
        '''
        服务器监听消息的线程
        
        Arguments:
            client_socket {socket} -- 用户套接字
        '''
        while True:
            try:
                # self.con.acquire()
                recv_content = recv_func(client_socket)
                # print "id : {}".format(str(id))
                # if account =="":
                #     client_socket.close()
                #     self.con.release()
                #     return
                # msg = client_socket.recv(1024)
                # # print "received id {} and msg {}...\n".format(str(id),str(msg))
                # self.msg_queue.put((account,msg))
                # self.con.notifyAll()
                # self.con.release()
                if recv_content['op'] == 3:
                    src_nickname = recv_content['args']['src_nickname']
                    dst_nickname = recv_content['args']['dst_nickname']
                    content = recv_content['args']['content']


                    # src = self.get_user_account(src_nickname)
                    dst = self.get_user_account(dst_nickname)
                    resp = {
                            "op": 3,
                            "args": {
                                "src_nickname": src_nickname,
                                "dst_nickname": dst_nickname,
                                "content": content
                            }
                        }
                    send_func(self.__client_sockets[dst], resp)
                    print("sender: %s, receiver: %s, content: %s" %(src_nickname, dst_nickname, content))
            except Exception as e:
                pass

    # def send_thread(self):
    #     while True:
    #         if not self.__client_sockets:
    #             for account, client_socket in self.__client_sockets.items():
    #                 req = {
    #                     'op': 5,
    #                     'args': {
    #                         'check_alive': True
    #                     }
    #                 }
    #                 send_func(client_socket, req)
    #                 try:
    #                     if recv_func(client_socket)['']
    #                 except Exce as e:
    #                     pass
    #     while True:
    #         self.con.acquire()
    #         while self.msg_queue.empty():
    #             # print"queue is empty...\n"
    #             self.con.wait()
    #         while self.msg_queue.qsize():
    #             # print "get from queue...\n"
    #             msg = self.msg_queue.get()
    #             if self.__client_sockets.has_key(msg[0]):
    #                 # print"id is active...\n"
    #                 self.__client_sockets[msg[0]].send(msg[1])
    #                 # print "send successful...\n"
    #             else:
    #                 self.msg_queue.put(msg)
    #         self.con.release()
    #         time.sleep(1)

    def user_login_thread(self):
        '''
        用户登陆线程
        '''
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(("", 8888))
        self.__socket.listen(8)
        while True:
            print("Waiting for connection....")
            client_socket, client_addr = self.__socket.accept()
            # print "New connection from : %s" % str(addr)
            recv_content = recv_func(client_socket)

            # 客户端发起登陆请求
            if recv_content['op'] == 1:
                account = recv_content['args']['account']
                passwd = recv_content['args']['passwd']
                if self.check_passwd(account, passwd):
                    resp = {
                        "op": 1,
                        "args": {
                            "check_flag":  True
                        }
                    }
                    # 动态维护
                    print("New Connection from: %s" %str(client_addr))
                    if self.__client_sockets.get(account):
                        self.__client_sockets[account] = client_socket
                    else:
                        self.__client_sockets[account] = client_socket
                    send_func(client_socket, resp)
                    # 登陆成功 为用户新开一个线程
                    recv_thread = threading.Thread(target=self.recv_msg_thread,args=(client_socket,))
                    recv_thread.start()
                else:
                    resp = {
                            "op": 1,
                            "args": {
                                "check_flag": False
                            }
                        }
                    print("Failed Connection from: %s" %str(client_addr))
                    send_func(client_socket, resp)

            # 客户端发起注册请求
            elif recv_content['op'] == 2:
                account = recv_content['args']['account']
                passwd = recv_content['args']['passwd']
                nickname = recv_content['args']['nickname']
                if self.add_user(account, passwd, nickname):
                    print("Add new user success! account: %s nickname: %s" %(account, nickname))
                    resp = {
                        "op": 2,
                        "args": {
                            "check_flag":  True
                        }
                    }
                    send_func(client_socket, resp)
                else:
                    print("Add new user failed!")
                    resp = {
                        "op": 2,
                        "args": {
                            "check_flag":  False
                        }
                    }
                    send_func(client_socket, resp)
            # 其他请求
            
            else:
                # send_thread = threading.Thread(target=self.send_msg_thread)
                # send_thread.start()
                pass

    def run(self):
        '''
        启动线程
        '''
        login_thread = threading.Thread(target=self.user_login_thread)
        login_thread.start()
        # send_thread = threading.Thread(target=self.send_thread)
        # send_thread.start()
        # thread2 = threading.Thread(target=self.send_msg_thread)
        # thread2.start()

if __name__ == "__main__":
    Server().run()
    
    
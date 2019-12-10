import socket
import sqlite3
import os
import json
import threading

class Server():
    
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_sockets = []
        self.db_file = os.path.join(os.path.dirname(__file__), 'test.db')
        # self.__connections = list()
        # self.__nicknames = list()

    def __user_thread(self, client_socket, client_addr):
        """
        用户线程
        """
        # 数据大小
        data_size = int(client_socket.recv(15).decode().rstrip())
        # 已接受的数据大小
        recv_size = 0
        # 接受的数据内容
        recv_content = b''
        
        while recv_size < data_size:
            recv_data = client_socket.recv(data_size - recv_size)
            if not recv_data:
                break
            recv_size += len(recv_data)
            recv_content += recv_data
        
        recv_content = json.loads(recv_content.decode())
        print("receive data done")

        if recv_content['op'] == 0:
            pass
        elif recv_content['op'] == 1:
            pass
        else:
            pass
                            
    def init_db(self):
        """
        初始化数据库
        """
        # 连接到SQLite数据库
        # 数据库文件是test.db
        # 如果文件不存在，会自动在当前目录创建:
        # db_file = os.path.join(os.path.dirname(__file__), 'test.db')
        if os.path.isfile(self.db_file):
            os.remove(self.db_file)    
        conn = sqlite3.connect('test.db')
        try:
            with conn.cursor() as cur:
                # 执行SQL语句，创建user表
                cur.execute('create table user(account varchar(20) primary key, nickname varchar(20), password varchar(20))')
                # 插入记录:
                cur.execute(r"insert into user values ('123', 'Adam', '123456')")
                cur.execute(r"insert into user values ('456', 'Bart', '123456')")
                cur.execute(r"insert into user values ('789', 'Lisa', '123456')") 
        finally:
            conn.commit()
            conn.close()
        cursor = conn.cursor()
        
        print('[Server] initializing database...')

    def check_user(self, account, password):
        '''
        检测用户名和密码是否匹配\n
        rtype: bool
        '''
        conn = sqlite3.connect('test.db')

        try:
            with conn.cursor() as cur:
                cur.execute('select account from user where account=%s and password=%s', (account, password))
                rows = cur.fetchone()
        finally:
            conn.close()

        return False if rows else True


    def start(self):
        # self.__socket.bind(socket.gethostname(), 8888)
        self.init_db()
        IP_Port = tuple(eval(json.load(open("IP_address.json", encoding='utf-8'))['server_IP']))
        self.__socket.listen(5)
        print('[Server]: server is Running...')

        # self.__connections.clear()
        # self.__nicknames.clear()
        # self.__connections.append(None)
        # self.__nicknames.append('system')

        while True:
            client_socket, addr = self.__socket.accept()
            self.__client_sockets.append(client_socket, addr)
            print('[Server]: new connection from', connection.getsockname())
            # threading.Thread(target=self.__user_thread, args=)
            pass
            # try:
            #     buffer = connection.recv(1024).decode('utf-8')
            #     obj = json.loads(buffer)
            #     if not obj['username']:
            #         pass
            #     else:
            #         self.__connections.append(connection)
            #         self.__nicknames.append(obj['username'])
            #         connection.send(json.dumps({
            #             'id': len(self.__connections) - 1
            #             }).encode())
                    
            #         t = threading.Thread(target=self.__user_thread, args=(len(self.__connections) - 1))
            #         t.setDaemon(True)
            #         t.start()
            # except Exception:
            #     print('[Server]: cannot receive data correctly')


if __name__ == "__main__":
    pass
    
    
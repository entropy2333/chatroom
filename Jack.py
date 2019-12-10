import time
import json
import socket

def recv_func(client_socket):
        '''
        接收客户端的发送内容
        
        Arguments:
            client_socket {socket} -- 客户端套接字
        
        Returns:
            str -- 客户端发送的内容
        '''
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
        return recv_content

def send_func(client_socket, resp):
    '''
    向客户端发送数据长度和数据
    
    Arguments:
        client_socket {socket} -- 客户端套接字
        resp {dict} -- [description]
    '''
    resp = json.dumps(resp).encode()
    len_resp = str(len(resp)).ljust(15).encode()
    client_socket.send(len_resp)
    client_socket.send(resp)

if __name__ == "__main__":
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8888))
    req = {
        "op": 1,
        "args": {
            "account": 'admin',
            "passwd": '123456'
        }
    }
    send_func(s, req)
    recv_content = recv_func(s)
    if recv_content['op'] == 1:
        if recv_content['args']['check_flag'] == True:
            print('login success')
    else:
        print('login error')

    time.sleep(5)
    req = {
        "op": 3,
        "args": {
            "src_nickname": 'Jack',
            "dst_nickname": 'Jack',
            "content": "this is a test"
        }
    }
    send_func(s, req)
    recv_content = recv_func(s)
    print(recv_content)
    # s.close()


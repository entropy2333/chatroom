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
            recv_data = client_socket.recv(1024)
            if not recv_data:
                break
            recv_size += len(recv_data)
            recv_content += recv_data
        
        recv_content = json.loads(recv_content.decode())
        return recv_content

def send_func(client_socket, req):
    '''
    向客户端发送数据长度和数据
    
    Arguments:
        client_socket {socket} -- 客户端套接字
        req {dict} -- [description]

    Returns:
        bool
    '''
    req = json.dumps(req).encode()
    len_req = str(len(req)).ljust(15).encode()
    client_socket.send(len_req)
    client_socket.send(req)
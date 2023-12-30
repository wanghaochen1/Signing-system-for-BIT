import socket
import datetime


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 定义服务器的主机和端口
host = '192.168.21.97'
port = 12345

# 绑定主机和端口
server_socket.bind((host, port))

try:
# 监听连接
    server_socket.listen(10)

    print('等待客户端连接...')

    # 接受客户端连接
    client_socket, addr = server_socket.accept()
    print('客户端已连接:', addr)

    # 接收客户端发送的数据
    data = client_socket.recv(1024)
    print('接收到的数据:', data.decode())


    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 向客户端发送当前时间
    client_socket.send(current_time.encode())
except:
    print('连接异常')
finally:
    # 关闭连接
    client_socket.close()
    server_socket.close()

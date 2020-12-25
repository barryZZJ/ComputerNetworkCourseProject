#TODO
# loginHandler 处理登录行为
# pDataHandler 处理收到pData时的行为，如加入到形状列表、把形状转发给其他client。（每个功能写一个函数比较好）
#TODO 考虑需不需要把收到的形状存在列表里；重做时server传什么内容（重做信号还是需要重做的形状信息）
#TODO 可以给每个object一个标号，删除的时候通过标号判断
import sys, os

module_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(module_path)        # 导入的绝对路径
import socket
from threading import Thread, Lock
from WhiteBoard.ClientEnd.GUIs.connect import validIp, validPort
from WhiteBoard.controlData import pRequest, pResponse, Type

# TODO 用分配一个id识别不同主机，用于转发时的识别，客户端发现 昵称/id 与自己相同则不画。

# 全局变量
# 存客户端线程实例
clients = []
# 存服务器的数据，用于图像的复现
Logs = {}

class Server:
    """连接客户端的类，封装socket"""

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        if not validIp(self.host) or not validPort(str(self.port)):
            print(f"invalid server address {self.host}:{self.port}")
            return

        self.nextUserId = 0 # 为用户分配id
        self.lock = Lock()
        self.initSocket()
        self.serveForever()

    def initSocket(self):
        # 新建一个socket
        self.s = socket.socket() # type: socket.socket
        self.s.bind((self.host, self.port))
        print(f"hosting at {self.host}:{self.port}")
        self.s.listen(5) # 开启监听，设置允许等待的连接个数=5

    # 用多线程以支持多个连接
    def serveForever(self):
        while True:
            conn, addr = self.s.accept() # 阻塞，收到连接后唤醒
            # 新建一个处理该连接的线程
            Thread(target=self.handle, args=[conn, addr]).start()

    def handle(self, conn: socket.socket, addr):
        # 处理一个连接
        exitFlag = False
        with conn:
            print('connected by', addr)
            while not exitFlag:

                newCl = ClientObj(conn, self.nextUserId)
                clients.append(newCl)

                data = conn.recv(1024) # 阻塞，收到数据后唤醒
                type = pRequest.decode(data)
                print("receive from", addr, "-", type)
                if type == Type.ID:
                    conn.sendall(pResponse().makeId(self.nextUserId).encode())
                    print("respond to", addr, "-", type, ":", self.nextUserId)
                    self.mutexIncUserId()
                elif type == Type.DISCONNECT:
                    exitFlag = True

        # 连接关闭
        print("connection closed")
        self.mutexDecUserId()

    def mutexIncUserId(self):
        # 互斥修改nextUserId
        self.lock.acquire()
        self.nextUserId += 1
        self.lock.release()

    def mutexDecUserId(self):
        # 互斥修改nextUserId
        self.lock.acquire()
        self.nextUserId -= 1
        self.lock.release()

class ClientObj(Thread):
    # 为每个连接的客户端创建一个线程实例，用于并行处理所有客户端发来的消息
    def __init__(self, conn: socket.socket, id):
        super().__init__()
        self.conn = conn
        self.id = id

    def start(self):
        data = self.conn.recv(1024)  # 阻塞，收到数据后唤醒


if __name__ == '__main__':
    Server()
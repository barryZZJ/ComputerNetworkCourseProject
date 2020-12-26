#TODO
# loginHandler 处理登录行为
# pDataHandler 处理收到pData时的行为，如加入到形状列表、把形状转发给其他client。（每个功能写一个函数比较好）
#TODO 考虑需不需要把收到的形状存在列表里；重做时server传什么内容（重做信号还是需要重做的形状信息）
#TODO 可以给每个object一个标号，删除的时候通过标号判断
import sys, os
from typing import List

module_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(module_path)        # 导入的绝对路径
import socket
from threading import Thread, Lock
from WhiteBoard.ClientEnd.GUIs.connect import validIp, validPort
from WhiteBoard.controlData import PRequest, PResponse, CType

# TODO 用分配一个id识别不同主机，用于转发时的识别，客户端发现 昵称/id 与自己相同则不画。

# 全局变量
BUFSIZE = 1024
# 存客户端线程实例
users = {}
userinfos = {}
# 存服务器的数据，用于图像的复现
Logs = {}

class Server(socket.socket):
    """连接客户端的类，封装socket"""
    nextUserId = 1  # 为用户分配id
    lock = Lock()

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        if not validIp(self.host) or not validPort(str(self.port)):
            print(f"invalid server address {self.host}:{self.port}")
            return

        # 新建一个socket
        super().__init__()  # create ip socket
        self.bind((self.host, self.port))
        print(f"hosting at {self.host}:{self.port}")
        self.listen(5)  # 开启监听，设置允许等待的连接个数=5

        self.serveForever()

    # 用多线程以支持多个连接
    def serveForever(self):
        while True:
            conn, addr = self.accept() # 阻塞，每收到一个连接就唤醒
            # 新建一个处理该连接的ClientObj线程
            print('connected by', addr)
            user = User(conn, self.nextUserId, addr)
            users[user.id] = user
            userinfos[user.id] = user.ip
            user.start()

    @classmethod
    def mutexIncUserId(cls):
        # 互斥修改nextUserId
        cls.lock.acquire()
        cls.nextUserId += 1
        cls.lock.release()

    @classmethod
    def mutexDecUserId(cls):
        # 互斥修改nextUserId
        cls.lock.acquire()
        cls.nextUserId -= 1
        cls.lock.release()

class User(Thread):
    # 为每个连接的客户端创建一个线程实例，用于并行处理所有客户端发来的消息
    def __init__(self, conn: socket.socket, id, addr):
        super().__init__()
        self.conn = conn
        self.id = id
        self.alive = True
        self.ip = addr[0]

    def handleCtrlRequest(self, pReq: PRequest):
        print("receive from", self.ip, self.id, "-", pReq.type)
        if pReq.type == CType.ID:
            self.handleIDRequest()
        elif pReq.type == CType.ALL_USERINFOS:
            self.sendAllUsers()
        elif pReq.type == CType.PDATA:
            pass
        elif pReq.type == CType.DISCONNECT:
            self.handleDisconnRequest()


    def handleIDRequest(self):
        pResp = PResponse().id(self.id)
        try:
            self.conn.sendall(pResp.encode())
            print("respond to", self.ip, self.id)
            Server.mutexIncUserId()
        except Exception as e:
            print("handleIDRequest failure")
            print(e)

    def handleDisconnRequest(self):
        # 连接关闭
        self.conn.close()
        del users[self.id]
        del userinfos[self.id]
        print("connection from", self.ip, self.id, "is closed")
        Server.mutexDecUserId()
        self.alive = False

    def sendAllUsers(self):
        pResp = PResponse().allUsers(userinfos)
        try:
            self.conn.sendall(pResp.encode())
            print("send client info to", self.ip, self.id)
        except Exception as e:
            print("sendAllUsers failure")
            print(e)

    def run(self):
        while self.alive:
            try:
                cdata = self.conn.recv(BUFSIZE)  # 阻塞，收到数据后唤醒
                self.handleCtrlRequest(PRequest().decode(cdata))
            except ConnectionResetError:
                pass
            except ConnectionAbortedError:
                self.handleDisconnRequest()

if __name__ == '__main__':
    Server()
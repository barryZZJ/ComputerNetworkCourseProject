import sys, os
from typing import Dict
module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(module_path)        # 导入绝对路径
import socket
from threading import Thread, Lock
from WhiteBoard.ClientEnd.GUIs.connect import validIp, validPort
from WhiteBoard.controlData import CRequest, CResponse, CType

#TODO log forward to new user

# 全局变量
BUFSIZE = 1024
# 存客户端线程实例
users = {} # type: Dict[str, User]
userInfos = {}
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
            user = User(conn, self.nextUserId, addr)
            print('connected by', addr, '-', user.id)
            # 记入字典
            users[user.id] = user
            userInfos[user.id] = user.ip
            # 启动对应的线程，转发数据
            user.start()
            # 每当新用户连接时，发送id给该用户
            user.assignId()
            # 每当新用户连接时或有用户断开时，发送userinfos给所有用户
            for id, user in users.items():
                user.sendUserInfos()

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

    def assignId(self):
        cResp = CResponse.id(self.id)
        print("respond to", self.ip, '-', self.id)
        self.sendCResp(cResp)
        Server.mutexIncUserId()

    def forwardContent(self, bodyStr):
        # 把内容封装到response里，转发给除了自己之外的所有用户
        cResp = CResponse.pData(bodyStr)
        for id, user in users.items():
            if id != self.id:
                print("forward pdata to user ", id)
                user.sendCResp(cResp)

    def sendUserInfos(self):
        cResp = CResponse.userInfos(userInfos)
        print("send userinfo to", self.ip, '-', self.id)
        self.sendCResp(cResp)

    def sendCResp(self, cResp: CResponse):
        cRespBytes = cResp.encode()
        try:
            print("send", cRespBytes)
            self.conn.sendall(cRespBytes)
        except ConnectionError:
            print("connection error, closing")
            self.handleDisconnRequest()

    def recvCReq(self) -> CRequest:
        # 一次接收一个CReq
        # TODO 为什么会收到''?
        data = self.conn.recv(CRequest.HEADER_LEN)
        if data != b'':
            print("receive header", data)
            cReq = CRequest.decodeHeader(data)
            data = self.conn.recv(cReq.bodyLen)
            print("receive body", data)
            cReq.decodeBody(data)
            return cReq
        return CRequest(CType.NOOP)

    def handleCtrlRequest(self, cReq: CRequest):
        print("type:", cReq.ctype.name)
        if cReq.ctype == CType.PDATA:
            self.forwardContent(cReq.body)
        elif cReq.ctype == CType.DISCONNECT:
            self.handleDisconnRequest()

    def handleDisconnRequest(self):
        # 连接关闭
        self.conn.close()
        del users[self.id]
        del userInfos[self.id]
        print("connection from", self.ip, '-', self.id, "is closed")
        Server.mutexDecUserId()
        self.alive = False
        # 每当新用户连接时或有用户断开时，发送userinfos给所有用户
        for id, user in users.items():
            user.sendUserInfos()

    def run(self):
        while self.alive:
            try:
                print("receive from", self.ip, '-', self.id)
                cReq = self.recvCReq()  # 阻塞，收到数据后唤醒
                self.handleCtrlRequest(cReq)
            except ConnectionError:
                print("connection error, closing")
                self.handleDisconnRequest()

if __name__ == '__main__':
    Server()
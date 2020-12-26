import socket

from ClientEnd.GUIs import connect
from controlData import PRequest, PResponse, CType

BUFSIZE = 1024
debug = False


class ClientConn(socket.socket):
    """连接服务器的类，封装socket"""
    # Hint: 可以看一下help(socket)
    _poll_all_users_interval = 500

    def __init__(self):
        socket.socket.__init__(self) # create ip socket
        if debug:
            self.serverIp = "127.0.0.1"
            self.serverPort = 5000
            self.tryConnect()
        else:
            self.getValuesFromUser()
        print(f"connected to server at {self.serverIp}:{self.serverPort}")

        self.isAlive = True

    def getValuesFromUser(self):
        # 弹出连接窗口，获取服务器地址
        connectWind = connect.connectWindow()
        connected = False  # 是否连接上
        while not connected:
            self.serverIp = connectWind.getServerIp()
            self.serverPort = connectWind.getServerPorti()
            # 测试连接能否建立成功，不成功则重新输入
            connected = self.tryConnect()
            if not connected:
                connectWind = connectWind.connectFailedHandler()

        return self.serverIp, self.serverPort

    def getHostIp(self):
        # 获取本机IP
        return self.getsockname()[0]

    def getHostId(self) -> str:
        # 获取本机ID，用于唯一标识一个主机
        while self.isAlive:
            data = PRequest().id().encode()
            self.sendall(data)
            data = self.recvCData()
            pResp = PResponse().decode(data)
            if pResp.type == CType.ID:
                return pResp.transToId()
            # 如果回复是其他类型，就丢弃，再次发送请求
#TODO 连接断开时的处理
    def getUserInfoDict(self) -> dict:
        # 获取所有客户端ip和id。需要定期轮询
        while self.isAlive:
            data = PRequest().allUsers().encode()
            self.sendall(data)
            data = self.recvCData()
            pResp = PResponse().decode(data)
            if pResp.type == CType.ALL_USERINFOS:
                return pResp.transToUserInfoDict()
            # 如果回复是其他类型，就丢弃，再次发送请求

    def tryConnect(self) -> bool:
        """连接服务器，返回是否成功"""
        try:
            self.connect((self.serverIp, self.serverPort))
        except socket.error as e:
            print("Error:", e)
            return False
        return True

    def disconnect(self):
        self.sendall(PRequest().disconnect().encode())
        self.close()
        self.isAlive = False

    def sendCData(self, data) -> bool:
        """发送数据，返回发送是否成功"""
        # TODO socket.send错误处理
        # TODO 怎么发送bit位
        # TODO 传输字典可以用json字符串
        # TODO 把字符串编码成bytes再发送："xxx".encode()，默认UTF8编码
        pass

    def recvCData(self) -> bytes:
        cdata = self.recv(BUFSIZE)
        return cdata
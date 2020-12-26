import socket

from WhiteBoard.ClientEnd.GUIs import connect
from WhiteBoard.controlData import CRequest

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

#TODO 连接断开时的处理

    def tryConnect(self) -> bool:
        """连接服务器，返回是否成功"""
        try:
            self.connect((self.serverIp, self.serverPort))
        except socket.error as e:
            print("Error:", e)
            return False
        return True

    def disconnect(self):
        self.sendall(CRequest().disconnect().encode())
        self.close()
        self.isAlive = False

    def recvCDataBytes(self):
        return self.recv(BUFSIZE)


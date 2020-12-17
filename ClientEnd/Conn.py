import socket
from PaintData import PData
from ClientEnd.GUIs import connect

debug = False

# 给出类的框架，自行添加函数和参数。
class Conn:
    """连接服务器的类，封装socket"""
    # Hint: 可以看一下help(socket)

    def __init__(self):
        if debug:
            self.s = socket.socket() # create ip socket
            self.serverIp = "127.0.0.1"
            self.serverPort = 5000
            self.connect()
        else:
            self.s = socket.socket() # create ip socket
            self.getValuesFromUser()
            print(f"connected to server at {self.serverIp}:{self.serverPort}")


    def getValuesFromUser(self):
        # 弹出连接窗口，获取服务器地址
        connectWind = connect.connectWindow()
        connected = False  # 是否连接上
        while not connected:
            self.serverIp = connectWind.getServerIp()
            self.serverPort = connectWind.getServerPorti()
            # 测试连接能否建立成功，不成功则重新输入
            connected = self.connect()
            if not connected:
                connectWind = connectWind.connectFailedHandler()

        return self.serverIp, self.serverPort

    def getHostIp(self):
        # 获取本机IP
        return self.s.getsockname()[0]

    def connect(self) -> bool:
        """连接服务器，返回是否成功"""
        try:
            self.s.connect((self.serverIp, self.serverPort))
        except socket.error as e:
            print("Error:", e)
            return False
        return True

    def sendData(self, data) -> bool:
        """发送数据，返回发送是否成功"""
        # TODO socket.send错误处理
        # TODO 怎么发送bit位
        # TODO 传输字典可以用json字符串
        # TODO 把字符串编码成bytes再发送："xxx".encode()，默认UTF8编码
        pass

    def recvData(self) -> PData:
        """接受数据，返回收到的对象"""

        pass

if __name__ == '__main__':
    Conn()
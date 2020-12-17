import socket
from PaintData import PData
from Client.GUIs import connect

# 给出类的框架，自行添加函数和参数。
class Conn:
    """连接服务器的类，封装socket"""
    # Hint: 可以看一下help(socket)

    def __init__(self):
        # 弹出连接窗口，获取服务器地址
        connectWind = connect.connectWindow()
        connected = False # 是否连接上
        while not connected:
            self.serverIP = connectWind.getIp()
            self.serverPort = connectWind.getPort()
            #测试连接能否建立成功，不成功则重新输入
            connected = self.connect()
            if not connected:
                connectWind.connectFailedHandler()

    def connect(self) -> bool:
        """连接服务器，返回是否成功"""
        return False

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
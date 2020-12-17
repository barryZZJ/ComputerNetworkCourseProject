import socket
from PaintData import PData

# 给出类的框架，自行添加函数和参数。
class Conn:
    """连接服务器的类，封装socket"""
    # Hint: 可以看一下help(socket)
    # TODO
    def __init__(self, serverIP=None, serverPort=None):
        if serverIP:
            self.serverIP = serverIP
        if serverPort:
            self.serverPort = serverPort

    # 以下为对外接口（可自行修改）
    def setServerIP(self, serverIP):
        self.serverIP = serverIP

    def setServerPort(self, serverPort):
        self.serverPort = serverPort

    def login(self) -> bool:
        """登录服务器，返回登陆是否成功"""
        pass

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
#TODO
# loginHandler 处理登录行为
# pDataHandler 处理收到pData时的行为，如加入到形状列表、把形状转发给其他client。（每个功能写一个函数比较好）
#TODO 考虑需不需要把收到的形状存在列表里；重做时server传什么内容（重做信号还是需要重做的形状信息）
#TODO 可以给每个object一个标号，删除的时候通过标号判断

import socketserver
from ClientEnd.GUIs.connect import validIp, validPort

# TODO 用昵称（或分配一个id）识别不同主机，用于转发时的识别，客户端发现 昵称/id 与自己相同则不画。
import sys


class TCPHandler(socketserver.BaseRequestHandler):
    # 请求处理类
    def handle(self):
        pass

class Server:
    """连接客户端的类，封装socketserver"""
    # Hint: 可以看一下help(socketserver)
    # 可以用多线程或线程池，以支持多个socket
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port

        if not validIp(self.host) or not validPort(str(self.port)):
            print(f"invalid server address {self.host}:{self.port}")
            return

        try:
            with socketserver.ThreadingTCPServer((self.host, self.port), TCPHandler) as server:
                print(f"hosting at {self.host}:{self.port}")
                server.serve_forever()
        except OSError as e:
            print(f"can't create server.\n", e)

Server()
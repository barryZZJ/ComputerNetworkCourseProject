# @Author : ZZJ

from Client.Conn import Conn

class Client:
    """客户端逻辑，调用GUI模块，显示界面"""
    def __init__(self):
        self.conn = Conn()



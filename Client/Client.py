# @Author : ZZJ
from Client.Conn import Conn
from Client.WhiteBoardGUI import *

class Client:
    """客户端逻辑，调用GUI模块，显示界面"""
    def __init__(self):
        self.conn = Conn()

    def start(self):
        """启动客户端程序。按照流程图过程实现。"""
        #TODO 逻辑在GUI里写还是在这里写？
        pass



if __name__ == '__main__':
    Client()
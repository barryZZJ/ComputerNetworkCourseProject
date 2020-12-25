# @Author : ZZJ
import sys, os

from PyQt5.QtWidgets import QApplication

from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoard

module_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(module_path)        # 导入的绝对路径

from WhiteBoard.ClientEnd.Conn import Conn
from WhiteBoard.ClientEnd.GUIs.main import Main


class Client:
    """客户端逻辑，调用GUI模块，显示界面"""
    def __init__(self):
        # 弹出连接窗口，获取服务器IP和端口，连接成功后返回conn对象
        self.conn = Conn()
        # 进入主窗体
        Main(self.conn)
        self.conn.disconnect()


    def start(self):
        """启动客户端程序。按照流程图过程实现。"""
        #TODO 逻辑在GUI里写还是在这里写？
        pass




if __name__ == '__main__':
    Client()
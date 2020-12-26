# @Author : ZZJ
import sys, os
module_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(module_path)        # 导入的绝对路径
from WhiteBoard.ClientEnd.GUIs.main import Main

from WhiteBoard.ClientEnd.ClientConn import ClientConn

class Client:
    """客户端逻辑，调用GUI模块，显示界面"""
    def __init__(self):
        # 弹出连接窗口，获取服务器IP和端口，连接成功后返回conn对象
        self.conn = ClientConn()
        # 进入主窗体
        self.main = Main(self.conn)

if __name__ == '__main__':
    Client()
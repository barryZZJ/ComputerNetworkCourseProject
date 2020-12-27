# @Author : ZZJ
import sys, os
from threading import Thread
module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(module_path)        # 导入的绝对路径

from PyQt5.QtWidgets import QApplication

from WhiteBoard.ClientEnd.GUIs.connect import ConnectWindow
from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardWindow
from WhiteBoard.ClientEnd.GUIs.main import Main
from WhiteBoard.ClientEnd.ClientConn import ClientConn
from WhiteBoard.controlData import CResponse, CType


class Client(Thread, QApplication):
    """客户端逻辑，调用GUI模块，显示界面"""
    def __init__(self):
        Thread.__init__(self)
        # 启动app主线程
        QApplication.__init__(self, [])
        self.conn = ClientConn()
        try:
            self.connWind = ConnectWindow(self.conn) # 使用lambda函数防止直接获取还未定义的main
        except Exception as e:
            print(e)
            exit()

    def startConnWindow(self):
        self.connWind.show()
        self.exec()
        # conn 窗口关闭
        if not self.conn.isAlive:
            return
        # 获取id
        cdata = self.conn.recvCResp()
        self.id = cdata.body

        # 创建白板窗体
        self.board = WhiteBoardWindow(self.conn, self.id, callback=lambda: self.main.toggleWhiteBoard()) # 使用lambda函数防止直接获取还未定义的main
        # 创建主窗体
        self.main = Main(self.board, self.conn, self.id)

        # 接收数据线程启动
        self.start()

        self.startMainWindow()

    def startMainWindow(self):
        # 弹出连接窗口，获取服务器IP和端口
        self.main.show()
        self.exec()

    def run(self):
        print("running thread")
        while self.conn.isAlive:
            try:
                cResp = self.conn.recvCResp()
            except OSError as e:
                # 关闭socket连接后阻塞中的recv会触发OSError
                print("recv error")
                print("connection to server is unavailable, closing program...")
                break
            print("receive", cResp)
            if cResp.ctype == CType.USERINFOS:
                # 收到用户信息
                userinfodict = cResp.body
                l = []
                for id, ip in userinfodict.items():
                    if id == self.id:
                        l.append(f"{ip} - {id} (me)")
                    else:
                        l.append(f"{ip} - {id}")
                self.main.setUserInfos(l)

            elif cResp.ctype == CType.PDATA:
                # 收到PDATA
                pData = cResp.body
                self.board.wb.paintFromMsg(pData)

        # 执行到这里说明连接断开了，关闭窗口
        self.main.close()

if __name__ == '__main__':
    cl = Client()
    cl.startConnWindow()

    print("client window closed")

    print("waiting thread")
    cl.join()
    print("main thread done")

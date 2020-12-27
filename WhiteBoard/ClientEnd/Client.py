# @Author : ZZJ
import sys, os
from threading import Thread

from PyQt5.QtWidgets import QApplication

module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(module_path)        # 导入的绝对路径
from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardWindow
from WhiteBoard.controlData import CResponse, CType

from WhiteBoard.ClientEnd.ClientConn import ClientConn
from WhiteBoard.ClientEnd.GUIs.main import Main


class Client(Thread, QApplication):
    """客户端逻辑，调用GUI模块，显示界面"""
    def __init__(self):
        Thread.__init__(self)
        # 弹出连接窗口，获取服务器IP和端口，连接成功后返回conn对象
        self.conn = ClientConn()
        # 获取id
        cdata = self.conn.recvCDataBytes()
        id = CResponse.decode(cdata).transToId()
        # 启动app主线程
        QApplication.__init__(self, [])
        # 创建白板窗体
        self.board = WhiteBoardWindow(self.conn, id, callback=self.toggleWhiteBoard)
        # 创建主窗体
        self.main = Main(self.board, self.conn, id)

    def toggleWhiteBoard(self):
        self.main.toggleWhiteBoard()

    def startClientWindow(self):
        self.main.show()
        self.exec()

    def run(self):
        print("running thread")
        while self.conn.isAlive:
            try:
                cdata = self.conn.recvCDataBytes()
            except OSError as e:
                # 关闭socket连接后阻塞中的recv会触发OSError
                print("connection to server is unavailable, closing program...")
                break
            print("receive", cdata)
            cResp = CResponse.decode(cdata)
            if cResp.ctype == CType.USERINFOS:
                userinfodict = cResp.transToUserInfoDict()
                l = []
                for id, ip in userinfodict.items():
                    if id == self.main.id:
                        l.append(f"{ip} - {id} (me)")
                    else:
                        l.append(f"{ip} - {id}")
                self.main.setUserInfos(l)
            elif cResp.ctype == CType.PDATA:
                pData = cResp.transToPData()
                self.board.wb.paintFromMsg(pData)
        # 执行到这里说明连接断开了，关闭窗口
        self.main.close()

if __name__ == '__main__':
    cl = Client()
    cl.start()

    cl.startClientWindow()
    print("client window closed")

    print("waiting thread")
    cl.join()
    print("main thread done")

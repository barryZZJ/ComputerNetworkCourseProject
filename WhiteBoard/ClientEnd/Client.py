# @Author : ZZJ
import sys, os
from threading import Thread
module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(module_path)        # 导入的绝对路径
from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardApp
from WhiteBoard.controlData import CResponse, CType
from WhiteBoard.ClientEnd.GUIs.main import Main
from WhiteBoard.ClientEnd.ClientConn import ClientConn

class Client(Thread, Main, WhiteBoardApp):
    """客户端逻辑，调用GUI模块，显示界面"""
    def __init__(self):
        Thread.__init__(self)
        # 弹出连接窗口，获取服务器IP和端口，连接成功后返回conn对象
        self.conn = ClientConn()
        # 获取id
        cdata = self.conn.recvCDataBytes()
        id = CResponse.decode(cdata).transToId()
        # 创建主窗体
        Main.__init__(self, self.conn, id)
        # 创建白板窗体
        WhiteBoardApp.__init__(self, self.conn)

    def exit(self):
        self.conn.disconnect()
#TODO 掉线时的处理
    def run(self):
        while self.conn.isAlive:
            cdata = self.conn.recvCDataBytes()
            cResp = CResponse.decode(cdata)
            if cResp.ctype == CType.USERINFOS:
                userinfodict = cResp.transToUserInfoDict()
                l = []
                for id, ip in userinfodict.items():
                    if id == self.id:
                        l.append(f"{ip} - {id} (me)")
                    else:
                        l.append(f"{ip} - {id}")
                self.allUserInfos = l
                self.allUserInfosVar.set(l)
            elif cResp.ctypeype == CType.PDATA:
                pData = cResp.transToPData()
                self.wb.paintFromMsg(pData)


if __name__ == '__main__':
    cl = Client()
    cl.start()
    cl.showWindow()
    # 关闭窗口后断开连接
    cl.exit()
    cl.join()

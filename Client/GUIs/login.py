from tkinter import *
from Client.GUILogics.login import *
from Client.Conn import Conn
from tkinter import ttk

class UILogin(Tk):
    _size = '300x200'
    _but_width = '10'
    _but_height = '2'
    _text_but = '登录'
    _text_ip = '服务器IP    '
    _text_port = '服务器端口'

    def __init__(self, conn: Conn):
        super().__init__()
        self.geometry(self._size)
        self.resizable(0, 0) # 禁止调整窗口大小
        self.initMainUi()
        self.conn = conn

#TODO 错误提示
    def initMainUi(self):
        # 生成主界面
        #TODO 位置

        labelblock = Label(self,height = 2)
        labelblock.pack()

        fIp = Frame(self)
        fIp.pack()
        #TODO 一些细节，比如placeholder，点击文本框默认全选，文本框时回车触发按钮行为
        # ip输入
        self.serverIp = StringVar()
        labelIp = Label(fIp, text=self._text_ip)
        entryIp = Entry(fIp, textvariable=self.serverIp)
        labelIp.pack(side=LEFT)
        entryIp.pack(side=RIGHT)

        labelblock2 = Label(self)
        labelblock2.pack()

        # 端口输入
        fPort = Frame(self)
        fPort.pack()
        self.serverPort = StringVar()
        labelPort = Label(fPort, text=self._text_port)
        entryPort = Entry(fPort, textvariable=self.serverPort)
        labelPort.pack(side=LEFT)
        entryPort.pack(side=RIGHT)

        labelblock3 = Label(self)
        labelblock3.pack()

        # 登录按钮
        but_login = ttk.Button(self,
                           text=self._text_but,
                           width=self._but_width)
        # 绑定触发函数
        but_login['command'] = lambda: loginButHandler(self.conn, self.serverIp.get(), self.serverPort.get())
        but_login.pack()


if __name__ == '__main__':
    conn = Conn()
    login = UILogin(conn)
    login.mainloop()
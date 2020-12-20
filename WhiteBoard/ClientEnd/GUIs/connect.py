# @Author : ZZJ, CJY

from tkinter import *
import tkinter.messagebox as messagebox

# 连接窗口

class connectWindow(Tk):
    _title = "Connection"
    _size = '300x200'
    _but_width = '10'
    _but_height = '2'
    _text_but = 'Connect'
    _text_ip = 'server IP  '
    _text_default_ip = '127.0.0.1'
    _text_port = 'server port'
    _text_default_port = '5000'
    _font = ('Consolas', 11)

    # TODO 改icon等
    def __init__(self):
        super().__init__()
        self.geometry(self._size)
        self.title(self._title)
        self.initMainUi(self)
        self.focus_force()
        self.mainloop()

    def initMainUi(self, master):
        # 生成主界面

        # 占位
        labelblock = Label(master, height=2)
        labelblock.pack()

        fIp = Frame(master)
        fIp.pack()

        # ip输入
        labelIp = Label(fIp, text=self._text_ip, font=self._font)
        labelIp.pack(side=LEFT)
        self.serverIp = StringVar(value=self._text_default_ip)
        self.entryIp = Entry(fIp, font=self._font, textvariable=self.serverIp)
        self.entryIp.focus()
        self.entryIp.pack(side=RIGHT)

        labelblock2 = Label(master)
        labelblock2.pack()

        # 端口输入
        fPort = Frame(master)
        fPort.pack()
        labelPort = Label(fPort, text=self._text_port, font=self._font)
        labelPort.pack(side=LEFT)
        self.serverPort = StringVar(value=self._text_default_port)
        self.entryPort = Entry(fPort, font=self._font, textvariable=self.serverPort)
        self.entryPort.pack(side=RIGHT)

        labelblock3 = Label(master)
        labelblock3.pack()

        # 登录按钮
        but_connect = Button(master,
                             text=self._text_but,
                             height=self._but_height,
                             font=self._font)
        # 绑定触发函数
        but_connect['command'] = self.butConnectHandler
        but_connect.pack()

        # 回车触发按钮行为
        self.entryIp.bind('<Return>', self.butConnectHandler)
        self.entryPort.bind('<Return>', self.butConnectHandler)

    def butConnectHandler(self, evnet=None):
        """button逻辑，判断输入是否合法"""

        # 验证IP地址是否合法
        if not validIp(self.getServerIp()):
            messagebox.showerror(message=f"Invalid IP address: {self.getServerIp()}")
            self.entryIp.focus()
            return
        # 验证端口号是否合法
        if not validPort(self.getServerPorta()):
            messagebox.showerror(message=f"Invalid port: {self.getServerPorta()}")
            self.entryPort.focus()
            return

        self.destroy()

    def exit_program(self):
        exit()

    def getServerIp(self) -> str:
        return self.serverIp.get()
    def getServerPorti(self) -> int:
        return int(self.serverPort.get())
    def getServerPorta(self) -> str:
        return self.serverPort.get()

    @staticmethod
    def connectFailedHandler():
        '''连接服务器失败时的处理。弹出对应提示框。'''
        showerrorTop("Failed to connect to server, please try again.")
        return connectWindow()

def showerrorTop(msg):
    # 用于没有主窗体时的showerror
    temp = Tk()
    temp.withdraw()
    messagebox.showerror(message=msg)
    temp.destroy()


def validIp(ip: str) -> bool:
    """检查IP地址是否合法"""
    pattern = r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$'
    return re.match(pattern, ip) is not None

def validPort(port: str) -> bool:
    """检查port是否合法"""
    # 0~65535
    return port.isnumeric() and 0<=int(port)<=65535

if __name__ == '__main__':
    login = connectWindow()
    connectWindow.connectFailedHandler()
    # print(validIp('123'))
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
    _text_port = 'server port'
    _font = ('Consolas', 11)

    def __init__(self):
        super().__init__()
        # TODO 改标题、icon等
        self.geometry(self._size)
        self.resizable(0, 0)  # 禁止调整窗口大小
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
        self.entryIp = Entry(fIp, font=self._font)
        self.entryIp.focus()
        self.entryIp.pack(side=RIGHT)

        labelblock2 = Label(master)
        labelblock2.pack()

        # 端口输入
        fPort = Frame(master)
        fPort.pack()
        labelPort = Label(fPort, text=self._text_port, font=self._font)
        labelPort.pack(side=LEFT)
        self.entryPort = Entry(fPort, font=self._font)
        self.entryPort.pack(side=RIGHT)

        labelblock3 = Label(master)
        labelblock3.pack()

        # 登录按钮
        but_connect = Button(master,
                             text=self._text_but,
                             width=self._but_width,
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
        if not validIp(self.getIp()):
            messagebox.showerror(message=f"Invalid IP address: {self.getIp()}")
            self.entryIp.focus()
            return
        # 验证端口号是否合法
        if not validPort(self.getPort()):
            messagebox.showerror(message=f"Invalid port: {self.getPort()}")
            self.entryPort.focus()
            return

        self.exit()

    def exit(self):
        self.destroy()

    def getIp(self) -> str:
        return self.entryIp.get()
    def getPort(self) -> str:
        return self.entryPort.get()

    @staticmethod
    def connectFailedHandler():
        '''连接服务器失败时的处理。弹出对应提示框。'''
        showerrorTop("Failed to connect to server, please try again.")
        connectWindow()

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
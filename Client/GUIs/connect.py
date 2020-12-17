# @Author : ZZJ, CJY

from tkinter import *
from ErrorDialog import ErrorDialog

# 连接窗口

class connectWindow(Tk):
    _size = '300x200'
    _but_width = '10'
    _but_height = '2'
    _text_but = '连接'
    _text_ip = '服务器IP    '
    _text_port = '服务器端口'

    def __init__(self):
        #TODO 改标题、icon等
        super().__init__()
        self.geometry(self._size)
        self.resizable(0, 0) # 禁止调整窗口大小
        self.initMainUi()
        self.mainloop()


#TODO 错误提示
    def initMainUi(self):
        # 生成主界面
        #TODO 控件位置
        fIp = Frame(self)
        fIp.pack()
        #TODO 一些细节，比如placeholder，点击文本框默认全选，文本框时回车触发按钮行为
        # ip输入
        labelIp = Label(fIp, text=self._text_ip)
        labelIp.pack(side=LEFT)
        self.entryIp = Entry(fIp)
        self.entryIp.pack(side=RIGHT)

        # 端口输入
        fPort = Frame(self)
        fPort.place(x=35, y=70)
        labelPort = Label(fPort, text=self._text_port)
        labelPort.pack(side=LEFT)
        self.entryPort = Entry(fPort)
        self.entryPort.pack(side=RIGHT)

        # 登录按钮
        but_connect = Button(self,
                             text=self._text_but,
                             width=self._but_width,
                             height=self._but_height)
        # 绑定触发函数
        but_connect['command'] = self.butConnectHandler
        but_connect.place(x=90,y=120)

    def butConnectHandler(self):
        """button逻辑，判断输入是否合法"""

        # 验证IP地址是否合法
        if not validIp(self.getIp()):

            # errorDiaglog(f"Invalid IP address: {self.getIp()}").show()
            return

        # 验证端口号是否合法
        if not validPort(self.getPort()):
            # TODO
            # errorDiaglog(f"Invalid port: {self.getPort()}").show()
            return
        self.exit()

    def exit(self):
        self.destroy()

    def connectFailedHandler(self):
        '''连接服务器失败时的处理。弹出对应提示框。'''
        # TODO 弹出连接失败提示框
        self.mainloop()

    def getIp(self) -> str:
        return self.entryIp.get()
    def getPort(self) -> str:
        return self.entryPort.get()


def validIp(ip: str) -> bool:
    """检查IP地址是否合法"""
    pattern = r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$'
    return re.match(pattern, ip) is None

def validPort(port: str) -> bool:
    """检查port是否合法"""
    # 0~65535
    return port.isnumeric() and 0<=int(port)<=65535

if __name__ == '__main__':
    login = connectWindow()
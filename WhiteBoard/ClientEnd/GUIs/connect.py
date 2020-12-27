# @Author : ZZJ, CJY
import re
# 连接窗口
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, \
    QMessageBox, QHBoxLayout


class ConnectWindow(QMainWindow):
    _title = "Connection"
    _size = '300x200'
    _but_width = '10'
    _but_height = '2'
    _text_but = 'Connect'
    _text_ip = 'server IP    '
    _text_default_ip = '127.0.0.1'
    _text_port = 'server port'
    _text_default_port = '5000'
    _font = ('Consolas', 11)

    # TODO 改icon等
    def __init__(self):
        self.app = QApplication([])
        self.validInputs = False
        super().__init__()

        self.resize(300, 200)
        self.setFixedSize(300, 200)
#        self.title(self._title)
        self.initMainUi(self)

    def initMainUi(self, master):
        # 生成主界面

        # 占位
        # labelblock = Label(master, height=2)
        # labelblock.pack()
        self.serverPort = self._text_default_port
        self.fIp = QLineEdit(self)
        self.fIp.setText("127.0.0.1")

        # ip输入
        self.labelIp = QLabel(self._text_ip)


        # 端口输入
        self.fPort = QLineEdit(self)
        self.fPort.setText("5000")
        self.labelPort = QLabel(self._text_port)


        # 登录按钮

        self.button1 = QPushButton()
        self.button1.setText(self._text_but)
        self.button1.setToolTip("connect")

        # 绑定触发函数

        self.button1.clicked.connect(self.butConnectHandler)


        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout2.addWidget(self.labelIp)
        layout2.addWidget(self.fIp)
        layout3.addWidget(self.labelPort)
        layout3.addWidget(self.fPort)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addWidget(self.button1)

        # 主框架，所有控件的放置位置
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)

        self.show()
        self.app.exec()

    def keyPressEvent(self, event):#回车事件
        if str(event.key()) == '16777220':  # 回车
            self.butConnectHandler()

    def butConnectHandler(self, evnet=None):
        """button逻辑，判断输入是否合法"""
        # 验证IP地址是否合法
        print("进入逻辑判断")
        if not validIp(self.getServerIp()):
            #QMessageBox.show("Invalid IP address: {self.getServerIp()}")

            #self.entryIp.focus()
            print("bbb")
            return
        # 验证端口号是否合法
        if not validPort(self.getServerPorta()):
            print("aaa")
            #QMessageBox.showerror(message=f"Invalid port: {self.getServerPorta()}")
            #self.entryPort.focus()
            return
        self.validInputs = True
        self.destroy()

    def getServerIp(self) -> str:
        return self.fIp.text()
    def getServerPorti(self) -> int:
        return int(self.fPort.text())
    def getServerPorta(self) -> str:
        return self.serverPort

    @staticmethod
    def connectFailedHandler():
        '''连接服务器失败时的处理。弹出对应提示框。'''
        showerrorTop("Failed to connect to server, please try again.")
        return ConnectWindow()

def showerrorTop(msg):
    # 用于没有主窗体时的showerror
    #temp = Tk()

    QMessageBox.showerror(message=msg)



def validIp(ip: str) -> bool:
    """检查IP地址是否合法"""
    pattern = r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$'
    return re.match(pattern, ip) is not None

def validPort(port: str) -> bool:
    """检查port是否合法"""
    # 0~65535
    return port.isnumeric() and 0<=int(port)<=65535

if __name__ == '__main__':
    app = QApplication([])
    theWindow = ConnectWindow
    # theWindow.show()
    app.exec()
    # print(validIp('123'))
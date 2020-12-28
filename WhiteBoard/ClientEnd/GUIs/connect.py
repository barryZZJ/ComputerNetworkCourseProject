# @Author : ZZJ, CJY
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, \
    QMessageBox, QHBoxLayout

from WhiteBoard.ClientEnd.ClientConn import ClientConn

class ConnectWindow(QMainWindow):
    # 连接窗口
    _title = "Connection"
    _size = (280, 180)
    _text_but = 'Connect'
    _text_ip = 'server IP'
    _default_ip = '127.0.0.1'
    _text_port = 'server port'
    _default_port = '5000'

    def __init__(self, conn: ClientConn):
        super().__init__()
        self.conn = conn
        self.setFixedSize(*self._size)
        self.setWindowTitle(self._title)
        self.initMainUi()

    def initMainUi(self):
        # 生成主界面

        # ip输入
        labelIp = QLabel(self._text_ip)
        self.tIp = QLineEdit(self._default_ip)

        # 端口输入
        labelPort = QLabel(self._text_port)
        self.tPort = QLineEdit(self._default_port)

        # 登录按钮
        self.butConn = QPushButton(self._text_but)

        # 绑定触发函数
        self.butConn.clicked.connect(self.butConnHandler)

        layout = QVBoxLayout()
        layout2 = QHBoxLayout()

        layLabels = QVBoxLayout()
        layLabels.addWidget(labelIp)
        layLabels.addWidget(labelPort)
        layTexts = QVBoxLayout()
        layTexts.addWidget(self.tIp)
        layTexts.addWidget(self.tPort)

        layout2.addLayout(layLabels)
        layout2.addLayout(layTexts)


        layout.addLayout(layout2)
        layout.addWidget(self.butConn)

        # 主框架，所有控件的放置位置
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # 回车
            print("触发按钮事件")
            # self.butConnHandler()

    def butConnHandler(self):
        """button逻辑，判断输入是否合法"""

        # 验证IP地址是否合法
        if not validIp(self.serverIp):
            QMessageBox.critical(self, 'Invalid Ip', f"Invalid IP address: {self.serverIp}", QMessageBox.Ok)
            self.tIp.setFocus()
            return
        # 验证端口号是否合法
        if not validPort(self.serverPorta):
            QMessageBox.critical(self, 'Invalid Port', f"Invalid port number: {self.serverPorta}", QMessageBox.Ok)
            self.tPort.setFocus()
            return
        # 都合法，尝试连接
        self.conn.initConn(self.serverIp, self.serverPorti)
        if not self.conn.isAlive:
            self.connectFailedHint()
            return
        # 连接成功，关闭连接窗体
        self.close()

    def connectFailedHint(self):
        '''连接服务器失败时的处理。弹出对应提示框。'''
        QMessageBox.critical(self, "Error", "Failed to connect to server, please try again.", QMessageBox.Ok)

    @property
    def serverIp(self) -> str:
        return self.tIp.text()
    @property
    def serverPorti(self) -> int:
        return int(self.tPort.text())
    @property
    def serverPorta(self) -> str:
        return self.tPort.text()


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
    theWindow = ConnectWindow()
    theWindow.show()
    app.exec()
    # print(validIp('123'))
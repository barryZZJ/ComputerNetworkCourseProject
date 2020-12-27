import time
from threading import Thread

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QListWidget, QLabel, QVBoxLayout

from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardWindow
from WhiteBoard.ClientEnd.ClientConn import ClientConn

class Main(QMainWindow):
    _title = "Main"
    _size = (350, 350)
    _label_text = "Members list"
    _but_text_1 = "Start white board"
    _but_text_2 = "Stop white board"
    _but_height = '2'

    def __init__(self, board: WhiteBoardWindow, conn: ClientConn, id):
        super().__init__()
        self.setFixedSize(*self._size)
        self.conn = conn
        self.id = id
        print("user id is", self.id)

        self.board = board
        self.initMainUi()

    def closeEvent(self, event):
        self.board.close()
        self.conn.disconnect()

    def initMainUi(self):
        self.setWindowTitle(self._title)
        self.setGeometry(200, 200, 200, 100)
        # 状态栏
        self.butWB = QPushButton(self._but_text_1)

        self.listMembers = QListWidget()
        labelMembers = QLabel(self._label_text)

        layout2 = QVBoxLayout()
        layout2.addWidget(labelMembers)
        layout2.addWidget(self.listMembers)

        layout = QHBoxLayout()
        layout.addLayout(layout2)
        layout.addWidget(self.butWB)


        # 主框架，所有控件的放置位置
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        # 使充满屏幕
        self.setCentralWidget(mainFrame)

        self.butWB.clicked.connect(self.toggleWhiteBoard)

    def setUserInfos(self, allUserInfos):
        self.listMembers.clear()
        for i, userinfo in enumerate(allUserInfos):
            self.listMembers.insertItem(i, userinfo)

    def toggleWhiteBoard(self):
        if self.board.isHidden():
            # 打开白板
            self.board.show()
            self.butWB.setText(self._but_text_2)
        else:
            # 关掉了白板
            self.board.close()
            self.butWB.setText(self._but_text_1)





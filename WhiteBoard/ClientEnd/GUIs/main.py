#from tkinter import *
# from mttkinter.mtTkinter import *
#TODO 改成mttk行不行
import sys

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QListWidget

from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardApp
from WhiteBoard.ClientEnd.ClientConn import ClientConn


class Main(QMainWindow):
    _title = "Main"
    _size = '350x350'
    _font = ('Consolas', 11)
    _lf_text = "Members"
    _but_text_1 = "Start white board"
    _but_text_2 = "Stop white board"
    _but_height = '2'

    def __init__(self, board: WhiteBoardApp, conn: ClientConn, id):
        super().__init__()
        self.resize(300, 350)
        self.setFixedSize(300, 350)
        self.app = QApplication([])
#        self.title(self._title)

        self.conn = conn
        self.id = id
        print("user id is", self.id)

        self.isBoardOn = False # 白板是否打开
        self.allUserInfos = []
#        self.allUserInfosVar = StringVar(value=self.allUserInfos)
        self.initMainUi(self)

        self.board = board

    def showWindow(self):
        self.show()
        self.app.exec()

    def run(self):
        self.show()
        self.app.exec()

    def initMainUi(self, master):
        #lf = LabelFrame(master, text=self._lf_text, font=self._font)
        #lf.pack(expand=1, fill=Y, side=LEFT, anchor=W)
        self.setWindowTitle("第一个主窗口应用")
        self.setGeometry(200, 200, 200, 100)
        # 状态栏
        self.status = self.statusBar()
        self.button1 = QPushButton()
        self.button1.setText(self._but_text_1)
        self.button1.setToolTip("按钮说明")
        self.listwidget = QListWidget()
        self.listwidget.clear()
        print(self.allUserInfos)
        for i in range(0,len(self.allUserInfos)):
            self.listwidget.insertItem(i, self.allUserInfos[i])
        # self.listwidget.insertItem(1, "Orange")
        # self.listwidget.insertItem(2, "Blue")
        # self.listwidget.insertItem(3, "White")
        # self.listwidget.insertItem(4, "Green")
        #self.listwidget.clear()

        layout = QHBoxLayout()

        layout.addWidget(self.listwidget)
        layout.addWidget(self.button1)


        # 主框架，所有控件的放置位置
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        # 使充满屏幕
        self.setCentralWidget(mainFrame)

        self.button1.clicked.connect(self.toggleWhiteBoard)

        #TODO 禁止click
        #self.lst = Listbox(lf, listvariable=self.allUserInfosVar)
        #self.lst.pack(expand=1, fill=Y)

        #self.but_text = StringVar(value=self._but_text_1)



    def setListBox(self,allUserInfos):
        self.listwidget.clear()
        print(allUserInfos)
        for i in range(0, len(allUserInfos)):
            self.listwidget.insertItem(i, self.allUserInfos[i])

    def toggleWhiteBoard(self):
        print("testDone====")
        #TODO 白板启动时main无法响应的问题
        if self.isBoardOn:
            # 关掉了白板

            self.but_text.set(self._but_text_1)
            self.board.exitApp()
        else:
            # 打开白板
            self.board.showBoard()
            #self.but_text.set(self._but_text_2)
        self.isBoardOn = not self.isBoardOn
#TODO 手动关掉白板，修改button行为




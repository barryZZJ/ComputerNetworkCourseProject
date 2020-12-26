from threading import Thread
from time import sleep
from tkinter import *

from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow

from WhiteBoard.ClientEnd.ClientConn import ClientConn
from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardApp, WhiteBoardWindow
from WhiteBoard.controlData import PResponse, CType


class Main(QMainWindow):
    _title = "Main"
    _size = '350x350'
    _font = ('Consolas', 11)
    _lf_text = "Members"
    _but_text_1 = "Start white board"
    _but_text_2 = "Stop white board"
    _but_height = '2'

    def __init__(self, conn: ClientConn):
        super().__init__()
        self.geometry(self._size)
        self.title(self._title)

        self.conn = conn
        self.userId = conn.getHostId()
        print("user id is", self.userId)

        self.isBoardOn = False # 白板是否打开
        self.board = None
        self.allUserInfos = []
        self.allUserInfosVar = StringVar(value=self.allUserInfos)
        self.initMainUi(self)
        self.after(self.conn._poll_all_users_interval, self.pollAllUsers)

        self.focus_force()

        self.mainloop()

    def initMainUi(self, master):
        lf = LabelFrame(master, text=self._lf_text, font=self._font)
        lf.pack(expand=1, fill=Y, side=LEFT, anchor=W)

        self.lst = Listbox(lf, listvariable=self.allUserInfosVar)
        self.lst.pack(expand=1, fill=Y)

        self.but_text = StringVar(value=self._but_text_1)

        but = Button(master, textvariable=self.but_text, font=self._font,
                     height=self._but_height)
        but.pack(side=RIGHT, expand=1)
        but['command'] = self.toggleWhiteBoard

    def toggleWhiteBoard(self):
        if not self.isBoardOn:
            # 结束共享后改为“打开白板”
            self.but_text.set(self._but_text_1)
            self.board = WhiteBoardApp()
            self.after(1, self.board.show)
        else:
            # 成功打开白板后改为“结束白板”
            # 成功打开白板后隐藏按钮
            self.but_text.set(self._but_text_2)
            self.board.exit()
        self.isBoardOn = not self.isBoardOn

    def pollAllUsers(self):
        # 定时轮询，请求所有成员的信息，更新listbox
        userinfodict = self.conn.getUserInfoDict()
        l = []
        for id, ip in userinfodict.items():
            if id == self.userId:
                l.append(f"{ip} - {id} (me)")
            else:
                l.append(f"{ip} - {id}")
        self.allUserInfos = l
        self.allUserInfosVar.set(l)
        self.after(self.conn._poll_all_users_interval, self.pollAllUsers)

    def show(self):
        self.app = QApplication([])
        window = Main(self.conn)
        window.show()
        self.app.exec()

if __name__ == '__main__':

    Main(None).show()
    #Main(None)



from tkinter import *

from WhiteBoard.ClientEnd.ClientConn import ClientConn
from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardApp

class Main(Tk):
    _title = "Main"
    _size = '350x350'
    _font = ('Consolas', 11)
    _lf_text = "Members"
    _but_text_1 = "Start white board"
    _but_text_2 = "Stop white board"
    _but_height = '2'

    def __init__(self, conn: ClientConn, id):
        super().__init__()
        self.geometry(self._size)
        self.title(self._title)

        self.conn = conn
        self.id = id
        print("user id is", self.id)

        self.isBoardOn = False # 白板是否打开
        self.board = None
        self.allUserInfos = []
        self.allUserInfosVar = StringVar(value=self.allUserInfos)
        self.initMainUi(self)

        # Thread(target=self.conn.recvCData).start()

        self.focus_force()

    def showWindow(self):
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
        #TODO 有问题，打开白板后main不能正确响应用户操作
        if not self.isBoardOn:
            # 结束共享后改为“打开白板”
            self.but_text.set(self._but_text_1)
            self.board = WhiteBoardApp(self.conn)
            self.board.showBoard()
        else:
            # 成功打开白板后改为“结束白板”
            # 成功打开白板后隐藏按钮
            self.but_text.set(self._but_text_2)
            self.board.exit()
        self.isBoardOn = not self.isBoardOn


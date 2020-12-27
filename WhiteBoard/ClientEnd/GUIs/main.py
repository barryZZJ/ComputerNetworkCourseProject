from tkinter import *
# from mttkinter.mtTkinter import *
#TODO 改成mttk行不行

from threading import Thread
from ClientEnd.GUIs import tmp
from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardApp
from WhiteBoard.ClientEnd.ClientConn import ClientConn

class Main(Tk):
    _title = "Main"
    _size = '350x350'
    _font = ('Consolas', 11)
    _lf_text = "Members"
    _but_text_1 = "Start white board"
    _but_text_2 = "Stop white board"
    _but_height = '2'

    def __init__(self, board: WhiteBoardApp, conn: ClientConn, id):
        Tk.__init__(self)
        self.geometry(self._size)
        self.title(self._title)

        self.conn = conn
        self.id = id
        print("user id is", self.id)

        self.isBoardOn = False # 白板是否打开
        self.allUserInfos = []
        self.allUserInfosVar = StringVar(value=self.allUserInfos)
        self.initMainUi(self)

        self.board = board

    def showWindow(self):
        self.mainloop()

    def run(self):
        self.mainloop()

    def initMainUi(self, master):
        lf = LabelFrame(master, text=self._lf_text, font=self._font)
        lf.pack(expand=1, fill=Y, side=LEFT, anchor=W)

        #TODO 禁止click
        self.lst = Listbox(lf, listvariable=self.allUserInfosVar)
        self.lst.pack(expand=1, fill=Y)

        self.but_text = StringVar(value=self._but_text_1)

        but = Button(master, textvariable=self.but_text, font=self._font,
                     height=self._but_height)
        but.pack(side=RIGHT, expand=1)
        but['command'] = self.toggleWhiteBoard

    def toggleWhiteBoard(self):
        #TODO 白板启动时main无法响应的问题
        if self.isBoardOn:
            # 关掉了白板
            self.but_text.set(self._but_text_1)
            self.board.exitApp()
        else:
            # 打开白板
            self.board.showBoard()
            self.but_text.set(self._but_text_2)
        self.isBoardOn = not self.isBoardOn
#TODO 手动关掉白板，修改button行为

if __name__ == '__main__':
    main = Main(None, None, 1)
    main.start()
    main.destroy()
    # Thread(target=main.mainloop).start()
    # main.mainloop()
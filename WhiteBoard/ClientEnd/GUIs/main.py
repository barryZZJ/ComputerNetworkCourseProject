from tkinter import *
from WhiteBoard.ClientEnd.Conn import Conn

class Main(Tk):
    _title = "Main"
    _size = '350x350'
    _font = ('Consolas', 11)
    _lf_text = "Members"
    _but_text = "Start white board"
    _but_height = '2'

    def __init__(self, conn: Conn):
        super().__init__()
        self.geometry(self._size)
        self.title(self._title)
        self.initMainUi(self)
        # self.appendToUserList(f"127.0.0.1 (me)")
        self.userId = conn.getHostId()
        print("user id is", self.userId)
        self.appendToUserList(f"{conn.getHostIp()}-{self.userId} (me)")
        self.conn = conn
        self.focus_force()
        self.mainloop()


    def initMainUi(self, master):
        lf = LabelFrame(master, text=self._lf_text, font=self._font)
        lf.pack(expand=1, fill=Y, side=LEFT, anchor=W)

        self.lst = Listbox(lf)
        self.lst.pack(expand=1, fill=Y)

        but = Button(master, text=self._but_text, font=self._font,
                     height=self._but_height)
        but.pack(side=RIGHT, expand=1)
        but['command'] = self.startWhiteBoardHandler

    def startWhiteBoardHandler(self):
        # 成功打开白板后改为“结束白板”
        # 结束共享后改为“打开白板”

        return

    def appendToUserList(self, content):
        # 在listbox中添加新的成员信息
        self.lst.insert(self.lst.size(), content)

if __name__ == '__main__':
    Main(None)



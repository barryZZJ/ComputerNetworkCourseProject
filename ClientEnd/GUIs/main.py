from tkinter import *
from ClientEnd.Conn import Conn

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
        self.focus_force()
        self.conn = conn
        self.mainloop()


    def initMainUi(self, master):
        lf = LabelFrame(master, text=self._lf_text, font=self._font)
        lf.pack(expand=1, fill=Y, side=LEFT, anchor=W)

        lst = Listbox(lf)
        #debug
        lst.insert(0, ["127.0.0.1(me)"])
        # lst.insert(0, [self.conn.getHostIp()])
        lst.pack(expand=1, fill=Y)

        but = Button(master, text=self._but_text, font=self._font,
                     height=self._but_height)
        but.pack(side=RIGHT, expand=1)
        but['command'] = self.startWhiteBoardHandler

    def startWhiteBoardHandler(self):
        # 成功打开白板后改为“结束白板”
        # 结束共享后改为“打开白板”
        return

if __name__ == '__main__':
    Main(None)



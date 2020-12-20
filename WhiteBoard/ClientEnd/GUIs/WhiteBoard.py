# init函数应该需要传入conn对象，用于传给GUILogic的各种handler
#! 白板板大小同步问题
from tkinter import *


class WhiteBoard(Tk):
    _title = "WhiteBoard"
    _size = '800x600'
    _font = ('Consolas', 11)

    def __init__(self):
        super().__init__()
        self.geometry(self._size)
        self.title(self._title)
        self.initMainUi(self)
        self.focus_force()
        self.mainloop()

    def initMainUi(self, master):
        lf = LabelFrame(master, text=self._lf_text, font=self._font)
        lf.pack(expand=1, side=LEFT, font=self._font)

        but = Button(master, text=self._but_text, font=self._font,
                     width=self._but_width,
                     height=self._but_height)
        but.pack(side=RIGHT)

        but['command'] = self.startWhiteBoardHandler

    def startWhiteBoardHandler(self):
        return



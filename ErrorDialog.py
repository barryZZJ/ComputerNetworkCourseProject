from tkinter import *

class ErrorDialog(Tk):
    def __init__(self, msg):
        super().__init__()
        self.resizable(0, 0)
        Label(self, text=msg).pack()
        Button(self, text="OK", command=self.destroy).pack()

    def show(self):
        self.mainloop()

import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

# create the application
root = tk.Tk()
myapp = App(root)
#
# here are method calls to the window manager class
#
root.title("My Do-Nothing Application")
root.maxsize(1000, 400)

# start the program
myapp.mainloop()
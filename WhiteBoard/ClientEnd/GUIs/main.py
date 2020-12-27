#TODO 改成mttk行不行
from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QListWidget

from WhiteBoard.ClientEnd.GUIs.WhiteBoardGUI import WhiteBoardWindow
from WhiteBoard.ClientEnd.ClientConn import ClientConn


class Main(QMainWindow):
    _title = "Main"
    _size = '350x350'
    _font = ('Consolas', 11)
    _lf_text = "Members"
    _but_text_1 = "Start white board"
    _but_text_2 = "Stop white board"
    _but_height = '2'

    def __init__(self, board: WhiteBoardWindow, conn: ClientConn, id):
        super().__init__()
        self.resize(300, 350)
        self.setFixedSize(300, 350)
        self.conn = conn
        self.id = id
        print("user id is", self.id)
        self.allUserInfos = []

        self.initMainUi()
        self.board = board

    def closeEvent(self, event):
        self.board.close()
        self.conn.disconnect()

    def initMainUi(self):
        self.setWindowTitle("第一个主窗口应用")
        self.setGeometry(200, 200, 200, 100)
        # 状态栏
        self.status = self.statusBar()
        self.button1 = QPushButton()
        self.button1.setText(self._but_text_1)
        self.button1.setToolTip("按钮说明")

        self.listwidget = QListWidget()

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



    def setUserInfos(self, allUserInfos):
        self.allUserInfos = allUserInfos
        self.listwidget.clear()
        for i, userinfo in enumerate(self.allUserInfos):
            self.listwidget.insertItem(i, userinfo)
        self.listwidget.adjustSize()


    def toggleWhiteBoard(self):
        if self.board.isHidden():
            # 打开白板
            self.board.show()
            self.button1.setText(self._but_text_2)
        else:
            # 关掉了白板
            self.board.hide()
            self.button1.setText(self._but_text_1)

#TODO 手动关掉白板时，修改button行为
#TODO 关掉main时，白板也要关掉；发送disconnect之类的




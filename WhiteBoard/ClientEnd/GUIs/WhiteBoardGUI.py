import os
from time import sleep

from PyQt5.QtWidgets import QMainWindow, QApplication,  QLineEdit, QInputDialog, QColorDialog, QLabel, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QMouseEvent, QCursor
from PyQt5.QtCore import Qt


from WhiteBoard.ClientEnd.ClientConn import ClientConn
from WhiteBoard.paintData import PData, PType, SType
from WhiteBoard.controlData import CRequest

RESOURCES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
PATHTOTEXT = os.path.join(RESOURCES, "text.png")
PATHTOREC = os.path.join(RESOURCES, "Rec.png")
PATHTOCIRCLE = os.path.join(RESOURCES, "Circle.png")
PATHTOLINE = os.path.join(RESOURCES, "Line.png")
PATHTOPEN = os.path.join(RESOURCES, "pen.png")
PATHTOERASER = os.path.join(RESOURCES, "eraser.png")
PATHTOCOLOR = os.path.join(RESOURCES, "color.png")
PATHTOWIDTH = os.path.join(RESOURCES, "changewidth.png")


class WhiteBoardCanvas(QLabel):

    def __init__(self, parent, conn: ClientConn):
        QLabel.__init__(self, parent)
        self.conn=conn
        self.whiteboard = QPixmap(797, 597)  # 考虑边框的间距 减去px
        self.whiteboard.fill(Qt.white)
        self.setStyleSheet("border: 2px solid white")
        self.foreColor = Qt.black  # pen color
        self.backColor = Qt.white  # eraser color
        self.x1 = 0 # 坐标
        self.y1 = 0 # 坐标
        self.x2 = 0 # 坐标
        self.y2 = 0 # 坐标
        self.text = ""  # 记录输入的文字
        self.width = 4  # pen width
        self.pData = PData(PType.BRUSH, self.foreColor)
        self.serverMsg: PData
        self.isMouseDown = False
        self.isMouseUp = not self.isMouseDown
        self.isPaintFromMsg = False

# 切换绘制类型
    def setToDot(self):
        print('set to brush')
        self.setCursor(Qt.CrossCursor)
        self.pData.setToBrush()

    def setToLine(self):
        print('set to line')
        self.setCursor(Qt.CrossCursor)
        self.pData.setToShape(SType.LINE)

    def setToCircle(self):
        print("set to circle")
        self.setCursor(Qt.CrossCursor)
        self.pData.setToShape(SType.CIRCLE)

    def setToRec(self):
        print("set to rec")
        self.setCursor(Qt.CrossCursor)
        self.pData.setToShape(SType.RECT)

    def setToText(self):
        print("set to text")
        self.setCursor(Qt.ArrowCursor)
        self.pData.setToText()

    def setToEraser(self):
        # 自定义鼠标形状（png）
        print("set to eraser")
        myPixmp = QPixmap(PATHTOERASER).scaled(30,30)
        myCursor = QCursor(myPixmp)
        self.setCursor(myCursor)
        self.pData.setToEraser()

    def paintEvent(self, event):
        painter = QPainter(self.whiteboard)
        if not self.isPaintFromMsg:
            # 本地作画行为
            if self.pData.isEraser():
                painter.setPen(QPen(self.backColor, self.width, Qt.SolidLine))
            else:
                painter.setPen(QPen(self.foreColor, self.width, Qt.SolidLine))

            print(self.x1, self.y1, self.x2, self.y2)
            #这里需要接受服务器的图形添加在客户端

            if (self.pData.isBrush() or self.pData.isEraser()) and self.isMouseDown:
                # 笔刷画点、橡皮，使用同一种画法
                if self.pData.isBrush():
                    self.pData.updateArgs((self.x1, self.y1), (self.x2, self.y2), self.width)
                    print("draw dot local")
                else:
                    self.pData.updateArgs((self.x1, self.y1), (self.x2, self.y2), self.width)
                    print("draw eraser local")
                painter.drawLine(self.x1, self.y1, self.x2, self.y2)

            elif self.pData.isLine() and self.isMouseUp:
                # 画直线
                print("draw line local")
                self.pData.updateArgs(SType.LINE, (self.x1, self.y1), (self.x2, self.y2), self.width)
                painter.drawLine(self.x1, self.y1, self.x2, self.y2)

            elif self.pData.isCircle() and self.isMouseUp:
                # 画圆
                print("draw circle local")
                self.pData.updateArgs(SType.CIRCLE, (self.x1, self.y1), (self.x2, self.y2), self.width)
                painter.drawEllipse(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)

            elif self.pData.isRect() and self.isMouseUp:
                # 画矩形
                print("draw rec local")
                self.pData.updateArgs(SType.RECT, (self.x1, self.y1), (self.x2, self.y2), self.width)
                painter.drawRect(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)

            elif self.pData.isText() and self.text != "" and self.isMouseDown:
                # 画文字
                print("draw text local")
                self.pData.updateArgs(self.text, (self.x1, self.y1))
                painter.drawText(self.x1, self.y1,self.text)
            self.sendCData()
            self.isPaintFromMsg = False
        else:
            # 根据远程信息作画
            if self.serverMsg.isEraser():
                painter.setPen(QPen(self.backColor, self.serverMsg.body.width, Qt.SolidLine))
            elif self.serverMsg.isText():
                # 需要width参数，但画文字用不到，就设成本地的好了
                painter.setPen(QPen(self.foreColor, self.width, Qt.SolidLine))
            else:
                painter.setPen(QPen(self.foreColor, self.serverMsg.body.width, Qt.SolidLine))


            if self.serverMsg.isBrush() or self.serverMsg.isEraser():
                # 笔刷画点、橡皮，使用同一种画法
                if self.serverMsg.isBrush():
                    print("draw dot remote")
                else:
                    print("draw eraser remote")
                x1 = self.serverMsg.body.st[0]
                y1 = self.serverMsg.body.st[1]
                x2 = self.serverMsg.body.ed[0]
                y2 = self.serverMsg.body.ed[1]
                painter.drawLine(x1, y1, x2, y2)

            elif self.serverMsg.isLine():
                # 画直线
                print("draw line remote")
                x1 = self.serverMsg.body.st[0]
                y1 = self.serverMsg.body.st[1]
                x2 = self.serverMsg.body.ed[0]
                y2 = self.serverMsg.body.ed[1]
                painter.drawLine(x1, y1, x2, y2)

            elif self.serverMsg.isCircle():
                # 画圆
                print("draw circle remote")
                x1 = self.serverMsg.body.st[0]
                y1 = self.serverMsg.body.st[1]
                x2 = self.serverMsg.body.ed[0]
                y2 = self.serverMsg.body.ed[1]
                painter.drawEllipse(x1, y1, x2 - x1, y2 - y1)

            elif self.serverMsg.isRect():
                # 画矩形
                print("draw rec remote")
                x1 = self.serverMsg.body.st[0]
                y1 = self.serverMsg.body.st[1]
                x2 = self.serverMsg.body.ed[0]
                y2 = self.serverMsg.body.ed[1]
                painter.drawRect(x1, y1, x2 - x1, y2 - y1)

            elif self.serverMsg.isText():
                # 画文字
                print("draw text remote")
                x1 = self.serverMsg.body.pos[0]
                y1 = self.serverMsg.body.pos[1]
                painter.drawText(x1, y1, self.serverMsg.body.content)
            self.isPaintFromMsg = False

        Label_painter = QPainter(self)
        Label_painter.drawPixmap(2, 2, self.whiteboard)

    def mousePressEvent(self, event: QMouseEvent):
        # 鼠标按下
        if event.button() == Qt.LeftButton:
            print("mouse pressed")
            self.x1 = event.x()
            self.y1 = event.y()
            self.x2 = self.x1
            self.y2 = self.y1
            self.isMouseDown = True
            self.isMouseUp = not self.isMouseDown


    def mouseMoveEvent(self, event):

        if self.isMouseDown and self.pData.isBrush():
            # 刷子事件需要更新鼠标平移的情况
            sleep(0.0001)
            self.x1 = self.x2
            self.y1 = self.y2
            self.x2 = event.x()
            self.y2 = event.y()

            self.update()

    def mouseReleaseEvent(self, event):
        #鼠标弹起
        if event.button() == Qt.LeftButton:
            print("mouse released")
            self.x1 = self.x2
            self.y1 = self.y2
            self.x2 = event.x()
            self.y2 = event.y()
            self.isMouseDown = False
            self.isMouseUp = not self.isMouseDown
            self.update()

    def sendCData(self):
        self.conn.sendall(CRequest().pData(self.pData).encode())

    def paintFromMsg(self, pData: PData):
        self.isPaintFromMsg = True
        self.serverMsg = pData
        self.update()

class WhiteBoardWindow(QMainWindow):
    def __init__(self, conn: ClientConn):
        QMainWindow.__init__(self)
        self.wb = WhiteBoardCanvas(self, conn)
        self.initUi()

    def initUi(self):
        self.resize(770, 570)
        self.setFixedSize(770, 570)

        # 设置画板
        self.wb.setGeometry(10, 50, 750, 501)
        # 橡皮
        eraser = QAction(QIcon(PATHTOERASER), "Eraser", self)
        eraser.setToolTip("Eraser")

        color = QAction(QIcon(PATHTOCOLOR), "color", self)
        color.setToolTip("color")

        pen = QAction(QIcon(PATHTOPEN), "pen", self)
        pen.setToolTip("pen")

        Line = QAction(QIcon(PATHTOLINE), "Line", self)
        Line.setToolTip("Line")

        Circle = QAction(QIcon(PATHTOCIRCLE), "Circle", self)
        Circle.setToolTip("Circle")

        Rec = QAction(QIcon(PATHTOREC), "Rec", self)
        Rec.setToolTip("Rec")

        Text = QAction(QIcon(PATHTOTEXT), "Text", self)
        Text.setToolTip("Text")

        changeWidth = QAction(QIcon(PATHTOWIDTH), "Width", self)
        changeWidth.setToolTip("Width")


        #工具栏
        self.menubar = self.addToolBar("ToolBar")
        self.menubar.setMovable(False)
        self.menubar.addAction(eraser)
        self.menubar.addAction(color)
        self.menubar.addAction(pen)
        self.menubar.addAction(Line)
        self.menubar.addAction(Circle)
        self.menubar.addAction(Rec)
        self.menubar.addAction(Text)
        self.menubar.addAction(changeWidth)
        # 主页面
        self.setWindowTitle("Drawing Board")

        eraser.triggered.connect(self.wb.setToEraser)
        color.triggered.connect(self.chooseColor)
        pen.triggered.connect(self.wb.setToDot)
        Line.triggered.connect(self.wb.setToLine)
        Circle.triggered.connect(self.wb.setToCircle)
        Rec.triggered.connect(self.wb.setToRec)
        Text.triggered.connect(self.trySetToText)
        changeWidth.triggered.connect(self.changeWidth)

        #默认点一下笔刷
        pen.trigger()

    def chooseColor(self):
        Color = QColorDialog.getColor()  # color是Qcolor
        if Color.isValid():
            self.wb.foreColor = Color

    def changeWidth(self):
        width, okPressed = QInputDialog.getInt(self, '选择画笔粗细', '请输入粗细：', min=1, step=1)
        if okPressed:
            self.wb.width = width

    def trySetToText(self):
        validFlag = False
        while not validFlag:
            text, okPressed = QInputDialog.getText(self, "Get text", "要共享的文字:", QLineEdit.Normal, "")
            if not okPressed:
                validFlag = True
            elif text != '':
                validFlag = True
                self.wb.text = text
                self.wb.setToText()
            else:
                QMessageBox(self, "Error", "输入不能为空！")

class WhiteBoardApp(WhiteBoardWindow):
    def __init__(self, conn: ClientConn):
        self.app = QApplication([])
        WhiteBoardWindow.__init__(self, conn)
        self.closed = False


    def exit(self):
        self.app.exit()
        self.closed = True

    def showBoard(self):
        self.show()
        self.app.exec()


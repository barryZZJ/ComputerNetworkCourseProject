import os
from time import sleep

from PyQt5.QtWidgets import QMainWindow, QApplication,  QLineEdit, QInputDialog, QColorDialog, QLabel, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QMouseEvent, QCursor, QPaintEvent, QColor, QActionEvent, \
    QCloseEvent
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
PATHTOERASE = os.path.join(RESOURCES, "erase.png")
PATHTOREPAINT = os.path.join(RESOURCES, "repaint.png")


PATHTOTEXT2 = os.path.join(RESOURCES, "text2.png")
PATHTOREC2 = os.path.join(RESOURCES, "Rec2.png")
PATHTOCIRCLE2 = os.path.join(RESOURCES, "Circle2.png")
PATHTOLINE2 = os.path.join(RESOURCES, "Line2.png")
PATHTOPEN2 = os.path.join(RESOURCES, "pen2.png")
PATHTOERASER2 = os.path.join(RESOURCES, "eraser2.png")
PATHTOCOLOR2 = os.path.join(RESOURCES, "color2.png")
PATHTOWIDTH2 = os.path.join(RESOURCES, "changewidth2.png")


class WhiteBoardCanvas(QLabel):

    def __init__(self, parent, conn: ClientConn):
        QLabel.__init__(self, parent)
        self.conn=conn
        self.whiteboard = QPixmap(797, 597)  # 考虑边框的间距 减去px
        self.whiteboard.fill(Qt.white)
        self.setStyleSheet("border: 2px solid white")
        self.foreColor = QColor(Qt.black) # pen color
        self.backColor = QColor(Qt.white) # eraser color
        self.x1 = 0 # 坐标
        self.y1 = 0 # 坐标
        self.x2 = 0 # 坐标
        self.y2 = 0 # 坐标
        self.text = ""  # 记录输入的文字
        self.width = 4  # pen width
        self.eraserWidth = 10
        self.pData = PData(PType.NA, self.foreColor, self.backColor)
        self.serverMsg: PData
        self.isMouseDown = False
        self.isMouseUp = True
        self.isPaintFromMsg = False
        self.clearSign = False

    def setForeColor(self, color: QColor):
        self.foreColor = color
        self.pData.setForeColor(color)

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
        self.setCursor(Qt.CrossCursor)
        self.pData.setToText()

    def setToEraser(self):
        # 自定义鼠标形状（png）
        print("set to eraser")
        myPixmp = QPixmap(PATHTOERASE).scaled(10,10)
        myCursor = QCursor(myPixmp)
        self.setCursor(myCursor)
        self.pData.setToEraser()

    def Repaint(self):
        print("clear")
        self.clearSign = True
        self.update()


#TODO 橡皮、文本框失灵

#TODO 加一个清屏

    def paintEvent(self, event: QPaintEvent):
        QPainter(self).drawPixmap(2, 2, self.whiteboard)
        event.accept()

    def doPaint(self):
        painter = QPainter(self.whiteboard)
        if not self.isPaintFromMsg:
            # 本地作画行为
            #这里需要接受服务器的图形添加在客户端

            if self.clearSign == True:
                self.clearSign = False
                painter.eraseRect(0,0,1000,1000)

            print("in do paint")


            if self.pData.isBrush() and self.isMouseDown:
                painter.setPen(QPen(self.foreColor, self.width, Qt.SolidLine))
                self.pData.set((self.x1, self.y1), (self.x2, self.y2), self.width)
                print("draw dot local")
                painter.drawLine(self.x1, self.y1, self.x2, self.y2)
                if self.conn:
                    self.sendCReq()
            elif self.pData.isEraser() and self.isMouseDown:
                painter.setPen(QPen(self.backColor, self.eraserWidth, Qt.SolidLine))
                self.pData.set((self.x1, self.y1), (self.x2, self.y2), self.eraserWidth)
                print("draw eraser local")
                painter.drawLine(self.x1, self.y1, self.x2, self.y2)
                if self.conn:
                    self.sendCReq()

            elif self.pData.isLine() and self.isMouseUp:
                # 画直线
                painter.setPen(QPen(self.foreColor, self.width, Qt.SolidLine))
                print("draw line local")
                self.pData.set(SType.LINE, (self.x1, self.y1), (self.x2, self.y2), self.width)
                painter.drawLine(self.x1, self.y1, self.x2, self.y2)
                if self.conn:
                    self.sendCReq()

            elif self.pData.isCircle() and self.isMouseUp:
                # 画圆
                painter.setPen(QPen(self.foreColor, self.width, Qt.SolidLine))
                print("draw circle local")
                self.pData.set(SType.CIRCLE, (self.x1, self.y1), (self.x2, self.y2), self.width)
                painter.drawEllipse(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)
                if self.conn:
                    self.sendCReq()

            elif self.pData.isRect() and self.isMouseUp:
                # 画矩形
                painter.setPen(QPen(self.foreColor, self.width, Qt.SolidLine))
                print("draw rec local")
                self.pData.set(SType.RECT, (self.x1, self.y1), (self.x2, self.y2), self.width)
                painter.drawRect(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)
                if self.conn:
                    self.sendCReq()

            elif self.pData.isText() and self.text != "" and self.isMouseDown:
                # 画文字
                painter.setPen(QPen(self.foreColor, self.width, Qt.SolidLine))
                print("draw text local")
                self.pData.set(self.text, (self.x1, self.y1))
                painter.drawText(self.x1, self.y1,self.text)
                if self.conn:
                    self.sendCReq()
            #TODO 清屏相关
            # elif 清屏:
            #     if self.conn:
            #         self.sendCReq(PData(PType.CLS, self.foreColor, self.backColor))

            self.isPaintFromMsg = False
        else:
            try:
                # 根据远程信息作画
                print("painting from server")
                if self.serverMsg.isBrush():
                    print("draw dot remote")
                    painter.setPen(QPen(self.serverMsg.foreColor, self.serverMsg.body.width, Qt.SolidLine))
                    x1 = self.serverMsg.body.st[0]
                    y1 = self.serverMsg.body.st[1]
                    x2 = self.serverMsg.body.ed[0]
                    y2 = self.serverMsg.body.ed[1]
                    painter.drawLine(x1, y1, x2, y2)

                elif self.serverMsg.isEraser():
                    print("draw eraser remote")
                    painter.setPen(QPen(self.serverMsg.backColor, self.serverMsg.body.width, Qt.SolidLine))
                    x1 = self.serverMsg.body.st[0]
                    y1 = self.serverMsg.body.st[1]
                    x2 = self.serverMsg.body.ed[0]
                    y2 = self.serverMsg.body.ed[1]
                    painter.drawLine(x1, y1, x2, y2)

                elif self.serverMsg.isLine():
                    # 画直线
                    painter.setPen(QPen(self.serverMsg.foreColor, self.serverMsg.body.width, Qt.SolidLine))
                    print("draw line remote")
                    x1 = self.serverMsg.body.st[0]
                    y1 = self.serverMsg.body.st[1]
                    x2 = self.serverMsg.body.ed[0]
                    y2 = self.serverMsg.body.ed[1]
                    painter.drawLine(x1, y1, x2, y2)

                elif self.serverMsg.isCircle():
                    # 画圆
                    painter.setPen(QPen(self.serverMsg.foreColor, self.serverMsg.body.width, Qt.SolidLine))
                    print("draw circle remote")
                    x1 = self.serverMsg.body.st[0]
                    y1 = self.serverMsg.body.st[1]
                    x2 = self.serverMsg.body.ed[0]
                    y2 = self.serverMsg.body.ed[1]
                    painter.drawEllipse(x1, y1, x2 - x1, y2 - y1)

                elif self.serverMsg.isRect():
                    # 画矩形
                    painter.setPen(QPen(self.serverMsg.foreColor, self.serverMsg.body.width, Qt.SolidLine))
                    print("draw rec remote")
                    x1 = self.serverMsg.body.st[0]
                    y1 = self.serverMsg.body.st[1]
                    x2 = self.serverMsg.body.ed[0]
                    y2 = self.serverMsg.body.ed[1]
                    painter.drawRect(x1, y1, x2 - x1, y2 - y1)

                elif self.serverMsg.isText():
                    # 画文字
                    # 需要width参数，但画文字用不到，就设成本地的好了
                    painter.setPen(QPen(self.serverMsg.foreColor, self.width, Qt.SolidLine))
                    print("draw text remote")
                    x1 = self.serverMsg.body.pos[0]
                    y1 = self.serverMsg.body.pos[1]
                    painter.drawText(x1, y1, self.serverMsg.body.content)
                # TODO 清屏相关
                elif self.serverMsg.isCls():
                    # 清屏
                    pass

                self.isPaintFromMsg = False
            except Exception as e:
                print(e)


    def mousePressEvent(self, event: QMouseEvent):
        # 鼠标按下
        if event.button() == Qt.LeftButton:
            print("mouse pressed")
            self.x1 = event.x()
            self.y1 = event.y()
            self.x2 = self.x1
            self.y2 = self.y1
            self.isMouseDown = True
            self.isMouseUp = False
            self.doPaint()
            self.update()

    def mouseMoveEvent(self, event):
        if self.isMouseDown and (self.pData.isBrush() or self.pData.isEraser()):
            # 刷子事件需要更新鼠标平移的情况
            sleep(0.0001)
            self.x1 = self.x2
            self.y1 = self.y2
            self.x2 = event.x()
            self.y2 = event.y()
            self.doPaint()
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
            self.isMouseUp = True
            self.doPaint()
            self.update()

    def sendCReq(self, pData=None):
        if pData:
            cReq = CRequest.pData(pData)
        else:
            cReq = CRequest.pData(self.pData)
        self.conn.sendCReq(cReq)
        if not self.conn.isAlive:
            return
        print("sent", cReq)


    def paintFromMsg(self, pData: PData):
        self.isPaintFromMsg = True
        self.serverMsg = pData
        self.doPaint()
        self.update()


class WhiteBoardWindow(QMainWindow):
    def __init__(self, conn: ClientConn, id, callback):
        super().__init__()
        self.wb = WhiteBoardCanvas(self, conn)
        if conn is None:
            print("Offline mode!")
            self.initUi()
        else:
            self.initUi(conn.hostIp, id)
        self.callback = callback
        self.forceClosing = False

    def forceClose(self):
        print("board force close")
        self.forceClosing = True
        self.close()

    def closeEvent(self, event: QCloseEvent):
        print("board close")
        event.accept()
        if not self.forceClosing and self.callback:
            print("callback")
            self.callback()


    def initUi(self, ip='', id=''):
        self.resize(770, 570)
        self.setFixedSize(770, 570)

        # 设置画板
        self.wb.setGeometry(10, 50, 750, 501)
        # 橡皮
        self.eraser = QAction(QIcon(PATHTOERASER), "Eraser", self)
        self.eraser.setToolTip("Eraser")

        self.repaint = QAction(QIcon(PATHTOREPAINT), "repaint", self)
        self.repaint.setToolTip("repaint")

        self.color = QAction(QIcon(PATHTOCOLOR), "color", self)
        self.color.setToolTip("color")

        self.pen = QAction(QIcon(PATHTOPEN), "pen", self)
        self.pen.setToolTip("pen")

        self.Line = QAction(QIcon(PATHTOLINE), "Line", self)
        self.Line.setToolTip("Line")

        self.Circle = QAction(QIcon(PATHTOCIRCLE), "Circle", self)
        self.Circle.setToolTip("Circle")

        self.Rec = QAction(QIcon(PATHTOREC), "Rec", self)
        self.Rec.setToolTip("Rec")

        self.Text = QAction(QIcon(PATHTOTEXT), "Text", self)
        self.Text.setToolTip("Text")

        self.changeWidth = QAction(QIcon(PATHTOWIDTH), "Width", self)
        self.changeWidth.setToolTip("Width")


        #工具栏
        self.menubar = self.addToolBar("ToolBar")
        self.menubar.setMovable(False)
        self.menubar.addAction(self.eraser)
        self.menubar.addAction(self.color)
        self.menubar.addAction(self.pen)
        self.menubar.addAction(self.Line)
        self.menubar.addAction(self.Circle)
        self.menubar.addAction(self.Rec)
        self.menubar.addAction(self.Text)
        self.menubar.addAction(self.changeWidth)
        self.menubar.addAction(self.repaint)
        # 主页面
        self.setWindowTitle(f"Drawing Board {ip} - {id}")

        self.eraser.triggered.connect(self.setToEraser)
        self.color.triggered.connect(self.chooseColor)
        self.pen.triggered.connect(self.setToDot)
        self.Line.triggered.connect(self.setToLine)
        self.Circle.triggered.connect(self.setToCircle)
        self.Rec.triggered.connect(self.setToRec)
        self.Text.triggered.connect(self.trySetToText)
        self.changeWidth.triggered.connect(self.changewidth)
        self.repaint.triggered.connect(self.wb.Repaint)



        #默认点一下笔刷
        self.pen.trigger()
#TODO 处于选中状态的图标
    def setIcon(self):
        self.eraser = QAction(QIcon(PATHTOERASER), "Eraser", self)
        self.color = QAction(QIcon(PATHTOCOLOR), "color", self)
        self.pen = QAction(QIcon(PATHTOPEN), "pen", self)
        self.Line = QAction(QIcon(PATHTOLINE), "Line", self)
        self.Circle = QAction(QIcon(PATHTOCIRCLE), "Circle", self)
        self.Rec = QAction(QIcon(PATHTOREC), "Rec", self)
        self.Text = QAction(QIcon(PATHTOTEXT), "Text", self)
        self.changeWidth = QAction(QIcon(PATHTOWIDTH), "Width", self)


    def setToEraser(self):
        print(" ==== ")
        self.setIcon()
        self.eraser.setIcon(QIcon(PATHTOERASER2))
        self.wb.setToEraser()

    def setToDot(self):
        self.setIcon()
        self.pen = QAction(QIcon(PATHTOPEN2), "pen", self)
        self.wb.setToDot()

    def setToLine(self):
        self.setIcon()
        self.Line = QAction(QIcon(PATHTOLINE2), "Line", self)
        self.wb.setToLine()

    def setToCircle(self):
        self.setIcon()
        self.Circle = QAction(QIcon(PATHTOCIRCLE2), "Circle", self)
        self.wb.setToCircle()

    def setToRec(self):
        self.setIcon()
        self.Rec = QAction(QIcon(PATHTOREC2), "Rec", self)
        self.wb.setToRec()

    def chooseColor(self):
        self.setIcon()
        self.color = QAction(QIcon(PATHTOCOLOR2), "color", self)
        Color = QColorDialog.getColor()  # color是Qcolor
        if Color.isValid():
            self.wb.setForeColor(Color)

    def changewidth(self):
        self.setIcon()
        self.changeWidth = QAction(QIcon(PATHTOWIDTH2), "Width", self)
        width, okPressed = QInputDialog.getInt(self, '选择画笔粗细', '请输入粗细：', min=1, step=1)

        if okPressed:
            self.wb.width = width

    def trySetToText(self):
        self.setIcon()
        self.Text = QAction(QIcon(PATHTOTEXT2), "Text", self)
        text, okPressed = QInputDialog.getText(self, "Get text", "要共享的文字:")
        if okPressed and text != '':
            self.wb.text = text
            self.wb.setToText()



if __name__ == '__main__':
    app = QApplication([])
    WhiteBoardWindow(None, 1, None).show()
    app.exec()

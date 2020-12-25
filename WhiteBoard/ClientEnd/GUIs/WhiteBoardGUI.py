import sys
import os
from time import sleep

from PyQt5.QtWidgets import QMainWindow, QApplication,  QLineEdit, QInputDialog, QColorDialog, QLabel, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QColor, QBrush, QFont, QMouseEvent
from PyQt5.QtCore import Qt, QRect, QCoreApplication

from WhiteBoard.paintData import PData, PDataBrush, PDataShape, PDataEraser, Ctrl, PType, SType

RESOURCES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
PATHTOTEXT = os.path.join(RESOURCES, "text.png")
PATHTOREC = os.path.join(RESOURCES, "Rec.png")
PATHTOCIRCLE = os.path.join(RESOURCES, "Circle.png")
PATHTOLINE = os.path.join(RESOURCES, "Line.png")
PATHTOPEN = os.path.join(RESOURCES, "pen.png")
PATHTOERASER = os.path.join(RESOURCES, "eraser.png")
PATHTOCOLOR = os.path.join(RESOURCES, "color.png")
PATHTOWIDTH = os.path.join(RESOURCES, "changewidth.png")


class WhiteBoard(QLabel):
#TODO 窗体大小固定

    def __init__(self, parent):
        super(WhiteBoard, self).__init__(parent)
        self.pixmap = QPixmap(797, 597)  # 考虑边框的间距 减去px
        self.pixmap.fill(Qt.white)
        self.setStyleSheet("border: 2px solid white")
        self.foreColor = Qt.black  # pen color
        self.backColor = Qt.white
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.text = ""  # 这个是记录输入的文字
        self.width = 4  # pen width : default:4
        self.pData = PData(Ctrl.NOOP, PType.BRUSH, self.foreColor)
        self.isMouseDown = False
        self.isMouseUp = not self.isMouseDown

# TODO 图形预览，文本框预览


# 切换绘制类型
    def setToDot(self):
        print('set to brush')
        self.setCursor(Qt.CrossCursor)
        self.pData.setToBrush()

    def updateDotArgs(self):
        self.pData.updateArgs((self.x1, self.y1), (self.x2, self.y2), self.width)

    def setToLine(self):
        print('set to line')
        self.setCursor(Qt.CrossCursor)
        self.pData.setToShape(SType.LINE)

    def updateLineArgs(self):
        self.pData.updateArgs(SType.LINE, (self.x1, self.y1), (self.x2, self.y2), self.width)

    def setToCircle(self):
        print("set to circle")
        self.setCursor(Qt.CrossCursor)
        self.pData.setToShape(SType.CIRCLE)

    def updateCircleArgs(self):
        self.pData.updateArgs(SType.CIRCLE, (self.x1, self.y1), (self.x2, self.y2), self.width)

    def setToRec(self):
        print("set to rec")
        self.setCursor(Qt.CrossCursor)
        self.pData.setToShape(SType.RECT)

    def updateRecArgs(self):
        self.pData.updateArgs(SType.RECT, (self.x1, self.y1), (self.x2, self.y2), self.width)

    def setToText(self):
        print("set to text")
        self.setCursor(Qt.ArrowCursor)
        self.pData.setToText()

    def updateTextArgs(self):
        self.pData.updateArgs(self.text, (self.x1, self.y1))

    def setToEraser(self):
        #TODO 自定义鼠标形状（png）
        print("set to eraser")
        self.setCursor(Qt.CrossCursor)
        self.pData.setToEraser()

    def updateEraserArgs(self):
        self.pData.updateArgs((self.x1, self.y1), (self.x2, self.y2), self.width)

    def paintEvent(self, event):
        painter = QPainter(self.pixmap)
        if self.pData.isEraser():
            painter.setPen(QPen(self.backColor, self.width, Qt.SolidLine))
        else:
            painter.setPen(QPen(self.foreColor, self.width, Qt.SolidLine))

        print(self.x1, self.y1, self.x2, self.y2)
        #这里需要接受服务器的图形添加在客户端
        if (self.pData.isBrush() or self.pData.isEraser()) and self.isMouseDown:
            # 笔刷画点、橡皮，使用同一种画法
            if self.pData.isBrush():
                self.updateDotArgs()
                print("draw dot")
            else:
                self.updateEraserArgs()
                print("draw eraser")
            painter.drawLine(self.x1, self.y1, self.x2, self.y2)

        elif self.pData.isLine() and self.isMouseUp:
            # 画直线
            print("draw line")
            self.updateLineArgs()
            painter.drawLine(self.x1, self.y1, self.x2, self.y2)

        elif self.pData.isCircle() and self.isMouseUp:
            # 画圆
            print("draw circle")
            self.updateCircleArgs()
            painter.drawEllipse(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)

        elif self.pData.isRect() and self.isMouseUp:
            # 画矩形
            print("draw rec")
            self.updateRecArgs()
            painter.drawRect(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)

        elif self.pData.isText() and self.text != "" and self.isMouseDown:
            # 画文字
            print("draw text")
            self.updateTextArgs()
            painter.drawText(self.x1, self.y1,self.text)

        #TODO
        Label_painter = QPainter(self)
        Label_painter.drawPixmap(2, 2, self.pixmap)

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
            sleep(0.001)
            self.x1 = self.x2
            self.y1 = self.y2
            self.x2 = event.x()
            self.y2 = event.y()
            self.update()
        #TODO 其他图形的预览在这写


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


class WhiteBoardWindow(QMainWindow):
    def __init__(self):
        super(WhiteBoardWindow, self).__init__()
        self.initUi()

    def initUi(self):
        self.resize(800, 600)

        # 设置画板
        self.wb = WhiteBoard(self)
        self.wb.setGeometry(10, 10, 750, 501)
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
#TODO
        eraser.triggered.connect(self.wb.setToEraser)
        color.triggered.connect(self.chooseColor)
        pen.triggered.connect(self.wb.setToDot)
        Line.triggered.connect(self.wb.setToLine)
        Circle.triggered.connect(self.wb.setToCircle)
        Rec.triggered.connect(self.wb.setToRec)
        Text.triggered.connect(self.trySetToText)
        changeWidth.triggered.connect(self.changeWidth)

        #TODO 默认点一下笔刷

    def chooseColor(self):
        Color = QColorDialog.getColor()  # color是Qcolor
        if Color.isValid():
            self.wb.foreColor = Color

    def erase(self):
        self.clearTheSign()
        self.wb.isDrawDot = 1
        self.wb.color = Qt.white
        self.wb.width = self.wb.width

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



def startWhiteBoard():
    app = QApplication([])
    the_window = WhiteBoardWindow()
    the_window.show()
    app.exec_()


if __name__ == '__main__':
    startWhiteBoard()
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QLineEdit, QInputDialog, QFileDialog, \
    QColorDialog, QFontDialog, QLabel, QPushButton, QVBoxLayout, QStyle, QAction, QDialog, QFrame
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect, QCoreApplication
RESOURCES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
PATHTOTEXT = os.path.join(RESOURCES, "text.png")
PATHTOREC = os.path.join(RESOURCES, "Rec.png")
PATHTOCIRCLE = os.path.join(RESOURCES, "Circle.png")
PATHTOSTRAIGHTLINE = os.path.join(RESOURCES, "StraightLine.png")
PATHTOPEN = os.path.join(RESOURCES, "pen.png")
PATHTOERASER = os.path.join(RESOURCES, "eraser.png")
PATHTOCOLOR = os.path.join(RESOURCES, "color.png")

print(" === ",PATHTOCOLOR)
class mylable(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
#=======
#这里是记录绘制图形时的位置
    straightlineXBegin = 0
    straightlineYBegin = 0
    straightlineXEnd = 0
    straightlineYEnd = 0
    straightSign = 0
    text = ""#这个是记录输入的文字
#=======

#=======
#这里是判断执行绘制什么图形的信号
    isDrawStraightline = 0
    isDrawLine = 1
    isDrawCircle = 0
    isDrawRec = 0
    isDrawText = 0
    isAddFromOther = 0
#=======

#=======
#这个信号是用来控制画板防止重复绘制
    drawStraightline = 0
    drawCircle = 0
    drawRec = 0
    drawText = 0
#=======
    flag = False

    def __init__(self, parent):
        super(mylable, self).__init__(parent)
        self.pixmap = QPixmap(797, 597)  # 考虑边框的间距 减去px
        self.pixmap.fill(Qt.white)
        self.setStyleSheet("border: 2px solid white")
        self.Color = Qt.black  # pen color: defult:blue
        self.penwidth = 4  # pen width : default:4
        self.listX = []
        self.listY = []
        self.shape = 1

    def paintEvent(self, event):
        # super().paintEvent(event)

        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.Color, self.penwidth, Qt.SolidLine))
        #print(self.isDrawStraightline,self.drawStraightline)

        #这里需要接受服务器的图形添加在客户端

        if self.isDrawStraightline and self.drawStraightline:
            print("painter.drawLine(",self.straightlineXBegin, self.straightlineYBegin, self.straightlineXEnd, self.straightlineYEnd,")")
            painter.drawLine(self.straightlineXBegin, self.straightlineYBegin, self.straightlineXEnd, self.straightlineYEnd)
            self.drawStraightline = 0

        elif self.isDrawLine:
            painter.drawLine(self.x0, self.y0, self.x1, self.y1)

        elif self.isDrawCircle and self.drawCircle:
            painter.drawEllipse(self.straightlineXBegin, self.straightlineYBegin, self.straightlineXEnd - self.straightlineXBegin, self.straightlineYEnd - self.straightlineYBegin)
            self.drawCircle = 0

        elif self.isDrawRec and self.drawRec:
            painter.drawRect(self.straightlineXBegin, self.straightlineYBegin, self.straightlineXEnd - self.straightlineXBegin, self.straightlineYEnd - self.straightlineYBegin)
            self.drawRec = 0

        elif self.isDrawText and self.drawText:
            painter.drawText(self.straightlineXBegin, self.straightlineYBegin,self.text)
            self.drawText = 0

        Label_painter = QPainter(self)
        Label_painter.drawPixmap(2, 2, self.pixmap)

    def mousePressEvent(self, event):
        self.x1 = event.x()
        self.y1 = event.y()
        if self.straightSign == 0:
            self.straightlineXBegin = event.x()
            self.straightlineYBegin = event.y()
            print("self.straightlineXBegin: ", self.straightlineXBegin)
            print("self.straightlineYBegin: ",self.straightlineYBegin)

            self.straightSign = 1

        self.flag = True


    def mouseMoveEvent(self, event):

        if self.flag and self.shape == 1:
            self.x0 = self.x1
            self.y0 = self.y1
            self.x1 = event.x()
            self.y1 = event.y()
            self.listX.append(self.x1)
            self.listY.append(self.y1)
            #print("x1: " + str(self.x1))
            #print("y1: " + str(self.y1))
            self.update()


    def mouseReleaseEvent(self, event):
        self.straightlineXEnd = event.x()
        self.straightlineYEnd = event.y()
        self.straightSign = 0

        print("self.straightlineXEnd: ", self.straightlineXEnd)
        print("self.straightlineYEnd: ", self.straightlineYEnd)
        if self.isDrawStraightline:
            self.drawStraightline = 1
        elif self.isDrawCircle:
            self.drawCircle = 1
        elif self.isDrawRec:
            self.drawRec = 1
        elif self.isDrawText:
            self.drawText = 1

        self.update()
        self.flag = False


class WhiteBoard(QMainWindow):
    def __init__(self):
        super(WhiteBoard, self).__init__()
        self.initUi()

    def initUi(self):
        self.resize(800, 600)

        # 设置画板
        self.lb = mylable(self)
        self.lb.setGeometry(10, 10, 750, 501)
        # 橡皮
        eraser = QAction(QIcon(PATHTOERASER), "Eraser", self)
        eraser.setToolTip("Eraser")

        color = QAction(QIcon(PATHTOCOLOR), "color", self)
        color.setToolTip("color")

        pen = QAction(QIcon(PATHTOPEN), "pen", self)
        pen.setToolTip("pen")

        straightline = QAction(QIcon(PATHTOSTRAIGHTLINE), "straightline", self)
        straightline.setToolTip("straightline")

        Circle = QAction(QIcon(PATHTOCIRCLE), "Circle", self)
        Circle.setToolTip("Circle")

        Rec = QAction(QIcon(PATHTOREC), "Rec", self)
        Rec.setToolTip("Rec")

        Text = QAction(QIcon(PATHTOTEXT), "Text", self)
        Text.setToolTip("Text")


        #工具栏
        self.menubar = self.addToolBar("ToolBar")

        self.menubar.addAction(eraser)
        self.menubar.addAction(color)
        self.menubar.addAction(pen)
        self.menubar.addAction(straightline)
        self.menubar.addAction(Circle)
        self.menubar.addAction(Rec)
        self.menubar.addAction(Text)

        # 主页面
        self.setWindowIcon(QIcon("1216867.png"))
        self.setWindowTitle("Drawing Board")

        eraser.triggered.connect(self.erase)
        color.triggered.connect(self.chooseColor)
        pen.triggered.connect(self.drawLine)
        straightline.triggered.connect(self.drawStraightline)
        Circle.triggered.connect(self.drawCircle)
        Rec.triggered.connect(self.drawRec)
        Text.triggered.connect(self.drawText)

    def chooseColor(self):
        Color = QColorDialog.getColor()  # color是Qcolor
        if Color.isValid():
            self.lb.Color = Color

    def erase(self):
        self.clearTheSign()
        self.lb.isDrawLine = 1
        self.lb.Color = Qt.white
        self.lb.setCursor(Qt.CrossCursor)
        self.lb.penwidth = self.lb.penwidth

    def choose_width(self):
        width, ok = QInputDialog.getInt(self, '选择画笔粗细', '请输入粗细：', min=1, step=1)
        if ok:
            self.lb.penwidth = width

#=========
#这里是控制画板去绘制什么图形
    def drawLine(self):
        self.clearTheSign()
        self.lb.isDrawLine = 1
        self.lb.Color = Qt.black
        self.lb.setCursor(Qt.CrossCursor)
        self.lb.penwidth = self.lb.penwidth

    def drawStraightline(self):
        self.clearTheSign()
        self.lb.Color = Qt.black
        self.lb.isDrawStraightline = 1

    def drawCircle(self):
        self.clearTheSign()
        self.lb.Color = Qt.black
        self.lb.isDrawCircle = 1

    def drawRec(self):
        self.clearTheSign()
        self.lb.Color = Qt.black
        self.lb.isDrawRec = 1

    def drawText(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "请输入文字信息:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.lb.text = text
        self.lb.Color = Qt.black
        self.clearTheSign()
        self.lb.isDrawText = 1

#=========

    def clearTheSign(self): #这里是将原有的信号置为0，然后执行该函数之后在后面添加现有的信号
        self.lb.isDrawStraightline = 0
        self.lb.isDrawLine = 0
        self.lb.isDrawCircle = 0
        self.lb.isDrawRec = 0
        self.lb.isDrawText = 0

################################################
#######登录对话框
################################################
class logindialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('登录界面')
        self.resize(200, 200)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        ###### 设置界面控件
        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)

        ###### 绑定按钮事件
        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)





    def on_pushButton_enter_clicked(self):
        # 账号判断
        if self.lineEdit_account.text() == "":
            return

        # 密码判断
        if self.lineEdit_password.text() == "":
            return

        # 通过验证，关闭对话框并返回1
        self.accept()


###############################################
######显示用户界面
###############################################
class showMember(QMainWindow):
    def __init__(self):
        super(showMember, self).__init__()
        self.setWindowTitle('主界面')
        self.resize(400, 200)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        ###### 设置界面控件
        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.labelAccountHost = QLabel("Host: " + "111.111.11.11")
        self.verticalLayout.addWidget(self.labelAccountHost)

        self.labelAccountMember1 = QLabel("Member1: " + "111.111.11.12")
        self.verticalLayout.addWidget(self.labelAccountMember1)

        self.labelAccountMember2 = QLabel("Member2: " + "111.111.11.13")
        self.verticalLayout.addWidget(self.labelAccountMember2)


# class showMember(QDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setWindowTitle('主界面')
#         self.resize(400, 200)
#         self.setFixedSize(self.width(), self.height())
#         self.setWindowFlags(Qt.WindowCloseButtonHint)
#
#         ###### 设置界面控件
#         self.frame = QFrame(self)
#         self.verticalLayout = QVBoxLayout(self.frame)
#
#         self.labelAccountHost = QLabel("Host: " + "111.111.11.11")
#         self.verticalLayout.addWidget(self.labelAccountHost)
#
#         self.labelAccountMember1 = QLabel("Member1: " + "111.111.11.12")
#         self.verticalLayout.addWidget(self.labelAccountMember1)
#
#         self.labelAccountMember2 = QLabel("Member2: " + "111.111.11.13")
#         self.verticalLayout.addWidget(self.labelAccountMember2)
#
#         self.pushButton_enter = QPushButton()
#         self.pushButton_enter.setText("确定")
#         self.verticalLayout.addWidget(self.pushButton_enter)
#
#         self.pushButton_quit = QPushButton()
#         self.pushButton_quit.setText("取消")
#         self.verticalLayout.addWidget(self.pushButton_quit)
#
#         ###### 绑定按钮事件
#         self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
#         self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)



    def on_pushButton_enter_clicked(self):
        # 账号判断
        if self.lineEdit_account.text() == "":
            return

        # 密码判断
        if self.lineEdit_password.text() == "":
            return

        # 通过验证，关闭对话框并返回1
        self.accept()

def main():
    app = QApplication([])
    # dialog2 = showMember()
    # dialog = logindialog()

    # if dialog.exec_() == QDialog.Accepted:
    # dialog2 = showMember()
    the_window = WhiteBoard()

    # the_window2 = showMember()
    the_window.show()
    # the_window2.show()
    app.exec_()


if __name__ == '__main__':
    app = QApplication([])
    # dialog2 = showMember()
    #dialog = logindialog()

    #if dialog.exec_() == QDialog.Accepted:
        #dialog2 = showMember()
    the_window = WhiteBoard()

    #the_window2 = showMember()
    the_window.show()
    #the_window2.show()
    app.exec_()


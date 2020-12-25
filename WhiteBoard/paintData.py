from enum import Enum
from typing import Tuple

class Ctrl(Enum):
    """枚举类。
    控制位，0-无操作，1-撤销，2-重做"""
    NOOP = 0
    UNDO = 1
    REDO = 2

class PType(Enum):
    """绘制类型，0-刷子，1-形状，2-文字，3-橡皮"""
    BRUSH = 0
    SHAPE = 1
    TEXT = 2
    ERASER = 3

class SType(Enum):
    """形状类型，0-直线，1-矩形，2-圆，3-不适用（不是画形状）"""
    LINE = 0
    RECT = 1
    CIRCLE = 2
    NA = 3

class PData:
    """传输的数据结构，父类定义Header，子类定义Body"""
    def __init__(self, ctrl: Ctrl, pType: PType, color):
        """
        :param ctrl: 控制位，0-无操作，1-撤销，2-重做 TODO
        :param pType: 绘制类型，0-刷子，1-形状，2-文字，3-橡皮
        :param color: 颜色
        """
        # Header
        self.ctrl = ctrl
        self.pType = pType
        self.color = color

        # Body
        self.data = None

    def setToBrush(self):
        self.pType = PType.BRUSH

    def isBrush(self):
        return self.pType == PType.BRUSH

    def setToShape(self, sType: SType):
        self.pType = PType.SHAPE
        self.updateArgs(sType)

    def isLine(self):
        return self.pType == PType.SHAPE and self.data.sType == SType.LINE

    def isRect(self):
        return self.pType == PType.SHAPE and self.data.sType == SType.RECT

    def isCircle(self):
        return self.pType == PType.SHAPE and self.data.sType == SType.CIRCLE

    def setToText(self):
        self.pType = PType.TEXT

    def isText(self):
        return self.pType == PType.TEXT

    def setToEraser(self):
        self.pType = PType.ERASER

    def isEraser(self):
        return self.pType == PType.ERASER

    def updateArgs(self, *args):
        '''
        if PType.BRUSH:
            args: st, ed, width
        elif PType.SHAPE:
            args: sType, st, ed, width
        elif PType.TEXT:
            args: content, pos
        elif PType.ERASER:
            args: st, ed, width
        '''
        if self.pType == PType.BRUSH:
            self.data = PDataBrush(*args)
        elif self.pType == PType.SHAPE:
            self.data = PDataShape(*args)
        elif self.pType == PType.TEXT:
            self.data = PDataText(*args)
        elif self.pType == PType.ERASER:
            self.data = PDataEraser(*args)


class PDataBrush:
    """刷子类型的数据结构"""
    def __init__(self, st: Tuple, ed: Tuple, width):
        """
        :param st: 起点坐标
        :param ed: 终点坐标
        :param width: 笔刷粗细
        """
        self.st = st
        self.ed = ed
        self.width = width


class PDataShape:
    """形状类型的数据结构"""
    def __init__(self, sType: SType, st: Tuple=None, ed: Tuple=None, width=10):
        """
        :param sType: 形状类型，0-直线，1-矩形，2-圆
        :param st: 起点
        :param ed: 终点
        :param width: 笔刷粗细
        """
        # TODO
        self.sType = sType
        # ...
        pass

class PDataText:
    """文字类型的数据结构"""
    # TODO 字体、字号默认值
    def __init__(self, content: str, pos: Tuple):
        """
        :param content: 文本内容
        :param pos: 位置
        """
        # TODO

        pass

class PDataEraser:
    """橡皮类型的数据结构"""
    def __init__(self, st: Tuple, ed: Tuple, width):
        """
        :param st: 起点坐标
        :param ed: 终点坐标
        :param width: 橡皮笔刷粗细
        """
        self.st = st
        self.ed = ed
        self.width = width
from enum import Enum

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
    """形状类型，0-直线，1-矩形，2-圆"""
    LINE = 0
    RECT = 1
    CIRCLE = 2

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        self.body = {}

class PDataBrush(PData):
    """刷子类型的数据结构"""
    # TODO thickness默认值
    def __init__(self, ctrl, pType, color, pos: Point, thickness=10):
        """
        :param pos: 像素点坐标
        :param thickness: 像素点粗细
        """
        super().__init__(ctrl, pType, color)
        self.body['pos'] = pos
        self.body['thickness'] = thickness


class PDataShape(PData):
    """形状类型的数据结构"""
    def __init__(self, ctrl, pType, color, sType: SType, st: Point, ed: Point, isHolding: bool, thickness=10):
        """
        :param sType: 形状类型，0-直线，1-矩形，2-圆
        :param st: 起点
        :param ed: 终点
        :param isHolding: 是否按住鼠标左键
        :param thickness: 粗细
        """
        super().__init__(ctrl, pType, color)
        # TODO
        self.body['sType'] = sType
        # ...
        pass

class PDataText(PData):
    """文字类型的数据结构"""
    # TODO 字体、字号默认值
    def __init__(self, ctrl, pType, color, content: str, pos: Point, fSize, font):
        """
        :param content: 文本内容
        :param pos: 位置
        :param fSize: font size, 字号
        :param font: 字体
        """
        super().__init__(ctrl, pType, color)
        # TODO

        pass

class PDataEraser(PData):
    """橡皮类型的数据结构"""
    # TODO
    pass
from enum import Enum
from typing import Tuple, TypeVar, Type

ENCODING = 'utf8'

class PType(Enum):
    """绘制类型，0-刷子，1-形状，2-文字，3-橡皮"""
    BRUSH = 0
    SHAPE = 1
    TEXT = 2
    ERASER = 3
    def __str__(self):
        return str(self.value)

class SType(Enum):
    """形状类型，0-直线，1-矩形，2-圆，3-不适用（不是画形状）"""
    LINE = 0
    RECT = 1
    CIRCLE = 2
    NA = 3
    def __str__(self):
        return str(self.value)

TPDataBody = TypeVar('TPDataBody', bound='PDataBody')
TPData = TypeVar('TPData', bound='PData')

class PData:
    """传输的数据结构"""
    SEP = '_'
    def __init__(self, pType: PType, color: int, body:Type[TPDataBody]=None):
        """
        :param pType: 绘制类型，0-刷子，1-形状，2-文字，3-橡皮
        :param color: 颜色
        """
        # Header
        self.pType = pType
        self.color = color

        # Body
        self.body = body

    def __str__(self):
        # 转为字符串
        l = [str(self.pType), str(self.color), str(self.body)]
        return PData.SEP.join(l)

    @staticmethod
    def decodeFromStr(pdata: str)-> TPData:
        l = pdata.split(PData.SEP)
        pType = PType(int(l[0]))
        color = int(l[1])
        body = None
        if pType == PType.BRUSH:
            body = PDataBrush.decodeFromStr(l[2])
        elif pType == PType.SHAPE:
            body = PDataShape.decodeFromStr(l[2])
        elif pType == PType.TEXT:
            body = PDataText.decodeFromStr(l[2])
        elif pType == PType.ERASER:
            body = PDataEraser.decodeFromStr(l[2])
            
        return PData(pType, color, body)

    def setToBrush(self):
        self.pType = PType.BRUSH

    def isBrush(self):
        return self.pType == PType.BRUSH

    def setToShape(self, sType: SType):
        self.pType = PType.SHAPE
        self.updateArgs(sType)

    def isLine(self):
        return self.pType == PType.SHAPE and self.body.sType == SType.LINE

    def isRect(self):
        return self.pType == PType.SHAPE and self.body.sType == SType.RECT

    def isCircle(self):
        return self.pType == PType.SHAPE and self.body.sType == SType.CIRCLE

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
            self.body = PDataBrush(*args)
        elif self.pType == PType.SHAPE:
            self.body = PDataShape(*args)
        elif self.pType == PType.TEXT:
            self.body = PDataText(*args)
        elif self.pType == PType.ERASER:
            self.body = PDataEraser(*args)

class PDataBody:
    """传输的数据结构的body部分"""
    SEP = '^'
    def __str__(self):
        pass

class PDataBrush(PDataBody):
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

    def __str__(self):
        l = [str(self.st[0]), str(self.st[1]), str(self.ed[0]), str(self.ed[1]), str(self.width)]
        return PDataBody.SEP.join(l)

    @staticmethod
    def decodeFromStr(body: str) -> TPDataBody:
        l = body.split(PDataBody.SEP)
        st = (int(l[0]), int(l[1]))
        ed = (int(l[2]), int(l[3]))
        width = int(l[4])
        return PDataBrush(st, ed, width)

class PDataShape(PDataBody):
    """形状类型的数据结构"""
    def __init__(self, sType: SType, st: Tuple=None, ed: Tuple=None, width=None):
        """
        :param sType: 形状类型，0-直线，1-矩形，2-圆
        :param st: 起点
        :param ed: 终点
        :param width: 笔刷粗细
        """
        self.sType = sType
        self.st = st
        self.ed = ed
        self.width = width
        
    def __str__(self):
        l = [str(self.sType), str(self.st[0]), str(self.st[1]), str(self.ed[0]), str(self.ed[1]), str(self.width)]
        return PDataBody.SEP.join(l)

    @staticmethod
    def decodeFromStr(body: str) -> TPDataBody:
        l = body.split(PDataBody.SEP)
        sType = SType(int(l[0]))
        st = (int(l[1]), int(l[2]))
        ed = (int(l[3]), int(l[4]))
        width = int(l[5])
        return PDataShape(sType, st, ed, width)

class PDataText(PDataBody):
    """文字类型的数据结构"""
    def __init__(self, content: str, pos: Tuple):
        """
        :param content: 文本内容
        :param pos: 位置
        """
        self.content = content
        self.pos = pos
        
    def __str__(self):
        l = [self.content, str(self.pos[0]), str(self.pos[1])]
        return PDataText.SEP.join(l)
    
    @staticmethod
    def decodeFromStr(body: str) -> TPDataBody:
        l = body.split(PDataBody.SEP)
        content = l[0]
        pos = (int(l[1]), int(l[2]))
        return PDataText(content, pos)

class PDataEraser(PDataBody):
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
    
    def __str__(self):
        l = [str(self.st[0]), str(self.st[1]), str(self.ed[0]), str(self.ed[1]), str(self.width)]
        return PDataBody.SEP.join(l)

    @staticmethod
    def decodeFromStr(body: str) -> TPDataBody:
        l = body.split(PDataBody.SEP)
        st = (int(l[0]), int(l[1]))
        ed = (int(l[2]), int(l[3]))
        width = int(l[4])
        return PDataEraser(st, ed, width)
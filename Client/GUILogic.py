# @Author : ZZJ, CJY
# GUI界面背后的处理逻辑，被GUI调用

from Client.Conn import Conn
from PaintData import Ctrl, PType, SType, Point, PDataBrush, PDataShape, PDataText, PData


def loginHandler(conn: Conn, serverIP: str) -> bool:
    """处理登录逻辑，返回登陆是否成功"""
    conn.setServerIP(serverIP)
    # 登录
    return conn.login()

# TODO
def onShareStartHandler():
    """处理“开始共享”按钮点击事件。点击后 1. 按钮变为“结束共享”；2.弹出白板界面"""
    pass

# TODO
def onShareEndHandler():
    """处理“结束共享”按钮点击事件。点击后 按钮变为“开始共享”"""
    pass

# TODO
def onExitHandler():
    pass

# TODO 待完善
def onPaintHandler(conn:Conn, pType: PType, color, *bodyArgs):
    """在白板上发生了绘制动作，1.在canvas上画出对应形状；2.生成对应数据发送给server

    if pType == BRUSH:
        bodyArgs: (pos: Point, thickness=10)
    elif pType == SHAPE:
        bodyArgs: (sType: SType, startPoint: Point, endPoint: Point, isHolding: bool, thickness=10)
    elif pType == TEXT:
        bodyArgs: (content: str, pos: Point, fSize, font)
    """
    # 生成数据
    pData = makePData(pType, color, *bodyArgs)
    # 本地画形状
    drawObject(pData)
    # 发送
    # TODO 错误处理
    conn.sendData(pData)

#TODO 待完善
def drawObject(pData: PData):
    """根据pData计算出画该物体所需的参数，并在canvas上渲染对应形状"""
    if pData.pType == PType.BRUSH:
        drawDot(pData.body['pos'], pData.body['thickness'])
    elif pData.pType == PType.SHAPE:
        sType = pData.body['sType']
        st = pData.body['st']
        ed = pData.body['ed']
        isHolding = pData.body['isHolding']
        thickness = pData.body['thickness']
        # TODO 计算所需参数
        if sType == SType.LINE:
            pass
        elif sType == SType.RECT:
            pass
        elif sType == SType.CIRCLE:
            pass
        else:
            raise ValueError(f"Wrong sType {sType}!")
    elif pData.pType == PType.TEXT:
        drawText(pData.body['content'], pData.body['pos'], pData.body['fSize'], pData.body['font'])
    else:
        raise ValueError(f"Wrong pType {pType}!")

    renderObject()

#TODO
def drawDot(pos, thickness):
    pass
#TODO
def drawLine():
    pass
#TODO
def drawRect():
    pass
#TODO
def drawCircle():
    pass
#TODO
def drawText(content:str, pos: Point, fSize, font):
    pass
#TODO
def renderObject():
    pass

def makePData(pType: PType, color, *bodyArgs):
    """生成PData对象"""
    ctrl = Ctrl.NOOP  # 无操作
    pData = None
    if pType == PType.BRUSH:
        # 生成刷子类型的数据
        pData = PDataBrush(ctrl, pType, color, *bodyArgs)
    elif pType == PType.SHAPE:
        # 生成形状类型的数据
        pData = PDataShape(ctrl, pType, color, *bodyArgs)
    elif pType == PType.TEXT:
        # 生成文本类型的数据
        pData = PDataText(ctrl, pType, color, *bodyArgs)
    else:
        raise ValueError(f"Not support value of pType {pType}")
    return pData

# TODO 怎么配合conn.recvData使用
def onRecvDataHandler(pData: PData):
    """处理来自服务器的数据。控制信号和绘制物体分别处理"""
    if pData.ctrl == Ctrl.UNDO:
        undoHandler()
    elif pData.ctrl == Ctrl.REDO:
        redoHandler()
    elif pData.ctrl == Ctrl.NOOP:
        drawObject(pData)

# TODO 怎么实现？数据列表？与server转发数据代码配合。
def undoHandler():
    """处理撤销信号"""
    pass

def redoHandler():
    """处理重做信号"""
    pass

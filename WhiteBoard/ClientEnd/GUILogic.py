# @Author : ZZJ, CJY
# GUI界面背后的处理逻辑，被GUI调用

from ClientEnd.ClientConn import ClientConn
from WhiteBoard.paintData import Ctrl, PType, SType, PDataBrush, PDataShape, PDataText, PData


# ----------------- 主界面相关 --------------------
#TODO 要修改PData的Header了，同时recvData函数也要修改处理逻辑
def getMemberList(conn):
    """获取在线成员列表"""
    pass

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
# ----------------- 主界面相关 --------------------

# ----------------- 白板界面相关 --------------------
#TODO 注意不要把远程收到的绘制动作当成本地绘制的再发给服务器了。

# TODO eraser: find_overlapping函数，tag

# TODO 待完善
def onLocalDrawHandler(conn:ClientConn, pType: PType, color, *bodyArgs):
    """本地在白板上发生了绘制动作，1.在canvas上渲染对应形状；2.生成对应数据发送给server

    if pType == BRUSH:
        bodyArgs: (pos: Point, thickness=10)
    elif pType == SHAPE:
        bodyArgs: (sType: SType, startPoint: Point, endPoint: Point, isHolding: bool, thickness=10)
    elif pType == TEXT:
        bodyArgs: (content: str, pos: Point, fSize, font)
    """
    # 生成数据
    pData = makePData(pType, color, *bodyArgs)
    # 本地画形状并渲染
    drawObject(pData)
    renderObject()
    # 发送给服务器
    # TODO send发生错误的处理
    conn.sendData(pData)

#TODO 待完善
def drawObject(pData: PData):
    """根据本地或远端的pData计算出画该物体所需的参数，并在canvas上渲染对应形状"""
    if pData.pType == PType.BRUSH:
        drawDot(pData.body['pos'], pData.body['thickness'])
    elif pData.pType == PType.SHAPE:
        sType = pData.body['sType']
        st = pData.body['st']
        ed = pData.body['ed']
        isHolding = pData.body['isHolding']
        thickness = pData.body['thickness']
        # TODO 计算所需参数，然后调用对应的draw函数
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
        raise ValueError(f"Wrong pType {pData.pType}!")

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

# TODO 怎么实现？数据列表？与server转发数据代码配合。
def undoHandler():
    """处理撤销信号"""
    pass

def redoHandler():
    """处理重做信号"""
    pass

#TODO
def renderObject():
    pass
# ----------------- 白板界面相关 --------------------

# ----------------- 后台逻辑相关 --------------------
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

# TODO 怎么配合conn.recvData使用；以及错误处理
def onRecvDataHandler(pData: PData):
    """处理来自服务器的数据。控制信号和绘制物体分别处理"""
    #TODO 还没有点“开始共享”，白板窗体还没显示时怎么处理。
    if pData.ctrl == Ctrl.UNDO:
        undoHandler()
    elif pData.ctrl == Ctrl.REDO:
        redoHandler()
    elif pData.ctrl == Ctrl.NOOP:
        drawObject(pData)


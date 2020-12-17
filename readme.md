## 编程语言：Python 3.6

## 相关库

### tkinter（GUI）

https://docs.python.org/zh-cn/3.9/library/tkinter.html

https://cloud.tencent.com/developer/section/1372347

### PyQt5（另一个GUI）
https://doc.qt.io/

https://doc.qt.io/qt-5/gettingstarted.html

### Qpainter（来自PyQt5）

`from PyQt5.QtGui import QPainter`

https://doc.qt.io/qt-5/qpainter.html

### turtle 

https://docs.python.org/zh-cn/3/library/turtle.html

https://cloud.tencent.com/developer/section/1372423

### socket

https://docs.python.org/zh-cn/3.6/library/socket.html

### socketserver

https://docs.python.org/zh-cn/3.6/library/socketserver.html#module-socketserver



## 界面设计（/文档/GUIx_xxx.png）

<img src="./文档/GUI_1登录.png" alt="登录" style="zoom: 40%;" />
<img src="./文档/GUI_2主界面.png" alt="主界面" style="zoom:40%;" />
<img src="./文档/GUI_3白板.png" alt="白板" style="zoom: 40%;" />

## 业务逻辑（/文档/业务逻辑.jpg）
<img src="./文档/业务逻辑.jpg" alt="业务逻辑" style="zoom:90%;" />

## 结构介绍

### 协议设计
> 共同讨论得出

/PaintData.py : 应用层的协议设计，要传的数据结构的定义。

### 客户端 /Client/*
> zzj

/Client/Clinet.py : 客户端主逻辑代码，负责显示各种GUI界面、使用各个模块的功能。

> xkl, zyl

/Client/Conn.py : 连接服务器的类，封装socket。主要有`login`，`sendData`，`recvData`等函数。

> cjy

/Client/GUI.py : 设计客户端的各个界面，在Client.py中调用。

> cjy, zzj

/Client/GUILogic.py : GUI界面背后的处理逻辑代码，被GUI调用。

### 服务端 /Server/*

> xkl, zyl

/Server/Conn.py : 连接客户端的类，封装socketserver。

> xkl, zyl

/Server/Server.py : 服务端主逻辑代码。处理登录、转发数据等。

## enum枚举类用法
https://docs.python.org/3/library/enum.html
```python
from enum import Enum

class Color(Enum):
    YELLOW = 1
    BLUE = 2

def f(color: Color):
    print(color)
f(Color.BLUE) # 输出 Color.BLUE

Color.BLUE.value # 2
Color.BLUE.name # 'BLUE'
Color(2) # <color.BLUE: 2>
Color['BLUE'] # <color.BLUE: 2>
```

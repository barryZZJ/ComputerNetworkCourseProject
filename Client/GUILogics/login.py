# @Author : ZZJ, CJY
# GUI界面背后的处理逻辑，被GUI调用

import re
from Client.Conn import Conn

# 登录界面相关
def loginButHandler(conn: Conn, serverIP: str, serverPort: str):
    """处理登录逻辑，登陆成功后关闭登陆界面，进入主界面。"""

    # 验证IP地址是否合法
    if not validIp(serverIP):
        # TODO 温和的处理方法
        raise ValueError(f"Invalid IP address: {serverIP}")
    conn.setServerIP(serverIP)

    # 验证端口号是否合法
    if not validPort(serverPort):
        # TODO 温和的处理方法
        raise ValueError(f"Invalid port: {serverPort}")
    conn.setServerPort(serverPort)

    # 登录
    res = conn.login()
    #TODO 处理不同res的情况
    if res:
        #TODO 关闭登陆页面
        #TODO 打开主界面
        return 0
    else:
        return -1

def validIp(ip: str) -> bool:
    """检查IP地址是否合法"""
    pattern = r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$'
    return re.match(pattern, ip) is None

def validPort(port: str) -> bool:
    """检查port是否合法"""
    # 0~65535
    return port.isnumeric() and 0<=int(port)<=65535
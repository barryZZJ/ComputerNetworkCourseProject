# @Author : ZZJ

from Client.Conn import Conn

def loginHandler(conn: Conn, serverIP: str) -> bool:
    """处理登录逻辑，返回登陆是否成功"""
    conn.setServerIP(serverIP)

    # 登录
    return conn.login()


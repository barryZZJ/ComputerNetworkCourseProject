import socketserver

# TODO 用昵称（或分配一个id）识别不同主机，用于转发时的识别，客户端发现 昵称/id 与自己相同则不画。

class Conn:
    """连接客户端的类，封装socketserver"""
    # Hint: 可以看一下help(socketserver)
    # 可以用多线程或线程池，以支持多个socket
    def __init__(self):
        pass

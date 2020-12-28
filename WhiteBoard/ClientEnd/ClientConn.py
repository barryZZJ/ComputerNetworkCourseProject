import socket

from WhiteBoard.controlData import CRequest, CResponse

class ClientConn(socket.socket):
    """连接服务器的类，封装socket"""
    # Hint: 可以看一下help(socket)
    _poll_all_users_interval = 500

    def __init__(self):
        socket.socket.__init__(self) # create tcp/ip socket
        self.isAlive = False
        self.serverIp = None
        self.serverPort = None

    def initConn(self, ip, port):
        """连接服务器，返回是否成功"""
        try:
            self.connect((ip, port))
        except socket.error as e:
            print("Error:", e)
            return False

        self.isAlive = True
        self.serverIp = ip
        self.serverPort = port
        print(f"connected to server at {self.serverIp}:{self.serverPort}")
        return True

    @property
    def hostIp(self):
        # 获取本机IP
        return self.getsockname()[0]

    def disconnect(self):
        try:
            self.sendall(CRequest.disconnect().encode())
        except ConnectionError:
            pass
        self.shutdown(socket.SHUT_RDWR)
        self.close()
        self.isAlive = False

    def sendCReq(self, cReq: CRequest):
        cDataBytes = cReq.encode()
        try:
            self.sendall(cDataBytes)
            print("sent", cReq.print())
        except ConnectionError:
            print("send error")
            print("connection to server is unavailable, closing program...")
            self.shutdown(socket.SHUT_RDWR)
            self.close()
            self.isAlive = False


    def recvCResp(self) -> CResponse:
        # 一次接收一个CResp
        data = self.recv(CResponse.HEADER_LEN)
        cResp = CResponse.decodeHeader(data)
        data = self.recv(cResp.bodyLen)
        cResp.decodeBody(data)
        print("receive raw", cResp)
        return cResp


import json
from builtins import bytes
from enum import Enum, auto

from WhiteBoard.paintData import PData

ENCODING = 'utf8'
CSEP = ''

class CType(Enum):
    ID = 0 # 用户的ID
    USERINFOS = 1 # 在线用户信息
    PDATA = 2 # 画图数据
    DISCONNECT = 3 # 断开连接
    NOOP = 4 # 不可用

    def __str__(self):
        """The value of the Enum member."""
        return str(self.value)

    def __bytes__(self):
        return str(self.value).encode(ENCODING)

    def print(self):
        # 输出debug信息用
        return f"CType.{self.name}"


class CRequest:
    HEADER_LEN = 4
    def __init__(self, ctype=None, bodyLen=None, body=None):
        # header
        self.ctype = ctype # 1 byte
        self.bodyLen = bodyLen # 3 byte
        # body
        self.body = body
    
    def print(self):
        # 输出debug信息用
        if self.ctype == CType.PDATA:
            if type(self.body) == bytes:
                body = PData.decodeFromStr(self.body.decode(ENCODING))
            else:
                body = self.body.print()
        else:
            body = ''
        return f"{self.ctype.print()} {body}"

    @staticmethod
    def mkRequest(ctype, body=None):
        if body:
            bodyLen = '%03d' % len(str(body))
        else:
            bodyLen =  '000'
        return CRequest(ctype, bodyLen, body)

    @staticmethod
    def pData(pData: PData):
        return CRequest.mkRequest(CType.PDATA, pData)

    @staticmethod
    def disconnect():
        ctype = CType.DISCONNECT
        return CRequest.mkRequest(ctype)

    def __str__(self):
        # bodyLen 占 3 位
        l = [str(self.ctype), str(self.bodyLen), str(self.body) if self.body else '']
        return CSEP.join(l)

    def encode(self) -> bytes:
        return str(self).encode(ENCODING)

    @staticmethod
    def decodeHeader(headers: bytes):
        l = headers.decode(ENCODING)
        type = CType(int(l[0]))
        bodyLen = int(l[1:CResponse.HEADER_LEN])
        return CRequest(type, bodyLen=bodyLen)

    def decodeBody(self, bodyData):
        self.body = bodyData
        return self

class CResponse:
    HEADER_LEN = 4
    def __init__(self, ctype=None, bodyLen=None, body:str=None):
        # header
        self.ctype = ctype  # 1 byte
        self.bodyLen = bodyLen  # 3 byte
        # body
        self.body = body

    def print(self):
        # 输出debug信息用

        if self.ctype == CType.PDATA:
            if type(self.body) == str:
                body = PData.decodeFromStr(self.body).print()
            elif type(self.body) == PData:
                body = self.body.print()
        elif self.ctype == CType.ID:
            body = self.body
        elif self.ctype == CType.USERINFOS:
            body = self.body
        else:
            body = ''

        return f"{self.ctype.print()} {body}"

    @staticmethod
    def mkResponse(ctype: CType, body: str):
        if body:
            bodyLen = '%03d' % len(str(body))
        else:
            bodyLen = '000'
        return CResponse(ctype, bodyLen, body)

    @staticmethod
    def id(id: int):
        # 每当新用户连接时，发送给该用户
        return CResponse.mkResponse(CType.ID, str(id))

    @staticmethod
    def userInfos(usersdict: dict):
        # 每当新用户连接时或有用户断开时，发送给所有用户
        return CResponse.mkResponse(CType.USERINFOS, json.dumps(usersdict))

    @staticmethod
    def pData(pDataBytes: bytes):
        return CResponse.mkResponse(CType.PDATA, pDataBytes.decode(ENCODING))

    def __str__(self):
        l = [str(self.ctype), str(self.bodyLen), str(self.body)]
        return CSEP.join(l)

    def encode(self) -> bytes:
        return str(self).encode(ENCODING)

    @staticmethod
    def decodeHeader(headers: bytes):
        l = headers.decode(ENCODING)
        type = CType(int(l[0]))
        bodyLen = int(l[1:CResponse.HEADER_LEN])
        return CResponse(type, bodyLen=bodyLen)

    def decodeBody(self, bodyDataBytes: bytes):
        bodyData = bodyDataBytes.decode(ENCODING)
        if self.ctype == CType.PDATA:
            self.body = PData.decodeFromStr(bodyData)
        elif self.ctype == CType.ID:
            self.body = bodyData
        elif self.ctype == CType.USERINFOS:
            self.body = json.loads(bodyData)
        return self


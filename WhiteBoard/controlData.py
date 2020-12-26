import json
from builtins import bytes
from enum import Enum, auto

from WhiteBoard.paintData import PData

ENCODING = 'utf8'
CSEP = ';'

class CType(Enum):
    ID = auto() # 用户的ID
    USERINFOS = auto() # 所有用户
    PDATA = auto() # 画图数据
    DISCONNECT = auto() # 断开连接

    def __str__(self):
        """The value of the Enum member."""
        return str(self.value)

    def __bytes__(self):
        return str(self.value).encode(ENCODING)


class CRequest:
    def __init__(self, ctype=None, body=None):
        self.ctype = ctype
        self.body = body

    def pData(self, pData: PData):
        self.ctype = CType.PDATA
        self.body = pData
        return self

    def disconnect(self):
        self.ctype = CType.DISCONNECT
        return self

    def __str__(self):
        l = [str(self.ctype), '' if self.body is None else str(self.body)]
        return CSEP.join(l)

    def encode(self) -> bytes:
        return str(self).encode(ENCODING)

    @staticmethod
    def decode(cdata: bytes):
        l = cdata.decode(ENCODING).split(CSEP)
        type = CType(int(l[0]))
        bodystr = None
        if l[1] != '':
            bodystr = l[1]
        return CRequest(type, bodystr)

class CResponse:
    def __init__(self, ctype=None, contents=None):
        self.ctype = ctype
        self.contents = contents

    def mkResponse(self, type: CType, contents: str):
        self.ctype = type
        self.contents = contents
        return self

    def id(self, id: int):
        # 每当新用户连接时，发送给该用户
        return self.mkResponse(CType.ID, str(id))

    def userInfos(self, usersdict: dict):
        # 每当新用户连接时或有用户断开时，发送给所有用户
        return self.mkResponse(CType.USERINFOS, json.dumps(usersdict))

    def pData(self, pData:PData):
        return self.mkResponse(CType.PDATA, str(pData))

    def __str__(self):
        data = []
        data.append(str(self.ctype))
        data.append(self.contents)
        return CSEP.join(data)

    def encode(self) -> bytes:
        return str(self).encode(ENCODING)

    @staticmethod
    def decode(cdata: bytes):
        type, contents = cdata.decode(ENCODING).split(CSEP)
        type = CType(int(type))
        return CResponse(type, contents)

    def transToPData(self) -> PData:
        return PData.decodeFromStr(self.contents)

    def transToId(self):
        return self.contents

    def transToUserInfoDict(self) -> dict:
        userinfos = json.loads(self.contents)
        return userinfos

if __name__ == '__main__':

    pass


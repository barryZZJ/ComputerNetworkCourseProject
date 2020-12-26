import json
from builtins import bytes
from enum import Enum, auto
from types import DynamicClassAttribute

#! 使用request - response模式，客户端发送请求，服务器返回相应

ENCODING = 'utf8'
SEP = ';'

class CType(Enum):
    ID = auto() # 用户的ID
    ALL_USERINFOS = auto() # 所有用户
    PDATA = auto() # 画图数据
    DISCONNECT = auto() # 断开连接

    @DynamicClassAttribute
    def value(self):
        """The value of the Enum member."""
        return str(self._value_)

    def __bytes__(self):
        return bytes(self.value, ENCODING)


class PRequest:
    def __init__(self):
        self.type = None

    def id(self):
        self.type = CType.ID
        return self

    def allUsers(self):
        self.type = CType.ALL_USERINFOS
        return self

    def disconnect(self):
        self.type = CType.DISCONNECT
        return self

    def encode(self):
        data = bytes(self.type)
        return data

    def decode(self, data: bytes):
        type = data.decode(ENCODING)
        self.type = CType(int(type))
        return self


class PResponse:
    def __init__(self):
        self.type = None
        self.contents = None

    def mkResponse(self, type: CType, contents: str):
        self.type = type
        self.contents = contents
        return self

    def id(self, id: int):
        return self.mkResponse(CType.ID, str(id))

    def allUsers(self, usersdict: dict):
        return self.mkResponse(CType.ALL_USERINFOS, json.dumps(usersdict))

    def encode(self):
        data = []
        data.append(self.type.value)
        data.append(self.contents)
        return SEP.join(data).encode(ENCODING)

    def decode(self, data: bytes):
        type, self.contents = data.decode(ENCODING).split(SEP)
        self.type = CType(int(type))
        return self

    def transToId(self):
        return self.contents

    def transToUserInfoDict(self) -> dict:
        userinfos = json.loads(self.contents)
        return userinfos

if __name__ == '__main__':

    pass


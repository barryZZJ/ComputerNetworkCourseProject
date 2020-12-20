from builtins import bytes
from enum import Enum
from typing import Tuple
from types import DynamicClassAttribute


encoding = 'utf8'
sep = ' ' # 分隔符

class Type(Enum):
    ID = 0 # 用户的ID
    DISCONNECT = 1 # 断开连接
    PDATA = 2 #

    @DynamicClassAttribute
    def value(self):
        """The value of the Enum member."""
        return str(self._value_)

    def __bytes__(self):
        return bytes(self.value, encoding)


class pRequest:
    def __init__(self):
        self.type = None

    def id(self):
        self.type = Type.ID
        return self

    def disconnect(self):
        self.type = Type.DISCONNECT
        return self

    def encode(self):
        data = bytes(self.type)
        return data

    @staticmethod
    def decode(data: bytes) -> Type:
        type = data.decode(encoding)
        type = Type(int(type))
        return type


class pResponse:
    def __init__(self):
        self.type = None
        self.content = None

    def respond(self, type: Type, content: str):
        self.type = type
        self.content = content
        return self

    def makeId(self, id: int):
        return self.respond(Type.ID, str(id))

    def encode(self):
        data = []
        data.append(self.type.value)
        data.append(self.content)
        return sep.join(data).encode(encoding)

    @staticmethod
    def decode(data: bytes) -> Tuple[Type, str]:
        type, content = data.decode(encoding).split(sep)
        type = Type(int(type))
        return type, content

if __name__ == '__main__':

    pass


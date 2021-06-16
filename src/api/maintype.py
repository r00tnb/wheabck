import enum

class Message:
    '''消息类

    :param name: str，消息名称
    :param data: Any， 消息传递的数据
    :param need_reply: bool，表示消息是否需要回复处理结果，默认不需要回复
    '''
    def __init__(self, name:str, data, need_reply:bool=False):
        self.name = name
        self.data = data
        self.need_reply = need_reply


@enum.unique
class OSType(enum.Enum):
    '''定义服务器操作系统类型
    '''
    UNIX = enum.auto() # Unix类型
    WINDOWS = enum.auto() # Windows类型
    OSX = enum.auto() # mac osx类型
    OTHER = enum.auto() # 其他类型

@enum.unique
class SessionType(enum.Enum):
    '''session的类型枚举，枚举值指定对应webshell的类型，一般它应该为对应脚本后缀名的小写
    '''
    PHP = 'php'
    ASP_NET_CS = 'cs'
    JSP = 'jsp'

    @property
    def suffix(self)->str:
        '''返回session类型对应的后缀名

        :returns: str
        '''
        return str(self.value)

class ServerInfo:
    '''用于描述远程服务器的基本信息
    '''

    def __init__(self):
        self.ostype:OSType
        
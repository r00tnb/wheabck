import enum
import copy
from logging import setLoggerClass
from typing import Final, List, Union

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
        return '.'+str(self.value)

class ServerInfo:
    '''用于描述远程服务器的基本信息
    '''

    def __init__(self):
        self.ostype:OSType
        

class SessionOptions:
    '''session实例使用的选项，用于配置payload如何执行
    '''
    def __init__(self) -> None:
        self.timeout = 30 # 每次请求的超时时间，单位秒，设置为0则表示无限等待请求完成
        self.encoding = 'utf8' # 默认编码
        self.target = '' # webshell的url地址
        self.wrapper_id = '' # 使用的payload包装器id,当为None时则不使用包装器
        self.code_executor_id = '' # 使用的代码执行器id，必须是有效的id否则session不会创建成功
        self.command_executor_id = ''# 当前的命令执行器id， 当为None时则表示无命令执行器

    @property
    def copy(self):
        '''获得一个副本
        '''
        return copy.deepcopy(self)
    
    @staticmethod
    def from_dict(json:dict):
        '''从字典对象中获取同名键来创建实例
        '''
        opt = SessionOptions()
        for k,v in json.items():
            for name, value in opt.__dict__:
                if name == k:
                    setattr(opt, name, v)
        return opt
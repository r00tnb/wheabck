import enum
from typing import Union


class Service:
    '''描述服务的类

    :param name: str，服务名称
    :param data: Any， 服务传递的参数
    :param need_reply: 表示该服务是否需要返回处理结果
    '''
    def __init__(self, name:str, params:Union[list, dict]={}, need_reply=True):
        self.name = name
        self.params = params
        self.need_reply = need_reply

class ServiceStatus(enum.IntEnum):
    '''定义服务处理结果的状态
    '''
    OK = 0
    ERROR = -1

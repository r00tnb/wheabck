import abc
from typing import Any
from .maintype import Message

class MessageHandler(metaclass=abc.ABCMeta):
    '''消息处理者用于处理自定义消息
    '''

    @abc.abstractproperty
    def messages(self)->tuple:
        '''返回定义的消息列表，每一项为消息实例
        '''
        pass

    @abc.abstractmethod
    def handler(self, msg:Message)->Any:
        '''处理指定的消息

        :param msg: 消息实例，包含消息传递的数据。
        :returns: 返回消息处理结果,一般当msg需要回复时才会返回处理结果
        '''
        pass
import abc
from .session import Session
from .maintype import Message

class Helper(metaclass=abc.ABCMeta):
    '''为插件或核心提供帮助的接口
    '''
    @abc.abstractmethod
    def get_name(self)->str:
        '''获得当前程序的名称

        :returns: str
        '''
        pass

    
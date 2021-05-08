import abc
from .maintype import SessionType
from .executor import ServerInfo

class Exploit(metaclass=abc.ABCMeta):
    '''利用webshell执行代码，只会在session建立成功后才会被加载
    '''
    
    @abc.abstractmethod
    def is_supported(self, session_type:SessionType, server_info:ServerInfo)->bool:
        '''判断exploit是否支持当前session，支持返回True之后插件会被加载到session中，否则返回False。这将会在加载该插件之前执行

        :param session_type: 当前Session实例的类型
        :param server_info: 当前服务器的基本信息
        :returns: bool
        '''
        pass

    @abc.abstractmethod
    def init_exploit(self, session):
        '''初始化exploit插件，这将在exploit实例加载到session中时调用

        :param session: 当前Session实例
        '''
        pass
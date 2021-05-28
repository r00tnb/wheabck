import abc
from .maintype import OSType, SessionType

class ServerInfo(metaclass=abc.ABCMeta):
    '''用于描述远程服务器的基本信息
    '''

    @abc.abstractproperty
    def ostype(self)->OSType:
        '''获取服务器操作系统类型
        '''
        pass

    @abc.abstractproperty
    def osinfo(self)->str:
        '''获取服务器操作系统的描述性文字

        :returns: 操作系统的描述性文字
        '''
        pass

class Payload(metaclass=abc.ABCMeta):
    '''封装payload
    '''
    
    @abc.abstractproperty
    def code(self)->bytes:
        '''返回payload的字节流

        :returns: bytes
        '''
        pass


class EvalResult(metaclass=abc.ABCMeta):
    '''描述代码执行的结果
    '''

    @abc.abstractproperty
    def rawdata(self)->bytes:
        '''返回执行代码后的原始数据

        :returns: bytes
        '''
        pass

    @abc.abstractproperty
    def data(self)->bytes:
        '''返回执行代码后的数据，它可能是经过处理的数据

        :returns: bytes
        '''
        pass

    @abc.abstractmethod
    def is_failed(self)->bool:
        '''执行成功返回True，否则False

        :returns: bool
        '''
        pass

class CodeExecutor(metaclass=abc.ABCMeta):
    '''代码执行器，用于在远程服务器执行任意代码
    '''

    @abc.abstractproperty
    def supported_session_type(self)->SessionType:
        '''返回执行器支持的session类型
        '''
        pass

    @abc.abstractmethod
    def connect(self)->ServerInfo:
        '''测试代码执行器是否可用，成功返回服务端基本信息，失败返回None

        :returns: ServerInfo|None
        '''
        pass

    @abc.abstractmethod
    def eval(self, payload:Payload, options: dict={})->EvalResult:
        '''在远程服务器执行payload，并返回执行结果

        :param payload: Payload实例
        :param options: 额外的配置参数，由插件实现如何使用
        :returns: 执行结果
        '''
        pass

class CommandExecutor(metaclass=abc.ABCMeta):
    '''命令执行器，用于在远程服务器执行命令，一般它依赖代码执行器
    '''

    @abc.abstractmethod
    def exec(self, cmd:str)->str:
        '''在远程服务器执行命令并返回命令执行结果

        :param cmd: 合法的命令字符串
        :returns: str, 命令执行结果
        '''
        pass
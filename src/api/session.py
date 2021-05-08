import abc
import enum
from collections.abc import Callable
from .executor import CodeExecutor, ServerInfo, CommandExecutor
from .explot import Exploit
from .maintype import SessionType

class Session(metaclass=abc.ABCMeta):
    '''session用于描述当前webshell的信息
    '''

    @abc.abstractproperty
    def plugins_list(self)->tuple:
        '''获取已加载的插件实例列表
        '''
        pass

    @abc.abstractproperty
    def session_id(self)->str:
        '''获取一个唯一标识session的字符串
        '''
        pass

    @abc.abstractproperty
    def session_type(self)->SessionType:
        '''获取当前session类型

        :returns: SessionType
        '''
        pass

    @abc.abstractproperty
    def server_info(self)->ServerInfo:
        '''获取远程服务器的基本信息

        :returns: ServerInfo
        '''
        pass
        
    @abc.abstractproperty
    def code_executor(self)->CodeExecutor:
        '''获取与当前session绑定的代码执行器实例

        :returns: CodeExecutor
        '''
        pass

    @abc.abstractproperty
    def command_executor(self)->CommandExecutor:
        '''获取与当前session绑定的命令执行器实例

        :returns: CommandExecutor
        '''
        pass

    @abc.abstractmethod
    def load_exploit(self, exploit:Exploit)->bool:
        '''将exploit加载到session中

        :param exploit: Exploit实例
        :returns: bool,加载成功返回True，否则False
        '''
        pass
    
    @abc.abstractmethod
    def register_on_loaded(self, handler):
        '''注册一个回调函数，它将在session加载完成所有插件后执行

        :param handler: 回调函数, 形如 def handler(session)->None: ...
        :returns: None
        '''
        pass

    @abc.abstractmethod
    def register_on_destroy_before(self, handler):
        '''注册一个回调函数，它将在session销毁前执行

        :param handler: 回调函数, 形如def handler(session)->None: ...
        :returns: None
        '''
        pass
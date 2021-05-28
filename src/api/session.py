import abc
import enum
from collections.abc import Callable
from .executor import CodeExecutor, ServerInfo, CommandExecutor
from .explot import Exploit
from .maintype import SessionType

class Session(metaclass=abc.ABCMeta):
    '''session用于描述当前webshell的信息，并提供工具方法
    '''

    ## 属性
    @abc.abstractproperty
    def is_loaded(self)-> bool:
        '''判断当前session是否已经加载完毕

        :returns: bool, 当所有插件均已加载完毕时返回True，否则False
        '''

    @abc.abstractproperty
    def plugins_list(self)->tuple:
        '''获取已加载的插件实例列表
        '''

    @abc.abstractproperty
    def session_id(self)->str:
        '''获取一个唯一标识session的字符串
        '''

    @abc.abstractproperty
    def session_type(self)->SessionType:
        '''获取当前session类型

        :returns: SessionType
        '''

    @abc.abstractproperty
    def server_info(self)->ServerInfo:
        '''获取远程服务器的基本信息

        :returns: ServerInfo
        '''
        
    @abc.abstractproperty
    def code_executor(self)->CodeExecutor:
        '''获取与当前session绑定的代码执行器实例

        :returns: CodeExecutor
        '''

    @abc.abstractproperty
    def command_executor(self)->CommandExecutor:
        '''获取与当前session绑定的命令执行器实例

        :returns: CommandExecutor
        '''

    ## 方法
    @abc.abstractmethod
    def register_on_loaded(self, handler):
        '''注册一个回调函数，它将在session加载完成所有插件后执行

        :param handler: 回调函数, 形如 def handler(session)->None: ...
        :returns: None
        '''

    @abc.abstractmethod
    def register_on_destroy_before(self, handler):
        '''注册一个回调函数，它将在session销毁前执行

        :param handler: 回调函数, 形如def handler(session)->None: ...
        :returns: None
        '''

    @abc.abstractmethod
    def save_json(self, name: str, value)-> bool:
        '''保存一个json对象

        :param name: 为保存的对象起的名字，名字存在则会覆盖
        :param value: 一个可被序列化为json字符串的对象
        :returns: bool,保存成功返回True，否则False
        '''

    @abc.abstractmethod
    def load_json(self, name:str):
        '''加载一个已保存的json对象

        :param name: json对象的名字
        :returns: 若存在则返回一个保存前的json对象，失败返回None
        '''
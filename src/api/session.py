import abc
from src.api.executor import CommandExecutor, EvalResult, Payload
from src.api.plugin import Plugin
from .maintype.info import SessionOptions, SessionType, ServerInfo
from typing import Any, Callable, Dict, NoReturn, Tuple, Union, final

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
    def options(self)->SessionOptions:
        '''获得一个session选项实例的副本

        :returns: session选项实例，它是一个副本，所以可以修改里面的数据而不影响session的选项
        '''

    @abc.abstractproperty
    def plugins_list(self)->Tuple[Plugin]:
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

    ## 方法

    @abc.abstractmethod
    def save_json(self, name: str, value:Union[list,dict, None])-> bool:
        '''保存一个json对象到当前session,在同一个连接下，若已存在一个相同名称的json数据则会覆盖，若value为None则删除该json数据

        :param name: 为保存的对象起的名字，名字存在则会覆盖
        :param value: 一个可被序列化为json字符串的对象,若为None则删除该条json数据
        :returns: bool,保存成功返回True，否则False
        '''

    @abc.abstractmethod
    def load_json(self, name:str)->Union[list, dict, None]:
        '''从当前session加载一个已保存的json对象

        :param name: json对象的名字
        :returns: 若存在则返回一个保存前的json对象，失败返回None
        '''

    @abc.abstractmethod
    def eval(self, payload:Payload, timeout:float=None)->Union[bytes, None]:
        '''执行payload代码并获取执行结果,不会验证payload是否是当前session支持的

        :param payload: payload实例
        :param timeout: 本次执行payload的超时时间(单位秒)，设置为0则无限等待，设置为小于0或None的则使用默认超时时间
        :returns: 执行结果，失败返回None
        '''
    
    @abc.abstractmethod
    def evalfile(self, payload_path:str, vars:Dict[str, Any]={}, timeout:float=-1)->Union[bytes, None]:
        '''执行指定路径下的payload文件并获取执行结果。
        若传入的文件路径不带后缀，该方法将根据当前session类型读取同目录下相应的payload文件。
        该方法会根据session类型自动构造对应的payload实例并调用eval方法执行（若文件后缀不是session支持的则会构造失败）。

        :param payload_path: payload文件路径，该路径可以是绝对路径，也可以是相对路径，当为相对路径时，它相对的是调用该方法的文件的路径。
        :param vars: 向该payload传递的全局变量字典
        :param timeout: 本次执行payload的超时时间(单位秒)，设置为0则无限等待，设置为小于0或None的则使用默认超时时间
        :returns: 执行结果，失败返回None
        '''

    @abc.abstractmethod
    def exec(self, cmd:bytes)->Union[bytes, None]:
        '''执行系统命令，并获取命令输出的结果

        :param cmd: 命令字节流
        :returns: 命令的输出结果，只获取标准输出流内容，对于错误输出需要在命令中使用重定向来获取。若执行错误（系统命令错误之外的错误）则返回None
        '''

    @abc.abstractmethod
    def set_default_exec(self, executor:CommandExecutor)->bool:
        '''设置默认的命令执行器，它会影响exec方法

        :param executor: 命令执行器实例，若参数非法，则不会设置成功
        :returns: 成功返回True，失败返回False
        '''
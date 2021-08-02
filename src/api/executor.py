import abc
from typing import Any, Dict, List, Union
from .maintype import SessionType, ServerInfo
from .staticui import StaticUI

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

class CodeExecutor(StaticUI, metaclass=abc.ABCMeta):
    '''代码执行器，用于在远程服务器执行任意代码
    '''

    @abc.abstractproperty
    def configure_collection_page(self)->str:
        '''返回一个用于收集配置信息的页面url地址，该页面将在StaticUI中返回的静态目录中寻址，必须使用相对地址(也可以在url中添加查询参数等用于更高级的需求)

        如 配置为 /index.html，则在创建webshell 连接使用该代码执行器时会在静态目录中寻找对应的文件并返回到页面上用于收集配置信息。
        该页面的注意点：
            1.该页面一般情况下无需向后台交互，只用于信息收集
            2.页面需监听来自上层窗口发来的submit-config消息，并在消息来到时将收集的信息以json数据的格式返回到上层窗口
            3.之后该页面任务完成，
        
        :returns: 页面的相对url地址
        '''

    @abc.abstractmethod
    def get_server_info(self)->ServerInfo:
        '''获取远程服务器基本信息，成功返回服务端基本信息，失败返回None

        :returns: ServerInfo|None
        '''

    @abc.abstractmethod
    def generate(self, config: Dict[str, Any]={}) -> bytes:
        '''生成webshell服务端文件

        :params config: 若webshell需要根据参数来配置，可通过该参数传入
        :returns: 返回最终生成的webshell字节流
        '''

    @abc.abstractmethod
    def eval(self, payload: bytes, timeout: float) -> Union[bytes, None]:
        '''向目标URL发送payload执行请求并获取执行结果

        :params payload: payload的字节流
        :params timeout: 本次payload的执行中请求的超时时间，为0时则无限等待（这是一个约定，实现该方法时应该实现此特性）
        :returns: 返回payload在目标上的执行结果,失败则返回None
        '''

class CommandExecutor(metaclass=abc.ABCMeta):
    '''命令执行器，用于在远程服务器执行命令，一般它依赖代码执行器
    '''

    @abc.abstractmethod
    def exec(self, cmd:bytes)->Union[bytes, None]:
        '''在远程服务器执行命令并返回命令执行结果

        :param cmd: 合法的命令字节流
        :returns: 命令执行结果， 失败返回None
        '''
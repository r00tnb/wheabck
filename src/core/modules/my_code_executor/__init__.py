import os
from src.api.session import Session
from src.api.plugin import Plugin
from src.api.executor import CodeExecutor
from typing import Callable, Dict, List, Literal, NewType, Tuple, Union
from src.api.maintype.info import ServerInfo, SessionType
from types import ModuleType
import src.utils as utils
import requests
from .data import DbData


def get_plugin_class():
    return DefaultCodeExecutor

Params = Dict[str, str]
Headers = Dict[str, str]
BodyData = NewType('BodyData', bytes)
Body = Union[Dict[str, str], BodyData]
BodyMode = Literal['json', 'form', 'file', 'raw']
Request = Tuple[Params, Headers, Body, BodyMode]


StatusCode = NewType('StatusCode', int)
StatusMsg = NewType('StatusMsg', str)
Response = Tuple[StatusCode, StatusMsg, Headers, BodyData]


class Webshell:
    '''用于定义Python脚本如何扩展webshell，适用于默认的代码执行器
    '''

    def __init__(self) -> None:
        self.name = ''  # 名称
        self.webshell_id = -1  # 对应的id
        self.session_type: SessionType = None  # 支持的session
        self.pycode = b''  # 用于执行payload的Python代码


    @property
    def module(self) -> ModuleType:
        '''从pycode中加载的Python模块
        '''
        if self.__module is None:
            self.__module = utils.load_module_from_bytes(self.pycode)
        return self.__module

    def __set_request(self, payload: bytes, params: Params, headers: Headers, body: Body,
                      body_mode: BodyMode) -> Request:
        '''设置请求内容

        :params payload: 该次需要执行的payload内容，为bytes类型
        :params params: 指定查询参数内容，为字典类型
        :params headers: 指定请求头部内容，为字典类型
        :params body: 指定请求体内容，若body_mode为raw则，应为bytes类型，其他情况为字典类型
        :params body_mode: 指定body的类型，可选：json，form（普通表单数据格式），file（文件上传格式），raw（原始数据格式，此时body参数应为bytes字节流）
        :returns: 返回除payload外和入参顺序一致的参数,将会根据返回的内容构造请求数据
        '''

        return params, headers, body, body_mode

    def __parse_response(self, status_code: int, status_msg: str, headers: Headers, body: bytes) -> Union[bytes, None]:
        '''解析响应内容，并获取payload执行结果

        :params status_code: 响应的状态码，为整数
        :params status_msg: 响应的状态消息，为字符串
        :params headers: 响应头部内容，为字典类型
        :params body: 响应体内容， 为bytes类型
        :returns: 返回payload执行后对应的结果，成功返回bytes类型，失败可返回None
        '''
        return body

    def __set_actions(self, payload:bytes) -> List[Tuple[Request, Callable[[StatusCode, StatusMsg, Headers, BodyData], Union[bytes, None]]]]:
        '''设置webshell的动作序列用于更复杂的webshell交互，如:需要多次握手的webshell交互

        :params payload: 该次需要执行的payload内容，为bytes类型
        :returns: 返回交互序列的列表，将会按照列表顺序进行请求响应。其中每个元素为一个元组，元组的第一个元素为请求体信息，第二个元素为对该次请求结果的处理函数。
                    若返回一个空列表，将按照默认的set_request和parse_response函数来进行请求响应。
                    总是将最后一组的处理结果当做payload的执行结果
        '''
        return []

class DefaultCodeExecutor(Plugin, CodeExecutor):
    '''该类实现默认的代码执行器，可使用Python脚本快速扩展webshell
    '''

    def __init__(self) -> None:
        self.db_path = os.path.join(os.path.dirname(__file__), 'webshell.db')
        self.db = DbData(self.db_path)
        self.session:Session = None


    def on_loading(self, session: Session) -> bool:
        self.session = session
        return True

    def on_loaded(self):
        '''加载所有可用的webshell脚本
        '''
        

    def generate(self, config: Dict[str, any]={}) -> bytes:
        return b''

    def eval(self, payload: bytes, timeout: float) -> Union[bytes, None]:
        default_headers = {
            'User-Agent':'Wheabck'
        }
        actions = self.__set_actions(payload)
        if not actions:
            actions = [(self.__set_request(payload, {}, default_headers, {}, 'form'),self.__parse_response)]
        for act in actions:
            req, parse_func = act


    def get_server_info(self) -> ServerInfo:
        return ServerInfo()

    def configure_collection_page(self) -> str:
        return '/get-config-collection-page'

    def static_dir(self) -> str:
        return '/test'
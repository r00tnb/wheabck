import os
import re
from src.api.maintype.payload import PHPPayload
from src.api.wrapper import Wrapper
from src.api.executor import CodeExecutor, CommandExecutor, EvalResult, Payload
from src.api.plugin import Plugin
from src.api.session import Session
from src.api.maintype.info import ServerInfo, SessionOptions, SessionType
import src.utils as utils
from .pluginmanager import plugin_manager
from .connectionmanager import Connection, connection_manager
from typing import Any, Callable, Dict, List, Tuple, Union


class SessionInitError(Exception):
    '''session初始化失败的错误
    '''


class SessionAdapter(Session):
    '''实现Session类,session必须从Connection实例建立
    '''

    def __init__(self, config: Connection):
        self.config = config
        # 已加载的插件实例字典,不包括代码执行器和包装器
        self.__plugin_instance_map: Dict[str, Plugin] = {}
        self.__loaded = False  # 是否加载完毕
        self.__id = utils.random_str()  # session id

        # 初始化代码执行器和payload包装器，它们不会加载到__plugin_instance_map中
        self.__code_executor: CodeExecutor = plugin_manager.get_code_executor(
            self.config.options.code_executor_id)
        if self.__code_executor is None:
            raise SessionInitError(
                f'Code executor with ID {self.config.options.code_executor_id} is not found!')
        elif self.session_type not in self.__code_executor.supported_session_types or not self.__code_executor.on_loading(self):
            raise SessionInitError(
                f'Code executor with ID {self.config.options.code_executor_id} is not support the session!')

        self.__payload_wrapper: Wrapper = plugin_manager.get_wrapper(
            self.config.options.wrapper_id)
        if self.__payload_wrapper is None or self.session_type not in self.__payload_wrapper.supported_session_types or \
                not self.__payload_wrapper.on_loading(self):
            self.__payload_wrapper = plugin_manager.get_default_wrapper()

        # 命令执行器一般在__plugin_instance_map中(此时会在加载插件时初始化)，也可能是代码执行器或包装器
        self.__command_executor: CommandExecutor = None
        if self.config.options.command_executor_id == self.config.options.code_executor_id and \
                isinstance(self.__code_executor, CommandExecutor):
            self.__command_executor = self.__code_executor
        if self.config.options.wrapper_id == self.config.options.command_executor_id and \
                isinstance(self.__payload_wrapper, CommandExecutor):
            self.__command_executor = self.__payload_wrapper

    def __del__(self):
        '''session销毁后执行
        '''
        # 执行相应回调
        for plugin in self.__plugin_instance_map.values():
            plugin.on_destroy()
        self.__payload_wrapper.on_destroy()
        self.__code_executor.on_destroy()

    @property
    def session_type(self) -> SessionType:
        return self.config.session_type

    @property
    def server_info(self) -> ServerInfo:
        return self.config.server_info

    @property
    def is_loaded(self) -> bool:
        return self.__loaded

    @property
    def options(self) -> SessionOptions:
        return self.config.options.copy

    @property
    def plugins_list(self) -> Tuple[Plugin, ...]:
        '''注意：返回的插件列表是包含代码执行器和payload包装器的插件列表
        '''
        return tuple(self.__plugin_instance_map.values())+(self.__code_executor, self.__payload_wrapper)

    @property
    def session_id(self) -> str:
        return self.__id

    def load_plugins(self) -> int:
        '''从插件管理器中加载插件实例，返回加载成功的插件数量

        :returns: int, 加载成功的插件数量
        '''
        ret = 0
        for ID, plugin_class in plugin_manager.plugins_map.items():
            if self.session_type not in plugin_class.supported_session_types:
                continue
            if issubclass(plugin_class, (CodeExecutor, Wrapper)):
                continue
            plugin = plugin_class()
            if plugin.on_loading(self):
                self.__plugin_instance_map[utils.random_str()] = plugin
                ret += 1
                if self.__command_executor is None and self.config.options.command_executor_id == ID and \
                        isinstance(plugin, CommandExecutor):  # 初始化命令执行器
                    self.__command_executor = plugin

        # 所有插件加载完毕后执行相应的回调函数
        self.__code_executor.on_loaded()
        self.__payload_wrapper.on_loaded()
        for plugin in self.__plugin_instance_map.values():
            plugin.on_loaded()

        return ret

    def load_json(self, name: str) -> Union[list, dict, None]:
        return connection_manager.get_json_data(self.config.conn_id, name)

    def save_json(self, name: str, value: Union[list, dict, None]) -> bool:
        if value is None:
            connection_manager.del_json_data(self.config.conn_id, name)
        elif connection_manager.get_json_data(self.config.conn_id, name) is None:
            connection_manager.add_json_data(self.config.conn_id, name, value)
        else:
            connection_manager.update_json_data(self.config.conn_id, name, value)

    def eval(self, payload: Payload, timeout: float = None) -> Union[bytes, None]:
        code = payload.code
        if self.__payload_wrapper:
            code = self.__payload_wrapper.wrap(code)
        if timeout is None or timeout < 0:
            timeout = self.config.options.timeout
        return self.__code_executor.eval(code, timeout)

    def evalfile(self, payload_path: str, vars: Dict[str, Any] = {}, timeout: float = None) -> Union[bytes, None]:
        old_dir = os.getcwd()
        os.chdir(utils.call_path(2))  # 切换到调用该函数处的文件所在目录
        if not payload_path.lower().endswith(self.session_type.suffix):
            payload_path += self.session_type.suffix
        code = utils.file_get_content(payload_path)
        if code is None:
            return None
        p: Payload = None
        if self.session_type == SessionType.PHP:
            p = PHPPayload(code, vars)
        if p is None:
            return None

        return self.eval(p, timeout)

    def exec(self, cmd: bytes) -> Union[bytes, None]:
        return self.__command_executor.exec(cmd)

    def set_default_exec(self, executor: CommandExecutor) -> bool:
        if not issubclass(executor, CommandExecutor):
            return False
        self.__command_executor = executor
        self.config.options.command_executor_id = plugin_manager.get_plugin_id(executor)
        return True

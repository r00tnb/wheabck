from api.session import Session, SessionType, ServerInfo
from api.executor import CodeExecutor, CommandExecutor
from api.plugin import Plugin
import src.utils as utils
from .pluginmanager import plugin_manager
from typing import Dict

class SessionConfig:
    '''session配置类
    '''
    def __init__(self):
        self.session_type = SessionType.PHP # session类型
        self.code_executor_id = '' # session使用的代码执行器的插件id
        self.command_executor_id = ''


class SessionAdapter(Session):
    '''实现Session类
    '''
    def __init__(self, config:SessionConfig):
        self.raw_config = config
        self.__plugin_instance_map:Dict[str, Plugin] = {} # 已加载的插件实例字典

        self.__type = config.session_type
        self.__server_info = None
        self.__code_executor = plugin_manager.get_code_executor(config.code_executor_id)
        self.__command_executor = plugin_manager.get_command_executor(config.command_executor_id)
        

    @property
    def session_type(self)->SessionType:
        return self.__type

    @property
    def server_info(self)->ServerInfo:
        return self.__server_info
    
    @property
    def code_executor(self)->CodeExecutor:
        return self.__code_executor
    
    @property
    def command_executor(self)->CommandExecutor:
        return self.__command_executor

    def load_plugins(self)-> int:
        '''从插件管理器中加载插件实例，返回加载成功的插件数量

        :returns: int, 加载成功的插件数量
        '''
        ret = 0
        for plugin_class in plugin_manager.plugins_list:
            plugin = plugin_class()
            if plugin.is_supported(self):
                self.__plugin_instance_map[utils.random_str()] = plugin
                ret += 1

        return ret
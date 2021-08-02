from src.api.wrapper import Wrapper
from src.api.plugin import Plugin
from src.api.session import Session
from src.api.executor import CodeExecutor, CommandExecutor
from src.core.helperadapter import helper
import src.utils as utils
import src.config as config
import os
from typing import Callable, Dict, Type, Tuple, Union

__all__ = ['plugin_manager']

class DefaultWrapper(Plugin, Wrapper):
    '''默认的payload包装器，不做处理的返回输入payload
    '''
    def wrap(self, payload: bytes) -> bytes:
        return payload
    
    def on_load(self, session: Session) -> bool:
        return True

class PluginManager:
    '''管理所有插件
    '''

    def __init__(self):
        self.__plugin_map:Dict[str, Type[Plugin]] = {} # 插件字典，键为ID，值为Plugin派生类

    def load_all_plugin(self)->Tuple[int, int]:
        '''加载插件目录下的所有插件

        :returns: (int, int)，返回(加载成功的数量, 加载失败的数量)
        '''
        win, fail = 0, 0
        for d in os.listdir(config.plugins_path):# 插件目录加载
            if self.load_plugin(os.path.join(config.plugins_path, d)):
                win += 1
            else:
                fail += 1

        m_path = os.path.join(os.path.dirname(__file__), 'modules')
        for d in os.listdir(m_path):# 内置插件目录加载
            if self.load_plugin(os.path.join(m_path, d)):
                win += 1
            else:
                fail += 1
        
        self.__plugin_map['__default_wrapper'] = DefaultWrapper # 默认的payload包装器插件
        win += 1
        return win, fail

    def load_plugin(self, path:str)->bool:
        '''从指定路径加载插件

        每个插件应该都是一个Python模块，插件加载过程如下：
            1. 判断是否为一个python模块，是则进行下一步
            2. 判断该模块是否导出了一个名为get_plugin_class的函数，有则进行下一步
            3. 尝试无参调用该包的get_plugin_class函数，若发生异常则加载失败，否则保存返回值进行下一步
            4. 若返回值为一个Plugin的派生类则加载成功，否则加载失败

        :param path: 一个合法的目录路径字符串
        :returns: bool, 加载成功返回True，失败返回False
        '''
        func_name = 'get_plugin_class'
        module = utils.load_module(path)
        if not module or not hasattr(module, func_name):
            return False
        get_plugin_class:Callable[[], Type[Plugin]] = getattr(module, func_name)
        try:
            plugin_class = get_plugin_class()
        except:
            return False
        else:
            if not issubclass(plugin_class, Plugin):
                return False
            
            ID = os.path.relpath(os.path.abspath(path), config.plugins_path)
            self.__plugin_map[ID] = plugin_class
            plugin_class.plugin_id = ID
        return True

    def remove(self, ID:str)->Plugin:
        return self.__plugin_map.pop(ID)

    def get_plugin(self, ID:str, type=Plugin):
        '''获取指定ID的插件实例
        '''
        plugin = self.__plugin_map.get(ID)
        if plugin and issubclass(plugin, type):
            return plugin()
        return None

    def get_command_executor(self, ID:str)->CommandExecutor:
        '''获取CommandExecutor插件实例, 失败返回None
        '''
        return self.get_plugin(ID, CommandExecutor)

    def get_code_executor(self, ID:str)->CodeExecutor:
        '''获取代码执行器插件实例, 失败返回None
        '''
        return self.get_plugin(ID, CodeExecutor)

    def get_wrapper(self, ID:str)->Wrapper:
        '''获取包装器插件实例, 失败返回None
        '''
        return self.get_plugin(ID, Wrapper)

    def get_default_wrapper(self)->DefaultWrapper:
        '''获取一个默认的payload包装器实例
        '''
        return DefaultWrapper()

    def get_plugin_id(self, plugin:Plugin)->Union[str, None]:
        '''根据插件实例获取插件对应的ID

        :params plugin: 需要查找ID的插件实例
        :returns: 返回插件实例对应的插件ID，失败返回None
        '''
        for ID, p in self.__plugin_map.items():
            if plugin.__class__ == p:
                return ID
        return None

    @property
    def plugins_map(self)->Dict[str, Type[Plugin]]:
        return self.__plugin_map.copy()


plugin_manager = PluginManager()

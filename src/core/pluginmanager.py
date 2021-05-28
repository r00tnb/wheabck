from src.api.plugin import Plugin
from src.api.session import Session
from src.api.executor import CodeExecutor, CommandExecutor
from src.core.helperadapter import helper
import src.utils as utils
import src.config as config
import os

__all__ = ['plugin_manager']

class PluginManager:
    '''管理所有插件
    '''

    def __init__(self):
        self.__plugin_map = {} # 插件字典，键为ID，值为Plugin派生类

    def load_from_plugin_dir(self)->tuple:
        '''加载插件目录下的所有插件

        :returns: (int, int)，返回(加载成功的数量, 加载失败的数量)
        '''
        win, fail = 0, 0
        for d in os.listdir(config.plugins_path):
            if self.load_plugin(os.path.join(config.plugins_path, d)):
                win += 1
            else:
                fail += 1
        return win, fail

    def load_plugin(self, path:str)->bool:
        '''从指定路径加载插件

        每个插件应该都是一个Python包，插件加载过程如下：
            1. 判断是否为一个python包，是则进行下一步
            2. 判断该包是否导出了一个名为get_plugin_class的属性，有则进行下一步
            3. 尝试无参调用该包的get_plugin_class函数，若发生异常则加载失败，否则保存返回值进行下一步
            4. 若返回值为一个Plugin的派生类则加载成功，否则加载失败

        :param path: 一个合法的目录路径字符串
        :returns: bool, 加载成功返回True，失败返回False
        '''
        func_name = 'get_plugin_class'
        module = utils.load_package(path)
        if not module or hasattr(module, func_name):
            return False
        get_plugin_class = getattr(module, func_name)
        try:
            plugin_class = get_plugin_class()
        except:
            return False
        else:
            if not issubclass(plugin_class, Plugin):
                return False
            
            ID = os.path.relpath(os.path.abspath(path), config.plugins_path)
            self.__plugin_map[ID] = plugin_class
        return True

    def remove(self, ID:str)->Plugin:
        return self.__plugin_map.pop(ID)

    def get_command_executor(self, ID:str)->CommandExecutor:
        '''获取CommandExecutor插件, 失败返回None
        '''
        plugin = self.__plugin_map.get(ID)
        if plugin and issubclass(plugin, CommandExecutor):
            return plugin
        return None

    def get_code_executor(self, ID:str)->CodeExecutor:
        '''获取代码执行器插件, 失败返回None
        '''
        plugin = self.__plugin_map.get(ID)
        if plugin and issubclass(plugin, CodeExecutor):
            return plugin
        return None

    @property
    def plugins_list(self)->tuple:
        return tuple(self.__plugin_map.values())


plugin_manager = PluginManager()
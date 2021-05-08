from src.api.plugin import Plugin
from src.api.explot import Exploit
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

        每个插件应该都是一个Python包,并且导出一个名为plugin的Plugin派生类，否则不会认为是一个可用的插件

        :param path: 一个合法的目录路径字符串
        :returns: bool, 加载成功返回True，失败返回False
        '''
        cls_name = 'plugin'
        module = utils.load_package(path)
        if not module or hasattr(module, cls_name):
            return False
        plugin_class = getattr(module, cls_name)
        if not issubclass(plugin_class, Plugin):
            return False
        
        ID = os.path.relpath(os.path.abspath(path), config.plugins_path)
        self.__plugin_map[ID] = plugin_class
        return True

    def remove(self, ID:str)->Plugin:
        return self.__plugin_map.pop(ID)

    def load_to_session(self, session:Session)->int:
        '''将插件实例化并加载到session中,一般只有exploit实例才会加载到session中
        '''
        count = 0
        for plugin in self.__plugin_map.values():
            if issubclass(plugin, Exploit):
                exp = plugin(helper)
                if exp.is_supported(session.session_type, session.server_info):
                    session.load_exploit(plugin)
                    plugin.init_exploit(session)
                    count += 1
        return count
        

    def get_exploit(self, ID:str)->Exploit:
        '''获取Exploit插件, 失败返回None
        '''
        plugin = self.__plugin_map.get(ID)
        if plugin and issubclass(plugin, Exploit):
            return plugin
        return None

    def get_command_executor(self, ID:str)->CommandExecutor:
        '''获取CommandExecutor插件, 失败返回None
        '''
        plugin = self.__plugin_map.get(ID)
        if plugin and issubclass(plugin, CommandExecutor):
            return plugin
        return None

    def get_code_executor(self, ID:str)->Exploit:
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
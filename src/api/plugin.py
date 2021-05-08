import abc
from .session import SessionType, ServerInfo, Session
from .helper import Helper


class Plugin(metaclass=abc.ABCMeta):
    '''所有插件应该实现该接口,插件指的是实现了Plugin的类

    :param helper: Helper实例
    '''

    def __init__(self, helper:Helper):
        '''派生类应该接受传入的helper参数
        '''
        self.helper = helper

    @abc.abstractproperty
    def name(self)->str:
        '''返回插件名称, 插件名称应该设置为包名并保证唯一性

        :returns: str
        '''
        pass

    @abc.abstractproperty
    def static_dir(self)->str:
        '''返回当前插件的静态目录绝对路径，若插件有前端页面则可以返回它的目录路径，否则返回None表示没有前端页面

        :returns: str|None
        '''
        pass
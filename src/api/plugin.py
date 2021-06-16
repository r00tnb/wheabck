import abc
from .session import SessionType, ServerInfo, Session
from .helper import Helper

class Plugin(metaclass=abc.ABCMeta):
    '''所有插件应该实现该接口,插件指的是实现了Plugin的类

    插件类的类属性表示插件的属性，派生类需覆盖这些属性来配置当前插件
    '''

    name = 'plugin' # 插件名称
    author = 'r00tnb' # 插件作者

    def __init__(self):
        self.session:Session

    def is_supported(self, session:Session)-> bool:
        '''判断当前插件是否支持该session，返回True表示支持（注意保存该session的引用），session会加载该插件否则session不会加载该插件。

        :returns: bool,支持返回True不支持返回False
        '''
        self.session = session
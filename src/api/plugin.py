import abc
from .session import SessionType, ServerInfo, Session
from .helper import Helper
from .maintype import SessionNotSupportedException

class Plugin(metaclass=abc.ABCMeta):
    '''所有插件应该实现该接口,插件指的是实现了Plugin的类

    插件类的类属性表示插件的属性，派生类需覆盖这些属性来配置当前插件

    :param Session: Session实例
    :raises: SessionNotSupportedException, 当插件不支持当前session时可抛出该异常，session将不会加载该插件
    '''

    name = 'plugin' # 插件名称
    author = 'r00tnb' # 插件作者

    def __init__(self, session:Session):
        '''派生类应该接受传入的session参数
        '''
        self.session = session
        # Example：
        #   if session.session_type != SessionType.PHP:
        #       raise SessionNotSupportedException("Current Session is not PHP!")

    @abc.abstractproperty
    def static_dir(self)->str:
        '''返回当前插件的静态目录绝对路径，若插件有前端页面则可以返回它的目录路径，否则返回None表示没有前端页面

        :returns: str|None
        '''
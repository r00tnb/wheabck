from .data import db_data, PyWrapper
from typing import Callable, Dict, List, Tuple, Type
from src.api.session import Session
from src.api.plugin import Plugin
from src.api.wrapper import Wrapper

def get_plugin_class()->Type[Plugin]:
    return MyWrapper

class MyWrapper(Plugin, Wrapper):
    '''实现payload包装器，并使其能够使用Python脚本扩展功能
    '''

    def __init__(self):
        super().__init__()
        self.__wrappers:List[PyWrapper] = [] # 用于保存已加载的payload包装器,后续会按照列表顺序一次调用包装器

    def set_wrappers(self, wrapper_ids:List[int]):
        '''设置当前的包装器列表
        '''
        for ID in wrapper_ids:
            w = db_data.get_wrapper(ID)
            if w is not None:
                self.__wrappers.append(w)

    def get_all_wrappers(self)->List[PyWrapper]:
        '''获取所有当前session类型可用的包装器
        '''
        ret = []
        for w in db_data.get_all_wrappers():
            if self.session.session_type in w.supported_session_types:
                ret.append(w)
        return ret

    def on_loading(self, session: Session) -> bool:
        self.session = session
        return True

    def wrap(self, payload: bytes) -> bytes:
        code = payload
        for w in self.__wrappers:
            code = w.wrap(code)
        return code
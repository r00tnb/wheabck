from typing import Dict
from src.api.session import Session

__all__ = ['session_manager']

class SessionManager:
    '''用于管理当前存活的session
    '''
    def __init__(self) -> None:
        self.__session_map:Dict[str, Session] = {} # 保存当前存活的session

    def add_session(self, session:Session):
        '''添加一个session
        '''
        self.__session_map[session.session_id] = session
    
    def del_session(self, session_id:str)->bool:
        '''删除一个存活的session
        '''
        session = self.__session_map.pop(session_id, None)
        if session is None:
            return False
        del session
        return True


session_manager = SessionManager()
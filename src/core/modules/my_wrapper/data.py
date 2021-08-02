import json
from src.api.maintype.info import SessionConfig, SessionType
from typing import Dict, List, NewType, Tuple, Union, final
from types import ModuleType
import sqlite3
import src.utils as utils
import pickle
import os

__all__ = ['db_data', 'PyWrapper']

class PyWrapper:
    '''描述使用Python脚本扩展的payload包装器
    '''
    def __init__(self, ID:int, name:str, supported_session_types:List[SessionType], pycode:bytes) -> None:
        self.name = name # 包装器名称
        self.ID = ID # 包装器ID
        self.supported_session_types = supported_session_types # 支持的session类型列表
        self.pycode = pycode # Python脚本字节流

        self.__module:ModuleType = utils.load_module_from_bytes(self.pycode) # 从pycode中加载的模块, 该模块必须导出一个名为wrap的可调用函数

    def wrap(self, payload:bytes)->bytes:
        '''处理payload字节流并返回结果
        '''
        try:
            ret = self.__module.wrap(payload)
            if not isinstance(ret, bytes):
                return payload
            else:
                return ret
        except:
            return payload


@final
class DbData:
    '''提供简易数据操作
    '''

    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.wrapper_table = 'wrappers'
        self.wrapper_rule_table = 'rules'
        self.cur = self.conn.cursor()

        # 初始化数据库
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.wrapper_table}(\
            wrapper_id INTEGER PRIMARY KEY,name TEXT, supported_session_types TEXT, code BLOB)')
        self.conn.commit()

    def __to_wrapper(self, row)->Union[PyWrapper, None]:
        '''将从数据库中查询到的数据转为PyWrapper对象
        '''
        if row is None:
            return None
        result = list(row)
        try:
            temp = json.loads(result[2])
            result[2] = [SessionType(i) for i in temp]
        except:
            return None
        return PyWrapper(*result)

    def get_wrapper(self, wrapper_id: int) -> Union[PyWrapper, None]:
        '''获取指定webshell

        :param wrapper_id: wrapper id
        :returns: 返回一个PyWrapper实例，失败则返回None
        '''
        self.cur.execute(
            f'select * from {self.wrapper_table} where wrapper_id=?', (wrapper_id,))
        return self.__to_wrapper(self.cur.fetchone())

    def get_all_wrappers(self)->List[PyWrapper]:
        '''获取数据表中所有的wrapper
        '''
        self.cur.execute(f'select * from {self.wrapper_table}')
        ret:List[PyWrapper] = []
        for d in self.cur.fetchall():
            ret.append(self.__to_wrapper(d))
        return ret

    def update_wrapper(self, wrapper:PyWrapper):
        '''保存包装器的更改
        '''
        supported_session_types = json.dumps(wrapper.supported_session_types)
        self.cur.execute(f'update {self.wrapper_table} set name=?,session_type=?,code=? where wrapper_id=?',
            (wrapper.name, supported_session_types, wrapper.pycode, wrapper.ID))
        self.conn.commit()

    def del_wrapper(self, wrapper_id:int):
        '''删除指定的包装器
        '''
        self.cur.execute(f'delete from {self.wrapper_table} where wrapper_id=?', (wrapper_id,))
        self.conn.commit()

    def add_wrapper(self, name:str, supported_session_types:List[SessionType], pycode:bytes):
        '''新增一个包装器
        '''
        self.cur.execute(f'insert into {self.wrapper_table}(name, session_type, code) values (?,?,?)',
            (name, json.dumps(supported_session_types), pycode))
        self.conn.commit()

db_data = DbData(os.path.join(os.path.dirname(__file__), 'wrapper.db'))
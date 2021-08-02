from src.api.maintype.info import SessionConfig, SessionType
from typing import Dict, List, NewType, Tuple, Union, final
import sqlite3
import json
import pickle
import os

Name = NewType('Name', str)  # 名称类型
ID = NewType('ID', int)  # id类型
PyCode = NewType('PyCode', bytes)  # Python代码字节流


@final
class DbData:
    '''提供简易数据操作
    '''

    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.table_name = 'webshell'
        self.cur = self.conn.cursor()

        # 初始化数据库
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name}(\
            webshell_id INTEGER PRIMARY KEY,name TEXT, session_type TEXT, code BLOB)')
        self.conn.commit()

    def get_webshell(self, webshell_id: int) -> Union[Tuple[ID, Name, SessionType, PyCode], None]:
        '''获取指定webshell

        :param webshell_id: webshell id
        :returns: 类似(1,'my wrapper','php',b'python code') 其中元组元素的第一个为webshell id，第二个为包装器名称，第三个为支持的session类型，第四个为对应的Python代码字节流。失败返回None
        '''
        self.cur.execute(
            f'select * from {self.table_name} where webshell_id=?', (webshell_id,))
        data = self.cur.fetchone()
        if data is None:
            return None
        result = list(data)
        try:
            result[2] = SessionType[data['session_type']]
        except:
            return None
        return tuple(result)

    def set_webshell(self, webshell_id: Union[int, None], name: Union[str, None], session_type: Union[SessionType, None], code: Union[bytes, None]) -> bool:
        '''更新webshell信息，当webshe_id存在时更新webshell信息（此时若name、session_type或code为None则删除该条信息），否则新增一条webshell信息

        :param webshell_id: webshell信息
        :param name: webshell的名称
        :param session_type: webshell支持的session类型
        :param code: webshell对应的Python代码字节流
        :returns: 成功返回True，否则返回False
        '''
        self.cur.execute(
            f'select * from {self.table_name} where webshell_id=?', (webshell_id,))
        row = self.cur.fetchone()
        try:
            if row is None:
                if None in (name, session_type, code):
                    return False
                else:  # 新增webshell
                    self.cur.execute(f'insert into {self.table_name}(name, session_type, code) values (?,?,?)',
                                     (name, session_type, code))
            else:
                if None in (name, session_type, code):
                    self.cur.execute(
                        f'delete from {self.table_name} where webshell_id=?', (webshell_id,))
                else:
                    self.cur.execute(f'update {self.table_name} set name=?,session_type=?,code=?',
                                     (name, session_type, code))
            self.conn.commit()
        except:
            return False
        return True

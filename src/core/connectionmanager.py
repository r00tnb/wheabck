from src.api.maintype.info import SessionOptions, SessionType, ServerInfo
import src.config as config
import sqlite3
from typing import Dict, List, Union
import json
import pickle

__all__ = ['Connection', 'connection_manager']

class Connection:
    '''描述webshell连接的属性，session需要通过该类来初始化
    '''

    def __init__(self) -> None:
        self.conn_id = -1
        self.options = SessionOptions()
        self.session_type = SessionType.PHP
        self.server_info = ServerInfo()


class ConnectionManager:
    '''用于管理记录的webshell连接
    '''

    def __init__(self) -> None:
        self.conn = sqlite3.connect(config.db_path)
        self.cur = self.conn.cursor()

        self.json_table_name = 'json_data'
        self.conn_table_name = 'webshell_connections'

        # 初始化数据库
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.json_table_name}(\
            conn_id INTEGER,name TEXT, data TEXT)')
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.conn_table_name}(\
            conn_id INTEGER PRIMARY KEY, connection BLOB)') # connection字段为Connection对象的序列化值
        self.conn.commit()

    def get_json_data(self, conn_id:int, name:str)->Union[Union[dict,list], None]:
        '''获取指定的json数据
        '''
        self.cur.execute(f'select * from {self.json_table_name} where conn_id=? and name=?', (conn_id, name))
        row = self.cur.fetchone()
        if row is None:
            return None
        try:
            return json.loads(row['data'])
        except:
            return None

    def add_json_data(self, conn_id:int, name:str, data:Union[dict,list])->bool:
        '''添加新的json数据
        '''
        try:
            self.cur.execute(f'insert into {self.json_table_name}(conn_id, name, data) values (?,?,?)', (
                conn_id, name, json.dumps(data)))
            self.conn.commit()
            return True
        except:
            return False
        
    def update_json_data(self, conn_id:int, name:str, data:Union[dict,list])->bool:
        '''更新指定的json数据
        '''
        try:
            self.cur.execute(f'update {self.json_table_name} set data=? where conn_id=? and name=?', (json.dumps(data),
                conn_id, name))
            self.conn.commit()
            return True
        except:
            return False

    def del_json_data(self, conn_id:int, name:str):
        '''删除指定的json数据
        '''
        self.cur.execute(f'delete from {self.json_table_name} where conn_id=? and name=?', (conn_id, name))
        self.conn.commit()

    def del_connection(self, conn_id:int):
        '''删除指定连接
        '''
        self.cur.execute(f'delete from {self.conn_table_name} where conn_id=?', (conn_id, ))
        self.conn.commit()

    def get_all_connections(self)->List[Connection]:
        '''获取所有保存的连接
        '''
        self.cur.execute(f'select * from {self.conn_table_name}')
        ret = []
        for row in self.cur.fetchall():
            try:
                conn:Connection = pickle.loads(row['connection'])
                conn.conn_id = row['conn_id'] # 防止两个id不一致
                ret.append(conn)
            except:
                continue
        return ret

    def get_connection(self, conn_id:int)->Union[Connection, None]:
        '''获取指定的连接
        '''
        self.cur.execute(f'select * from {self.conn_table_name} where conn_id=?', (conn_id,))
        row = self.cur.fetchone()
        if row is None:
            return None
        try:
            conn:Connection = pickle.loads(row['connection'])
            conn.conn_id = row['conn_id'] # 防止两个id不一致
            return conn
        except:
            return None

    def update_connection(self, connection:Connection)->bool:
        '''更新指定的连接信息
        '''
        try:
            self.cur.execute(f'update {self.conn_table_name} set connection=? where conn_id=?', 
                (pickle.dumps(connection), connection.conn_id))
            self.conn.commit()
            return True
        except:
            return False

    def add_connection(self, connection:Connection)->bool:
        '''添加新的连接
        '''
        try:
            self.cur.execute(f'insert into {self.conn_table_name}(connection) values (?)', (pickle.dumps(connection),))
            self.conn.commit()
            return True
        except:
            return False


connection_manager = ConnectionManager()
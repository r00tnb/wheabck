from src.api.maintype.service import Service
from src.api.servicefactory import ServiceFactory
from flask_socketio import SocketIO
from src.api.maintype.info import SessionOptions, SessionType
from typing import Union
from src.core.sessionadapter import SessionAdapter
from flask import session, request, Flask
from src.core.pluginmanager import plugin_manager
from src.core.sessionmanager import session_manager
from src.core.connectionmanager import connection_manager, Connection

class WebApi:
    '''为插件注册web api。约定前后端通信使用json数据类型
    '''

    def __init__(self, socketio:SocketIO, app:Flask):
        self.socketio = socketio
        self.app = app

    def register_api_for_session(self, session:SessionType):
        '''为session注册所有插件的service api
        '''
        for plugin in session.plugins_list:
            if isinstance(plugin, ServiceFactory):
                plugin:ServiceFactory = plugin
                for ser in plugin.services_list:
                    if ser.need_reply:
                        @self.app.route(f'/{session.session_id}/http/{plugin.name}/{ser.name}', methods=['POST'])
                        def handler():
                            return plugin.handler(Service(ser.name, request.json, True))
                    else:
                        @self.socketio.on(f'{plugin.name}_{ser.name}', f'/{session.session_id}/ss')
                        def handler(data):
                            plugin.handler(Service(ser.name, data, False))

    def register_main_api(self):
        '''注册全局api
        '''
        app = self.app

        def _(path:str)->str:
            '''返回正确的路由路径
            '''
            return f'/global-api/{str}'

        def r(data:Union[list,dict]={}, code=0, msg='ok')->dict:
            '''构造标准的响应数据
            '''
            return {
                'code':code,
                'msg':msg,
                'data':data
            }

        @app.route('/')
        def index():
            '''访问时加载所有插件，完成初始化
            '''
            if session.get('need_init', True):
                plugin_manager.load_all_plugin()
                session['need_init'] = False

        @app.route(_('/add-session/<int:conn_id>'))
        def add_session(conn_id:int):
            '''添加一个新的session
            '''
            conn = connection_manager.get_connection(conn_id)
            if conn is None:
                return r({}, -1, 'error')

            session = SessionAdapter(conn)
            session.load_plugins()
            self.register_api_for_session(session)
            session_manager.add_session(session)
            return r({'session_id':session.session_id})

        @app.route(_('/del-session/<session_ids>'))
        def del_session(session_ids:str):
            '''批量删除指定session， 以逗号分割id值
            '''
            ids = session_ids.split(',')
            for i in ids:
                session_manager.del_session(i)
            return r()

        @app.route(_('/add-connection'), methods=['POST'])
        def add_connection():
            '''根据前端传来的配置新建一个连接
            '''
            data:dict = request.get_json(True, True)
            if data is None or not isinstance(data) or data.get('options') is None \
                or data.get('session_type') is None:
                return r(code=-1, msg='params error!')
            conn = Connection()
            conn.options = SessionOptions.from_dict(data['options'])
            conn.session_type = data['session_type']
            if connection_manager.add_connection(conn):
                return r()
            return r(code=-1, msg='error')

        @app.route(_('/del-connection/<conn_ids>'))
        def del_connection(conn_ids:str):
            '''批量删除指定的连接，以逗号分割id值
            '''
            ids = conn_ids.split(',')
            for i in ids:
                connection_manager.del_connection(int(i))
            return r()
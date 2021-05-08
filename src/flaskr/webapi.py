from flask_socketio import SocketIO, emit
from flask import Flask, request, jsonify
from src.core.pluginmanager import plugin_manager
from src.api.maintype import Message
from src.api.messagethandler import MessageHandler
from src.api.session import Session
import src.utils as utils

class WebApi:
    '''为插件注册web api。约定前后端通信使用json数据类型
    '''

    def __init__(self, socketio:SocketIO, app:Flask):
        self.socketio = socketio
        self.app = app

    def register_api_for_session(self, session:Session):
        '''为session注册所有插件的api
        '''
        for plugin in session.plugins_list:
            if isinstance(plugin, MessageHandler):
                for msg in plugin.messages:
                    if msg.need_reply:
                        @self.app.route(f'/{session.session_id}/http/{plugin.name}/{msg.name}', methods=['POST'])
                        def handler():
                            m = Message(msg.name, request.json, True)
                            return plugin.handler(m)
                    else:
                        @self.socketio.on(f'{plugin.name}_{msg.name}', f'/{session.session_id}/ss')
                        def handler(data):
                            m = Message(msg.name, data, False)
                            plugin.handler(m)

    def register_main_api(self):
        '''注册全局api
        '''
        namespace = '/global-api'
        @self.app.route(namespace+'/get-menus', methods=['GET'])
        def get_menus():
            menus = [
                {}
            ]
            return jsonify(menus)
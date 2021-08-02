from src.flaskr import create_app
from flask_socketio import SocketIO
from src.flaskr.webapi import WebApi

if __name__ == "__main__":
    app = create_app()
    socketio = SocketIO(app)
    webapi = WebApi(socketio, app)
    webapi.register_main_api()
    
    socketio.run(app, debug=True)
import os
import src.config as config
from flask import Flask

path = os.path.join(os.path.dirname(__file__), 'instance')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, instance_path=path, static_folder=config.static_path, static_url_path='')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    return app

from api.plugin import Plugin
from api.helper import Helper
import os

class plugin(Plugin):

    def __init__(self, helper:Helper):
        super().__init__(helper)

    @property
    def name(self)->str:
        return "connection-manage"
    
    @property
    def static_dir(self)->str:
        return os.path.join(os.path.dirname(__file__), 'ui', 'public', 'dist')
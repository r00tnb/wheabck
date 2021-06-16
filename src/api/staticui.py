import abc

class StaticUI(metaclass=abc.ABCMeta):
    '''插件若需要前端页面等则需要继承并实现该类.一旦继承该类就认为插件具有前端页面，且在展示时加载目录下的index.html文件
    '''

    @abc.abstractproperty
    def static_dir(self)->str:
        '''返回当前插件的静态目录绝对路径，若插件有前端页面则可以返回它的目录路径。

        :returns: str
        '''
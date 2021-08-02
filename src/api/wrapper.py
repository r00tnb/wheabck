import abc


class Wrapper(metaclass=abc.ABCMeta):
    '''用于对payload代码进行包装处理
    '''

    @abc.abstractmethod
    def wrap(self, payload:bytes)->bytes:
        '''对传入的payload字节流进行处理，并返回处理后的结果

        :params payload: payload的字节流
        :returns: 处理结果
        '''
    
    
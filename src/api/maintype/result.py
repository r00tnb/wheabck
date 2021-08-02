

class RequestData:
    '''描述HTTP请求数据
    '''

    def __init__(self) -> None:
        self.__headers = {}
        self.__cookies = {}


class EvalResult:
    '''描述代码执行结果
    '''
    def __init__(self) -> None:
        self.__raw_data = b''

    def rawdata(self)->bytes:
        '''返回执行代码后的原始数据

        :returns: bytes
        '''
        return self.__raw_data

    @abc.abstractproperty
    def data(self)->bytes:
        '''返回执行代码后的数据，它可能是经过处理的数据

        :returns: bytes
        '''
        pass

    def is_failed(self)->bool:
        '''执行成功返回True，否则False

        :returns: bool
        '''
        pass
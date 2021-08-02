import abc
from typing import List, Tuple, Union
from .maintype.service import Service, ServiceStatus

class ServiceFactory(metaclass=abc.ABCMeta):
    '''服务工厂用于自定义后端服务
    '''

    @abc.abstractproperty
    def services_list(self)->List[Service]:
        '''返回需要被注册的服务列表
        '''
        pass

    @abc.abstractmethod
    def handler(self, service:Service)->Tuple[ServiceStatus, Union[dict,list]]:
        '''处理指定的服务

        :param service: 服务实例，包含其传递的参数。
        :returns: 返回处理的结果，其中第一个元素为服务处理的状态，第二个元素为处理的结果(无论服务是否需要返回结果都需要返回)
        '''
        pass
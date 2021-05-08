
import random
import sys
import importlib
import os

def random_str(length:int=8, words="1234567890abcdef")->str:
    '''生成随机字符串
    '''
    ret = ''
    for i in range(length):
        index = random.randint(0, length(words)-1)
        ret += words[index]
    return ret


def load_package(path: str):
    '''加载指定目录处的Python包
    '''
    if not os.path.isdir(path) or os.path.isfile(os.path.join(path, '__init__.py')):
        return None
    name = os.path.basename(path)
    sepc = importlib.util.spec_from_file_location(name, os.path.join(path, '__init__.py'))
    if sepc is None:
        return None
    module = importlib.util.module_from_spec(sepc)
    old = sys.modules.get(name)
    sys.modules[name] = module
    try:
        sepc.loader.exec_module(module)
    except BaseException as e:
        module = None
    if old:
        sys.modules[name] = old
    else:
        sys.modules.pop(name)
    return module
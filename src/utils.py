
import random
import sys
import importlib.util
import os
import traceback
from types import ModuleType
from typing import NoReturn, Union
import tempfile

def random_str(length:int=8, words="1234567890abcdef")->str:
    '''生成随机字符串
    '''
    ret = ''
    for i in range(length):
        index = random.randint(0, length(words)-1)
        ret += words[index]
    return ret

def print_traceback()->NoReturn:
    '''输出堆栈信息
    '''
    traceback.print_exc()

def load_module_from_bytes(code:bytes)->Union[ModuleType, None]:
    '''从字节流加载Python模块
    '''
    fd, fpath = tempfile.mkstemp()
    with open(fpath, 'wb') as f:
        f.write(code)
    m = load_module(fpath)
    os.unlink(fpath)
    return m

def load_module(path: str)->Union[ModuleType, None]:
    '''加载指定位置处的Python模块
    '''
    def load(file_path:str, name:str=None)->Union[ModuleType, None]:
        sepc = importlib.util.spec_from_file_location(name, file_path)
        if sepc is None:
            return None
        module:Union[ModuleType, None] = importlib.util.module_from_spec(sepc)
        old = sys.modules.get(name)
        if name is not None:
            sys.modules[name] = module
        try:
            sepc.loader.exec_module(module)
        except BaseException as e:
            module = None
        if name is not None:
            if old:
                sys.modules[name] = old
            else:
                sys.modules.pop(name)
        return module

    if os.path.isdir(path):# 如果是目录则当做Python包加载
        name = os.path.basename(path)
        path = os.path.join(path, '__init__.py')
        if not os.path.isfile(path):
            return None
        else:
            return load(path, name)
    elif os.path.isfile(path) and path.lower().endswith(".py"):
        return load(path)
    else:
        return None

def call_path(floor=1)-> str:
    '''返回调用该函数时指定层数的文件绝对路径,默认返回调用该函数时所在的文件路径

    :params floor: 指定调用该函数时调用栈的层序数（从最低层1开始），将会返回该层的文件路径.
    :returns: 返回指定调用栈所在的文件绝对路径
    '''
    stack = traceback.extract_stack()
    return os.path.abspath(stack[-floor-1].filename)

def file_get_content(fpath:str)->Union[bytes, None]:
    '''获取指定文件的内容

    :params fpath: 一个系统中的文件路径
    :returns: 返回文件内容的字节流，失败返回None
    '''
    if not os.path.isfile(fpath):
        return None
    with open(fpath, 'rb') as f:
        return f.read()

def file_set_content(fpath:str, content:bytes)->Union[int, None]:
    '''向指定文件路径写入字节流内容

    :params fpath: 一个系统中的文件路径，若存在多级目录不存在则写入会失败
    :params content: 向文件写入的字节流内容
    :returns: 返回写入的字节数，失败返回None
    '''
    try:
        with open(fpath, 'wb') as f:
            return f.write(content)
    except:
        return None
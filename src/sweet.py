from typing import Collection, Callable
from importlib import import_module


def peek_count(collection: Collection) -> None:
    """简单打印一下某个集合的数量"""
    print("count: ", len(collection))


def import_from_string(module_name: str, func_name: str) -> Callable:
    """从模块中导入方法"""
    module = import_module(module_name)
    func = getattr(module, func_name)
    return func

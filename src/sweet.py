import json
import re
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


def extract_json_values_by_path(data: dict | str, *path, safely: bool = True):
    """根据路径获取JSON的值"""
    if isinstance(data, str):
        data = json.loads(data)

    # 定义一个递归函数来遍历给定路径
    def traverse(data, *keys):
        # 如果已经没有更多的key，返回当前的数据
        if not keys:
            return data

        # 获取当前的keys中的一个
        current_key, *remaining_keys = keys

        # 如果当前的key存在于数据中
        if isinstance(data, list) and current_key.isdigit():
            # 假设当前的key是数字，意味着它是列表中的索引
            current_index = int(current_key)
            return traverse(data[current_index], *remaining_keys)
        elif isinstance(data, list):
            # 如果数据本身是列表，则遍历每个元素
            return [traverse(elem, *keys) for elem in data]
        elif isinstance(data, dict) and current_key in data:
            # 如果数据是字典，则直接进入下一个层级
            return traverse(data[current_key], *remaining_keys)
        else:
            # 如果路径不正确，返回None或抛出异常
            if safely:
                return None

            raise KeyError("JSON路径有错！")

    # 从JSON数据的根部开始遍历
    return traverse(data, *path)


def is_equivalent_naming(name1: str, name2: str) -> bool:
    """
    判断大小驼峰或者蛇形是否相等
    """

    def normalize(s: str) -> str:
        # 将大驼峰和小驼峰转换为蛇形
        s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
        s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
        # 转换为小写
        return s.lower()

    return normalize(name1) == normalize(name2)

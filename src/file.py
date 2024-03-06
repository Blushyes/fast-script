import os
from dataclasses import dataclass
from typing import Callable, Collection


@dataclass
class FileInfo:
    name: str
    content: str
    abspath: str
    relpath: str


def loads_file(path: str, safely=False) -> str:
    """读取某个文件的文本内容，utf-8编码

    Args:
        path: 文件的路径
        safely: 如果为 true 则遇见异常的时候不会报错


    Returns:
        str: 文件所有的内容，UTF-8编码，如果文件不存在或者出现其他异常，返回一个空串
    """

    try:
        with open(path, "r", encoding="utf8") as f:
            return f.read()
    except Exception as e:
        if safely:
            return ""
        raise e


def list_files_recursive(
        directory: str = os.path.curdir,
        exclude: Collection[str] | str = None,
        file_filter: Callable[[FileInfo], bool] | Collection[
            Callable[[FileInfo], bool]] = None,
        safely=True,
) -> list[FileInfo]:
    """递归列出所有的文件，默认为当前目录下面所有文件

    Args:
        directory: 目录
        exclude: 排除哪个或者哪些文件，只是简单地排除某个文件名或者目录名
        file_filter: 过滤器，可以更自由地定义排除哪些文件，可以是列表也可以是单个
        safely: 如果为 true 则遇见异常的时候不会报错

    Returns:
        收集到的所有文件信息
    """
    files_list = []

    # 转换一下参数
    if isinstance(exclude, str):
        exclude = [exclude]

    if isinstance(file_filter, Callable):
        file_filter = [file_filter]

    # 使用os.walk遍历目录
    for root, _, files in os.walk(directory):
        for file in files:
            filename = os.path.basename(file)

            # 使用os.path.join拼接完整的文件路径
            full_path = os.path.join(root, file)

            if exclude and any(
                    filename == name or name in full_path for name in exclude
            ):
                continue

            # 使用os.path.relpath获取相对路径
            relative_path = os.path.relpath(full_path, directory)

            file_info = FileInfo(
                name=filename,
                content=loads_file(relative_path, safely),
                abspath=full_path,
                relpath=relative_path,
            )

            files_list.append(file_info)

    filtered_list = None
    if file_filter:
        filtered_list = files_list
        for e in file_filter:
            filtered_list = filter(e, filtered_list)

    return list(filtered_list) if filtered_list else files_list


def write_text(text: str, file_path: str, safely=False) -> None:
    """以utf-8编码写入文本到某个文件"""
    try:
        with open(file_path, "w", encoding="utf8") as f:
            f.write(text)
    except Exception as e:
        if not safely:
            raise e


class FileProcessChain:
    def __init__(self):
        self._path: str | None = None
        self._safely: bool = False
        self._exclude_files: list[str] = []
        self._filters: list[Callable[[FileInfo], bool]] = []

    def path(self, path: str) -> 'FileProcessChain':
        self._path = path
        return self

    def safely(self) -> 'FileProcessChain':
        self._safely = True
        return self

    def exclude(self, *name: str) -> 'FileProcessChain':
        self._exclude_files.extend(name)
        return self

    def filter(self, filter_func: Callable[[FileInfo], bool]) -> 'FileProcessChain':
        self._filters.append(filter_func)
        return self

    def collect(self) -> list[FileInfo]:
        if self._path is None:
            raise Exception("path is required")

        return list_files_recursive(self._path, self._exclude_files, self._filters, self._safely)

    def safe_collect(self) -> list[FileInfo]:
        return self.safely().collect()

import os
from dataclasses import dataclass
from typing import Callable


@dataclass
class FileInfo:
    name: str
    content: str
    abspath: str
    relpath: str


def loads_file(path: str, safely=False) -> str:
    """读取某个文件的内容

    Args:
        path (str): 文件的路径

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
    exclude: list[str] | str = None,
    file_filter: Callable[[FileInfo], list[FileInfo]] = None,
) -> list[FileInfo]:
    """递归列出所有的文件，默认为当前目录下面所有文件

    Args:
        exclude: 排除哪个或者哪些文件，只是简单地排除某个文件名或者目录名。
        file_filter: 过滤器，可以更自由地定义排除哪些文件。

    Returns:
        收集到的所有文件信息
    """
    files_list = []

    # 转换一下参数
    if isinstance(exclude, str):
        exclude = [exclude]

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
                content=loads_file(relative_path),
                abspath=full_path,
                relpath=relative_path,
            )

            files_list.append(file_info)

    return list(filter(file_filter, files_list)) if files_list else files_list

from functools import reduce
import requests
from lxml import etree
from typing import Any, Collection, Callable
from sweet import import_from_string


def html_xpath_crawler(url: str, xpath: str, **kwargs) -> Any:
    """基于HTML和XPATH的简单页面爬虫

    Args:
        **kwargs: 这个为requests.get()的额外参数比如header

    Examples:
        html_xpath_crawler('https://www.baidu.com', '//div/text()')
        html_xpath_crawler('https://www.baidu.com', '//div/text()', headers=headers)
    """
    res = requests.get(url, **kwargs)
    text = res.text
    html = etree.HTML(text)
    contents = html.xpath(xpath)
    return contents


def json_crawler(
    url: str,
    method: str = "get",
    getter: None
    | str
    | Collection[str | int]
    | Collection[Collection[str | int]]
    | Callable[[dict], any] = None,
    **kwargs
) -> Any:
    """
    从给定的URL抓取JSON数据，并可以选择性地提取特定的数据。

    使用指定的HTTP方法从给定的URL请求数据，将返回的内容解析为JSON，
    并且根据提供的`getter`来检索JSON内部的特定数据。

    Args:
        getter: 用来从返回的JSON数据中提取特定数据的参数。此参数有多种形式：
            - 如果是None，将返回整个JSON。
            - 如果是字符串，会被看做是JSON对象内的属性路径，用'.'分隔（例如"results.0.name"）。
            - 如果是字符串或整数的集合，会依序检索每个键或索引（例如['results', 0, 'name']）。
            - 如果是集合的集合，会返回一个列表，其中包含通过每个子集合检索的数据（例如[['results', 0, 'name'], ['info', 'count']]）。
            - 如果是函数，将以整个JSON对象为参数调用此函数，并返回结果。
        **kwargs: 传递给请求函数的额外关键字参数。

    Returns:
        Any: 如果未指定`getter`，返回的是整个JSON对象。如果指定了`getter`，返回的类型取决于`getter`的行为。

    Raises:
        KeyError: 如果`getter`指定的路径不存在，会抛出KeyError。
        RequestException: 如果HTTP请求失败，会抛出requests库的RequestException。

    Example:
        # 获取整个JSON数据
        all_data = json_crawler("https://example.com/api/data")

        # 获取嵌套JSON内的特定值
        specific_value = json_crawler("https://example.com/api/data", getter="results.0.name")

        # 使用字符串和整数的集合来获取嵌套数据
        nested_value = json_crawler("https://example.com/api/data", getter=['results', 0, 'name'])

        # 处理列表中不同路径的数据
        multiple_values = json_crawler("https://example.com/api/data", getter=[['results', 0], ['info']])

        # 使用自定义函数来处理数据
        def custom_process(json_data):
            return [item['name'] for item in json_data['results']]
        processed_data = json_crawler("https://example.com/api/data", getter=custom_process)
    """
    request_func = import_from_string("requests", method)
    res = request_func(url, **kwargs).json()
    if getter is None:
        return res

    if isinstance(getter, str):
        getter = getter.split(".")

    if isinstance(getter, Collection):
        if all(isinstance(it, str) or isinstance(it, int) for it in getter):
            return reduce(lambda d, key: d[key], getter, res)

        if all(isinstance(it, Collection) for it in getter):
            return [reduce(lambda d, key: d[key], it, res) for it in getter]

    if isinstance(getter, Callable):
        return getter(res)

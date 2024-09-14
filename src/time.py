import re


def parse_time_to_ms(time_str):
    # 定义时间单位到毫秒的转换字典
    time_units = {
        "ms": 1,
        "s": 1000,
        "sec": 1000,
        "min": 60 * 1000,
        "h": 60 * 60 * 1000,
        "hour": 60 * 60 * 1000,
        "d": 24 * 60 * 60 * 1000,
        "day": 24 * 60 * 60 * 1000,
    }

    # 使用正则表达式匹配数字和单位
    match = re.match(r"^(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?$", time_str.strip())

    if not match:
        raise ValueError(f"Invalid time format: {time_str}")

    value, unit = match.groups()
    value = float(value)

    # 如果没有指定单位，默认为毫秒
    if not unit:
        return int(value)

    # 转换为小写并去除复数的 's'
    unit = unit.lower().rstrip("s")

    if unit not in time_units:
        raise ValueError(f"Unknown time unit: {unit}")

    # 计算并返回毫秒值
    return int(value * time_units[unit])

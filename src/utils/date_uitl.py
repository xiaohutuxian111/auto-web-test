"""
日期处理工具模块

该模块提供了日期时间相关的工具函数，包括日期格式化、时间戳转换等。
"""

from typing import Optional, Literal, Union
import datetime


def 返回当前时间xxxx_xx_xx() -> str:
    """
    返回当前日期的标准格式字符串
    
    Returns:
        str: 当前日期，格式为 'YYYY-MM-DD'
        
    Example:
        >>> 返回当前时间xxxx_xx_xx()
        '2024-01-15'
    """
    return datetime.datetime.now().strftime('%Y-%m-%d')


def 返回当前时间xxxx_xx_xx加N天(
    增加的天数: int, 
    格式: Optional[Literal["使用斜杠分隔符", "使用中划线分隔符", "使用datetime格式", "使用年月日格式"]] = "使用中划线分隔符"
) -> Union[str, datetime.datetime]:
    """
    返回当前时间加上指定天数后的日期
    
    Args:
        增加的天数: 要增加的天数，可以为负数
        格式: 返回格式，可选值：
            - "使用斜杠分隔符": 返回 'YYYY/MM/DD' 格式
            - "使用中划线分隔符": 返回 'YYYY-MM-DD' 格式（默认）
            - "使用datetime格式": 返回 datetime 对象
            - "使用年月日格式": 返回 'YYYY年MM月DD日' 格式
            
    Returns:
        Union[str, datetime.datetime]: 格式化后的日期
        
    Example:
        >>> 返回当前时间xxxx_xx_xx加N天(7)
        '2024-01-22'
        >>> 返回当前时间xxxx_xx_xx加N天(-3, "使用年月日格式")
        '2024年01月12日'
    """
    target_date = datetime.datetime.now() + datetime.timedelta(days=增加的天数)
    
    if 格式 == "使用斜杠分隔符":
        return target_date.strftime("%Y/%m/%d")
    elif 格式 == "使用中划线分隔符":
        return target_date.strftime("%Y-%m-%d")
    elif 格式 == "使用datetime格式":
        return target_date
    elif 格式 == "使用年月日格式":
        return target_date.strftime("%Y年%m月%d日")
    else:
        # 如果提供了自定义格式字符串，使用该格式
        try:
            return target_date.strftime(str(格式))
        except ValueError as e:
            raise ValueError(f"不支持的日期格式: {格式}, 错误: {e}")


def 返回当前时间时间戳() -> float:
    """
    返回当前时间的时间戳
    
    Returns:
        float: 当前时间的时间戳
        
    Example:
        >>> 返回当前时间时间戳()
        1705123456.789
    """
    return datetime.datetime.now().timestamp()


def 返回当前时间戳加N天(增加的天数: int) -> float:
    """
    返回当前时间加上指定天数后的时间戳
    
    Args:
        增加的天数: 要增加的天数，可以为负数
        
    Returns:
        float: 目标时间的时间戳
        
    Example:
        >>> 返回当前时间戳加N天(7)
        1705728256.789
    """
    target_date = datetime.datetime.now() + datetime.timedelta(days=增加的天数)
    return target_date.timestamp()


def 格式化时间戳(timestamp: float, 格式: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    将时间戳格式化为指定格式的字符串
    
    Args:
        timestamp: 时间戳
        格式: 格式化字符串，默认为 "%Y-%m-%d %H:%M:%S"
        
    Returns:
        str: 格式化后的时间字符串
        
    Example:
        >>> 格式化时间戳(1705123456.789)
        '2024-01-15 10:30:56'
    """
    try:
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime(格式)
    except (ValueError, OSError) as e:
        raise ValueError(f"无效的时间戳: {timestamp}, 错误: {e}")


def 解析日期字符串(date_str: str, 格式: str = "%Y-%m-%d") -> datetime.datetime:
    """
    解析日期字符串为datetime对象
    
    Args:
        date_str: 日期字符串
        格式: 日期格式，默认为 "%Y-%m-%d"
        
    Returns:
        datetime.datetime: 解析后的datetime对象
        
    Raises:
        ValueError: 当日期字符串格式不正确时
        
    Example:
        >>> 解析日期字符串("2024-01-15")
        datetime.datetime(2024, 1, 15, 0, 0)
    """
    try:
        return datetime.datetime.strptime(date_str, 格式)
    except ValueError as e:
        raise ValueError(f"无法解析日期字符串 '{date_str}' 使用格式 '{格式}': {e}")


def 计算日期差(开始日期: Union[str, datetime.datetime], 
              结束日期: Union[str, datetime.datetime], 
              格式: str = "%Y-%m-%d") -> int:
    """
    计算两个日期之间的天数差
    
    Args:
        开始日期: 开始日期，可以是字符串或datetime对象
        结束日期: 结束日期，可以是字符串或datetime对象
        格式: 当输入为字符串时使用的格式，默认为 "%Y-%m-%d"
        
    Returns:
        int: 天数差（结束日期 - 开始日期）
        
    Example:
        >>> 计算日期差("2024-01-01", "2024-01-15")
        14
    """
    # 确保两个日期都是datetime对象
    if isinstance(开始日期, str):
        开始日期 = 解析日期字符串(开始日期, 格式)
    if isinstance(结束日期, str):
        结束日期 = 解析日期字符串(结束日期, 格式)
    
    return (结束日期 - 开始日期).days

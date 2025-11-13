"""
Pandas数据处理工具模块

该模块提供了基于pandas的DataFrame处理工具函数，包括数据清理、转换等操作。
"""

from typing import Union, List, Dict, Any

import pandas as pd
from pandas import DataFrame


def delete_rows_by_all_none(df: DataFrame) -> DataFrame:
    """
    删除所有行全为空的数据
    
    Args:
        df: 输入的DataFrame
        
    Returns:
        DataFrame: 删除空行后的DataFrame
        
    Example:
        >>> df = pd.DataFrame({'A': [1, None, 3], 'B': [None, None, None]})
        >>> result = delete_rows_by_all_none(df)
        >>> print(result)
           A    B
        0  1  NaN
        2  3  NaN
    """
    return df.dropna(how='all').reset_index(drop=True)


def delete_rows_by_index(df: DataFrame, index: Union[int, List[int]]) -> DataFrame:
    """
    删除指定索引的行
    
    Args:
        df: 输入的DataFrame
        index: 要删除的行索引，可以是单个索引或索引列表
        
    Returns:
        DataFrame: 删除指定行后的DataFrame
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> result = delete_rows_by_index(df, [0, 2])
        >>> print(result)
           A  B
        1  2  5
    """
    return df.drop(index=index, axis=0).reset_index(drop=True)


def rename_df(df: DataFrame, columns: Dict[str, str]) -> DataFrame:
    """
    重命名DataFrame的列
    
    Args:
        df: 输入的DataFrame
        columns: 列名映射字典，格式为 {旧列名: 新列名}
        
    Returns:
        DataFrame: 重命名列后的DataFrame
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> result = rename_df(df, {'A': 'X', 'B': 'Y'})
        >>> print(result)
           X  Y
        0  1  3
        1  2  4
    """
    return df.rename(columns=columns)


def fillna_with_empty(df: DataFrame) -> DataFrame:
    """
    将DataFrame中的NaN值填充为空字符串
    
    Args:
        df: 输入的DataFrame
        
    Returns:
        DataFrame: 填充后的DataFrame
        
    Example:
        >>> df = pd.DataFrame({'A': [1, None, 3], 'B': ['a', 'b', None]})
        >>> result = fillna_with_empty(df)
        >>> print(result)
             A  B
        0    1  a
        1       b
        2    3
    """
    return df.fillna("")


def filter_df_by_condition(df: DataFrame, condition: Dict[str, Any]) -> DataFrame:
    """
    根据条件过滤DataFrame
    
    Args:
        df: 输入的DataFrame
        condition: 过滤条件字典，格式为 {列名: 值}
        
    Returns:
        DataFrame: 过滤后的DataFrame
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        >>> result = filter_df_by_condition(df, {'A': 2})
        >>> print(result)
           A  B
        1  2  b
    """
    mask = pd.Series([True] * len(df), index=df.index)
    for column, value in condition.items():
        if column in df.columns:
            mask &= (df[column] == value)
    return df[mask].reset_index(drop=True)


def get_unique_values(df: DataFrame, column: str) -> List[Any]:
    """
    获取指定列的唯一值列表
    
    Args:
        df: 输入的DataFrame
        column: 列名
        
    Returns:
        List[Any]: 唯一值列表
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 1, 3], 'B': ['a', 'b', 'a', 'c']})
        >>> result = get_unique_values(df, 'A')
        >>> print(result)
        [1, 2, 3]
    """
    if column not in df.columns:
        raise ValueError(f"列 '{column}' 不存在于DataFrame中")
    return df[column].unique().tolist()


def count_values(df: DataFrame, column: str) -> Dict[Any, int]:
    """
    统计指定列的值出现次数
    
    Args:
        df: 输入的DataFrame
        column: 列名
        
    Returns:
        Dict[Any, int]: 值计数字典
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 1, 3, 1]})
        >>> result = count_values(df, 'A')
        >>> print(result)
        {1: 3, 2: 1, 3: 1}
    """
    if column not in df.columns:
        raise ValueError(f"列 '{column}' 不存在于DataFrame中")
    return df[column].value_counts().to_dict()

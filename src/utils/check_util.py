"""
检查工具模块

该模块提供了各种数据检查和验证功能，包括字典比较、数据验证等。
"""

from typing import Dict, Any, Optional


def check_dict(dict1: Dict[str, Any], dict2: Dict[str, Any], strict_mode: bool = False) -> bool:
    """
    检查两个字典是否相同
    
    Args:
        dict1: 第一个字典
        dict2: 第二个字典
        strict_mode: 是否严格模式，默认为False
            - True: 检查所有键是否相同
            - False: 只检查共同存在的键
            
    Returns:
        bool: 两个字典是否相同
        
    Example:
        >>> dict1 = {'a': 1, 'b': 2}
        >>> dict2 = {'a': 1, 'c': 3}
        >>> check_dict(dict1, dict2, strict_mode=False)
        True
        >>> check_dict(dict1, dict2, strict_mode=True)
        False
    """
    if strict_mode:
        # 严格模式：检查所有键是否相同
        if set(dict1.keys()) != set(dict2.keys()):
            return False
        # 检查所有键值对是否相同
        return all(dict1[key] == dict2[key] for key in dict1)
    else:
        # 非严格模式：只检查共同存在的键
        common_keys = set(dict1.keys()) & set(dict2.keys())
        return all(dict1[key] == dict2[key] for key in common_keys)


def validate_required_fields(data: Dict[str, Any], required_fields: list) -> tuple[bool, list]:
    """
    验证字典中是否包含所有必需字段
    
    Args:
        data: 要验证的字典
        required_fields: 必需字段列表
        
    Returns:
        tuple[bool, list]: (是否验证通过, 缺失字段列表)
        
    Example:
        >>> data = {'name': '张三', 'age': 25}
        >>> required = ['name', 'email']
        >>> is_valid, missing = validate_required_fields(data, required)
        >>> print(f"验证通过: {is_valid}, 缺失字段: {missing}")
        验证通过: False, 缺失字段: ['email']
    """
    missing_fields = [field for field in required_fields if field not in data]
    return len(missing_fields) == 0, missing_fields


def check_data_type(data: Any, expected_type: type) -> bool:
    """
    检查数据类型是否符合预期
    
    Args:
        data: 要检查的数据
        expected_type: 期望的数据类型
        
    Returns:
        bool: 数据类型是否符合预期
        
    Example:
        >>> check_data_type(123, int)
        True
        >>> check_data_type("123", int)
        False
    """
    return isinstance(data, expected_type)


def validate_numeric_range(value: float, min_value: Optional[float] = None, 
                          max_value: Optional[float] = None) -> bool:
    """
    验证数值是否在指定范围内
    
    Args:
        value: 要验证的数值
        min_value: 最小值（可选）
        max_value: 最大值（可选）
        
    Returns:
        bool: 数值是否在范围内
        
    Example:
        >>> validate_numeric_range(5, min_value=0, max_value=10)
        True
        >>> validate_numeric_range(15, min_value=0, max_value=10)
        False
    """
    if not isinstance(value, (int, float)):
        return False
    
    if min_value is not None and value < min_value:
        return False
    
    if max_value is not None and value > max_value:
        return False
    
    return True


def check_string_length(text: str, min_length: Optional[int] = None, 
                       max_length: Optional[int] = None) -> bool:
    """
    检查字符串长度是否在指定范围内
    
    Args:
        text: 要检查的字符串
        min_length: 最小长度（可选）
        max_length: 最大长度（可选）
        
    Returns:
        bool: 字符串长度是否在范围内
        
    Example:
        >>> check_string_length("hello", min_length=3, max_length=10)
        True
        >>> check_string_length("hi", min_length=3, max_length=10)
        False
    """
    if not isinstance(text, str):
        return False
    
    length = len(text)
    
    if min_length is not None and length < min_length:
        return False
    
    if max_length is not None and length > max_length:
        return False
    
    return True







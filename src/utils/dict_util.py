"""
字典处理工具模块

该模块提供了字典相关的工具函数，包括键映射、字典比较、数据清理等。
"""

from typing import Dict, Any, List, Optional, Union


def replace_dict_key(dict_info: Dict[Any, Any], mapping: Union[Dict[Any, Any], List[str]]) -> Dict[Any, Any]:
    """
    对字典的键进行映射
    
    Args:
        dict_info: 原始字典
        mapping: 映射规则，可以是字典或字符串列表
            - 字典格式: {旧键: 新键}
            - 列表格式: ['旧键/新键', '旧键2/新键2'] 或 ['键名']（保持不变）
            
    Returns:
        Dict[Any, Any]: 映射后的字典
        
    Example:
        >>> data = {'name': '张三', 'age': 25}
        >>> mapping_dict = {'name': '姓名', 'age': '年龄'}
        >>> result = replace_dict_key(data, mapping_dict)
        >>> print(result)
        {'姓名': '张三', '年龄': 25}
        
        >>> mapping_list = ['name/姓名', 'age/年龄']
        >>> result = replace_dict_key(data, mapping_list)
        >>> print(result)
        {'姓名': '张三', '年龄': 25}
    """
    mapp = {}
    
    if isinstance(mapping, list):
        for key in mapping:
            if '/' in key:
                key1, key2 = key.split('/', 1)
                mapp[key1] = key2
            else:
                mapp[key] = key
    elif isinstance(mapping, dict):
        mapp = mapping
    else:
        raise ValueError("mapping参数必须是字典或列表类型")
    
    return {mapp[primary_key]: dict_info[primary_key] 
            for primary_key in mapp if primary_key in dict_info}


def compare_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any], 
                 strict: bool = False, keys: Optional[List[str]] = None) -> bool:
    """
    比较两个字典是否相同
    """
    if strict:
        return dict1 == dict2

    if not keys:
        raise ValueError("非严格模式下必须提供非空的keys参数")

    for key in keys:
        if '/' in key:
            key1, key2 = key.split('/', 1)
        else:
            key1 = key2 = key

        if dict1.get(key1) != dict2.get(key2):
            return False

    return True


def get_dict_info(info: Dict[str, str]) -> Dict[str, Any]:
    """
    清理字典中的特殊字符和格式
    
    处理以下情况：
    - 去除 '&&' 分隔符，只保留第一个值
    - 去除 '/' 分隔符，只保留最后一个值
    
    Args:
        info: 原始字典
        
    Returns:
        Dict[str, Any]: 清理后的字典
        
    Example:
        >>> data = {'name': '张三&&李四', 'path': 'a/b/c', 'age': '25'}
        >>> result = get_dict_info(data)
        >>> print(result)
        {'name': '张三', 'path': 'c', 'age': '25'}
    """
    cleaned_dict = {}
    
    for key, value in info.items():
        cleaned_value = value
        
        # 处理 '&&' 分隔符，只保留第一个值
        if '&&' in value:
            cleaned_value = value.split('&&')[0]
        
        # 处理 '/' 分隔符，只保留最后一个值
        if '/' in value:
            cleaned_value = value.split('/')[-1]
        
        cleaned_dict[key] = cleaned_value
    
    return cleaned_dict


def merge_dicts(*dicts: Dict[str, Any], overwrite: bool = True) -> Dict[str, Any]:
    """
    合并多个字典
    
    Args:
        *dicts: 要合并的字典
        overwrite: 是否覆盖重复的键，默认为True
        
    Returns:
        Dict[str, Any]: 合并后的字典
        
    Example:
        >>> dict1 = {'a': 1, 'b': 2}
        >>> dict2 = {'b': 3, 'c': 4}
        >>> result = merge_dicts(dict1, dict2)
        >>> print(result)
        {'a': 1, 'b': 3, 'c': 4}
    """
    if not dicts:
        return {}
    
    result = {}
    
    for d in dicts:
        if overwrite:
            result.update(d)
        else:
            # 不覆盖模式，只添加不存在的键
            for key, value in d.items():
                if key not in result:
                    result[key] = value
    
    return result


def filter_dict(dict_info: Dict[str, Any], keys: List[str], 
                include: bool = True) -> Dict[str, Any]:
    """
    过滤字典，保留或排除指定的键
    
    Args:
        dict_info: 原始字典
        keys: 要过滤的键列表
        include: True表示保留指定的键，False表示排除指定的键
        
    Returns:
        Dict[str, Any]: 过滤后的字典
        
    Example:
        >>> data = {'name': '张三', 'age': 25, 'city': '北京'}
        >>> result = filter_dict(data, ['name', 'age'], include=True)
        >>> print(result)
        {'name': '张三', 'age': 25}
        
        >>> result = filter_dict(data, ['city'], include=False)
        >>> print(result)
        {'name': '张三', 'age': 25}
    """
    if include:
        return {key: dict_info[key] for key in keys if key in dict_info}
    else:
        return {key: value for key, value in dict_info.items() if key not in keys}


def flatten_dict(dict_info: Dict[str, Any], separator: str = '.', 
                prefix: str = '') -> Dict[str, Any]:
    """
    扁平化嵌套字典
    
    Args:
        dict_info: 原始字典
        separator: 键分隔符，默认为 '.'
        prefix: 键前缀，默认为空字符串
        
    Returns:
        Dict[str, Any]: 扁平化后的字典
        
    Example:
        >>> data = {'user': {'name': '张三', 'info': {'age': 25}}}
        >>> result = flatten_dict(data)
        >>> print(result)
        {'user.name': '张三', 'user.info.age': 25}
    """
    flattened = {}
    
    for key, value in dict_info.items():
        new_key = f"{prefix}{separator}{key}" if prefix else key
        
        if isinstance(value, dict):
            flattened.update(flatten_dict(value, separator, new_key))
        else:
            flattened[new_key] = value
    
    return flattened


def deep_get(dict_info: Dict[str, Any], path: str, default: Any = None, 
             separator: str = '.') -> Any:
    """
    深度获取字典中的值
    
    Args:
        dict_info: 原始字典
        path: 路径字符串，使用分隔符分隔
        default: 默认值，当路径不存在时返回
        separator: 路径分隔符，默认为 '.'
        
    Returns:
        Any: 获取的值或默认值
        
    Example:
        >>> data = {'user': {'name': '张三', 'info': {'age': 25}}}
        >>> result = deep_get(data, 'user.info.age')
        >>> print(result)
        25
        
        >>> result = deep_get(data, 'user.info.city', default='未知')
        >>> print(result)
        未知
    """
    keys = path.split(separator)
    current = dict_info
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


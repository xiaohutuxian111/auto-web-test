import random
import time
from inspect import signature
from typing import Literal, Union, Dict, Any, Optional, List

from src.utils.fake_util import *
from  src.utils.date_uitl import *
from config.constants import Qualifications, Title, Degree, DeliverableType, InvestigateType



class As_dict:
    """
    基础数据模型类
    
    提供了数据模型的基础功能，包括字典转换、自动处理、格式化等。
    所有数据模型类都应该继承此类。
    """

    def as_dict(self, 自动处理: bool = False) -> Dict[str, Any]:
        """
        将对象转换为字典
        """
        if 自动处理:
            self.自动处理()

        return_dict = self.__dict__.copy()
        temp_dict = self.__dict__.copy()

        for key, value in temp_dict.items():
            if value is None:
                continue
            if value == "":
                return_dict.pop(key)
            if '时间戳' in str(value):
                value = str(value).replace('时间戳', str(time.time_ns()))
                return_dict.update({key: value})

        return return_dict

    def 自动处理(self) -> None:
        """
        自动处理数据
        
        子类可以重写此方法来实现特定的数据处理逻辑。
        """
        # 子类实现具体的自动处理逻辑
        pass

    def 格式化(self) -> Dict[str, Any]:
        """
        格式化数据
        
        Returns:
            Dict[str, Any]: 格式化后的数据字典
            
        Example:
            >>> data = MyDataModel()
            >>> formatted_data = data.格式化()
        """
        # 子类实现具体的格式化逻辑
        return self.as_dict(自动处理=True)

    def as_modify_dict(self) -> Dict[str, Any]:
        """
        获取修改后的参数字典
        
        只包含与默认值不同的参数。
        
        Returns:
            Dict[str, Any]: 修改后的参数字典
            
        Example:
            >>> data = MyDataModel(param1="value1", param2="default")
            >>> modified = data.as_modify_dict()
            >>> print(modified)  # {'param1': 'value1'}
        """
        temp = {}
        parameters = signature(self.__class__).parameters

        for parameter in parameters.values():
            parameter_name = parameter.name
            instance_value = getattr(self, parameter_name)

            if parameter.default != instance_value:
                if isinstance(instance_value, str) and '(' in instance_value and ')' in instance_value:
                    instance_value = instance_value.split("(")[0]
                temp[parameter_name] = instance_value

        return temp

    def validate(self) -> bool:
        """
        验证数据模型的有效性
        
        Returns:
            bool: 验证结果，True表示有效
            
        Raises:
            ValueError: 当数据无效时
        """
        # 子类实现具体的验证逻辑
        return True

    def copy(self) -> 'As_dict':
        """
        创建数据模型的副本
        
        Returns:
            As_dict: 数据模型的副本
        """
        import copy
        return copy.deepcopy(self)

    def update(self, **kwargs) -> None:
        """
        更新数据模型的属性
        
        Args:
            **kwargs: 要更新的属性键值对
            
        Example:
            >>> data = MyDataModel()
            >>> data.update(name="新名称", age=25)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"属性 '{key}' 不存在")

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取属性值，如果不存在则返回默认值
        
        Args:
            key: 属性名
            default: 默认值
            
        Returns:
            Any: 属性值或默认值
            
        Example:
            >>> data = MyDataModel()
            >>> value = data.get("name", "默认名称")
        """
        return getattr(self, key, default)

    def to_json(self) -> str:
        """
        将数据模型转换为JSON字符串
        
        Returns:
            str: JSON字符串
            
        Example:
            >>> data = MyDataModel()
            >>> json_str = data.to_json()
        """
        import json
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'As_dict':
        """
        从字典创建数据模型实例
        
        Args:
            data: 数据字典
            
        Returns:
            As_dict: 数据模型实例
            
        Example:
            >>> data_dict = {"name": "张三", "age": 25}
            >>> instance = MyDataModel.from_dict(data_dict)
        """
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'As_dict':
        """
        从JSON字符串创建数据模型实例
        
        Args:
            json_str: JSON字符串
            
        Returns:
            As_dict: 数据模型实例
            
        Example:
            >>> json_str = '{"name": "张三", "age": 25}'
            >>> instance = MyDataModel.from_json(json_str)
        """
        import json
        data = json.loads(json_str)
        return cls.from_dict(data)

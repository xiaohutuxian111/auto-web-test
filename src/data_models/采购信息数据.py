from src.data_models import *
from dataclasses import dataclass


@dataclass
class 采购品目配置新增Data(As_dict):
    采购品目名称: str = ''
    上级目录: str = ''
    是否末级目录: str = '是'  #归口部门  是才显示
    资产字典: str = ''
    归口部门: str = ''
    是否启用: str = '启用'
    品目说明: str = ''

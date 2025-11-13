import pytest
from typing import Dict, Any


@pytest.fixture
def 绩效申报(oc_page) -> str:
    """
    绩效申报项目名称
    
    Returns:
        str: 项目名称
    """
    return '信息化平台建设2'


@pytest.fixture
def 绩效自评(oc_page) -> Dict[str, str]:
    """
    绩效自评测试数据
    
    TODO: 增加创建绩效自评的完整过程
    
    Returns:
        Dict[str, str]: 包含填报编码和项目编码的字典
    """
    return {
        '填报编码': 'TB-20250611-1238', 
        '项目编码': 'CZXM002'
    }
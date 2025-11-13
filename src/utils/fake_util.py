"""
假数据生成工具模块

该模块提供了各种假数据生成功能，用于测试和开发环境。
基于 faker 库，支持中文假数据生成。
"""

import random
import string
import uuid
from typing import Literal, Optional

from faker import Faker

# 初始化中文假数据生成器
fake = Faker('zh_CN')


def faker_text(length: int) -> str:
    """
    生成指定长度的随机中文文本
    
    Args:
        length: 需要的文本长度
        
    Returns:
        str: 指定长度的随机中文文本
        
    Example:
        >>> faker_text(50)
        '这是一个随机生成的中文文本，用于测试目的。'
    """
    if length <= 0:
        return ""

    text = ""
    while len(text) < length:
        text += fake.sentence(nb_words=8)
    return text[:length]


def faker_职业() -> str:
    """
    生成随机职业名称
    
    Returns:
        str: 随机职业名称
    """
    return fake.job()


def faker_姓名() -> str:
    """
    生成随机中文姓名
    
    Returns:
        str: 随机中文姓名
    """
    return fake.name()


def fake_身份证() -> str:
    """
    生成随机身份证号码
    
    Returns:
        str: 随机身份证号码
    """
    return fake.ssn()


def faker_词组N连发(length: int = 10, split_char: str = '-') -> str:
    """
    生成指定数量的随机中文词组，用指定字符连接
    
    Args:
        length: 词组数量，默认为10
        split_char: 连接字符，默认为'-'
        
    Returns:
        str: 连接后的词组字符串
        
    Example:
        >>> faker_词组N连发(3, '-')
        '技术-创新-发展'
    """
    if length <= 0:
        return ""

    words = [fake.word() for _ in range(length)]
    return f"{split_char}".join(words)


def faker_uuid() -> str:
    """
    生成随机UUID字符串
    
    Returns:
        str: 随机UUID字符串
    """
    return str(uuid.uuid4())


def faker_城市() -> str:
    """
    生成随机城市名称
    
    Returns:
        str: 随机城市名称
    """
    return fake.city()


def faker_公司() -> str:
    return fake.company()


def faker_地址() -> str:
    """
    生成随机地址
    
    Returns:
        str: 随机地址
    """
    return fake.address()


def faker_移动电话() -> str:
    """
    生成随机手机号码
    
    Returns:
        str: 随机手机号码
    """
    return fake.phone_number()


def faker_邮箱() -> str:
    """
    生成随机邮箱地址
    
    Returns:
        str: 随机邮箱地址
    """
    return fake.ascii_email()


def faker_随机数生成(位数: int) -> int:
    """
    生成指定位数的随机整数
    
    Args:
        位数: 数字的位数
        
    Returns:
        int: 指定位数的随机整数
        
    Example:
        >>> faker_随机数生成(3)
        456
    """
    if 位数 <= 0:
        return 0

    return random.randrange(10 ** (位数 - 1), 10 ** 位数)


def faker_随机布尔值() -> bool:
    """
    生成随机布尔值
    
    Returns:
        bool: 随机布尔值
    """
    return fake.pybool()


def faker_单位() -> str:
    """
    生成随机计量单位
    
    Returns:
        str: 随机计量单位
    """
    # 常见计量单位列表
    units = [
        # 数量单位
        "个", "件", "台", "箱",
        # 长度单位
        "米", "厘米", "毫米",
        # 重量单位
        "千克", "克", "吨",
        # 时间单位
        "秒", "分钟", "小时",
        # 面积单位
        "平方米", "公顷", "亩",
        # 容积单位
        "升", "毫升",
        # 电学单位
        "伏特", "安培", "瓦",
        # 物理量单位
        "牛", "焦耳", "赫兹", "欧姆",
    ]
    return random.choice(units)


def faker_产品型号() -> str:
    """
    生成随机产品型号
    
    Returns:
        str: 随机产品型号
        
    Example:
        >>> faker_产品型号()
        'ABC-2025-X'
    """
    # 生成前缀（2-4个字母）
    prefix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(2, 4)))

    # 生成后缀
    suffix_options = [
        f"-{random.randint(100, 9999)}",
        f"{random.randint(2000, 2025)}",
        f"-{random.choice(['A', 'B', 'C', 'XL', 'PRO'])}"
    ]
    suffix = random.choice(suffix_options)

    return prefix + suffix


def faker_出版社():
    publisher_suffixes = [
        "出版社", "大学出版社", "科学出版社", "教育出版社",
        "文艺出版社", "人民出版社", "工业出版社", "交通出版社"
    ]

    # 随机生成地名/机构名 + 出版社后缀
    prefix = fake.city_name() if random.random() < 0.5 else fake.company_prefix()
    suffix = random.choice(publisher_suffixes)
    return prefix + suffix

def faker_文章名称():
    前缀 = random.choice(["关于", "浅谈", "如何看待", "探索", "基于", "研究", "新时代的"])
    主体 = random.choice([
        "人工智能发展",
        "大数据应用",
        "企业数字化转型",
        "区块链技术",
        "新能源产业",
        "网络安全",
        "云计算趋势",
        "教育改革",
        "医疗信息化",
        "自动驾驶技术"
    ])
    后缀 = random.choice([
        "的思考",
        "的研究",
        "的实践",
        "的案例分析",
        "的挑战与机遇",
        "的发展路径",
        "的现状与未来"
    ])
    return f"{前缀}{主体}{后缀}"



def faker_随机英文(长度: int = 20, 大小写: Optional[Literal["小写", "大写", "首字母大写"]] = "小写") -> str:
    """
    生成随机英文字符串
    
    Args:
        长度: 字符串长度，默认为20
        大小写: 大小写模式，可选值："小写"、"大写"、"首字母大写"
        
    Returns:
        str: 随机英文字符串
        
    Example:
        >>> faker_随机英文(5, "大写")
        'HELLO'
    """
    if 长度 <= 0:
        return ""

    if 大小写 == "小写":
        return "".join(random.choices(string.ascii_lowercase, k=长度))
    elif 大小写 == "大写":
        return "".join(random.choices(string.ascii_uppercase, k=长度))
    elif 大小写 == "首字母大写":
        return "".join(random.choices(string.ascii_lowercase, k=长度)).capitalize()
    else:
        raise ValueError(f"不支持的大小写模式: {大小写}")



def faker_发票号码(length: int = 10) -> str:
    """
    生成发票号码（默认10位数字）
    """
    return "".join([str(random.randint(0, 9)) for _ in range(length)])


def faker_会计凭证号(year: int = None) -> str:
    """
    生成会计凭证号（格式: 年份-5位顺序号）
    """
    if year is None:
        year = fake.year()
    seq = str(random.randint(1, 99999)).zfill(5)
    return f"{year}-{seq}"


if __name__ == '__main__':
    # 测试各种假数据生成函数
    print(f"UUID: {faker_uuid()}")
    print(f"姓名: {faker_姓名()}")
    print(f"城市: {faker_城市()}")
    print(f"产品型号: {faker_产品型号()}")
    print(f"随机文本: {faker_text(30)}")

from src.data_models import *
from dataclasses import dataclass, field


# ===============================
# 资产登记
# ===============================
@dataclass
class 资产登记_基本信息Data(As_dict):
    资产名称: str = field(default_factory=lambda: f'自动化创建_资产登记_{faker_随机数生成(4)}')
    关联资产字典: str = ''
    品牌: str = field(default_factory=lambda: random.choice(list(InvestigateType)).value)
    规格型号: str = field(default_factory=lambda: faker_产品型号())
    计量单位: str = ''
    启用日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-3000))
    归属部门: str = ''
    资产来源: str = field(default_factory=lambda: random.choice(['盘盈入库', '划拨', '重组并购', '购买']))
    使用部门: str = ''
    使用人: str = ''
    存放地点: str = field(default_factory=lambda: random.choice(['综合办公楼', '财务办公室']))
    质保截止日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(3000))
    备注: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 资产登记_财务信息Data(As_dict):
    入账日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-30))
    资产原值: str = field(default_factory=lambda: random.randint(100, 10000))
    资产残值: str = field(default_factory=lambda: random.randint(100, 10000))
    已折旧摊销月份: str = ''
    累计折旧摊销金额: str = ''
    资产净值: str = ''
    资金来源: str = field(default_factory=lambda: random.choice(['政府补贴换积分卡圣诞为出让人速度则维持',
                                                                 '住院医师培训经费-考试考核经费',
                                                                 '住院医师培训经费-生均定额',
                                                                 '补助住院医师培训经费-公用经费',
                                                                 '首医大经费-研究生',
                                                                 '财政资金',
                                                                 '科研课题经费']))
    资金来源明细金额: str = field(default_factory=lambda: random.randint(100, 10000))
    发票号码: str = field(default_factory=lambda: faker_发票号码)
    会计凭证号: str = field(default_factory=lambda: faker_会计凭证号)

@dataclass
class 资产登记_其他信息Data(As_dict):
    合同名称: str = ""
    采购验收单号: str = field(default_factory=lambda: faker_产品型号())
    供应商: str = field(default_factory=lambda: faker_出版社())
    生产厂商: str = field(default_factory=lambda: faker_出版社())

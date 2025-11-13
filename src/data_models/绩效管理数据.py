from src.data_models import *
from dataclasses import dataclass, field


@dataclass
class 绩效目标基础信息Data(As_dict):
    """绩效目标基础信息数据类"""
    年度目标: str = ''
    长期目标: str = ''


@dataclass
class 绩效指标信息Data(As_dict):
    """绩效指标信息数据类"""
    指标类型: str = field(default_factory=lambda: random.choice(["通用类项目", "对口援助项目", "教育费附加安排的支出"]))
    资金用途: str = ''
    一级指标: str = field(default_factory=lambda: random.choice(["产出指标", "效益指标", "满意度指标"]))
    二级指标: str = ''
    三级指标: str = ''
    指标解释: str = ''
    指标属性: str = field(default_factory=lambda: random.choice(["定性", "定量"]))
    指标性质: str = field(default_factory=lambda: random.choice(["≥", "≤", ">", "<", "=", '空值']))
    指标值: str = ''
    指标单位: str = field(default_factory=lambda: random.choice(["元", "万元", "吨", "个"]))
    指标方向性: str = field(default_factory=lambda: random.choice(["正向指标", "反向指标"]))
    评分标准: str = ''
    指标汇总规则: str = field(default_factory=lambda: random.choice(["累加", "最大值", "最小值", "平均值"]))
    是否必填: str = ''
    评价标准: str = ''

    def __post_init__(self):
        """
        自动根据一级指标设置对应的二级指标选项。
        可根据需要进一步扩展三级指标的自动处理逻辑。
        """
        # 二级指标可选项字典
        二级指标可选 = {
            "产出指标": ["数量指标", "质量指标", "时效指标", "成本指标"],
            "效益指标": ["社会效益指标", "经济效益指标", "生态效益指标", "可持续影响指标"],
            "满意度指标": ["服务对象满意度指标", "其他满意度指标"]
        }
        if self.一级指标 in 二级指标可选:
            self.二级指标 = random.choice(二级指标可选[self.一级指标])


@dataclass
class 绩效填报频率配置Data(As_dict):
    """绩效指标填报频率配置数据类"""
    填报频率: str = ''
    消息通知: str = ''


@dataclass
class 绩效指标库数据_新增绩效指标Data(绩效指标信息Data):
    pass


# ===============================
# 绩效填报
# ===============================

@dataclass
class 资金到位情况Data(As_dict):
    监控期资金使用计划金额: str = field(default_factory=lambda: str(faker_随机数生成(4)))
    监控期资金指标安排金额: str = field(default_factory=lambda: str(faker_随机数生成(4)))
    监控期资金实际支付金额: str = field(default_factory=lambda: str(faker_随机数生成(4)))


@dataclass
class 资金支付进度Data(As_dict):
    资金支付进度: str = field(default_factory=lambda: random.choice(
        ['资金计划执行正常', '因预算时对项目前期准备工作估计不足，需做大量准备导致进度延期',
         '报预算时的项目实施计划不够细化，实际进度落后目标进度']))


@dataclass
class 绩效运行监控结论与建议Data(As_dict):
    总体结论: str = field(
        default_factory=lambda: random.choice(['整体运行良好', '项目运行基本正常', '项目运行存在问题', '其他']))
    运行建议: str = field(
        default_factory=lambda: random.choice(['项目按计划继续执行', '项目按计划继续执行', '项目终止执行', '其他']))


# ===============================
# 整改下发
# ===============================
@dataclass
class 整改下发Data(As_dict):
    整改项目: str = ''
    整改负责人: str = ''
    整改截止日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(5))
    整改说明: str = field(default_factory=lambda: faker_text(20))


# ===============================
# 整改反馈
# ===============================
@dataclass
class 整改反馈Data(As_dict):
    整改完成情况: str = field(default_factory=lambda: random.choice(['已完成整改', '部分完成整改', '未完成整改'])),
    整改完成日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(50)),
    整改完成情况说明: str = field(default_factory=lambda: faker_text(50))

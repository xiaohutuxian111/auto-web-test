import random

from src.data_models import *
from dataclasses import dataclass, field


@dataclass
class 项目类型配置Data(As_dict):
    上级类型编码: str = ""
    上级类型: str = ""
    项目类型编码: str = ""
    项目类型: str = ""
    部门编码: str = ""
    归口部门: str = ""
    立项填报表单: str = ""
    绩效目标触发阈值: str = ""
    立项专项信息表单: str = ""
    是否分层级项目: str = "否"
    是否末级: str = "是"
    关联预算事项: str = ""
    是否启用: str = "是"
    关联预算事项编码: str = ""
    关联预算事项名称: str = ""

    def __post_init__(self):
        if "项目专项信息" not in self.立项填报表单:
            self.立项专项信息表单 = ""
        if "绩效目标" not in self.立项填报表单:
            self.绩效目标触发阈值 = ""


# ========== 示例：专项层级 ==========
@dataclass
class 专项层级Data(As_dict):
    上级名称: str = ""
    层级名称: str = ""
    归口部门: str = ""
    责任人: str = ""
    汇总人: str = ""
    审批人: str = ""
    审批流程: str = ""
    是否末级: str = "是"


# ========== 项目立项基本信息 ==========
@dataclass
class 项目立项基本信息Data(As_dict):
    项目名称: str = field(default_factory=lambda: f"自动化创建_项目立项_{faker_随机数生成(4)}")
    项目类型: str = ""
    项目周期: str = field(default_factory=lambda: str(random.randint(1, 3)))
    专项项目: str = field(default_factory=lambda: random.choice(["双高计划项目", "创新强校项目", "非专项项目"]))
    项目层级: str = ""
    项目总预算: str = ""
    立项方式: str = field(default_factory=lambda: random.choice(["年度统一立项", "临时立项"]))
    项目性质: str = field(default_factory=lambda: random.choice(["经常性项目", "一次性项目"]))
    归口部门: str = ""
    实施部门: str = "一级部门"
    项目负责人: str = "一级部门A_负责人"
    重要程度: str = field(default_factory=lambda: random.choice(["一般项目", "重要项目"]))
    是否政府投资类: str = field(default_factory=lambda: random.choice(["是", "否"]))
    项目前期文档: str = field(default_factory=lambda: random.choice(["项目建议书", "项目可行性报告", "项目概算"]))
    经费类型: str = ""
    关联需求: str = ""

    def __post_init__(self):
        if self.专项项目 == "非专项项目":
            self.项目层级 = ""
        if self.是否政府投资类 == "否":
            self.项目前期文档 = ""


# ===============================
# 立项信息
# ===============================
@dataclass
class 立项信息Data(As_dict):
    项目立项依据: str = field(default_factory=lambda: f"项目立项依据_{faker_text(20)}")
    项目概况: str = field(default_factory=lambda: f"项目概况_{faker_text(20)}")
    是否立项论证: str = "否"
    是否采购: str = ""


# ===============================
# 采购专项信息
# ===============================
@dataclass
class 采购信息Data(As_dict):
    采购类别: str = "自动化品目父级&&货物类&&采购品目新增123&&演示设备&&服务类&&工程类&&电子设备&&通用设备"
    采购组织方式: str = field(default_factory=lambda: random.choice(["非政府集中采购", "政府集中采购", "不限"]))
    是否一次性采购: str = field(default_factory=lambda: random.choice(["是", "否"]))


@dataclass
class 购置明细Data(As_dict):
    采购品目名称: str = ""
    采购品目编码: str = ""
    规格型号: str = field(default_factory=faker_产品型号)
    计量单位: str = field(default_factory=faker_单位)
    采购数量: str = field(default_factory=lambda: str(random.randint(1, 1000)))
    预算单价: str = field(default_factory=lambda: str(random.randint(1, 1000)))
    备注: str = field(default_factory=lambda: faker_text(50))

    导入采购物品信息 = [
        {"项采购品目名称": "工程类\构筑物施工\桥梁工程施工\铁路桥梁工程施工", "采购品目编码": "B020701"},
        {"项采购品目名称": "工程类\构筑物施工\桥梁工程施工\公路桥梁工程施工", "采购品目编码": "B020702"},
        {"项采购品目名称": "工程类\构筑物施工\桥梁工程施工\城市道路桥梁工程施工", "采购品目编码": "B020703"},
    ]


# ===============================
# 建设项目专项信息
# ===============================
@dataclass
class 工程建设信息Data(As_dict):
    计划开工时间: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-30))
    计划完工时间: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(30))
    项目建设必要性: str = field(default_factory=lambda: faker_text(50))
    项目建设可行性: str = field(default_factory=lambda: faker_text(50))
    现场条件与措施: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 施工区域及位置Data(As_dict):
    区域: str = field(default_factory=faker_城市)
    具体位置: str = field(default_factory=faker_地址)


# ===============================
# 科研专项信息
# ===============================
@dataclass
class 科研项目信息Data(As_dict):
    课题类型: str = field(default_factory=lambda: random.choice(["纵向课题", "横向课题"]))
    项目来源: str = field(
        default_factory=lambda: random.choice(["其他来源", "科技部(厅)其他项目", "国家自然科学基金项目"])
    )
    研究类型: str = field(default_factory=lambda: random.choice(list(InvestigateType)).value)
    预计项目周期: str = "-30,30"


@dataclass
class 项目负责人信息Data(As_dict):
    负责人: str = "审批领导"
    职称: str = field(default_factory=lambda: random.choice(list(Title)).value)
    学历: str = field(default_factory=lambda: random.choice(list(Qualifications)).value)
    学位: str = field(default_factory=lambda: random.choice(list(Degree)).value)
    联系电话: str = field(default_factory=faker_移动电话)
    邮箱: str = field(default_factory=faker_邮箱)


@dataclass
class 项目组成员信息Data(As_dict):
    姓名: str = "审批领导"
    所属部门: str = "福建省妇幼保健院"
    性别: str = field(default_factory=lambda: random.choice(["男", "女"]))
    出生日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-3000))
    职称: str = field(default_factory=lambda: random.choice(list(Title)).value)
    联系电话: str = field(default_factory=faker_移动电话)
    邮箱: str = field(default_factory=faker_邮箱)
    学历: str = field(default_factory=lambda: random.choice(list(Qualifications)).value)
    学位: str = field(default_factory=lambda: random.choice(list(Degree)).value)
    分工说明: str = field(default_factory=lambda: faker_text(50))


# ===============================
# 教学管理项目专项信息,项目专项信息
# ===============================
@dataclass
class 主导人信息Data(As_dict):
    主导人: str = "审批领导"
    性别: str = field(default_factory=lambda: random.choice(["女", "男"]))
    出生日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-4000))
    专业技术职务: str = field(default_factory=lambda: faker_text(10))
    职位: str = field(default_factory=faker_职业)
    邮箱: str = field(default_factory=faker_邮箱)
    最终学历: str = field(default_factory=lambda: random.choice(list(Qualifications)).value)
    学位: str = field(default_factory=lambda: random.choice(list(Degree)).value)
    教学技术与专长: str = field(default_factory=lambda: faker_text(20))
    成果与业绩: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 项目组成员Data(As_dict):
    姓名: str = "审批领导"
    所属部门: str = "福建省妇幼保健院"
    性别: str = field(default_factory=lambda: random.choice(["男", "女"]))
    出生日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-4000))
    职称: str = field(default_factory=lambda: random.choice(list(Title)).value)
    联系电话: str = field(default_factory=faker_移动电话)
    邮箱: str = field(default_factory=faker_邮箱)
    学历: str = field(default_factory=lambda: random.choice(list(Qualifications)).value)
    学位: str = field(default_factory=lambda: random.choice(list(Degree)).value)
    分工说明: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 项目专项信息_项目组成员Data(As_dict):
    姓名: str = "审批领导"
    性别: str = field(default_factory=lambda: random.choice(["男", "女"]))
    出生日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-4000))
    职务: str = field(default_factory=lambda: random.choice(list(Title)).value)
    专业技术职称: str = field(default_factory=lambda: random.choice(list(Title)).value)
    项目分工: str = field(default_factory=lambda: faker_text(20))
    备注: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 立项依据和目标Data(As_dict):
    课题类别: str = field(default_factory=lambda: random.choice(["一般", "重要", "重大"]))
    立项依据和目标: str = field(default_factory=lambda: faker_text(100))


# ===============================
# 绩效目标、预算、验收、成果物,执行任务
# ===============================
@dataclass
class 绩效目标Data(As_dict):
    本年度绩效目标: str = field(default_factory=lambda: faker_text(50))
    长期绩效目标: str = field(default_factory=lambda: faker_text(50))
    产出指标: list = field(default_factory=list)
    效益指标: list = field(default_factory=list)
    满意度指标: list = field(default_factory=list)


@dataclass
class 预算明细Data(As_dict):
    预算指标编码: list = field(default_factory=lambda: ["YSBM0238", "YSBM0237", "YSBM0236"])
    资金来源: dict = field(default_factory=lambda: {"资金来源": "财政&&非财政&&科研&&人力"})
    年度用款计划: dict = field(
        default_factory=lambda: {
            "第一季度用款计划": str(random.randint(1, 10000)),
            "第二季度用款计划": str(random.randint(1, 10000)),
            "第三季度用款计划": str(random.randint(1, 10000)),
            "第四季度用款计划": str(random.randint(1, 10000)),
        }
    )


@dataclass
class 项目计划分解Data(As_dict):
    任务阶段: str = ""
    任务名称: str = field(default_factory=lambda: faker_text(50))
    任务内容: str = field(default_factory=lambda: faker_text(50))
    任务时间: str = "-30,30"
    任务工时: str = ""
    责任人: str = "审批领导"
    拟实施部门: str = ("福建省妇幼保健院",)
    里程碑要求: str = field(default_factory=lambda: faker_text(50))
    输出成果: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 验收标准Data(As_dict):
    验收项: str = field(default_factory=lambda: faker_text(50))
    验收标准: str = field(default_factory=lambda: faker_text(100))


@dataclass
class 成果物Data(As_dict):
    成果物名称: str = field(default_factory=lambda: faker_text(20))
    成果物类型: str = field(default_factory=lambda: random.choice(list(DeliverableType)).value)
    负责人: str = "审批领导"
    说明: str = field(default_factory=lambda: faker_text(50))


# ===============================
#  立项论证
# ===============================
@dataclass
class 立项论证信息(As_dict):
    立项论证周期: str = "-30,30"
    论证说明: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 论证项目明细(As_dict):
    项目编码: str = ""
    项目名称: str = ""
    立项论证结果: str = field(default_factory=lambda: random.choice(["通过", "不通过"]))
    论证日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(5))
    项目类型: str = ""
    申报人: str = ""
    申报部门: str = ""
    项目总预算: str = ""
    不通过项目处置: str = field(default_factory=lambda: random.choice(["清理库", "立项退回"]))
    处置理由: str = field(default_factory=lambda: faker_text(50))

    def __post_init__(self):
        if self.立项论证结果 == "通过":
            self.不通过项目处置 = ""
            self.处置理由 = ""


# ===============================
# 项目建议书
# ===============================
@dataclass
class 项目建议书_基本信息(As_dict):
    项目名称: str = ""
    项目管理类型: str = field(default_factory=lambda: random.choice(["监管项目", "本级建设项目"]))
    项目业主单位: str = field(default_factory=lambda: faker_公司())
    责任人: str = ""
    说明: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 项目建议书_批文信息(As_dict):
    建议书批文号: str = field(default_factory=lambda: faker_产品型号())
    批复时间: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(5))
    批复单位: str = field(default_factory=lambda: faker_公司())
    批文名称: str = field(default_factory=lambda: faker_text(20))


# ===============================
# 项目可行性研究报告
# ===============================
@dataclass
class 项目可行性研究报告_基本信息(As_dict):
    项目名称: str = ""
    项目建设单位: str = field(default_factory=lambda: faker_公司())
    项目法人单位: str = field(default_factory=lambda: faker_公司())
    项目建设规模: str = f"{random.randint(1000, 9999)}人"
    预计项目周期: str = "-30,30"
    建设地点: str = field(default_factory=lambda: faker_地址())
    说明: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 项目可行性研究报告_批文信息(As_dict):
    可研报告批文号: str = field(default_factory=lambda: faker_产品型号())
    批复时间: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(5))
    批复单位: str = field(default_factory=lambda: faker_公司())
    批文名称: str = field(default_factory=lambda: faker_text(20))


# ===============================
# 项目概算
# ===============================
@dataclass
class 项目概算_基本信息(As_dict):
    项目名称: str = ""
    说明: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 项目概算_批文信息(As_dict):
    概算批文号: str = field(default_factory=lambda: faker_产品型号())
    批复时间: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(5))
    批复单位: str = field(default_factory=lambda: faker_公司())
    批文名称: str = field(default_factory=lambda: faker_text(20))


# ===============================
# 项目任务分解
# ===============================
@dataclass
class 项目计划分解(As_dict):
    任务阶段: str = ""
    任务名称: str = ""
    任务内容: str = field(default_factory=lambda: faker_text(20))
    任务时间: str = "-30,30"
    任务工时: str = ""
    责任人: str = ""
    拟实施部门: str = ""
    里程碑要求: str = field(default_factory=lambda: faker_text(50))
    输出成果: str = field(default_factory=lambda: faker_text(50))


# ===============================
# 成果物
# ===============================
@dataclass
class 奖励证书Data(As_dict):
    课题名称: str = f"自动化创建_课题名称_{faker_随机数生成(3)}"
    获奖类型: str = field(default_factory=lambda: random.choice(["单位级", "厅局级", "省级", "国家级", "国际级"]))
    获奖时间: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-5))
    关联项目: str = ""
    第一完成人员: str = field(default_factory=lambda: faker_姓名())
    其他完成人员: str = field(default_factory=lambda: faker_姓名())
    奖励描述: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 专著编书_基本信息Data(As_dict):
    专著名称: str = f"自动化创建_专著名称_{faker_随机数生成(3)}"
    出版社: str = field(default_factory=lambda: faker_出版社())
    出版时间: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-5))
    关联项目: str = ""
    专著描述: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 专著编书_参与作者Data(As_dict):
    担任职责: str = field(default_factory=lambda: random.choice(["主编", "副主编", "编委"]))
    作者名称: str = field(default_factory=lambda: faker_姓名())
    作者单位: str = field(default_factory=lambda: faker_公司())
    作者职级: str = field(default_factory=lambda: random.choice(["正高", "副高", "中级", "初级", "未评定"]))


@dataclass
class 专利证书_基本信息Data(As_dict):
    专利名称: str = f"自动化创建_专利名称_{faker_随机数生成(3)}"
    专利类型: str = field(default_factory=lambda: random.choice(["实用", "发明", "外观"]))
    专利号: str = field(default_factory=lambda: faker_产品型号())
    关联项目: str = ""
    专利公告日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-5))
    专利所有权人: str = field(default_factory=lambda: faker_姓名())
    所有发明人: str = field(default_factory=lambda: faker_姓名())
    专利描述: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 论文成果_基本信息Data(As_dict):
    论文题目: str = f"自动化创建_专利名称_{faker_随机数生成(3)}"
    期刊名称: str = field(default_factory=lambda: faker_文章名称())
    发表日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-5))
    关联项目: str = ""
    第一作者名称: str = field(default_factory=lambda: faker_姓名())
    第一作者单位: str = field(default_factory=lambda: faker_公司())
    通讯作者名称: str = field(default_factory=lambda: faker_姓名())
    通讯作者单位: str = field(default_factory=lambda: faker_公司())
    其他完成人员: str = field(default_factory=lambda: faker_姓名())
    论文描述: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 其他成果_基本信息Data(As_dict):
    成果名称: str = f"自动化创建_其他成果_{faker_随机数生成(3)}"
    成果登记号: str = field(default_factory=lambda: faker_产品型号())
    成果类型: str = field(default_factory=lambda: random.choice(["论文专著", "专利", "奖励证书"]))
    关联项目: str = ""
    成果所有人: str = ""
    申报日期: str = field(default_factory=lambda: 返回当前时间xxxx_xx_xx加N天(-5))
    成果描述: str = field(default_factory=lambda: faker_text(50))


# ===============================
# 我的任务
# ===============================


@dataclass
class 我的任务_执行进度填写Data(As_dict):
    项目名称: str = ""
    完成进度: str = field(default_factory=lambda: str(random.randint(1, 100)))
    任务执行时间: str = "-5,5"
    进度描述: str = field(default_factory=lambda: faker_text(200))
    风险描述: str = field(default_factory=lambda: faker_text(200))
    下一步计划: str = field(default_factory=lambda: faker_text(200))


# ===============================
# 项目工时填报
# ===============================
@dataclass
class 项目工时填报Data(As_dict):
    项目名称: str = ""
    日期: str = ""
    任务阶段: str = ""
    工作性质: str = field(default_factory=lambda: random.choice(["全天", "上半天", "下半天"]))
    工作情况说明: str = field(default_factory=lambda: faker_text(200))

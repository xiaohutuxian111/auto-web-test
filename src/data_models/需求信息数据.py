from src.data_models import *
from dataclasses import dataclass, field


# ========== 需求类型 dataclass ==========
@dataclass
class 需求类型基本信息Data(As_dict):
    需求类型编码: str = ''
    需求类型: str = ''
    归口部门: str = ''
    责任人: str = ''
    需求申报表单: str = '需求详情&专项信息&预算明细&需求附件'
    是否启用: str = '是'
    申报专项信息表单: str = ''
    项目类型: str = ''
    说明: str = ''


# ========== 创建需求 dataclass ==========
@dataclass
class 基本信息Data(As_dict):
    需求名称: str = field(default_factory=lambda: f'自动化创建_需求名称_{faker_随机数生成(4)}')
    需求类型: str = ''
    需求概算: str = ''
    重要程度: str = field(default_factory=lambda: random.choice(['重大需求', '重要需求', '一般需求']))
    专项项目: str = field(default_factory=lambda: random.choice(["双高计划项目", "创新强校项目", "非专项项目"]))
    牵头部门: str = ''
    责任人: str = ''
    责任领导: str = ''


@dataclass
class 需求详情Data(As_dict):
    需求描述: str = field(default_factory=lambda: faker_text(50))
    需求申报依据: str = field(default_factory=lambda: faker_text(50))
    工作措施: str = field(default_factory=lambda: faker_text(50))
    绩效评价点: str = field(default_factory=lambda: faker_text(50))


@dataclass
class 采购信息Data(As_dict):
    采购类型: str = ''
    采购组织方式: str = field(default_factory=lambda: random.choice(['政府集中采购', '不限', '非政府集中采购']))
    是否一次性采购: str = field(default_factory=lambda: random.choice(['是', '否']))


@dataclass
class 建设工程类专项信息Data(As_dict):
    施工区域: str = field(default_factory=faker_城市)
    具体位置: str = field(default_factory=faker_地址)
    施工需求: str = field(default_factory=lambda: faker_text(200))


@dataclass
class 教学管理类专项信息Data(As_dict):
    课程类别: str = field(default_factory=lambda: random.choice(['一般', '重要', '重大']))
    申报依据: str = field(default_factory=lambda: faker_text(200))


@dataclass
class 预算明细Data(As_dict):
    资金来源: str = ''
    def __post_init__(self):
        # 未传值，全选
        if self.资金来源 == '':
            self.资金来源 = '&&'.join(['财政', '非财政', '科研', '人力'])


@dataclass
class 科研项目类专项信息Data(As_dict):
    课题类型: str = field(default_factory=lambda: random.choice(['横向课题', '纵向课题']))
    项目来源: str = field(
        default_factory=lambda: random.choice(['国家自然科学基金项目', '科技部(厅)其他项目', '其他来源']))
    研究类型: str = field(
        default_factory=lambda: random.choice(['基础研究', '应用基础研究', '应用开发', '临床研究', '其他']))
    研究项目周期: str = field(default_factory=lambda: '-60,60')
    申报依据: str = field(default_factory=lambda: faker_text(50))


# ========== 附件类型配置 ==========
@dataclass
class 附件类型配置Data(As_dict):
    附件类型名称: str = ''
    表名: str = ''
    支持格式: str = ''
    大小限制: str = ''
    允许上传附件数: str = ''
    附件提示: str = ''
    说明: str = ''
    是否必填: str = ''
    操作: str = ''


# ========== 顶层表单信息 ==========
@dataclass
class 需求表单信息Data:
    基本信息: Optional[dict[str, Any]] = ''
    需求详情: Optional[dict[str, Any]] = ''
    采购类专项信息: Optional[dict[str, Any]] = ''
    建设工程类专项信息: Optional[dict[str, Any]] = ''
    教学管理类专项信息: Optional[dict[str, Any]] = ''
    预算明细: Optional[dict[str, Any]] = ''
    科研项目类专项信息: Optional[dict[str, Any]] = ''

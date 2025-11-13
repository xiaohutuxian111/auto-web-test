from src.test_cases import *
from src.test_cases.项目管理.conftest import 创建关联需求

@用例名称("储备需求编辑并审批")
@用例描述("""
需求申报提交审批功能
测试步骤:
1. 项目管理人员登录
2. 填写需求申报
3. 提交审批
4. 验证审批结果
""")
@用例级别(严重)
def test_需求申报审批(oc_page, oc_page_backup, 基础配置):
    创建关联需求(oc_page, oc_page_backup, 基础配置,'Atest4')

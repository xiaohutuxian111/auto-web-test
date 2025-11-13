from src.test_cases import *


@用例名称("项目绩效申报")
@用例描述("""
1. 绩效管理员登录
2. 点击申报
3. 引入绩效指标
4. 审批通过
""")
@用例级别(严重)
def test_项目绩效申报(oc_page, oc_page_backup, 财政项目审批通过, 基础配置):
    with  测试步骤('初始化数据'):
        项目名称 = 财政项目审批通过
        绩效指标 = [基础配置['绩效指标库']['产出指标'][0], 基础配置['绩效指标库']['效益指标'][0],
                    基础配置['满意度指标']['产出指标'][0]]
        申报信息info = {'目标信息': {
            '年度目标': faker_text(50),
            '长期目标': faker_text(50),
        }, '绩效指标': 绩效指标}

    with 测试步骤("绩效管理员登录"):
        oc_page.项目绩效申报页.set_设置当前用户为("superAdmin")
        oc_page.项目绩效申报页.navigate()
    with 测试步骤("填写申报数据"):
        oc_page.项目绩效申报页.获取申报按钮(项目名称)
        oc_page.项目绩效申报页.fill_绩效申报(申报信息info)

    with 测试步骤("审批人登录,审批绩效申报通过"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意('绩效申报')

    with 测试步骤("结果校验"):
        info = oc_page.项目绩效申报页.search_填写搜索框(项目名称)
        assert '已审批' in info['审批状态'], '绩效申报审批失败'

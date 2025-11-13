from src.test_cases import *


@用例名称("项目工时填报")
@用例描述(
    """
    项目工时填报
测试步骤:
    1. 我的任务审批通过
    2. 填写项目项目工时
    3. 审批
"""
)
@用例级别(严重)
def test_填写我的任务(oc_page, oc_page_backup, 工时填报_前置):
    with 测试步骤("初始化数据"):
        # 用户名 = "Atest14"
        用户名 = "testUser"
        项目名称 = 工时填报_前置
        任务阶段 = "第一阶段"
        当天日期 = datetime.datetime.today().day
        执行进度填写info = 项目工时填报Data(任务阶段=任务阶段).as_dict()
        logger.info(f"我的任务填写表单信息:{执行进度填写info}")
    with 测试步骤("我的任务填写任务"):
        oc_page.项目工时填报页.set_设置当前用户为(用户名)
        oc_page.项目工时填报页.navigate()
        oc_page.项目工时填报页.日历视图_tab.click()
        oc_page.项目工时填报页.select_calendar_day(当天日期)
        oc_page.项目工时填报页.fill_工时填报(项目名称, 当天日期, 执行进度填写info)

    with 测试步骤("审批"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("用户工时填报", 用户名)

    with 测试步骤("验证"):
        oc_page.项目工时填报页.原型视图_tab.click()
        oc_page.项目工时填报页.search_条件查询(项目名称=项目名称)
        table = oc_page.项目工时填报页.主表格
        状态 = table.get("审批状态", 任务阶段)
        assert "已完成" in 状态

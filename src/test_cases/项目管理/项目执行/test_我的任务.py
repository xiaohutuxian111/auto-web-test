from src.test_cases import *


@用例名称("我的任务执行填写")
@用例描述(
    """
    我的任务执行填写
测试步骤:
    1. 项目分解将项目分配到填写人
    2. 填写我的任务
    3. 审批
"""
)
@用例级别(严重)
def test_填写我的任务(oc_page, oc_page_backup, 我的任务_前置):
    with 测试步骤("初始化数据"):
        # 用户名 = "Atest13"
        用户名 = "superAdmin"
        执行进度填写info = 我的任务_执行进度填写Data().as_dict()
        项目名称 = 我的任务_前置
        logger.info(f"我的任务填写表单信息:{执行进度填写info}")
    with 测试步骤("我的任务填写任务"):
        oc_page.我的任务页.set_设置当前用户为(用户名)
        oc_page.我的任务页.navigate()
        任务_status = oc_page.我的任务页.get_card_info()
        oc_page.我的任务页.search_填写搜索框(placeholder="项目名称", 关键字=项目名称)
        oc_page.我的任务页.fill_任务("2-7项目变更-预算明细金额变更范围和判断逻辑", 执行进度填写info)

    with 测试步骤("审批"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("项目整体进度填报", 用户名)
        任务_status_after = oc_page.我的任务页.get_card_info()
        assert 任务_status_after["未完成任务"] - 任务_status["未完成任务"] == -1

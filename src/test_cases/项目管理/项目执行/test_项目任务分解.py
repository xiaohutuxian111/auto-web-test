from src.test_cases import *


@用例名称("项目执行任务分解")
@用例描述(
    """
    新建项目任务分解
测试步骤:
    1. 通过两种方式到项目执行
    2. 进行项目分解
    3. 审批
"""
)
@用例级别(严重)
def test_新增项目分解(oc_page, oc_page_backup, 项目执行_前置):
    with 测试步骤("初始化数据"):
        用户名 = "Atest12"
        项目任务分解info = {
            "项目任务列表": [f"第{i}阶段" for i in range(1, 4)],
            "项目计划分解": [
                项目计划分解(
                    任务阶段=f"第{i}阶段",
                    任务名称=f"第{i}阶段_第{i}任务",
                    责任人="一级部门A_负责人",
                    拟实施部门="一级部门",
                ).as_dict()
                for i in range(1, 4)
            ],
        }
        # 项目名称 = 项目执行_前置(用户名)
        项目名称 = "自动化创建_备选库管理_708"
        logger.info(f"项目任务分解表单信息:{项目任务分解info}")
    with 测试步骤("项目管理人员登录并进入立项申请页"):
        oc_page.项目任务分解页.set_设置当前用户为(用户名)
        oc_page.项目任务分解页.navigate()
        oc_page.项目任务分解页.search_填写搜索框(placeholder="编号/名称/类型", 关键字=项目名称)
        oc_page.项目任务分解页.click_任务分解(项目名称)

    with 测试步骤("新建项目任务分解"):
        # oc_page.项目任务分解页.fill_项目任务分解(项目任务分解info)
        oc_page.项目任务分解页.upload_附件(oc_page.log_dir)
        oc_page.项目任务分解页.click_button("送审")
        oc_page.项目任务分解页.confirm_弹框()

    with 测试步骤("审批"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("项目整体进度填报", 用户名)

from src.test_cases import *


@pytest.fixture
def 成果物_项目立项(oc_page, oc_page_backup, 基础配置, global_map):
    项目名称 = global_map.get("成果物_项目立项")
    if 项目名称:
        return 项目名称
    指标数据, 成果物_项目类型 = (
        基础配置["绩效指标库"],
        基础配置["项目类型"]["基本项目类型"],
    )
    直接立项info = {
        "基本信息": 项目立项基本信息Data(
            项目类型=成果物_项目类型,
            实施部门="一级部门",
            经费类型="创收经费",
            项目层级="【全部】",
            是否政府投资类="否",
            项目负责人="一级部门A_负责人",
        ).as_dict(),
        "立项信息": 立项信息Data().as_dict(),
    }
    项目基本信息 = 直接立项info["基本信息"]

    with 测试步骤("项目管理人员登录,跳转到立项申请"):
        oc_page.立项申请页.set_设置当前用户为("superAdmin")
        oc_page.立项申请页.navigate()
    with 测试步骤("创建数据并填写立项基本信息"):
        oc_page.立项申请页.click_button("直接立项")
        oc_page.立项申请页.fill_立项基本信息(项目基本信息)
        logger.info(直接立项info)
    with 测试步骤("填写详细数据并校验"):
        oc_page.立项申请页.fill_项目立项tab信息(
            直接立项info,
            year=项目基本信息.get("项目周期"),
            项目立项方式=项目基本信息["立项方式"],
            temp_path=oc_page.log_dir,
        )

    with 测试步骤("验证提交结果"):
        oc_page.立项申请页.click_button("提交")
        oc_page.立项申请页.confirm_弹框()
        error_message = oc_page.立项申请页.wait_for_error_message()
        if error_message:
            logger.warning(f"立项提交报错信息: {error_message}")

        项目信息 = oc_page.立项申请页.search_立项信息(项目基本信息["项目名称"])
        assert "审批中" in 项目信息.get("审批状态")

    with 测试步骤("审批通过"):
        oc_page_backup.我的待办.set_设置当前用户为("testUser")
        oc_page_backup.我的待办.navigate()
        oc_page_backup.我的待办.审批同意("立项申请")
        项目信息 = oc_page.立项申请页.search_立项信息(项目基本信息["项目名称"])
        assert "已审批" in 项目信息.get("审批状态")
    global_map.set("成果物_项目立项", 项目基本信息["项目名称"])
    return 项目基本信息["项目名称"]

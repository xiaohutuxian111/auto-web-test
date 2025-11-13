from src.test_cases import *


@用例名称("修改绩效填报频率配置")
@用例描述(
    """
1. 绩效管理员登录
2. 修改绩效填报频率配置
3. 验证配置结果
"""
)
@用例级别(严重)
def test_更新绩效填报频率配置(oc_page, test_name):
    with 测试步骤("绩效管理员登录,跳转到绩效填报配置页面"):
        oc_page.绩效填报频率配置页.set_设置当前用户为("superAdmin")
        oc_page.绩效填报频率配置页.navigate()
    with 测试步骤("修改绩效填报频率配置"):
        oc_page.绩效填报频率配置页.click_button("修改")
        季度填报频率配置_info = {
            "填报频率": random.choice(["年度", "季度", "半年", "月度"]),
            "消息通知": random.choice(["是", "否"]),
        }

        oc_page.绩效填报频率配置页.fill_快捷操作_填写表单(**季度填报频率配置_info)
        oc_page.绩效填报频率配置页.click_button("保存")
        oc_page.绩效填报频率配置页.confirm_弹框()
    with 测试步骤("验证配置"):
        # 1.验证填报的频率
        oc_page.绩效填报频率配置页.set_设置当前用户为("jxgly01")
        oc_page.绩效填报频率配置页.navigate()
        res = oc_page.绩效填报频率配置页.get_配置信息()

        freq = 季度填报频率配置_info.get("填报频率")
        expected_len_map = {"年度": 1, "季度": 4, "半年": 2, "月度": 12}

        # assert len(res) == expected_len_map[
        #     freq], f"填报频率为 {freq} 时，预期 {expected_len_map[freq]} 条，实际 {len(res)} 条"

        # todo 2.验证通知是否生效

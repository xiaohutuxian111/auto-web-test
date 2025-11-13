from  src.test_cases import  *


@pytest.fixture
def 财政项目审批通过(oc_page) -> Dict[str, str]:
    return {
        "项目名称": "信息化平台建设2",
        "项目编码": ""
    }



def split_score_integer(n: int, score: int = 100) -> List[int]:
    """
    将总分 score 随机分成 n 份整数，并且保证 sum(parts) == score。
    """
    if n <= 0:
        return []
    if n == 1:
        return [score]

    # 随机生成 n-1 个分割点，并排序
    cuts = sorted(random.randint(0, score) for _ in range(n - 1))
    # 计算每段分数
    parts = [cuts[0]] + [cuts[i] - cuts[i - 1] for i in range(1, n - 1)] + [score - cuts[-1]]
    # 转为整数
    parts = [int(p) for p in parts]
    # 修正因取整导致的差值
    diff = score - sum(parts)
    for i in range(diff):
        parts[i % n] += 1
    return parts

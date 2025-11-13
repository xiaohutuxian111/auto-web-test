import requests
import json
import time
import pandas as pd

BASE_URL = "http://192.168.10.240:8060/auth-ms/api/v1"
TOKEN = "7eb40ccbabfb496c82095a66eaf14791"
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Client-Id': '9075e5c8-e565-4ea9-a046-dded96c0407e',
    'Pragma': 'no-cache',
    'tenant-id': '1',
    'Content-Type': 'application/json'
}


def register_user(nums: int, csv_file="添加用户.csv"):
    """
    批量注册用户，并保存到 CSV
    """
    url = f"{BASE_URL}/systemUser/create"
    ans = []

    for i in range(1, nums + 1):
        username = f"Ztest{i}"
        payload = {
            "nick": username,
            "deptId": "81a882b9f54576341714e6542de2f3f8",
            "orgId": "7317823701dafed4d466dc595f7bde73",
            "loginName": username,
            "code": username,
            "password": "123456",
            "status": "1",
            "post": "2",
            "name": username,
            "postRank": "1",
            "isVerb": "1",
            "deptAndPostList": [
                {
                    "id": "",
                    "deptId": "81a882b9f54576341714e6542de2f3f8",
                    "postId": "3e2f363b74ff451395b372f8747e5b6c"
                }
            ]
        }

        response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
        print(f"[注册用户] {username} → {response.status_code}")

        if response.status_code == 200:
            try:
                resp_json = response.json()
                user_id = resp_json.get("data", {}).get("id", response.text)
            except Exception:
                user_id = response.text

            ans.append({
                "昵称": username,
                "登录名": username,
                "密码": "123456",
                "用户名": f"一级部门A_测试人员A{i}",
                "用户id": user_id
            })

        time.sleep(0.5)  # 防止请求过快

    if ans:
        df = pd.DataFrame(ans)
        df.to_csv(csv_file, index=False, encoding="utf-8-sig")
        print(f"[完成] 已保存 {len(ans)} 个用户到 {csv_file}")
    else:
        print("[警告] 没有成功注册的用户")


def add_permissions(user_ids: list[str], role_id="2D173F015EE54D9FAE7CB34F0983DB5E"):
    """
    批量为用户增加权限
    """
    url = f"{BASE_URL}/systemUser/assignUserRole"

    for user_id in user_ids:
        payload = {
            "userIds": [user_id],
            "roleIds": [role_id],
            "roleGroupIds": [],
            "userGroupIds": []
        }

        response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
        print(f"[授权用户] {user_id} → {response.status_code} {response.text}")
        time.sleep(0.5)


def delete_user(user_id: str):
    """
    删除用户
    """
    url = f"{BASE_URL}/systemUser/delete"
    params = {"id": user_id}
    response = requests.delete(url, headers=HEADERS, params=params)
    print(f"[删除用户] {user_id} → {response.status_code} {response.text}")


if __name__ == "__main__":
    # 1. 批量注册用户
    # register_user(20, csv_file="添加用户1.csv")

    # 2. 从 CSV 读取用户ID
    df = pd.read_csv("添加用户1.csv")
    user_ids = df["用户id"].dropna().astype(str).tolist()

    # 3. 批量赋权
    add_permissions(user_ids)

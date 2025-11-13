import requests
from typing import List, Dict, Any


class FeiShuApi:
    def __init__(self, app_id: str = "cli_a8e646c74938100c", app_secret: str = "JTHoWrkJTAgK2KtZH7lLogRJsTzzWJcD"):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self.tenant_access_token = self.get_tenant_access_token()

    def get_tenant_access_token(self) -> str:
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        data = resp.json()
        if data.get("code", -1) != 0:
            raise Exception(f"获取 tenant_access_token 失败: {data}")
        return data["tenant_access_token"]

    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.tenant_access_token}"
        headers["Content-Type"] = "application/json"
        resp = requests.request(method, url, headers=headers, **kwargs)
        data = resp.json()
        if data.get("code", -1) != 0:
            raise Exception(f"飞书 API 调用失败: {data}")
        return data

    def send(self, receive_id_type: str, receive_id: str, msg_type: str, content: str) -> Dict[str, Any]:
        url = f"{self.base_url}/im/v1/messages?receive_id_type={receive_id_type}"
        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": content
        }
        return self._request("POST", url, json=payload)

    def upload_img(self, img_bytes: bytes) -> str:
        url = f"{self.base_url}/im/v1/images"
        headers = {"Authorization": f"Bearer {self.tenant_access_token}"}
        files = {"image": img_bytes}
        resp = requests.post(url, headers=headers, files=files, data={"image_type": "message"})
        data = resp.json()
        if data.get("code", -1) != 0:
            raise Exception(f"上传图片失败: {data}")
        return data["data"]["image_key"]

    def upload_mp4(self, file_path: str) -> str:
        url = f"{self.base_url}/im/v1/files"
        headers = {"Authorization": f"Bearer {self.tenant_access_token}"}
        files = {"file": open(file_path, "rb")}
        resp = requests.post(url, headers=headers, files=files, data={
            "file_type": "mp4",
            "file_name": file_path.split("/")[-1]
        })
        data = resp.json()
        if data.get("code", -1) != 0:
            raise Exception(f"上传 MP4 失败: {data}")
        return data["data"]["file_key"]

    def bitable_create_records(self, table_token: str, table_id: str, raw_fields: List[Dict[str, Any]]) -> Dict[
        str, Any]:
        url = f"{self.base_url}/bitable/v1/apps/{table_token}/tables/{table_id}/records/batch_create"
        records = [{"fields": item} for item in raw_fields]
        payload = {"records": records}
        return self._request("POST", url, json=payload)

    def  upload_file(self):
        pass


# if __name__ == '__main__':
#     APP_ID = "cli_a8e646c74938100c"
#     APP_SECRET = "JTHoWrkJTAgK2KtZH7lLogRJsTzzWJcD"
#
#     chat_id = 'oc_b2350e0a81b15becb99e59e62c772e1f'
#     feishu = FeiShuApi(app_id=APP_ID, app_secret=APP_SECRET)
#
#     with open('demo.png', 'rb') as f:
#         bimg = f.read()
#
#     image_key = feishu.upload_img(bimg)
#     feishu.send(
#         receive_id_type="chat_id",
#         receive_id=chat_id,
#         msg_type="interactive",
#         content=json.dumps(
#             {
#                 "config": {"wide_screen_mode": True},
#                 "header": {
#                     "title": {
#                         "tag": "plain_text",
#                         # "content": f"{base_ul}的测试用例{request.node.name}发现接口告警:",
#                     },
#                     "template": "turquoise",
#                 },
#                 "elements": [
#                     {
#                         "tag": "div",
#                         "text": {
#                             "tag": "lark_md",
#                             # "content": f"url:\n{url}\n失败信息:\n{fail_info}",
#                         },
#                     },
#                     {
#                         "tag": "img",
#                         "img_key": image_key,
#                         "alt": {
#                             "tag": "plain_text",
#                             "content": "失败时的截图",
#                         },
#                     },
#                 ],
#             }
#         ),
#     )
#
# # 1. 上传图片并发消息
# api_error_img_binary = b"\x89PNG..."
#
# image_key = feishu.upload_img(api_error_img_binary)
# feishu.send(
#     receive_id_type="chat_id",
#     receive_id="chat_id",
#     msg_type="interactive",
#     content=json.dumps({
#         "config": {"wide_screen_mode": True},
#         "elements": [{"tag": "img", "img_key": image_key}]
#     }, ensure_ascii=False)
# )
# print("✅ 图片消息发送成功")
#
# 2. 上传视频
# file_key = feishu.upload_mp4("demo.webm")
# print("✅ 视频上传成功:", file_key)
#
# # 3. 多维表格写入
# table_token = "Bk4CbfXQ0adtvmsaSitcDoBrnyc"
# table_id = "tbl0rIx1AqSP5Ns0"
# update_list = [
#     {"字段A": "值1", "字段B": "值2"},
#     {"字段A": "值3", "字段B": "值4"}
# ]
# feishu.bitable_create_records(table_token, table_id, update_list)
# print("✅ 表格写入成功")

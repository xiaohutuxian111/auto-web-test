# -*- coding: utf-8 -*-
# @Time : 2026/4/30 16:32
# @Author : stone


class BaseDataFactory:
    def __init__(self, api_client):
        self.api = api_client

    def init_base_data(self):
        pass

    def ensure_department(self, name: str):
        pass

    def ensure_user(self, username: str):
        pass

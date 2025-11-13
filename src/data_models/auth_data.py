import json
import yaml
from typing import Dict, Optional, List, Any
from pathlib import Path
from functools import lru_cache

from config.settings import settings


class AuthData:
    """认证数据管理类"""

    def __init__(self, yaml_path: Optional[str] = None):
        self.yaml = yaml_path or f"{settings.BASE_DIR}/data/test_users.yaml"
        self._init_default_data()
        self._load_yaml_data()
        self._cache = {}

    def _init_default_data(self):
        """初始化默认数据"""
        self._default_data = {
            "users": [{
                "username": "winni",
                "password": "playwright001",
                "department": "测试部",
                "roles": ["测试员", "测试组长"],
                "enabled": True,

            }, {
                "username": "winni",
                "password": "playwright001",
                "department": "测试部",
                "roles": ["测试员", "测试组长"],
                "enabled": True,

            }]
        }

    def _load_yaml_data(self):
        """加载YAML数据"""
        try:
            yaml_path = Path(self.yaml)
            if yaml_path.exists():
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    self._yaml_data = yaml.safe_load(f)
            else:
                print(f"YAML文件不存在: {self.yaml}")
                self._yaml_data = None
        except Exception as e:
            print(f"加载YAML文件失败: {e}")
            self._yaml_data = None

    @lru_cache(maxsize=32)
    def get_user_info(self, role: str) -> Dict[str, str]:
        """通过角色获取用户信息"""
        cache_key = f"role_{role}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        if self._yaml_data and 'users' in self._yaml_data:
            users = self._yaml_data['users']
            for user in users:
                if role in user.get('roles', []):
                    result = {
                        "username": user['username'],
                        "password": user['password']
                    }
                    self._cache[cache_key] = result
                    return result

        # 从默认数据中查找
        for user in self._default_data['users']:
            if role in user.get('roles', []):
                result = {
                    "username": user['username'],
                    "password": user['password']
                }
                self._cache[cache_key] = result
                return result
        return {}

    def get_all_users(self) -> Dict[str, Dict[str, Any]]:
        """获取所有用户信息，按角色分组"""
        result = {}
        if self._yaml_data and 'users' in self._yaml_data:
            users = self._yaml_data['users']
            for user in users:
                for role in user.get('roles', []):
                    if role not in result:
                        result[role] = dict(user)
            return result
        return {}

    def get_user_details(self, username: str) -> Optional[Dict[str, Any]]:
        """获取用户的详细信息"""
        if self._yaml_data and 'users' in self._yaml_data:
            users = self._yaml_data['users']
            for user in users:
                if user['username'] == username:
                    return dict(user)
        return None

    def get_users_by_department(self, department: str) -> List[Dict[str, Any]]:
        """获取指定部门的所有用户"""
        if self._yaml_data and 'users' in self._yaml_data:
            users = self._yaml_data['users']
            return [dict(user) for user in users if user['department'] == department]
        return []

    def get_users_by_role(self, role: str) -> List[Dict[str, Any]]:
        """获取指定角色的所有用户"""
        if self._yaml_data and 'users' in self._yaml_data:
            users = self._yaml_data['users']
            return [dict(user) for user in users if role in user.get('roles', [])]
        return []

    def get_enabled_users(self) -> List[Dict[str, Any]]:
        """获取所有启用的用户"""
        if self._yaml_data and 'users' in self._yaml_data:
            users = self._yaml_data['users']
            return [dict(user) for user in users if user.get('enabled', False)]
        return []

    def clear_cache(self):
        """清除缓存"""
        self._cache.clear()
        self.get_user_info.cache_clear()

    def to_json(self) -> str:
        """将用户数据转换为JSON字符串"""
        if self._yaml_data and 'users' in self._yaml_data:
            return json.dumps(self._yaml_data['users'], ensure_ascii=False, indent=2)
        return json.dumps(self._default_data['users'], ensure_ascii=False, indent=2)

    def get_all_users_list(self) -> List[Dict[str, Any]]:
        """获取所有用户信息列表"""
        if self._yaml_data and 'users' in self._yaml_data:
            return [dict(user) for user in self._yaml_data['users']]
        return []


auth_data = AuthData()

if __name__ == '__main__':
    auth = AuthData()

    # 获取所有用户（按角色分组）
    all_users = auth.get_all_users()
    print(all_users)
    # 获取所有用户列表
    all_users_list = auth.get_all_users_list()
    print(all_users_list)

    # 获取指定部门的用户
    dept_users = auth.get_users_by_department("测试部")
    print(dept_users)

    # 获取指定角色的用户
    role_users = auth.get_users_by_role("测试员")
    print(role_users)

    user = auth.get_user_details('jxgly03')
    print(user)

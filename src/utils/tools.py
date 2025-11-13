"""
通用工具函数模块

该模块提供了各种通用工具函数，包括视频处理、图像处理、JSON解析等。
"""

import io
import json
from collections import defaultdict
from typing import Dict, List, Any, Optional

from jsonpath_ng.ext import parse
from moviepy import VideoFileClip
from PIL import Image

import cv2
from PIL import Image
import io


def select_users() -> List[Dict[str, Any]]:
    """
    查询账号密码SQL（示例函数）
    
    这是一个示例函数，展示了如何从数据库查询用户信息并转换为标准格式。
    
    Returns:
        List[Dict[str, Any]]: 用户信息列表
        
    Note:
        此函数目前返回空列表，需要根据实际数据库连接实现。
    """
    # SQL查询语句示例
    sql_query = """
    select
        a.登录名 as 登录名 ,
        a.密码  as 密码,
        a.用户名 as 用户名 ,
        a.角色code as  角色code,
        a.部门  as 部门,
        a.租户标识 as 租户标识,
        ts.name as 角色
    from
        (
        select
            tsu.login_name as 登录名 ,
            tsu."password" as 密码 ,
            tsu.nick as 用户名,
            tsur.role_id as 角色code ,
            tsd."name" as 部门 ,
            tst.code as 租户标识
        from
            t_system_user tsu
        join t_system_user_roles tsur on
            tsu.id = tsur.user_id
        join t_system_dept tsd on
            tsu.dept_id = tsd.id
        join t_system_tenant tst on
            tsu.tenant_id = tst.id)  as  a
    left join t_system_role ts on
        a.角色code = ts.id
    """
    
    # TODO: 实现数据库查询逻辑
    data_lines = []  # 这里应该是从数据库查询的结果
    
    user_dict = defaultdict(lambda: {"password": "", "department": "", "roles": set()})

    for line in data_lines:
        parts = line.strip().split('\t')
        if len(parts) < 7:
            continue
        username, password, _, _, department, _, role = parts
        user = user_dict[username]
        user["password"] = password
        user["department"] = department
        if role:
            user["roles"].add(role)

    users = []
    for username, info in user_dict.items():
        users.append({
            "username": f"{username}",
            "password": f"{info['password']}",
            "department": f"{info['department']}",
            "roles": sorted(list(info['roles'])),
            "enabled": True
        })
    
    return users


def get_frame_bytes_png(video_path: str, timestamp: float = 5.0) -> bytes:
    """
    从视频文件中提取指定时间戳的帧并转换为PNG格式的字节数据
    """
    try:
        clip = VideoFileClip(video_path)

        # 检查时间戳是否有效
        if timestamp > clip.duration:
            raise ValueError(f"时间戳 {timestamp} 超出视频长度 {clip.duration}")

        # 获取指定时间戳的帧
        frame = clip.get_frame(timestamp)

        # 转换为PIL图像
        pil_image = Image.fromarray(frame)

        # 转换为PNG字节数据
        output = io.BytesIO()
        pil_image.save(output, format="PNG")
        byte_png = output.getvalue()

        clip.close()

        return byte_png

    except FileNotFoundError:
        raise FileNotFoundError(f"视频文件不存在: {video_path}")
    except Exception as e:
        raise RuntimeError(f"处理视频文件时发生错误: {e}")




def get_token(storage_state_json: Dict[str, Any]) -> Optional[str]:
    """
    从存储状态JSON中提取ACCESS_TOKEN
    """
    try:
        # 使用JSONPath表达式查找ACCESS_TOKEN
        jsonpath_expr = parse('$..localStorage[?(@.name=="ACCESS_TOKEN")].value')
        
        # 提取匹配项
        matches = jsonpath_expr.find(storage_state_json)
        
        # 解析ACCESS_TOKEN
        if matches:
            value_json = matches[0].value
            return value_json
        
        return None
        
    except Exception as e:
        # 记录错误但不抛出异常，返回None
        print(f"提取ACCESS_TOKEN时发生错误: {e}")
        return None


def get_sub_url(url: str) -> str:
    """
    获取URL的子路径（待实现）
    
    Args:
        url: 完整URL
        
    Returns:
        str: 子路径
        
    TODO: 实现URL子路径提取逻辑
    """
    # TODO: 实现URL子路径提取功能
    raise NotImplementedError("get_sub_url 功能尚未实现")


def parse_json_safely(json_str: str) -> Optional[Dict[str, Any]]:
    """
    安全地解析JSON字符串
    
    Args:
        json_str: JSON字符串
        
    Returns:
        Optional[Dict[str, Any]]: 解析后的字典，解析失败时返回None
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return None


def extract_json_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    使用JSONPath从字典中提取值
    
    Args:
        data: 要搜索的字典
        path: JSONPath表达式
        default: 默认值，当路径不存在时返回
        
    Returns:
        Any: 提取的值或默认值
    """
    try:
        jsonpath_expr = parse(path)
        matches = jsonpath_expr.find(data)
        
        if matches:
            return matches[0].value
        return default
        
    except Exception:
        return default


if __name__ == '__main__':
    # 测试工具函数
    print('=' * 50)
    print("工具函数测试")
    print('=' * 50)
    
    # 测试JSON解析
    test_json = '{"name": "test", "value": 123}'
    result = parse_json_safely(test_json)
    print(f"JSON解析结果: {result}")
    
    # 测试JSONPath提取
    test_data = {"user": {"name": "张三", "age": 25}}
    name = extract_json_value(test_data, "$.user.name", "未知")
    print(f"提取的用户名: {name}")

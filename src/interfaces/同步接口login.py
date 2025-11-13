"""
登录接口模块

该模块提供了用户登录相关的API接口功能，包括：
- 异步登录接口
- 密码加密处理
- 重试机制

支持多种环境的登录认证。
"""

import re
import asyncio
from time import sleep
from typing import Optional, Dict, Any

from src.utils.log_util import logger


async def login(username: str, password: str, env: str, api_context: Any, 
                APIRequestContext: Any, retry_time: int = 3) -> Optional[str]:
    """
    异步登录接口
    
    Args:
        username: 用户名
        password: 密码
        env: 环境标识
        api_context: API上下文对象
        APIRequestContext: API请求上下文类
        retry_time: 重试次数，默认为3次
        
    Returns:
        Optional[str]: 访问令牌，登录失败时返回None或错误信息
        
    Raises:
        Exception: 登录过程中发生异常
        
    Example:
        >>> token = await login("admin", "password", "prod", api_context, APIRequestContext)
        >>> if token:
        >>>     print(f"登录成功，token: {token}")
    """
    for attempt in range(retry_time):
        try:
            logger.info(f"尝试登录用户 {username} 到环境 {env}，第 {attempt + 1} 次尝试")
            
            # 准备登录数据
            data = {"username": username, "password": encrypt(password)}
            
            # 发送登录请求
            oauth = await api_context.fetch(
                "/oauth/login",
                form=data,
                max_redirects=0
            )
            
            # 处理重定向
            location = oauth.headers.get("location")
            if location:
                authorization = await api_context.get(location, max_redirects=0)
                location_authorization = authorization.headers.get("location")
                
                if location_authorization:
                    # 提取访问令牌
                    token_match = re.search("access_token=(.*?)&", location_authorization)
                    if token_match:
                        token = token_match.group(1)
                        logger.info(f"用户 {username} 登录成功")
                        return token
                    else:
                        logger.warning(f"无法从响应中提取访问令牌: {location_authorization}")
                else:
                    error_msg = f"{username}在密码为{password}登录{env}失败"
                    logger.error(error_msg)
                    return error_msg
            else:
                logger.warning(f"登录响应中没有location头")
                
        except Exception as e:
            logger.error(f"登录尝试 {attempt + 1} 失败: {e}")
            if attempt < retry_time - 1:
                logger.info(f"等待2秒后重试...")
                sleep(2)
            else:
                logger.error(f"用户 {username} 登录失败，已重试 {retry_time} 次")
    
    return None


def encrypt(password: str) -> str:
    """
    密码加密处理
    
    Args:
        password: 原始密码
        
    Returns:
        str: 加密后的密码
        
    Note:
        当前实现为简单返回原密码，实际使用时应该实现真正的加密算法。
    """
    # TODO: 实现真正的密码加密算法
    # 当前为简单实现，实际应该使用安全的加密方式
    return password


async def login_with_token(username: str, password: str, env: str, 
                          api_context: Any, APIRequestContext: Any) -> Dict[str, Any]:
    """
    带令牌信息的登录接口
    
    Args:
        username: 用户名
        password: 密码
        env: 环境标识
        api_context: API上下文对象
        APIRequestContext: API请求上下文类
        
    Returns:
        Dict[str, Any]: 登录结果，包含token和状态信息
        
    Example:
        >>> result = await login_with_token("admin", "password", "prod", api_context, APIRequestContext)
        >>> if result["success"]:
        >>>     print(f"登录成功: {result['token']}")
    """
    try:
        token = await login(username, password, env, api_context, APIRequestContext)
        
        if token and not token.startswith(f"{username}在密码为"):
            return {
                "success": True,
                "token": token,
                "username": username,
                "env": env
            }
        else:
            return {
                "success": False,
                "error": token or "登录失败",
                "username": username,
                "env": env
            }
            
    except Exception as e:
        logger.error(f"登录过程中发生异常: {e}")
        return {
            "success": False,
            "error": str(e),
            "username": username,
            "env": env
        }


def validate_login_response(response_data: Dict[str, Any]) -> bool:
    """
    验证登录响应数据的有效性
    
    Args:
        response_data: 登录响应数据
        
    Returns:
        bool: 验证结果，True表示有效
        
    Example:
        >>> response = {"success": True, "token": "abc123"}
        >>> is_valid = validate_login_response(response)
    """
    required_fields = ["success"]
    
    for field in required_fields:
        if field not in response_data:
            logger.error(f"登录响应缺少必需字段: {field}")
            return False
    
    if response_data.get("success") and "token" not in response_data:
        logger.error("登录成功但缺少token字段")
        return False
    
    return True


async def logout(api_context: Any, token: str) -> bool:
    """
    用户登出接口
    
    Args:
        api_context: API上下文对象
        token: 访问令牌
        
    Returns:
        bool: 登出是否成功
        
    Example:
        >>> success = await logout(api_context, "abc123")
        >>> if success:
        >>>     print("登出成功")
    """
    try:
        # 发送登出请求
        response = await api_context.fetch(
            "/oauth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status == 200:
            logger.info("用户登出成功")
            return True
        else:
            logger.warning(f"登出请求返回状态码: {response.status}")
            return False
            
    except Exception as e:
        logger.error(f"登出过程中发生异常: {e}")
        return False

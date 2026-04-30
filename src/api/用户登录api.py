from typing import Optional, Dict, Any


async def login(username: str, password: str, env: str, api_context: Any,
                APIRequestContext: Any, retry_time: int = 3) -> Optional[str]:
    """
    异步登录接口
    """

    pass


async def login_with_token(username: str, password: str, env: str,
                           api_context: Any, APIRequestContext: Any) -> Dict[str, Any]:
    """
    带令牌信息的登录接口

    """
    pass

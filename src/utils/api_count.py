"""
API计数工具模块。

该模块提供轻量级的 Playwright 网络请求统计能力，主要用于：
- 兼容现有 ``with api_count(page):`` 调用方式
- 记录当前代码块内请求数量、失败数量和耗时
- 为后续性能统计和报告扩展保留统一入口
"""

import re
import time
from contextlib import ContextDecorator
from typing import Any, Dict, List, Optional

from playwright.sync_api import Page, Request, Response


def _matches(url: str, filter_pattern: Optional[str]) -> bool:
    if not filter_pattern:
        return True
    try:
        return re.search(filter_pattern, url) is not None
    except re.error:
        return filter_pattern in url


class ApiCounter(ContextDecorator):
    """统计一个代码块内的网络请求。"""

    def __init__(self, page: Page, filter_pattern: Optional[str] = None):
        self.page = page
        self.filter_pattern = filter_pattern
        self.started_at = 0.0
        self.finished_at = 0.0
        self._request_started_at: Dict[Request, float] = {}
        self.records: List[Dict[str, Any]] = []
        self.failed_records: List[Dict[str, Any]] = []

    def __enter__(self) -> "ApiCounter":
        self.started_at = time.perf_counter()
        self.page.on("request", self._on_request)
        self.page.on("response", self._on_response)
        self.page.on("requestfailed", self._on_request_failed)
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.finished_at = time.perf_counter()
        self._remove_listener("request", self._on_request)
        self._remove_listener("response", self._on_response)
        self._remove_listener("requestfailed", self._on_request_failed)
        return False

    def _remove_listener(self, event_name: str, handler) -> None:
        try:
            self.page.remove_listener(event_name, handler)
        except Exception:
            # Playwright 旧版本没有 remove_listener 时不阻断用例。
            pass

    def _on_request(self, request: Request) -> None:
        if not _matches(request.url, self.filter_pattern):
            return
        self._request_started_at[request] = time.perf_counter()

    def _on_response(self, response: Response) -> None:
        request = response.request
        if not _matches(request.url, self.filter_pattern):
            return
        started_at = self._request_started_at.pop(request, self.started_at)
        elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)
        record = {
            "method": request.method,
            "url": request.url,
            "status": response.status,
            "elapsed_ms": elapsed_ms,
            "ok": response.ok,
        }
        self.records.append(record)
        if not response.ok:
            self.failed_records.append(record)

    def _on_request_failed(self, request: Request) -> None:
        if not _matches(request.url, self.filter_pattern):
            return
        started_at = self._request_started_at.pop(request, self.started_at)
        elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)
        failure = request.failure
        if isinstance(failure, dict):
            failure_text = failure.get("errorText", "")
        else:
            failure_text = failure or ""
        record = {
            "method": request.method,
            "url": request.url,
            "status": None,
            "elapsed_ms": elapsed_ms,
            "ok": False,
            "failure": failure_text,
        }
        self.records.append(record)
        self.failed_records.append(record)

    @property
    def statistics(self) -> Dict[str, Any]:
        elapsed_ms = round(((self.finished_at or time.perf_counter()) - self.started_at) * 1000, 2)
        durations = [record["elapsed_ms"] for record in self.records]
        return {
            "total": len(self.records),
            "failed": len(self.failed_records),
            "success": len(self.records) - len(self.failed_records),
            "elapsed_ms": elapsed_ms,
            "avg_elapsed_ms": round(sum(durations) / len(durations), 2) if durations else 0,
            "records": self.records,
            "failed_records": self.failed_records,
        }


def api_count(page: Page, filter_pattern: Optional[str] = None) -> ApiCounter:
    """
    返回 API 统计上下文管理器。

    Example:
        >>> with api_count(page) as counter:
        ...     page.get_by_text("保存").click()
        >>> print(counter.statistics)
    """
    return ApiCounter(page, filter_pattern=filter_pattern)


def monitor_api_calls(page: Page, filter_pattern: Optional[str] = None) -> ApiCounter:
    """创建一个请求监控器，调用方可以手动进入或退出上下文。"""
    return ApiCounter(page, filter_pattern=filter_pattern)


def get_api_statistics(counter: ApiCounter) -> Dict[str, Any]:
    """获取 ApiCounter 的统计结果。"""
    return counter.statistics

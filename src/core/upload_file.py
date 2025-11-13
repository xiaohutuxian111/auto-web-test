"""
文件上传模块

该模块提供了文件上传相关的功能，包括：
- 文件上传操作
- 模板文件下载
- 上传对话框处理

支持Excel、图片、文档等多种文件格式的上传。
"""

from typing import Optional

from src.core import Page, logger


class UploadFile:
    """
    文件上传类
    
    提供了文件上传和模板下载的功能，支持各种文件格式。
    """
    
    def __init__(self, page: Page):
        """
        初始化文件上传类
        
        Args:
            page: Playwright页面对象
        """
        self.page = page
        self.page.wait_for_load_state("networkidle")
        
        # 初始化上传对话框元素
        self.upload_file_div = self.page.locator(".el-dialog")
        self.upload_file_cancel_button = self.upload_file_div.locator('button').filter(has_text='取 消')
        self.upload_file_confirm_button = self.upload_file_div.locator('button').filter(has_text='导入')
        self.upload_file_template_download_button = self.page.get_by_text("点击下载")

    def get_template_download_excel(self) -> None:
        """
        下载Excel模板文件
        
        Raises:
            Exception: 下载失败时抛出异常
        """
        try:
            self.upload_file_template_download_button.click()
            logger.info("Excel模板文件下载成功")
        except Exception as e:
            logger.error(f"Excel模板文件下载失败: {e}")
            raise Exception(f"模板文件下载失败: {e}")

    def upload_file(self, file_path: str, selector: str = "input[type='file']") -> None:
        """
        上传文件
        
        Args:
            file_path: 要上传的文件路径
            selector: 文件输入框的选择器，默认为"input[type='file']"
            
        Raises:
            FileNotFoundError: 当文件不存在时
            Exception: 上传失败时抛出异常
            
        Example:
            >>> uploader = UploadFile(page)
            >>> uploader.upload_file("./data/test.xlsx")
        """
        try:
            # 检查文件是否存在
            import os
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 等待文件上传input元素可见
            file_input = self.upload_file_div.locator(selector)
            
            # 设置文件路径
            file_input.set_input_files(file_path)
            
            # 等待文件处理完成
            self.page.wait_for_timeout(1000)
            
            # 点击确认按钮
            self.upload_file_confirm_button.click()
            
            logger.info(f"文件上传成功: {file_path}")
            
        except FileNotFoundError:
            logger.error(f"文件不存在: {file_path}")
            raise
        except Exception as e:
            error_msg = f"文件:{file_path}上传失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    def cancel_upload(self) -> None:
        """
        取消文件上传
        
        Raises:
            Exception: 取消操作失败时抛出异常
        """
        try:
            self.upload_file_cancel_button.click()
            logger.info("文件上传已取消")
        except Exception as e:
            logger.error(f"取消文件上传失败: {e}")
            raise Exception(f"取消上传失败: {e}")

    def wait_for_upload_complete(self, timeout: int = 10000) -> None:
        """
        等待文件上传完成
        
        Args:
            timeout: 超时时间（毫秒），默认为10000ms
            
        Raises:
            TimeoutError: 超时后上传仍未完成
        """
        try:
            # 等待上传对话框消失或显示成功消息
            self.page.wait_for_selector(".el-dialog", state="hidden", timeout=timeout)
            logger.info("文件上传完成")
        except Exception as e:
            logger.error(f"等待文件上传完成超时: {e}")
            raise TimeoutError(f"文件上传超时: {e}")

    def upload_multiple_files(self, file_paths: list, selector: str = "input[type='file']") -> None:
        """
        上传多个文件
        
        Args:
            file_paths: 要上传的文件路径列表
            selector: 文件输入框的选择器，默认为"input[type='file']"
            
        Raises:
            Exception: 上传失败时抛出异常
        """
        try:
            # 检查所有文件是否存在
            import os
            for file_path in file_paths:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 等待文件上传input元素可见
            file_input = self.upload_file_div.locator(selector)
            
            # 设置多个文件路径
            file_input.set_input_files(file_paths)
            
            # 等待文件处理完成
            self.page.wait_for_timeout(1000)
            
            # 点击确认按钮
            self.upload_file_confirm_button.click()
            
            logger.info(f"多个文件上传成功: {file_paths}")
            
        except FileNotFoundError as e:
            logger.error(f"文件不存在: {e}")
            raise
        except Exception as e:
            error_msg = f"多个文件上传失败: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

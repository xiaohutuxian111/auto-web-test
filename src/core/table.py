"""
表格处理模块

该模块提供了Web表格的操作功能，包括：
- 表格数据获取
- 单元格定位
- 行列操作
- 数据比对
"""

import random
import re
from typing import Union, List, Dict, Optional
from pathlib import Path

from src.core import Page, Locator, logger
from src.core.locators import Locators
from src.utils.excel_util import ExcelUtil


class Table:
    """
    表格处理类
    
    提供了Web表格的各种操作功能，支持数据获取、比对等。
    """

    def __init__(self, page: Page, 唯一文字: Union[str, Locator], 表格序号: int = -1):
        """
        初始化表格处理类
        
        Args:
            page: Playwright页面对象
            唯一文字: 表格的唯一标识文字或定位器
            表格序号: 表格序号，默认为-1（最后一个）
        """
        self.page = page
        self.locators = Locators(page)

        # 等待表格加载完成
        try:
            self.page.locator('*').filter(visible=True).first.click(trial=True)
            self.locators.loading_页面按钮加载()
        except Exception:
            pass

        # 初始化表格元素
        self.table_div = 唯一文字 if isinstance(唯一文字, Locator) else self.page.locator(
            ".el-table__inner-wrapper").filter(visible=True).filter(has_text=唯一文字).nth(表格序号)
        self.table_header_tr = self.table_div.locator("//thead/tr")
        self.除了all的checkbox = self.table_div.locator('//tbody//span[@class="el-checkbox"]').all()

    def click_select_all(self) -> None:
        """
        点击表格头部的全选复选框
        
        Raises:
            Exception: 点击失败时抛出异常
        """
        try:
            self.table_div.locator('//thead/tr').locator('//span[@class="el-checkbox__input"]').filter(
                visible=True).click()
            logger.info("全选复选框点击成功")
        except Exception as e:
            logger.error(f"全选复选框点击失败: {e}")
            raise Exception(f"全选复选框点击失败: {e}")

    def get_header_index(self, 表头文字: str) -> int:
        """
        获取表头所在的列索引
        
        Args:
            表头文字: 表头文字
            
        Returns:
            int: 列索引，从0开始
            
        Raises:
            ValueError: 当表头不存在时
        """
        try:
            header_lis = self.table_header_tr.filter(
                has=self.page.locator(f'th:has-text("{表头文字}")')).inner_text().replace(
                '\n', '').strip().split('\t')
            index = next((i for i, s in enumerate(header_lis) if 表头文字 in s), -1)

            if index == -1:
                raise ValueError(f"表头 '{表头文字}' 不存在")

            # 检查是否有复选框列
            check_box = self.table_header_tr.locator('//input[@type="checkbox"]').count()
            if check_box:
                return index + 1
            else:
                return index

        except Exception as e:
            logger.error(f"获取表头索引失败: {e}")
            raise ValueError(f"获取表头 '{表头文字}' 索引失败: {e}")

    def get_row_locator(self, 行元素定位: Locator) -> Locator:
        """
        获取行元素所在的行定位器
        """
        return self.table_div.locator("tr").filter(has=行元素定位)

    def get_cell(self, 表头文字or列序号: Union[str, int],
                 行元素定位or行序号or行文字: Union[Locator, int, str]) -> Locator:
        """
        获取指定单元格的定位器
        """
        # 获取列序号
        if isinstance(表头文字or列序号, str):
            列序号 = self.get_header_index(表头文字or列序号)
        else:
            列序号 = 表头文字or列序号

        # 获取行定位器
        if isinstance(行元素定位or行序号or行文字, Locator):
            行定位 = self.get_row_locator(行元素定位or行序号or行文字)
        elif isinstance(行元素定位or行序号or行文字, str):
            行定位 = self.table_div.locator("tr").filter(has_text=行元素定位or行序号or行文字)
        else:
            行定位 = self.table_div.locator("tbody").locator('//tr[not(@aria-hidden="true")]').nth(
                行元素定位or行序号or行文字)

        return 行定位.locator("td").nth(列序号)

    def get_row_dict(self, 行元素定位or行序号: Union[Locator, int]) -> Dict[str, str]:
        """
        获取指定行的数据字典
        
        Args:
            行元素定位or行序号: 行定位器或行序号
            
        Returns:
            Dict[str, str]: 行数据字典，键为表头，值为单元格内容
            
        Example:
            >>> row_data = table.get_row_dict(0)  # 获取第0行数据
            >>> print(row_data)  # {'姓名': '张三', '年龄': '25', '城市': '北京'}
        """
        try:
            if isinstance(行元素定位or行序号, int):
                tr = self.table_div.locator("tbody").locator("tr").locator("visible=true").nth(行元素定位or行序号)
            elif isinstance(行元素定位or行序号, Locator):
                tr = self.table_div.locator("tr").filter(has=行元素定位or行序号)
            else:
                all_tr = self.table_div.locator("tbody").locator("tr").locator("visible=true").all()
                tr = random.choice(all_tr)

            td_text_list = tr.locator("td").all_text_contents()
            header_text_list = self.table_header_tr.locator("th").all_text_contents()
            row_dict = dict(zip(header_text_list, td_text_list))
            return row_dict

        except Exception as e:
            logger.error(f"获取行数据失败: {e}")
            raise Exception(f"获取行数据失败: {e}")

    def get_col_list(self, 表头文字: str, text: bool = True) -> List[str]:
        """
        获取指定列的所有数据
        
        Args:
            表头文字: 表头文字
            text: 是否返回文本内容，默认为True
            
        Returns:
            List[str]: 列数据列表
            
        Example:
            >>> names = table.get_col_list("姓名")  # 获取姓名列的所有数据
            >>> print(names)  # ['张三', '李四', '王五']
        """
        try:
            index = self.get_header_index(表头文字)
            all_tr = self.table_div.locator("tbody").locator("tr").filter(has_not=self.page.locator('th')).locator(
                "visible=true").all()
            col_list = []
            for tr in all_tr:
                if text:
                    col_list.append(tr.locator("td").nth(index).text_content())
                else:
                    col_list.append(tr.locator("td").nth(index))
            return col_list

        except Exception as e:
            logger.error(f"获取列数据失败: {e}")
            raise Exception(f"获取列 '{表头文字}' 数据失败: {e}")

    def get_all_rows_as_dict(self) -> List[Dict[str, str]]:
        """
        获取表格中所有行的数据
        
        Returns:
            List[Dict[str, str]]: 所有行数据列表，每行是一个字典
            
        Example:
            >>> all_data = table.get_all_rows_as_dict()
            >>> print(all_data)  # [{'姓名': '张三', '年龄': '25'}, {'姓名': '李四', '年龄': '30'}]
        """
        try:
            rows = []
            all_tr = self.table_div.locator("tbody").locator("tr").filter(has_not=self.page.locator('th')).locator(
                "visible=true").all()
            for i in range(len(all_tr)):
                tr = self.table_div.locator("tbody").locator("tr").locator("visible=true").nth(i)
                td_text_list = tr.locator("td").all_text_contents()
                header_text_list = self.table_header_tr.locator("th").all_text_contents()
                row_dict = dict(zip(header_text_list, td_text_list))
                rows.append(row_dict)
            return rows

        except Exception as e:
            logger.error(f"获取所有行数据失败: {e}")
            raise Exception(f"获取所有行数据失败: {e}")

    def excel和页面table比对(self, excel_path: Path, 要检查的列名: List[str],
                             sheet_name: Optional[str] = None, skip_rows: int = 1) -> bool:
        """
        比对Excel文件与页面表格的数据是否一致
        """
        try:
            excel = ExcelUtil(excel_path)
            for 列名 in 要检查的列名:
                if '/' in 列名:
                    列名列表 = 列名.split('/')
                    页面列名 = 列名列表[0]
                    excel列名 = 列名列表[1]
                else:
                    页面列名 = 列名
                    excel列名 = 列名

                excel一列数据 = excel.get_col_excel(sheet_name, excel列名, skip_rows)
                页面一列数据 = self.get_col_list(页面列名)

                for excel一个数据 in excel一列数据:
                    excel一个数据 = str(excel一个数据)
                    一致 = False

                    for 页面一个数据 in 页面一列数据:
                        页面一个数据 = str(页面一个数据)

                        # 多种比对方式
                        完全相等 = excel一个数据 == 页面一个数据
                        加上百分比相等 = excel一个数据 == f"{页面一个数据}%"
                        数字相等 = False

                        try:
                            数字相等 = float(excel一个数据) == float(页面一个数据.replace(",", ''))
                        except (ValueError, TypeError):
                            pass

                        年月日相等 = excel一个数据.split(" ")[0] == 页面一个数据
                        excel为None = excel一个数据 == 'None'
                        剔除空格后相等 = re.sub(r'\s+', '', 页面一个数据) == re.sub(r'\s+', '', excel一个数据)

                        一致 = (完全相等 or 加上百分比相等 or 数字相等 or
                                年月日相等 or excel为None or 剔除空格后相等)

                        if 一致:
                            break

                    if not 一致:
                        error_msg = f"Excel数据{excel列名}:{excel一个数据}和页面数据 {页面列名}: {页面一个数据} 不一致"
                        logger.error(error_msg)
                        raise Exception(error_msg)

            logger.info("Excel和页面表格数据比对成功")
            return True

        except Exception as e:
            logger.error(f"Excel和页面表格比对失败: {e}")
            raise Exception(f"数据比对失败: {e}")

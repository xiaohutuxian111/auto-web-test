"""
Excel处理工具模块

该模块提供了Excel文件的读写操作功能，支持pandas和openpyxl两种引擎。
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Union

import pandas as pd
from openpyxl import load_workbook
from pandas import DataFrame

from src.utils.pd_util import delete_rows_by_all_none, fillna_with_empty


class ExcelUtil:
    """
    Excel文件处理工具类
    
    支持Excel文件的读取、写入、列名映射等功能。
    """

    def __init__(self, file_path: Union[Path, str, bytes], sheet_name: Optional[str] = None, skip_row: int = 1):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.skip_row = skip_row

    def _match_column(self, df_columns:List[str], key: str) -> Optional[str]:
        """
        使用正则匹配 key 对应的列名
        """
        pattern = re.compile(
            rf"^\s*\**{re.escape(key.replace('__', '.'))}\**([（(][^）)]*[）)])?[:：]*\s*$"
        )
        for col in df_columns:
            if re.match(pattern, str(col)):
                return col
        return None

    def write_excel(self, sheet_name: Optional[str] = None, info_data: Optional[List[Dict]] = None,
                    skip_row: int = 1) -> None:
        """
        写入数据到Excel文件，支持列名正则匹配
        """
        if not info_data:
            raise ValueError("info_data 不能为空")

        sheet = sheet_name or self.sheet_name
        df = pd.DataFrame(info_data)
        try:
            if os.path.exists(self.file_path):
                # 文件存在，加载已有文件
                existing = pd.read_excel(self.file_path, sheet_name=sheet, skiprows=skip_row)

                # 处理列名匹配
                col_map = {}
                for col in df.columns:
                    match_col = self._match_column(list(existing.columns), col)
                    if match_col:
                        col_map[col] = match_col
                df = df.rename(columns=col_map)

                # 追加写入
                with pd.ExcelWriter(self.file_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                    df.to_excel(writer, sheet_name=sheet, index=False, header=False, startrow=len(existing) + skip_row+1)
            else:
                # 文件不存在，新建
                with pd.ExcelWriter(self.file_path, engine="openpyxl") as writer:
                    df.to_excel(writer, sheet_name=sheet, index=False, startrow=skip_row)

        except Exception as e:
            raise RuntimeError(f"写入excel失败: {self.file_path}, 异常信息: {e}")

        try:
            if os.path.exists(self.file_path):
                # 文件存在，追加数据
                self._write_to_existing_file(sheet, df, skip_row)
            else:
                # 文件不存在，新建文件
                self._create_new_file(sheet, df, skip_row)

        except Exception as e:
            raise RuntimeError(f"写入excel失败: {self.file_path}, 异常信息: {e}")

    def _write_to_existing_file(self, sheet_name: str, df: DataFrame, skip_row: int) -> None:
        """
        向现有Excel文件写入数据
        
        Args:
            sheet_name: 工作表名称
            df: 要写入的DataFrame
            skip_row: 跳过的行数
        """
        # 加载原始Excel文件
        wb = load_workbook(self.file_path)
        ws = wb[sheet_name]

        # 获取目标sheet的列名（假设在skip_row行）
        header_row = skip_row + 1  # openpyxl 是从 1 开始计数的
        column_map = {}  # {列名: Excel中的列索引}

        for col in range(1, ws.max_column + 1):
            cell_value = ws.cell(row=header_row, column=col).value
            if cell_value:
                column_map[cell_value] = col

        # 找到DataFrame中的每列应该写到Excel的哪一列
        for df_row_idx, row in df.iterrows():
            excel_row = header_row + 1 + df_row_idx
            for col_name, value in row.items():
                if col_name in column_map:
                    col_idx = column_map[col_name]
                    ws.cell(row=excel_row, column=col_idx, value=value)

        wb.save(self.file_path)

    def _create_new_file(self, sheet_name: str, df: DataFrame, skip_row: int) -> None:
        """
        创建新的Excel文件并写入数据
        
        Args:
            sheet_name: 工作表名称
            df: 要写入的DataFrame
            skip_row: 跳过的行数
        """
        with pd.ExcelWriter(self.file_path, mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=self.skip_row - 1)

    def _df_header_2_excel_header(self, df_header: List[str], excel_header: List[str]) -> Dict[str, str]:
        """
        实现DataFrame的标题和Excel的标题映射
        
        Args:
            df_header: DataFrame的列名列表
            excel_header: Excel的列名列表
            
        Returns:
            Dict[str, str]: 映射字典
            
        Raises:
            ValueError: 当两个列表长度不一致时
        """
        if len(df_header) != len(excel_header):
            raise ValueError("df_header 和 excel_header 长度不一致，无法一一映射")

        mapping = {}
        for df_col in df_header:
            for excel_col in excel_header:
                if df_col in excel_col:
                    mapping[df_col] = excel_col
                    break  # 只取第一个匹配的
        return mapping

    def get_excel_headers(self) -> List[str]:
        """
        获取Excel文件的列标题
        
        Returns:
            List[str]: 列标题列表
        """
        column_headers = pd.read_excel(
            self.file_path,
            sheet_name=self.sheet_name,
            skiprows=self.skip_row,
            engine='openpyxl'
        )
        return column_headers.columns.tolist()

    def get_excel_info(self) -> List[Dict]:
        """
        读取Excel文件，将数据转换为List[dict]，每行为一个dict，key为表头
        
        Returns:
            List[Dict]: 数据列表
        """
        content = pd.read_excel(self.file_path, sheet_name=self.sheet_name, skiprows=self.skip_row)

        # 删除空行
        content = delete_rows_by_all_none(content)

        # 将na转化为空字符串
        content = fillna_with_empty(content)

        # 去除表头多余字符
        content = self._去除表头多余字符or空格(content)

        return content.to_dict(orient="records")

    def get_col_excel(self, sheet_name: str, col_name: str, skip_row: int = 1) -> List[str]:
        """
        获取指定列的Excel数据
        
        Args:
            sheet_name: 工作表名称
            col_name: 列名
            skip_row: 跳过的行数
            
        Returns:
            List[str]: 列数据列表
        """
        df = pd.read_excel(io=self.file_path, sheet_name=sheet_name, skiprows=skip_row)
        return df[col_name].tolist()

    def get_rows_excel(self) -> int:
        """
        获取Excel文件的有效行数
        
        Returns:
            int: 有效行数
        """
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name, skiprows=self.skip_row)
        df = delete_rows_by_all_none(df)
        return df.shape[0]

    def _去除表头多余字符or空格(self, df: DataFrame) -> DataFrame:
        """
        去除DataFrame所有列名中的*、（必填）、(必填)等必填标记
        
        Args:
            df: 原始DataFrame
            
        Returns:
            DataFrame: 处理后的DataFrame
        """
        df = df.copy()
        df.columns = [self.__clean_title(col) for col in df.columns]
        return df

    @staticmethod
    def __clean_title(title: str) -> str:
        """
        清理列标题，去除必填标记等多余字符
        
        Args:
            title: 原始标题
            
        Returns:
            str: 清理后的标题
        """
        # 去除*、（必填）、(必填)及其变体
        title = title.strip()
        title = re.sub(r"\*", "", title)
        title = re.sub(r"[（(]必填[)）]", "", title)
        return title.strip()

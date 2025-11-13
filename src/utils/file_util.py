import os
import shutil
import json
from datetime import datetime
from typing import Optional, Dict, Any, Callable, Literal

from docx import Document
from filelock import FileLock
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from PIL import Image, ImageDraw, ImageFont

from src.utils.log_util import logger


def clear_folder(folder_path: str) -> None:
    """
    清空文件夹中的所有内容
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"文件夹不存在: {folder_path}")

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            raise RuntimeError(f'删除 {file_path} 失败：{e}')


def check_file_exists(file_path: str) -> bool:
    """
    检查文件是否存在且不为空
    """

    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            return file_size > 0
    return False


def modify_docx(input_file: str, output_file: str,
                old_text: Optional[str] = None,
                new_text: Optional[str] = None,
                add_timestamp: bool = False) -> str:
    """
    修改Word文档内容
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")

    # 打开文档
    doc = Document(input_file)

    # 替换文本（如果提供了old_text和new_text）
    if old_text and new_text:
        # 遍历文档中的每个段落
        for para in doc.paragraphs:
            if old_text in para.text:
                para.text = para.text.replace(old_text, new_text)

        # 遍历文档中的每个表格
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        if old_text in para.text:
                            para.text = para.text.replace(old_text, new_text)

    # 添加时间戳（如果add_timestamp为True）
    if add_timestamp:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doc.add_paragraph(f"文档处理时间：{current_time}")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 另存为新的文档
    doc.save(output_file)
    return output_file


def generate_formatted_file(file_type: Literal['docx', 'txt', 'bmp', 'xlsx', 'pdf', 'jpg', 'jpeg', 'png'],
                            file_path: str) -> None:
    """
    生成指定格式的测试文件
    """
    file_type = file_type.lower()

    # 确保输出目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        if file_type == 'docx':
            _generate_docx(file_path)
        elif file_type == 'txt':
            _generate_txt(file_path)
        elif file_type == 'bmp':
            _generate_bmp(file_path)
        elif file_type == 'xlsx':
            _generate_xlsx(file_path)
        elif file_type == 'pdf':
            _generate_pdf(file_path)
        elif file_type in ['jpg', 'jpeg', 'png']:
            _generate_image(file_path, file_type)
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")

    except Exception as e:
        raise RuntimeError(f"生成文件失败: {e}")


def _generate_docx(file_path: str) -> None:
    """生成Word文档"""
    doc = Document()
    doc.add_heading('自动生成的 Word 文档', level=1)
    doc.add_paragraph('这是一个用于测试的 .docx 文件。')
    doc.save(file_path)
    logger.info(f"✔️ 已生成 Word 文件：{file_path}")


def _generate_txt(file_path: str) -> None:
    """生成文本文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('这是一个测试文本文件。')
    logger.info(f"✔️ 已生成 TXT 文件：{file_path}")


def _generate_bmp(file_path: str) -> None:
    """生成BMP图像文件"""
    img = Image.new('RGB', (400, 200), color='lightgreen')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    draw.text((10, 80), "测试 BMP 图像", fill='black', font=font)
    img.save(file_path, format='BMP')
    logger.info(f"✔️ 已生成 BMP 文件：{file_path}")


def _generate_xlsx(file_path: str) -> None:
    """生成Excel文件"""
    wb = Workbook()
    ws = wb.active
    ws.title = "测试数据"
    ws.append(["姓名", "年龄", "城市"])
    ws.append(["张三", 25, "北京"])
    ws.append(["李四", 30, "上海"])
    wb.save(file_path)
    logger.info(f"✔️ 已生成 Excel 文件：{file_path}")


def _generate_pdf(file_path: str) -> None:
    """生成PDF文件"""
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [
        Paragraph("自动生成的 PDF 文件", styles['Title']),
        Spacer(1, 12),
        Paragraph("这是用于测试的 PDF 内容段落。", styles['BodyText'])
    ]
    doc.build(elements)
    logger.info(f"✔️ 已生成 PDF 文件：{file_path}")


def _generate_image(file_path: str, file_type: str) -> None:
    """生成图像文件"""
    img = Image.new('RGB', (400, 200), color='skyblue')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    draw.text((10, 80), "测试图像文件", fill='black', font=font)
    img.save(file_path)
    logger.info(f"✔️ 已生成图像文件：{file_path}")


def get_file_size(file_path: str) -> int:
    """
    获取文件大小（字节）
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    return os.path.getsize(file_path)


def get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名
    """
    return os.path.splitext(file_path)[1]


def is_valid_file_path(file_path: str) -> bool:
    """
    检查文件路径是否有效
    """
    try:
        # 检查路径是否包含非法字符
        invalid_chars = '<>:"|?*'
        if any(char in file_path for char in invalid_chars):
            return False

        # 检查路径长度（Windows限制）
        if len(file_path) > 260:
            return False

        return True
    except Exception:
        return False


class JsonCache:
    """带锁的 JSON 缓存工具"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock_path = file_path + ".lock"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            self._write({})

    def _read(self) -> Dict[str, Any]:
        """读取 JSON 文件（带锁）"""

        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]):
        """写入 JSON 文件（带锁）"""
        with FileLock(self.lock_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def get_or_init(self, key: str, init_fn: Callable[[], Dict[str, Any]]) -> Dict[str, Any]:
        """获取指定 key，如果不存在则初始化（带二次检查，避免并发写覆盖）"""
        data = self._read()
        if key not in data:
            value = init_fn()
            # 二次检查
            data = self._read()
            if key not in data:
                data[key] = value
                self._write(data)
            else:
                value = data[key]  # 已被其他线程创建
            return value
        return data[key]

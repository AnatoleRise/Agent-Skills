#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 解析器 v1.0
用于将 Markdown 文本解析为结构化数据，并生成 DOCX 文档

功能：
1. 支持 Headers (H1-H6)
2. 支持 Paragraphs
3. 支持 Ordered/Unordered lists
4. 支持 Code blocks
5. 支持 Tables
6. 支持 Quotes
7. 支持 Images
8. 支持 Horizontal rules
9. 安全输入验证
10. 完善的错误处理
"""

import os
import re
from typing import List, Dict, Union, Optional, Any, Tuple
from pathlib import Path

# 导入 DocxGenerator
from docx_generator import DocxGenerator, DocxGeneratorError, ValidationError


# ==================== 自定义异常 ====================

class MarkdownParserError(Exception):
    """Markdown 解析器异常基类"""
    
    def __init__(self, message: str, line_number: Optional[int] = None):
        self.line_number = line_number
        if line_number is not None:
            message = f"第 {line_number} 行: {message}"
        super().__init__(message)


class MarkdownSyntaxError(MarkdownParserError):
    """Markdown 语法错误"""
    pass


class SecurityError(MarkdownParserError):
    """安全错误"""
    pass


# ==================== 安全验证函数 ====================

def validate_input_path(path: str) -> str:
    """
    验证输入文件路径，防止路径遍历攻击
    
    Args:
        path: 输入文件路径
        
    Returns:
        规范化后的绝对路径
        
    Raises:
        SecurityError: 路径不安全或文件不存在
        MarkdownParserError: 其他验证错误
    """
    if not path:
        raise MarkdownParserError("输入路径不能为空")
    
    # 检查是否包含空字节
    if '\x00' in path:
        raise SecurityError("路径包含空字节，可能是攻击尝试")
    
    # 规范化路径
    try:
        abs_path = os.path.abspath(os.path.normpath(path))
    except Exception as e:
        raise MarkdownParserError(f"路径规范化失败: {str(e)}")
    
    # 检查路径遍历攻击
    # 获取当前工作目录
    cwd = os.getcwd()
    
    # 检查路径是否在允许的安全范围内
    # 这里我们允许项目目录下的文件
    allowed_prefixes = [
        cwd,
        os.path.expanduser('~'),
        '/tmp',
        '/var/tmp'
    ]
    
    is_safe = any(
        abs_path.startswith(prefix) or abs_path == prefix
        for prefix in allowed_prefixes
    )
    
    if not is_safe:
        raise SecurityError(
            f"路径 '{path}' 不在安全范围内。只允许访问当前工作目录、用户主目录或临时目录下的文件"
        )
    
    # 检查文件是否存在
    if not os.path.exists(abs_path):
        raise MarkdownParserError(f"文件不存在: {path}")
    
    # 检查是否为文件
    if not os.path.isfile(abs_path):
        raise MarkdownParserError(f"路径不是文件: {path}")
    
    # 检查文件扩展名
    _, ext = os.path.splitext(abs_path.lower())
    if ext not in ['.md', '.markdown', '.txt']:
        raise MarkdownParserError(
            f"不支持的文件类型 '{ext}'。只支持 .md, .markdown, .txt 文件"
        )
    
    # 检查文件大小（防止内存耗尽攻击）
    max_size = 50 * 1024 * 1024  # 50MB
    try:
        file_size = os.path.getsize(abs_path)
        if file_size > max_size:
            raise MarkdownParserError(
                f"文件过大 ({file_size / 1024 / 1024:.1f}MB)，最大允许 50MB"
            )
    except OSError as e:
        raise MarkdownParserError(f"无法获取文件大小: {str(e)}")
    
    # 检查文件是否可读
    if not os.access(abs_path, os.R_OK):
        raise MarkdownParserError(f"文件不可读: {path}")
    
    return abs_path


def validate_output_path(path: str) -> str:
    """
    验证输出路径，防止路径遍历攻击
    
    Args:
        path: 输出文件路径
        
    Returns:
        规范化后的绝对路径
        
    Raises:
        SecurityError: 路径不安全
        MarkdownParserError: 其他验证错误
    """
    if not path:
        raise MarkdownParserError("输出路径不能为空")
    
    # 检查是否包含空字节
    if '\x00' in path:
        raise SecurityError("路径包含空字节，可能是攻击尝试")
    
    # 规范化路径
    try:
        abs_path = os.path.abspath(os.path.normpath(path))
    except Exception as e:
        raise MarkdownParserError(f"路径规范化失败: {str(e)}")
    
    # 检查路径遍历攻击
    cwd = os.getcwd()
    allowed_prefixes = [
        cwd,
        os.path.expanduser('~'),
        '/tmp',
        '/var/tmp'
    ]
    
    is_safe = any(
        abs_path.startswith(prefix) or abs_path == prefix
        for prefix in allowed_prefixes
    )
    
    if not is_safe:
        raise SecurityError(
            f"输出路径 '{path}' 不在安全范围内。只允许写入当前工作目录、用户主目录或临时目录"
        )
    
    # 获取目录路径
    dir_path = os.path.dirname(abs_path)
    
    # 如果目录不存在，尝试创建
    if dir_path and not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError as e:
            raise MarkdownParserError(f"无法创建输出目录: {str(e)}")
    
    # 检查目录是否可写
    if dir_path and os.path.exists(dir_path):
        if not os.access(dir_path, os.W_OK):
            raise MarkdownParserError(f"输出目录不可写: {dir_path}")
    
    # 检查文件扩展名
    if not abs_path.lower().endswith('.docx'):
        abs_path += '.docx'
    
    # 检查文件是否已存在且不可写
    if os.path.exists(abs_path):
        if not os.access(abs_path, os.W_OK):
            raise MarkdownParserError(f"输出文件已存在且不可写: {abs_path}")
    
    return abs_path


def sanitize_input(text: str) -> str:
    """
    清理输入文本，防止命令注入和其他攻击
    
    Args:
        text: 输入文本
        
    Returns:
        清理后的文本
    """
    if not isinstance(text, str):
        text = str(text)
    
    # 移除空字节
    text = text.replace('\x00', '')
    
    # 移除控制字符（保留换行、制表符等常用字符）
    # 允许: \t(9), \n(10), \r(13)
    allowed_controls = {9, 10, 13}
    text = ''.join(
        char if ord(char) >= 32 or ord(char) in allowed_controls else ''
        for char in text
    )
    
    # 限制文本长度（防止内存攻击）
    max_length = 10 * 1024 * 1024  # 10MB
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


# ==================== Markdown 元素类型 ====================

class MarkdownElement:
    """Markdown 元素基类"""
    
    def __init__(self, element_type: str, content: Any, line_number: int = 0):
        self.element_type = element_type
        self.content = content
        self.line_number = line_number
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'type': self.element_type,
            'content': self.content,
            'line_number': self.line_number
        }


class HeaderElement(MarkdownElement):
    """标题元素"""
    
    def __init__(self, level: int, text: str, line_number: int = 0):
        super().__init__('header', text, line_number)
        self.level = level
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result['level'] = self.level
        return result


class ParagraphElement(MarkdownElement):
    """段落元素"""
    
    def __init__(self, text: str, line_number: int = 0):
        super().__init__('paragraph', text, line_number)


class ListItemElement(MarkdownElement):
    """列表项元素"""
    
    def __init__(self, text: str, level: int = 0, line_number: int = 0):
        super().__init__('list_item', text, line_number)
        self.level = level


class ListElement(MarkdownElement):
    """列表元素"""
    
    def __init__(self, items: List[str], ordered: bool = False, line_number: int = 0):
        super().__init__('list', items, line_number)
        self.ordered = ordered
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result['ordered'] = self.ordered
        return result


class CodeBlockElement(MarkdownElement):
    """代码块元素"""
    
    def __init__(self, code: str, language: str = '', line_number: int = 0):
        super().__init__('code_block', code, line_number)
        self.language = language
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result['language'] = self.language
        return result


class TableElement(MarkdownElement):
    """表格元素"""
    
    def __init__(
        self,
        headers: List[str],
        rows: List[List[str]],
        line_number: int = 0
    ):
        super().__init__('table', {'headers': headers, 'rows': rows}, line_number)
        self.headers = headers
        self.rows = rows


class QuoteElement(MarkdownElement):
    """引用元素"""
    
    def __init__(self, text: str, line_number: int = 0):
        super().__init__('quote', text, line_number)


class ImageElement(MarkdownElement):
    """图片元素"""
    
    def __init__(self, alt: str, url: str, line_number: int = 0):
        super().__init__('image', {'alt': alt, 'url': url}, line_number)
        self.alt = alt
        self.url = url


class HorizontalRuleElement(MarkdownElement):
    """水平线元素"""
    
    def __init__(self, line_number: int = 0):
        super().__init__('horizontal_rule', None, line_number)


# ==================== Markdown 解析器 ====================

class MarkdownParser:
    """
    Markdown 解析器
    
    支持解析以下元素：
    - Headers (H1-H6): # 到 ######
    - Paragraphs: 普通文本段落
    - Ordered lists: 1. 2. 3. 格式
    - Unordered lists: - 或 * 格式
    - Code blocks: 三个反引号包裹的代码块
    - Tables: | 列1 | 列2 | 格式
    - Quotes: > 开头的引用
    - Images: ![alt](url) 格式
    - Horizontal rules: --- 或 *** 或 ___
    """
    
    # 正则表达式模式
    HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$')
    UNORDERED_LIST_PATTERN = re.compile(r'^(\s*)[-*+]\s+(.+)$')
    ORDERED_LIST_PATTERN = re.compile(r'^(\s*)\d+\.\s+(.+)$')
    CODE_BLOCK_START_PATTERN = re.compile(r'^```(\w*)\s*$')
    CODE_BLOCK_END_PATTERN = re.compile(r'^```\s*$')
    TABLE_PATTERN = re.compile(r'^\|(.+)\|\s*$')
    TABLE_SEPARATOR_PATTERN = re.compile(r'^\|[-:\s|]+\|\s*$')
    QUOTE_PATTERN = re.compile(r'^>\s*(.*)$')
    IMAGE_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    HORIZONTAL_RULE_PATTERN = re.compile(r'^(---|___|\*\*\*)\s*$')
    
    def __init__(self):
        self.elements: List[MarkdownElement] = []
        self.current_line = 0
    
    def parse_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        解析 Markdown 文件
        
        Args:
            filepath: Markdown 文件路径
            
        Returns:
            解析后的元素列表（字典格式）
            
        Raises:
            MarkdownParserError: 解析错误
            SecurityError: 安全错误
        """
        # 验证输入路径
        safe_path = validate_input_path(filepath)
        
        try:
            with open(safe_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            raise MarkdownParserError(f"文件编码错误，请使用 UTF-8 编码: {filepath}")
        except IOError as e:
            raise MarkdownParserError(f"无法读取文件: {str(e)}")
        
        return self.parse_text(content)
    
    def parse_text(self, text: str) -> List[Dict[str, Any]]:
        """
        解析 Markdown 文本
        
        Args:
            text: Markdown 文本内容
            
        Returns:
            解析后的元素列表（字典格式）
        """
        # 清理输入
        text = sanitize_input(text)
        
        self.elements = []
        lines = text.split('\n')
        self.current_line = 0
        
        while self.current_line < len(lines):
            line = lines[self.current_line]
            
            # 跳过空行
            if not line.strip():
                self.current_line += 1
                continue
            
            # 尝试解析各种元素
            if self._try_parse_code_block(lines):
                continue
            elif self._try_parse_table(lines):
                continue
            elif self._try_parse_header(line):
                pass
            elif self._try_parse_horizontal_rule(line):
                pass
            elif self._try_parse_list(lines):
                continue
            elif self._try_parse_quote(lines):
                continue
            else:
                self._try_parse_paragraph(lines)
                continue
            
            self.current_line += 1
        
        return [elem.to_dict() for elem in self.elements]
    
    def _try_parse_header(self, line: str) -> bool:
        """尝试解析标题"""
        match = self.HEADER_PATTERN.match(line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            element = HeaderElement(level, text, self.current_line + 1)
            self.elements.append(element)
            return True
        return False
    
    def _try_parse_horizontal_rule(self, line: str) -> bool:
        """尝试解析水平线"""
        if self.HORIZONTAL_RULE_PATTERN.match(line):
            element = HorizontalRuleElement(self.current_line + 1)
            self.elements.append(element)
            return True
        return False
    
    def _try_parse_code_block(self, lines: List[str]) -> bool:
        """尝试解析代码块"""
        line = lines[self.current_line]
        match = self.CODE_BLOCK_START_PATTERN.match(line)
        
        if not match:
            return False
        
        language = match.group(1).strip()
        code_lines = []
        start_line = self.current_line + 1
        self.current_line += 1
        
        while self.current_line < len(lines):
            current_line = lines[self.current_line]
            if self.CODE_BLOCK_END_PATTERN.match(current_line):
                break
            code_lines.append(current_line)
            self.current_line += 1
        
        # 检查是否正确关闭
        if self.current_line >= len(lines):
            raise MarkdownSyntaxError(
                "代码块未正确关闭，缺少结束标记 ```",
                start_line
            )
        
        code = '\n'.join(code_lines)
        element = CodeBlockElement(code, language, start_line)
        self.elements.append(element)
        self.current_line += 1  # 跳过结束标记
        return True
    
    def _try_parse_table(self, lines: List[str]) -> bool:
        """尝试解析表格"""
        line = lines[self.current_line]
        
        # 检查是否是表格开始
        if not self.TABLE_PATTERN.match(line):
            return False
        
        # 收集表格行
        table_lines = []
        start_line = self.current_line + 1
        
        while (self.current_line < len(lines) and 
               self.TABLE_PATTERN.match(lines[self.current_line])):
            table_lines.append(lines[self.current_line])
            self.current_line += 1
        
        # 表格至少需要两行（表头和分隔符）
        if len(table_lines) < 2:
            # 回退，当作普通段落处理
            self.current_line = start_line - 1
            return False
        
        # 检查第二行是否是分隔符
        if not self.TABLE_SEPARATOR_PATTERN.match(table_lines[1]):
            # 回退，当作普通段落处理
            self.current_line = start_line - 1
            return False
        
        # 解析表头
        headers = self._parse_table_row(table_lines[0])
        
        # 解析数据行（跳过分隔符）
        rows = []
        for table_line in table_lines[2:]:
            row = self._parse_table_row(table_line)
            rows.append(row)
        
        element = TableElement(headers, rows, start_line)
        self.elements.append(element)
        return True
    
    def _parse_table_row(self, line: str) -> List[str]:
        """解析表格行"""
        # 移除首尾的 |
        line = line.strip()
        if line.startswith('|'):
            line = line[1:]
        if line.endswith('|'):
            line = line[:-1]
        
        # 分割单元格
        cells = [cell.strip() for cell in line.split('|')]
        return cells
    
    def _try_parse_list(self, lines: List[str]) -> bool:
        """尝试解析列表"""
        line = lines[self.current_line]
        
        # 检查是否是列表项
        unordered_match = self.UNORDERED_LIST_PATTERN.match(line)
        ordered_match = self.ORDERED_LIST_PATTERN.match(line)
        
        if not unordered_match and not ordered_match:
            return False
        
        # 确定列表类型
        is_ordered = ordered_match is not None
        
        # 收集列表项
        items = []
        start_line = self.current_line + 1
        
        while self.current_line < len(lines):
            current_line = lines[self.current_line]
            
            # 检查无序列表项
            unordered = self.UNORDERED_LIST_PATTERN.match(current_line)
            # 检查有序列表项
            ordered = self.ORDERED_LIST_PATTERN.match(current_line)
            
            if unordered:
                if is_ordered:
                    # 类型混合，结束当前列表
                    break
                items.append(unordered.group(2).strip())
            elif ordered:
                if not is_ordered:
                    # 类型混合，结束当前列表
                    break
                items.append(ordered.group(2).strip())
            elif current_line.strip() == '':
                # 空行，检查下一行是否还是列表项
                next_idx = self.current_line + 1
                if next_idx < len(lines):
                    next_line = lines[next_idx]
                    if (self.UNORDERED_LIST_PATTERN.match(next_line) or
                        self.ORDERED_LIST_PATTERN.match(next_line)):
                        self.current_line += 1
                        continue
                break
            else:
                # 非列表行，结束
                break
            
            self.current_line += 1
        
        if items:
            element = ListElement(items, is_ordered, start_line)
            self.elements.append(element)
            return True
        
        return False
    
    def _try_parse_quote(self, lines: List[str]) -> bool:
        """尝试解析引用"""
        line = lines[self.current_line]
        match = self.QUOTE_PATTERN.match(line)
        
        if not match:
            return False
        
        # 收集引用行
        quote_lines = []
        start_line = self.current_line + 1
        
        while self.current_line < len(lines):
            current_line = lines[self.current_line]
            match = self.QUOTE_PATTERN.match(current_line)
            
            if match:
                quote_lines.append(match.group(1))
            elif current_line.strip() == '':
                # 空行，检查下一行是否还是引用
                next_idx = self.current_line + 1
                if next_idx < len(lines):
                    next_line = lines[next_idx]
                    if self.QUOTE_PATTERN.match(next_line):
                        self.current_line += 1
                        continue
                break
            else:
                break
            
            self.current_line += 1
        
        if quote_lines:
            text = '\n'.join(quote_lines)
            element = QuoteElement(text, start_line)
            self.elements.append(element)
            return True
        
        return False
    
    def _try_parse_paragraph(self, lines: List[str]) -> bool:
        """尝试解析段落"""
        start_line = self.current_line + 1
        para_lines = []
        
        while self.current_line < len(lines):
            line = lines[self.current_line]
            
            # 空行结束段落
            if not line.strip():
                break
            
            # 检查是否是其他元素的开始
            if (self.HEADER_PATTERN.match(line) or
                self.HORIZONTAL_RULE_PATTERN.match(line) or
                self.CODE_BLOCK_START_PATTERN.match(line) or
                self.TABLE_PATTERN.match(line) or
                self.UNORDERED_LIST_PATTERN.match(line) or
                self.ORDERED_LIST_PATTERN.match(line) or
                self.QUOTE_PATTERN.match(line)):
                break
            
            para_lines.append(line)
            self.current_line += 1
        
        if para_lines:
            text = ' '.join(para_lines)
            # 处理行内图片
            text = self._process_inline_images(text, start_line)
            element = ParagraphElement(text, start_line)
            self.elements.append(element)
            return True
        
        return False
    
    def _process_inline_images(self, text: str, line_number: int) -> str:
        """处理行内图片标记"""
        # 查找图片标记并创建图片元素
        # 注意：这里我们简化处理，将图片作为独立元素添加
        # 实际文本中的图片标记保留在段落中
        
        matches = list(self.IMAGE_PATTERN.finditer(text))
        
        for match in reversed(matches):  # 反向处理以保持索引正确
            alt = match.group(1)
            url = match.group(2)
            element = ImageElement(alt, url, line_number)
            self.elements.append(element)
        
        # 返回移除图片标记后的文本
        return self.IMAGE_PATTERN.sub('', text).strip()


# ==================== Markdown 转 DOCX 转换器 ====================

class MarkdownToDocxConverter:
    """
    Markdown 到 DOCX 转换器
    
    将解析后的 Markdown 元素转换为 DOCX 文档
    """
    
    def __init__(self, generator: Optional[DocxGenerator] = None):
        """
        初始化转换器
        
        Args:
            generator: 可选的 DocxGenerator 实例
        """
        self.generator = generator or DocxGenerator()
    
    def convert(
        self,
        elements: List[Dict[str, Any]],
        output_path: str,
        title: Optional[str] = None,
        footer_text: str = "AI生成，仅供参考",
        header_text: Optional[str] = None
    ) -> str:
        """
        将 Markdown 元素转换为 DOCX 文档
        
        Args:
            elements: Markdown 元素列表
            output_path: 输出文件路径
            title: 文档标题（可选）
            footer_text: 页脚文本
            header_text: 页眉文本
            
        Returns:
            保存的文件路径
        """
        # 验证输出路径
        safe_output_path = validate_output_path(output_path)
        
        # 设置页眉页脚
        if header_text:
            self.generator.set_header_text(header_text)
        self.generator.set_footer_text(footer_text)
        
        # 添加标题
        if title:
            self.generator.add_title(title, level=1)
        
        # 转换元素
        i = 0
        while i < len(elements):
            element = elements[i]
            elem_type = element.get('type', '')
            
            try:
                if elem_type == 'header':
                    self._convert_header(element)
                elif elem_type == 'paragraph':
                    self._convert_paragraph(element)
                elif elem_type == 'list':
                    self._convert_list(element)
                elif elem_type == 'code_block':
                    self._convert_code_block(element)
                elif elem_type == 'table':
                    self._convert_table(element)
                elif elem_type == 'quote':
                    self._convert_quote(element)
                elif elem_type == 'image':
                    self._convert_image(element)
                elif elem_type == 'horizontal_rule':
                    self._convert_horizontal_rule(element)
                elif elem_type == 'list_item':
                    # 列表项应该被包含在列表中，单独出现时作为段落处理
                    content = element.get('content', '')
                    if content:
                        self.generator.add_paragraph(content)
            except Exception as e:
                line_num = element.get('line_number', '未知')
                raise MarkdownParserError(
                    f"转换元素失败 ({elem_type}): {str(e)}",
                    line_num
                )
            
            i += 1
        
        # 保存文档
        return self.generator.save(safe_output_path)
    
    def _convert_header(self, element: Dict[str, Any]):
        """转换标题"""
        level = element.get('level', 1)
        content = element.get('content', '')
        
        # 调整级别以适应 DocxGenerator（1-9）
        # Markdown H1-H6 映射到 Word 标题 1-6
        docx_level = min(max(level, 1), 6)
        
        self.generator.add_title(content, level=docx_level)
    
    def _convert_paragraph(self, element: Dict[str, Any]):
        """转换段落"""
        content = element.get('content', '')
        if content.strip():
            self.generator.add_paragraph(content)
    
    def _convert_list(self, element: Dict[str, Any]):
        """转换列表"""
        items = element.get('content', [])
        ordered = element.get('ordered', False)
        
        if items:
            self.generator.add_list(items, ordered=ordered)
    
    def _convert_code_block(self, element: Dict[str, Any]):
        """转换代码块"""
        code = element.get('content', '')
        language = element.get('language', '')
        
        # 添加语言标签（如果有）
        if language:
            self.generator.add_paragraph(f"代码 ({language}):", italic=True, color='666666')
        
        if code:
            self.generator.add_code_block(code, language=language or 'text')
    
    def _convert_table(self, element: Dict[str, Any]):
        """转换表格"""
        content = element.get('content', {})
        headers = content.get('headers', [])
        rows = content.get('rows', [])
        
        if headers:
            table_data = [headers] + rows
            self.generator.add_table(table_data, header_row=True)
    
    def _convert_quote(self, element: Dict[str, Any]):
        """转换引用"""
        content = element.get('content', '')
        if content:
            self.generator.add_quote(content)
    
    def _convert_image(self, element: Dict[str, Any]):
        """转换图片"""
        content = element.get('content', {})
        alt = content.get('alt', '')
        url = content.get('url', '')
        
        # 检查是否是本地文件
        if os.path.isfile(url):
            try:
                self.generator.add_image(url, width=5.0, align='center')
            except Exception as e:
                # 图片加载失败，添加占位文本
                self.generator.add_paragraph(f"[图片: {alt}] (加载失败: {str(e)})", italic=True, color='999999')
        else:
            # 远程图片或无效路径，添加链接文本
            self.generator.add_paragraph(f"[图片: {alt}] ({url})", italic=True, color='666666')
    
    def _convert_horizontal_rule(self, element: Dict[str, Any]):
        """转换水平线"""
        self.generator.add_horizontal_rule()


# ==================== 便捷函数 ====================

def parse_markdown_file(filepath: str) -> List[Dict[str, Any]]:
    """
    解析 Markdown 文件
    
    Args:
        filepath: Markdown 文件路径
        
    Returns:
        解析后的元素列表
    """
    parser = MarkdownParser()
    return parser.parse_file(filepath)


def parse_markdown_text(text: str) -> List[Dict[str, Any]]:
    """
    解析 Markdown 文本
    
    Args:
        text: Markdown 文本内容
        
    Returns:
        解析后的元素列表
    """
    parser = MarkdownParser()
    return parser.parse_text(text)


def convert_markdown_to_docx(
    input_path: str,
    output_path: str,
    title: Optional[str] = None,
    footer_text: str = "AI生成，仅供参考",
    header_text: Optional[str] = None
) -> str:
    """
    将 Markdown 文件转换为 DOCX 文档
    
    Args:
        input_path: Markdown 文件路径
        output_path: 输出 DOCX 文件路径
        title: 文档标题（可选，默认使用文件名）
        footer_text: 页脚文本
        header_text: 页眉文本
        
    Returns:
        保存的文件路径
    """
    # 解析 Markdown
    parser = MarkdownParser()
    elements = parser.parse_file(input_path)
    
    # 如果没有指定标题，使用文件名
    if title is None:
        title = os.path.splitext(os.path.basename(input_path))[0]
    
    # 转换为 DOCX
    converter = MarkdownToDocxConverter()
    return converter.convert(
        elements,
        output_path,
        title=title,
        footer_text=footer_text,
        header_text=header_text
    )


def convert_markdown_text_to_docx(
    markdown_text: str,
    output_path: str,
    title: Optional[str] = None,
    footer_text: str = "AI生成，仅供参考",
    header_text: Optional[str] = None
) -> str:
    """
    将 Markdown 文本转换为 DOCX 文档
    
    Args:
        markdown_text: Markdown 文本内容
        output_path: 输出 DOCX 文件路径
        title: 文档标题（可选）
        footer_text: 页脚文本
        header_text: 页眉文本
        
    Returns:
        保存的文件路径
    """
    # 解析 Markdown
    parser = MarkdownParser()
    elements = parser.parse_text(markdown_text)
    
    # 转换为 DOCX
    converter = MarkdownToDocxConverter()
    return converter.convert(
        elements,
        output_path,
        title=title,
        footer_text=footer_text,
        header_text=header_text
    )


# ==================== 示例代码 ====================

def main():
    """示例：解析 Markdown 并生成 DOCX"""
    
    # 示例 Markdown 文本
    sample_markdown = """
# 示例文档

这是一个段落，包含一些**粗体**和*斜体*文本。

## 列表示例

### 无序列表
- 第一项
- 第二项
- 第三项

### 有序列表
1. 第一步
2. 第二步
3. 第三步

## 代码示例

```python
def hello_world():
    print("Hello, World!")
    return True
```

## 表格示例

| 姓名 | 年龄 | 城市 |
|------|------|------|
| 张三 | 25   | 北京 |
| 李四 | 30   | 上海 |
| 王五 | 28   | 广州 |

## 引用示例

> 这是一段引用文本。
> 可以包含多行。

## 分隔线

---

## 结束

这是文档的结尾。
"""
    
    print("=" * 50)
    print("Markdown 解析器示例")
    print("=" * 50)
    
    try:
        # 解析 Markdown
        print("\n1. 解析 Markdown 文本...")
        parser = MarkdownParser()
        elements = parser.parse_text(sample_markdown)
        
        print(f"   解析完成，共 {len(elements)} 个元素")
        
        # 显示解析结果
        print("\n2. 解析结果预览:")
        for i, elem in enumerate(elements[:10], 1):  # 只显示前10个
            elem_type = elem.get('type', 'unknown')
            content = elem.get('content', '')
            if isinstance(content, str) and len(content) > 50:
                content = content[:50] + '...'
            print(f"   [{i}] {elem_type}: {content}")
        
        if len(elements) > 10:
            print(f"   ... 还有 {len(elements) - 10} 个元素")
        
        # 转换为 DOCX
        print("\n3. 转换为 DOCX 文档...")
        output_path = "./output/markdown_sample.docx"
        
        converter = MarkdownToDocxConverter()
        result_path = converter.convert(
            elements,
            output_path,
            title="Markdown 示例文档",
            footer_text="由 Markdown 解析器生成"
        )
        
        print(f"   ✓ 文档已保存: {result_path}")
        
        # 测试文件解析
        print("\n4. 测试文件解析...")
        
        # 创建临时 Markdown 文件
        temp_md_path = "./output/temp_sample.md"
        os.makedirs(os.path.dirname(temp_md_path), exist_ok=True)
        
        with open(temp_md_path, 'w', encoding='utf-8') as f:
            f.write(sample_markdown)
        
        # 从文件转换
        result_path2 = convert_markdown_to_docx(
            temp_md_path,
            "./output/markdown_from_file.docx",
            title="从文件解析的文档"
        )
        
        print(f"   ✓ 文件解析完成: {result_path2}")
        
        # 清理临时文件
        os.remove(temp_md_path)
        
        print("\n" + "=" * 50)
        print("所有测试通过！")
        print("=" * 50)
        
    except MarkdownParserError as e:
        print(f"\n✗ 解析错误: {e}")
    except SecurityError as e:
        print(f"\n✗ 安全错误: {e}")
    except Exception as e:
        print(f"\n✗ 错误: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()

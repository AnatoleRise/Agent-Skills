#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX 生成器命令行工具 v1.0

用于将 Markdown 文件转换为 DOCX 文档的命令行工具。

功能：
1. 支持命令行参数解析
2. 输入验证和安全检查
3. 完善的错误处理和退出码机制
4. 详细的帮助信息和版本信息
5. 日志输出支持
6. 安全特性（路径遍历防护、命令注入防护等）

用法：
    python docx_cli.py -i input.md -o output.docx [选项]

退出码：
    0: 成功
    1: 一般错误
    2: 输入验证错误
    3: 文件不存在
    4: 权限错误
    5: 解析错误
    6: 安全错误
    7: 输出错误
"""

import sys
import os
import argparse
import logging
from typing import Optional, List, Tuple
from pathlib import Path

# 导入 markdown_parser 中的函数和异常
from markdown_parser import (
    validate_input_path,
    validate_output_path,
    convert_markdown_to_docx,
    MarkdownParserError,
    SecurityError,
    MarkdownSyntaxError,
)

# ==================== 常量定义 ====================

VERSION = "1.0.0"
APP_NAME = "DOCX Generator CLI"
DEFAULT_FOOTER = "AI生成，仅供参考"

# 退出码定义
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_VALIDATION_ERROR = 2
EXIT_FILE_NOT_FOUND = 3
EXIT_PERMISSION_ERROR = 4
EXIT_PARSE_ERROR = 5
EXIT_SECURITY_ERROR = 6
EXIT_OUTPUT_ERROR = 7

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = ['.md', '.markdown', '.txt']


# ==================== 自定义异常 ====================

class CLIError(Exception):
    """CLI 异常基类"""
    
    def __init__(self, message: str, exit_code: int = EXIT_GENERAL_ERROR):
        self.exit_code = exit_code
        super().__init__(message)


class ValidationCLIError(CLIError):
    """输入验证错误"""
    
    def __init__(self, message: str):
        super().__init__(message, EXIT_VALIDATION_ERROR)


class FileNotFoundCLIError(CLIError):
    """文件不存在错误"""
    
    def __init__(self, message: str):
        super().__init__(message, EXIT_FILE_NOT_FOUND)


class PermissionCLIError(CLIError):
    """权限错误"""
    
    def __init__(self, message: str):
        super().__init__(message, EXIT_PERMISSION_ERROR)


class ParseCLIError(CLIError):
    """解析错误"""
    
    def __init__(self, message: str):
        super().__init__(message, EXIT_PARSE_ERROR)


class SecurityCLIError(CLIError):
    """安全错误"""
    
    def __init__(self, message: str):
        super().__init__(message, EXIT_SECURITY_ERROR)


class OutputCLIError(CLIError):
    """输出错误"""
    
    def __init__(self, message: str):
        super().__init__(message, EXIT_OUTPUT_ERROR)


# ==================== 日志配置 ====================

def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    配置日志记录器
    
    Args:
        verbose: 是否启用详细日志
        
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger('docx_cli')
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # 清除现有处理器
    logger.handlers.clear()
    
    # 创建标准错误流处理器（用于错误信息）
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(message)s'
    ))
    
    # 创建标准输出流处理器（用于普通信息）
    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # 添加过滤器，确保 INFO 级别的日志只输出到 stdout
    class InfoFilter(logging.Filter):
        def filter(self, record):
            return record.levelno < logging.WARNING
    
    info_handler.addFilter(InfoFilter())
    
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)
    
    return logger


# ==================== 安全验证函数 ====================

def sanitize_text_input(text: Optional[str]) -> Optional[str]:
    """
    清理文本输入，防止命令注入和其他攻击
    
    Args:
        text: 输入文本
        
    Returns:
        清理后的文本，如果输入为 None 则返回 None
    """
    if text is None:
        return None
    
    if not isinstance(text, str):
        text = str(text)
    
    # 移除空字节
    text = text.replace('\x00', '')
    
    # 移除控制字符（保留换行、制表符等常用字符）
    allowed_controls = {9, 10, 13}  # \t, \n, \r
    text = ''.join(
        char if ord(char) >= 32 or ord(char) in allowed_controls else ''
        for char in text
    )
    
    # 限制文本长度
    max_length = 10000
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()


def validate_cli_input(args: argparse.Namespace) -> Tuple[str, str, Optional[str], str, Optional[str]]:
    """
    验证命令行输入参数
    
    Args:
        args: 解析后的命令行参数
        
    Returns:
        验证后的 (input_path, output_path, header_text, footer_text, title)
        
    Raises:
        ValidationCLIError: 输入验证错误
        FileNotFoundCLIError: 文件不存在
        PermissionCLIError: 权限错误
        SecurityCLIError: 安全错误
    """
    # 验证输入路径
    if not args.input:
        raise ValidationCLIError("输入文件路径不能为空，请使用 -i 或 --input 指定")
    
    # 清理输入路径
    input_path = sanitize_text_input(args.input)
    if not input_path:
        raise ValidationCLIError("输入文件路径无效")
    
    # 使用 markdown_parser 的验证函数验证输入
    try:
        validated_input_path = validate_input_path(input_path)
    except SecurityError as e:
        raise SecurityCLIError(f"输入路径安全检查失败: {e}")
    except MarkdownParserError as e:
        error_msg = str(e).lower()
        if "不存在" in error_msg:
            raise FileNotFoundCLIError(f"输入文件不存在: {input_path}")
        elif "不可读" in error_msg or "权限" in error_msg:
            raise PermissionCLIError(f"无法读取输入文件: {e}")
        elif "不支持" in error_msg or "文件类型" in error_msg:
            raise ValidationCLIError(f"不支持的文件类型: {e}")
        elif "过大" in error_msg:
            raise ValidationCLIError(f"文件过大: {e}")
        else:
            raise ValidationCLIError(f"输入验证失败: {e}")
    
    # 验证输出路径
    if not args.output:
        raise ValidationCLIError("输出文件路径不能为空，请使用 -o 或 --output 指定")
    
    # 清理输出路径
    output_path = sanitize_text_input(args.output)
    if not output_path:
        raise ValidationCLIError("输出文件路径无效")
    
    # 使用 markdown_parser 的验证函数验证输出
    try:
        validated_output_path = validate_output_path(output_path)
    except SecurityError as e:
        raise SecurityCLIError(f"输出路径安全检查失败: {e}")
    except MarkdownParserError as e:
        error_msg = str(e).lower()
        if "不可写" in error_msg or "权限" in error_msg:
            raise PermissionCLIError(f"无法写入输出路径: {e}")
        elif "创建" in error_msg:
            raise OutputCLIError(f"无法创建输出目录: {e}")
        else:
            raise ValidationCLIError(f"输出验证失败: {e}")
    
    # 清理可选参数
    header_text = sanitize_text_input(args.header)
    footer_text = sanitize_text_input(args.footer) or DEFAULT_FOOTER
    title = sanitize_text_input(args.title)
    
    return validated_input_path, validated_output_path, header_text, footer_text, title


# ==================== 命令行参数解析 ====================

def create_parser() -> argparse.ArgumentParser:
    """
    创建命令行参数解析器
    
    Returns:
        配置好的 ArgumentParser 实例
    """
    parser = argparse.ArgumentParser(
        prog='docx_cli.py',
        description=f"""
{APP_NAME} v{VERSION}

将 Markdown 文件转换为 DOCX 文档的命令行工具。

支持功能：
  - Headers (H1-H6)
  - Paragraphs
  - Ordered/Unordered lists
  - Code blocks
  - Tables
  - Quotes
  - Images
  - Horizontal rules

示例：
  python docx_cli.py -i input.md -o output.docx
  python docx_cli.py -i doc.md -o out.docx -t "我的文档" -H "页眉文本"
  python docx_cli.py -i doc.md -o out.docx -f "自定义页脚" -V
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False  # 我们自定义帮助信息
    )
    
    # 必需参数（在代码中手动检查，以便 --help 和 --version 能正常工作）
    parser.add_argument(
        '--input', '-i',
        type=str,
        default=None,
        help='输入 Markdown 文件路径（必需）'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='输出 DOCX 文件路径（必需）'
    )
    
    # 可选参数
    parser.add_argument(
        '--header', '-H',
        type=str,
        default=None,
        help='页眉文本（可选）'
    )
    
    parser.add_argument(
        '--footer', '-f',
        type=str,
        default=DEFAULT_FOOTER,
        help=f'页脚文本（可选，默认: "{DEFAULT_FOOTER}"）'
    )
    
    parser.add_argument(
        '--title', '-t',
        type=str,
        default=None,
        help='文档标题（可选，覆盖 Markdown 中的 H1）'
    )
    
    parser.add_argument(
        '--verbose', '-V',
        action='store_true',
        help='显示详细日志信息'
    )
    
    parser.add_argument(
        '--help', '-h',
        action='store_true',
        help='显示帮助信息并退出'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='显示版本信息并退出'
    )
    
    return parser


def print_help():
    """打印帮助信息"""
    help_text = f"""
{APP_NAME} v{VERSION}

用法: python docx_cli.py -i <输入文件> -o <输出文件> [选项]

必需参数:
  -i, --input <路径>     输入 Markdown 文件路径
  -o, --output <路径>    输出 DOCX 文件路径

可选参数:
  -H, --header <文本>    页眉文本
  -f, --footer <文本>    页脚文本（默认: "{DEFAULT_FOOTER}"）
  -t, --title <文本>     文档标题（覆盖 Markdown 中的 H1）
  -V, --verbose          显示详细日志信息
  -h, --help             显示此帮助信息并退出
  -v, --version          显示版本信息并退出

支持的输入格式:
  .md, .markdown, .txt

示例:
  1. 基本用法:
     python docx_cli.py -i input.md -o output.docx

  2. 指定标题和页眉:
     python docx_cli.py -i doc.md -o out.docx -t "我的文档" -H "公司机密"

  3. 自定义页脚:
     python docx_cli.py -i doc.md -o out.docx -f "内部资料，请勿外传"

  4. 显示详细日志:
     python docx_cli.py -i doc.md -o out.docx -V

退出码:
  0  成功
  1  一般错误
  2  输入验证错误
  3  文件不存在
  4  权限错误
  5  解析错误
  6  安全错误
  7  输出错误
"""
    print(help_text)


def print_version():
    """打印版本信息"""
    print(f"{APP_NAME} v{VERSION}")
    print("用于将 Markdown 文件转换为 DOCX 文档")
    print("Copyright (c) 2024")


# ==================== 核心功能 ====================

def convert_file(
    input_path: str,
    output_path: str,
    header_text: Optional[str],
    footer_text: str,
    title: Optional[str],
    logger: logging.Logger
) -> str:
    """
    转换 Markdown 文件为 DOCX 文档
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        header_text: 页眉文本
        footer_text: 页脚文本
        title: 文档标题
        logger: 日志记录器
        
    Returns:
        输出文件路径
        
    Raises:
        ParseCLIError: 解析错误
        OutputCLIError: 输出错误
        CLIError: 其他错误
    """
    logger.info(f"开始转换: {input_path}")
    logger.debug(f"输出路径: {output_path}")
    logger.debug(f"页眉: {header_text or '(无)'}")
    logger.debug(f"页脚: {footer_text}")
    logger.debug(f"标题: {title or '(自动检测)'}")
    
    try:
        # 执行转换
        result_path = convert_markdown_to_docx(
            input_path=input_path,
            output_path=output_path,
            title=title,
            footer_text=footer_text,
            header_text=header_text
        )
        
        logger.info(f"✓ 转换成功: {result_path}")
        return result_path
        
    except MarkdownSyntaxError as e:
        raise ParseCLIError(f"Markdown 语法错误: {e}")
    except MarkdownParserError as e:
        error_msg = str(e).lower()
        if "语法" in error_msg or "解析" in error_msg:
            raise ParseCLIError(f"解析失败: {e}")
        elif "输出" in error_msg or "保存" in error_msg:
            raise OutputCLIError(f"保存文档失败: {e}")
        else:
            raise CLIError(f"转换失败: {e}", EXIT_GENERAL_ERROR)
    except Exception as e:
        raise CLIError(f"转换过程中发生错误: {type(e).__name__}: {e}", EXIT_GENERAL_ERROR)


# ==================== 主函数 ====================

def main(argv: Optional[List[str]] = None) -> int:
    """
    主入口函数
    
    Args:
        argv: 命令行参数列表，默认为 sys.argv[1:]
        
    Returns:
        退出码
    """
    # 创建解析器
    parser = create_parser()
    
    # 解析参数
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        # argparse 会在遇到错误时调用 sys.exit()
        return e.code if isinstance(e.code, int) else EXIT_GENERAL_ERROR
    
    # 处理帮助和版本请求
    if args.help:
        print_help()
        return EXIT_SUCCESS
    
    if args.version:
        print_version()
        return EXIT_SUCCESS
    
    # 设置日志
    logger = setup_logging(verbose=args.verbose)
    
    try:
        # 验证输入
        logger.debug("验证输入参数...")
        input_path, output_path, header_text, footer_text, title = validate_cli_input(args)
        logger.debug("输入验证通过")
        
        # 执行转换
        result_path = convert_file(
            input_path=input_path,
            output_path=output_path,
            header_text=header_text,
            footer_text=footer_text,
            title=title,
            logger=logger
        )
        
        # 输出成功信息
        print(f"\n文档已成功生成: {result_path}")
        return EXIT_SUCCESS
        
    except CLIError as e:
        logger.error(f"✗ {e}")
        if args.verbose:
            import traceback
            logger.debug(traceback.format_exc())
        return e.exit_code
    except KeyboardInterrupt:
        logger.error("\n✗ 操作被用户中断")
        return EXIT_GENERAL_ERROR
    except Exception as e:
        logger.error(f"✗ 未预期的错误: {type(e).__name__}: {e}")
        if args.verbose:
            import traceback
            logger.debug(traceback.format_exc())
        return EXIT_GENERAL_ERROR


if __name__ == "__main__":
    sys.exit(main())

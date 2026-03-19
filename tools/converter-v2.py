#!/usr/bin/env python3
"""
道藏文本智能转换器 v2
将原始txt文件转换为排版良好的Markdown文档

改进：
1. 智能识别章节标题
2. 正确分段（按句读+空行）
3. 处理注释标记（#1, #2等）
4. 处理古文特殊格式（双行夹注、小字注疏）
5. 生成目录
6. 添加适当的空行和缩进

Author: DaimaRuge + Claude
Date: 2026-03-20
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Scripture:
    """经文数据结构"""
    category: str
    dynasty: str = ""
    author: str = ""
    title: str = ""
    content: str = ""
    source_file: str = ""
    size: int = 0
    sections: List[Dict] = field(default_factory=list)  # 章节列表


class DaozangConverterV2:
    """道藏智能转换器"""
    
    # 分类映射
    CATEGORY_MAP = {
        '洞真部': 'dongzhen',
        '洞玄部': 'dongxuan',
        '洞神部': 'dongshen',
        '太平部': 'taiping',
        '太玄部': 'taixuan',
        '太清部': 'taiqing',
        '正一部': 'zhengyi',
        '續道藏': 'xudaozang',
        '续道藏': 'xudaozang'
    }
    
    # 子分类映射
    SUBCATEGORY_MAP = {
        '本文類': 'benwen',
        '神符類': 'shenfu',
        '玉訣類': 'yujue',
        '靈圖類': 'lingtu',
        '譜錄類': 'pulu',
        '戒律類': 'jielu',
        '威儀類': 'weiyi',
        '方法類': 'fangfa',
        '記傳類': 'jizhuan',
        '讚頌類': 'zansong',
        '表奏類': 'biaozou',
        '眾術類': 'zhongshu'
    }
    
    # 章节标题模式
    SECTION_PATTERNS = [
        r'^[卷第][一二三四五六七八九十百千]+[篇章节]',  # 卷第一篇、第二章等
        r'^[一二三四五六七八九十]+[、.．][^\n]{1,20}$',  # 一、xxx
        r'^[（(][一二三四五六七八九十]+[)）][^\n]{1,20}$',  # （一）xxx
        r'^[上下][篇卷]',  # 上篇、下卷
        r'^[序跋附錄附录後記后记]',  # 序、跋等
        r'^.{1,8}[圖圖說說法法訣訣經經文文]$'  # xx圖、xx說、xx法等
    ]
    
    def __init__(self, source_dir: str, output_dir: str):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.index_data: Dict[str, List[Dict]] = {}
        
    def read_file(self, filepath: Path) -> str:
        """读取文件内容，尝试多种编码"""
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'big5', 'cp950']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                    # 验证内容是否正常
                    if '道' in content or '經' in content or '经' in content:
                        return content
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        # 最后尝试二进制读取后解码
        try:
            with open(filepath, 'rb') as f:
                raw = f.read()
                # 尝试检测编码
                import chardet
                detected = chardet.detect(raw)
                return raw.decode(detected['encoding'] or 'utf-8', errors='replace')
        except:
            return ""
    
    def is_section_title(self, line: str, next_line: str = "") -> Tuple[bool, int]:
        """
        判断是否为章节标题
        
        Returns:
            (is_title, level) - 是否标题，以及标题级别(2-4)
        """
        line = line.strip()
        if not line:
            return False, 0
        
        # 排除太长的行
        if len(line) > 30:
            return False, 0
        
        # 检查是否包含正文特征（有句号、逗号等连续文本）
        if re.search(r'[，。！？、；：]', line) and len(line) > 10:
            return False, 0
        
        # 一级标题：卷、篇
        if re.match(r'^[卷第][一二三四五六七八九十百千]+[篇卷]', line):
            return True, 2
        
        # 特殊标题模式
        for pattern in self.SECTION_PATTERNS:
            if re.match(pattern, line):
                return True, 3
        
        # 短行 + 后面有空行 = 可能是标题
        if len(line) <= 15 and not next_line.strip():
            # 检查是否有标题特征词
            title_keywords = ['圖', '说', '說', '法', '訣', '诀', '經', '经', '篇', '章', '門', '门', '品', '論', '论']
            if any(kw in line for kw in title_keywords):
                return True, 3
        
        # 带数字编号的短行
        if re.match(r'^[一二三四五六七八九十]+[、.．]?', line) and len(line) <= 20:
            return True, 3
        
        return False, 0
    
    def detect_footnotes(self, content: str) -> Dict[str, str]:
        """检测并提取脚注"""
        footnotes = {}
        
        # 查找脚注定义（通常在文末）
        # 格式：#1 xxx 或 ① xxx
        footnote_pattern = r'[#①②③④⑤⑥⑦⑧⑨⑩](\d+)\s*(.+?)(?=[#①②③④⑤⑥⑦⑧⑨⑩]|$)'
        
        matches = re.findall(footnote_pattern, content)
        for num, text in matches:
            footnotes[num] = text.strip()
        
        return footnotes
    
    def format_paragraph(self, text: str) -> str:
        """格式化段落，添加适当标点处理"""
        text = text.strip()
        if not text:
            return ""
        
        # 移除行内多余空格，但保留句读后的空格
        text = re.sub(r'([^\s，。！？、；：])\s+([^\s，。！？、；：])', r'\1\2', text)
        
        # 处理注释标记，转换为上标
        text = re.sub(r'#(\d+)', r'<sup>[\1]</sup>', text)
        
        return text
    
    def format_content(self, content: str) -> Tuple[str, List[Dict]]:
        """
        智能格式化内容
        
        Returns:
            (formatted_markdown, sections_list)
        """
        lines = content.split('\n')
        formatted = []
        sections = []
        current_section = None
        in_code_block = False
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            
            # 空行
            if not line:
                if formatted and formatted[-1] != '':
                    formatted.append('')
                i += 1
                continue
            
            # 检查是否为章节标题
            is_title, level = self.is_section_title(line, next_line)
            
            if is_title:
                # 添加锚点
                anchor = re.sub(r'[^\w\u4e00-\u9fff-]', '', line)
                heading = '#' * level
                formatted.append(f'\n{heading} {line}')
                formatted.append('')
                
                # 记录章节
                sections.append({
                    'title': line,
                    'level': level,
                    'anchor': anchor
                })
                current_section = line
                i += 1
                continue
            
            # 检测经文开头信息（經名、作者等）
            if re.match(r'^經名[：:]', line) or re.match(r'^經名[：:]', line):
                formatted.append(f'\n### {line}')
                formatted.append('')
                i += 1
                continue
            
            # 普通段落
            para = self.format_paragraph(line)
            
            # 如果段落很长，考虑是否需要分段
            if len(para) > 200:
                # 按句号分段，每段不超过100字
                sentences = re.split(r'([。！？])', para)
                current_para = ""
                for j in range(0, len(sentences) - 1, 2):
                    sentence = sentences[j] + (sentences[j+1] if j+1 < len(sentences) else "")
                    current_para += sentence
                    if len(current_para) > 100:
                        formatted.append(current_para)
                        formatted.append('')
                        current_para = ""
                if current_para:
                    formatted.append(current_para)
            else:
                formatted.append(para)
            
            i += 1
        
        # 清理多余空行
        result = '\n'.join(formatted)
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        return result, sections
    
    def convert_to_markdown(self, scripture: Scripture) -> str:
        """转换为排版良好的Markdown"""
        
        # 格式化内容
        formatted_content, sections = self.format_content(scripture.content)
        scripture.sections = sections
        
        # 构建Markdown
        md_parts = []
        
        # YAML front matter
        md_parts.append(f"""---
title: {scripture.title}
category: {scripture.category}
dynasty: {scripture.dynasty}
author: {scripture.author}
source: {scripture.source_file}
word_count: {scripture.size}
---

""")
        
        # 标题
        md_parts.append(f"# {scripture.title}\n\n")
        
        # 元信息
        if scripture.dynasty or scripture.author:
            md_parts.append('<div class="scripture-meta">\n\n')
            if scripture.dynasty:
                md_parts.append(f"- **朝代**：{scripture.dynasty}\n")
            if scripture.author:
                md_parts.append(f"- **作者**：{scripture.author}\n")
            md_parts.append(f"- **字数**：约 {scripture.size} 字\n")
            md_parts.append('\n</div>\n\n')
        
        # 分隔线
        md_parts.append('---\n\n')
        
        # 目录（如果有多个章节）
        if len(sections) > 3:
            md_parts.append('## 目录\n\n')
            for sec in sections:
                indent = '  ' * (sec['level'] - 2)
                md_parts.append(f"{indent}- [{sec['title']}](#{sec['anchor']})\n")
            md_parts.append('\n---\n\n')
        
        # 正文
        md_parts.append(formatted_content)
        
        # 页脚
        md_parts.append('\n\n---\n\n')
        md_parts.append('<div class="footer-note">\n\n')
        md_parts.append(f'本文出自《正统道藏》{scripture.category}\n\n')
        md_parts.append('仅供学术研究使用\n\n')
        md_parts.append('</div>\n')
        
        return ''.join(md_parts)
    
    def parse_filename(self, filename: str) -> Tuple[str, str, str, str]:
        """解析文件名"""
        name = filename.replace('.txt', '')
        
        # 尝试匹配完整格式：分类-朝代-作者-书名
        match = re.match(r'^(.+?)-([唐宋元明清金漢魏晋南北朝五代]+)-(.+?)-(.+)$', name)
        if match:
            return match.group(1), match.group(2), match.group(3), match.group(4)
        
        # 简单格式：分类-书名
        match = re.match(r'^(.+?)-(.+)$', name)
        if match:
            return match.group(1), "", "", match.group(2)
        
        return name, "", "", name
    
    def get_category_slug(self, category: str) -> str:
        """获取分类slug"""
        for key, slug in self.CATEGORY_MAP.items():
            if key in category:
                # 检查子分类
                for sub_key, sub_slug in self.SUBCATEGORY_MAP.items():
                    if sub_key in category:
                        return f"{slug}/{sub_slug}"
                return slug
        return 'other'
    
    def process_file(self, filepath: Path) -> Scripture:
        """处理单个文件"""
        category, dynasty, author, title = self.parse_filename(filepath.name)
        content = self.read_file(filepath)
        
        return Scripture(
            category=category,
            dynasty=dynasty,
            author=author,
            title=title,
            content=content,
            source_file=filepath.name,
            size=len(content)
        )
    
    def convert_all(self, dry_run: bool = False):
        """转换所有文件"""
        print(f"开始转换: {self.source_dir}")
        print(f"输出目录: {self.output_dir}")
        
        if not self.source_dir.exists():
            print(f"错误: 源目录不存在")
            return
        
        txt_files = list(self.source_dir.glob('*.txt'))
        print(f"找到 {len(txt_files)} 个文件")
        
        stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'by_category': {}
        }
        
        for filepath in txt_files:
            stats['total'] += 1
            
            try:
                scripture = self.process_file(filepath)
                md_content = self.convert_to_markdown(scripture)
                
                # 获取输出路径
                slug = self.get_category_slug(scripture.category)
                output_dir = self.output_dir / 'docs' / 'catalog' / slug
                output_file = output_dir / f"{scripture.title}.md"
                
                if dry_run:
                    print(f"[DRY-RUN] {filepath.name} -> {output_file}")
                else:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(md_content)
                    try:
                        print(f"[OK] {scripture.title}")
                    except:
                        print(f"[OK] {filepath.name}")
                
                stats['success'] += 1
                cat = scripture.category.split('-')[0] if '-' in scripture.category else scripture.category
                stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
                
            except Exception as e:
                try:
                    print(f"[FAIL] {filepath.name}: {e}")
                except:
                    print(f"[FAIL] {filepath.stem}: error")
                stats['failed'] += 1
        
        print(f"\n转换完成:")
        print(f"  成功: {stats['success']}")
        print(f"  失败: {stats['failed']}")
        print(f"\n按分类:")
        for cat, count in sorted(stats['by_category'].items()):
            print(f"  {cat}: {count}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='道藏文本智能转换器 v2')
    parser.add_argument('source', help='源目录（txt文件）')
    parser.add_argument('output', help='输出目录')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不写入文件')
    
    args = parser.parse_args()
    
    converter = DaozangConverterV2(args.source, args.output)
    converter.convert_all(dry_run=args.dry_run)


if __name__ == '__main__':
    main()

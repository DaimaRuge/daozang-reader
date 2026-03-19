#!/usr/bin/env python3
"""
道藏文本转换工具
将原始txt文件转换为结构化的Markdown文档

Author: DaimaRuge
Date: 2026-03-19
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Scripture:
    """经文数据结构"""
    category: str          # 分类（如：正統道藏洞真部本文類）
    dynasty: str = ""      # 朝代
    author: str = ""       # 作者
    title: str = ""        # 书名
    content: str = ""      # 正文内容
    source_file: str = ""  # 源文件名
    size: int = 0          # 文件大小


class DaozangConverter:
    """道藏文本转换器"""
    
    # 分类映射
    CATEGORY_MAP = {
        '正統道藏洞真部': 'dongzhen',
        '正統道藏洞玄部': 'dongxuan', 
        '正統道藏洞神部': 'dongshen',
        '正統道藏太平部': 'taiping',
        '正統道藏太玄部': 'taixuan',
        '正統道藏太清部': 'taiqing',
        '正統道藏正一部': 'zhengyi',
        '續道藏': 'xudaozang'
    }
    
    # 子分类映射
    SUBCATEGORY_MAP = {
        '本文類': 'benwen',
        '神符類': 'shenfu',
        '玉訣類': 'yujue',
        '靈圖類': 'lingtu',
        '譜籙類': 'pulu',
        '戒律類': 'jielu',
        '威儀類': 'weiyi',
        '方法類': 'fangfa',
        '記傳類': 'jizhuan',
        '讚頌類': 'zansong',
        '表奏類': 'biaozou',
        '眾術類': 'zhongshu'
    }
    
    def __init__(self, source_dir: str, output_dir: str):
        """
        初始化转换器
        
        Args:
            source_dir: 源文件目录（道藏_txt）
            output_dir: 输出目录
        """
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.index_data: Dict[str, List[Dict]] = {}
        
    def parse_filename(self, filename: str) -> Tuple[str, str, str, str]:
        """
        解析文件名
        
        格式: 分类-作者-书名.txt
              或 分类-朝代-作者-书名.txt
        
        Returns:
            (category, dynasty, author, title)
        """
        name = filename.replace('.txt', '')
        
        # 尝试匹配带朝代的格式
        # 如：正統道藏洞真部本文類-唐-佚名-書名
        match = re.match(r'^(.+?)-([唐宋元明清周秦漢魏晋南北朝五代金前蜀後蜀南唐西秦梁]+)-(.+?)-(.+)$', name)
        if match:
            return match.group(1), match.group(2), match.group(3), match.group(4)
        
        # 尝试匹配无朝代格式
        # 如：續道藏-書名
        match = re.match(r'^(.+?)-(.+)$', name)
        if match:
            return match.group(1), "", "", match.group(2)
        
        # 无法解析
        return name, "", "", name
    
    def read_file(self, filepath: Path) -> str:
        """读取文件内容，尝试多种编码"""
        encodings = ['utf-8', 'gbk', 'gb2312', 'big5']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        return ""
    
    def format_content(self, content: str) -> str:
        """
        格式化正文内容
        
        - 添加段落标记
        - 处理章节标题
        - 优化排版
        """
        lines = content.split('\n')
        formatted = []
        
        for line in lines:
            line = line.strip()
            
            # 空行
            if not line:
                formatted.append('')
                continue
            
            # 章节标题（如：卷一、第一章等）
            if re.match(r'^[卷第][一二三四五六七八九十百千零]+', line):
                formatted.append(f'\n## {line}\n')
            # 短句作为标题
            elif len(line) < 20 and not re.search(r'[，。、；：]', line):
                formatted.append(f'\n### {line}\n')
            # 普通段落
            else:
                formatted.append(line)
        
        return '\n'.join(formatted)
    
    def convert_to_markdown(self, scripture: Scripture) -> str:
        """
        将经文转换为Markdown格式
        
        Args:
            scripture: 经文数据
        
        Returns:
            Markdown文本
        """
        md = f"""---
title: {scripture.title}
category: {scripture.category}
dynasty: {scripture.dynasty}
author: {scripture.author}
source: {scripture.source_file}
---

# {scripture.title}

"""
        
        # 添加元信息
        if scripture.dynasty or scripture.author:
            md += '<div class="meta-info">\n\n'
            if scripture.dynasty:
                md += f'**朝代**: {scripture.dynasty}  \n'
            if scripture.author:
                md += f'**作者**: {scripture.author}  \n'
            md += f'**字数**: 约 {scripture.size} 字\n'
            md += '\n</div>\n\n'
        
        # 添加分隔线
        md += '---\n\n'
        
        # 添加正文
        md += self.format_content(scripture.content)
        
        # 添加页脚
        md += '\n\n---\n\n'
        md += f'<div class="footer-note">\n'
        md += f'本文出自《正统道藏》{scripture.category}\n'
        md += f'仅供学术研究使用\n'
        md += f'</div>\n'
        
        return md
    
    def get_category_slug(self, category: str) -> str:
        """获取分类slug"""
        for key, slug in self.CATEGORY_MAP.items():
            if key in category:
                # 提取子分类
                for sub_key, sub_slug in self.SUBCATEGORY_MAP.items():
                    if sub_key in category:
                        return f"{slug}/{sub_slug}"
                return slug
        return 'other'
    
    def process_file(self, filepath: Path) -> Scripture:
        """处理单个文件"""
        # 解析文件名
        category, dynasty, author, title = self.parse_filename(filepath.name)
        
        # 读取内容
        content = self.read_file(filepath)
        
        # 创建经文对象
        scripture = Scripture(
            category=category,
            dynasty=dynasty,
            author=author,
            title=title,
            content=content,
            source_file=filepath.name,
            size=len(content)
        )
        
        return scripture
    
    def generate_catalog_page(self, category: str, scriptures: List[Scripture]) -> str:
        """
        生成分类目录页面
        
        Args:
            category: 分类名称
            scriptures: 该分类下的所有经文
        
        Returns:
            Markdown文本
        """
        # 获取分类slug
        slug = self.get_category_slug(category)
        category_name = category
        
        md = f"""---
title: {category_name}
---

# {category_name}

共收录 **{len(scriptures)}** 部经典

<div class="scripture-list">

"""
        
        # 按作者分组
        by_author: Dict[str, List[Scripture]] = {}
        for s in scriptures:
            key = f"{s.dynasty}·{s.author}" if s.dynasty and s.author else (s.author or "佚名")
            if key not in by_author:
                by_author[key] = []
            by_author[key].append(s)
        
        # 输出分组
        for author, works in sorted(by_author.items()):
            md += f'## {author}\n\n'
            for work in works:
                md += f'- [{work.title}](/catalog/{slug}/{work.source_file.replace(".txt", "")})\n'
            md += '\n'
        
        md += '</div>\n'
        
        return md
    
    def convert_all(self):
        """转换所有文件"""
        print(f"开始转换: {self.source_dir}")
        print(f"输出目录: {self.output_dir}")
        
        # 统计
        total = 0
        success = 0
        
        # 遍历所有txt文件
        txt_files = list(self.source_dir.glob('*.txt'))
        
        # 按分类组织
        categories: Dict[str, List[Scripture]] = {}
        
        for filepath in txt_files:
            total += 1
            
            try:
                # 处理文件
                scripture = self.process_file(filepath)
                
                # 获取分类
                category = scripture.category
                
                # 添加到分类
                if category not in categories:
                    categories[category] = []
                categories[category].append(scripture)
                
                success += 1
                
                if total % 100 == 0:
                    print(f"已处理 {total}/{len(txt_files)} 文件...")
                    
            except Exception as e:
                print(f"处理失败: {filepath.name} - {e}")
        
        # 生成输出
        print("\n生成Markdown文件...")
        
        for category, scriptures in categories.items():
            # 获取分类slug
            slug = self.get_category_slug(category)
            
            # 创建输出目录
            out_dir = self.output_dir / 'docs' / 'catalog' / slug.replace('/', os.sep)
            out_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成各经文的Markdown
            for scripture in scriptures:
                md_content = self.convert_to_markdown(scripture)
                out_file = out_dir / f"{scripture.source_file.replace('.txt', '.md')}"
                out_file.write_text(md_content, encoding='utf-8')
            
            # 生成分类索引页
            catalog_md = self.generate_catalog_page(category, scriptures)
            catalog_file = self.output_dir / 'docs' / 'catalog' / f"{slug.split('/')[0]}.md"
            catalog_file.parent.mkdir(parents=True, exist_ok=True)
            catalog_file.write_text(catalog_md, encoding='utf-8')
        
        # 生成总索引
        self.generate_master_index(categories)
        
        print(f"\n转换完成！")
        print(f"总计: {total} 文件")
        print(f"成功: {success} 文件")
        print(f"失败: {total - success} 文件")
    
    def generate_master_index(self, categories: Dict[str, List[Scripture]]):
        """生成主索引JSON"""
        index = {
            'generated_at': datetime.now().isoformat(),
            'total_scriptures': sum(len(s) for s in categories.values()),
            'categories': {}
        }
        
        for category, scriptures in categories.items():
            slug = self.get_category_slug(category)
            index['categories'][category] = {
                'slug': slug,
                'count': len(scriptures),
                'scriptures': [
                    {
                        'title': s.title,
                        'dynasty': s.dynasty,
                        'author': s.author,
                        'path': f'/catalog/{slug}/{s.source_file.replace(".txt", "")}'
                    }
                    for s in scriptures
                ]
            }
        
        # 保存JSON
        api_dir = self.output_dir / 'docs' / 'api'
        api_dir.mkdir(parents=True, exist_ok=True)
        
        index_file = api_dir / 'index.json'
        index_file.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
        
        print(f"索引文件已生成: {index_file}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='道藏文本转换工具')
    parser.add_argument('--source', '-s', 
                        default=r'D:\道藏\道藏_txt',
                        help='源文件目录')
    parser.add_argument('--output', '-o',
                        default='.',
                        help='输出目录')
    
    args = parser.parse_args()
    
    converter = DaozangConverter(args.source, args.output)
    converter.convert_all()


if __name__ == '__main__':
    main()

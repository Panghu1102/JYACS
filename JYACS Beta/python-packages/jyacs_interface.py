# -*- coding: utf-8 -*-
# jyacs_interface.py - JYACS 文本处理接口模块
# 版本: 1.0.1 (已修复)
# 作者: Panghu1102

import re
import time

class JyacsTalkSplitV2:
    """JYACS 文本分句器 V2
    
    一个简单的基于标点符号的文本分句器。
    它将文本添加到内部缓冲区，并逐句分割。
    """
    
    def __init__(self):
        self.buffer = ""
        # 中英文句末标点
        self.sentence_endings = re.compile(r'([。！？.!?\n])')
        
    def add_part(self, text):
        """添加文本块到内部缓冲区。"""
        if isinstance(text, str):
            self.buffer += text
        
    def split_present_sentence(self):
        """尝试从缓冲区中分割出一个完整的句子。
        
        如果找到一个句子，则返回该句子并从缓冲区中移除。
        否则返回 None。
        """
        if not self.buffer:
            return None
        
        # 使用正则表达式查找第一个句子结束符
        match = self.sentence_endings.search(self.buffer)
        
        if not match:
            return None
            
        end_pos = match.end()
        sentence = self.buffer[:end_pos].strip()
        self.buffer = self.buffer[end_pos:]
        
        return sentence if sentence else None
        
    def announce_stop(self):
        """处理完成，返回缓冲区中所有剩余的文本。"""
        remaining_text = self.buffer.strip()
        self.buffer = ""
        return [remaining_text] if remaining_text else []

def key_replace(text, replace_dict=None):
    """关键词替换函数。
    
    将文本中所有 `replace_dict` 的键替换为对应的值。
    """
    if not isinstance(text, str):
        return ""
    if not replace_dict:
        return text
        
    for key, value in replace_dict.items():
        text = text.replace(str(key), str(value))
    return text

def add_pauses(text):
    """为文本中的标点符号添加 Ren'Py 暂停标记 {w} 或 {p}。"""
    if not isinstance(text, str):
        return ""
        
    # 在主要断句符号后添加长暂停 {p}
    text = re.sub(r'([。！？.!?])\s*', r'\1{p}', text)
    # 在次要断句符号后添加短暂停 {w}
    text = re.sub(r'([，、,;；])\s*', r'\1{w}', text)
    # 在换行符后添加暂停
    text = re.sub(r'(\n+)\s*', r'\1{p}', text)
        
    return text

class JyacsTextProcessor:
    """JYACS 文本处理器
    
    封装了分句、清理和格式化文本的常用操作。
    """
    
    def __init__(self):
        self.splitter = JyacsTalkSplitV2()
        
    def process_text(self, text):
        """将长文本分割成句子列表。"""
        if not isinstance(text, str):
            return []
            
        sentences = []
        self.splitter.add_part(text)
        
        while True:
            sentence = self.splitter.split_present_sentence()
            if not sentence:
                break
            sentences.append(sentence)
            
        # 获取并添加缓冲区中剩余的文本
        remaining = self.splitter.announce_stop()
        sentences.extend(remaining)
        
        return sentences
        
    def clean_text(self, text):
        """清理文本，移除多余的空白字符。"""
        if not isinstance(text, str):
            return ""
            
        # 将一个或多个空白字符（包括空格、制表符、换行符）替换为单个空格
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    def format_for_display(self, text):
        """格式化文本以在 Ren'Py 中显示，包括添加暂停和清理。"""
        if not isinstance(text, str):
            return ""
            
        # 1. 添加暂停标记
        text = add_pauses(text)
        
        # 2. 清理文本 (注意：add_pauses后可能会引入额外的空格，这里再次清理)
        text = self.clean_text(text)
        
        return text 
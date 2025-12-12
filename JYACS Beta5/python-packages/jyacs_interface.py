# -*- coding: utf-8 -*-
# jyacs_interface.py - JYACS 文本处理接口模块
# 版本: 1.0.0
# 作者: Panghu1102

import re
import time

class JyacsTalkSplitV2:
    """JYACS 文本分句器 V2
    
    基于标点符号的文本分句器。
    支持中英文标点，可以处理多种句子结构。
    """
    
    def __init__(self):
        """初始化分句器"""
        self.buffer = ""
        # 中英文句末标点
        self.sentence_endings = re.compile(r'([。！？.!?\n])')
        
    def add_part(self, text):
        """添加文本块到内部缓冲区。
        
        Args:
            text (str): 要添加的文本
        """
        if isinstance(text, str):
            self.buffer += text
        elif text is not None:
            try:
                self.buffer += str(text)
            except Exception as e:
                print(u"文本转换失败: {}".format(e))
        
    def split_present_sentence(self):
        """尝试从缓冲区中分割出一个完整的句子。
        
        Returns:
            str: 完整的句子，如果没有找到则返回None
        """
        if not self.buffer:
            return None
        
        try:
            # 使用正则表达式查找第一个句子结束符
            match = self.sentence_endings.search(self.buffer)
            
            if not match:
                return None
                
            end_pos = match.end()
            sentence = self.buffer[:end_pos].strip()
            self.buffer = self.buffer[end_pos:]
            
            return sentence if sentence else None
        except Exception as e:
            print(u"分句失败: {}".format(e))
            return None
        
    def announce_stop(self):
        """处理完成，返回缓冲区中所有剩余的文本。
        
        Returns:
            list: 包含剩余文本的列表
        """
        try:
            remaining_text = self.buffer.strip()
            self.buffer = ""
            return [remaining_text] if remaining_text else []
        except Exception as e:
            print(u"处理剩余文本失败: {}".format(e))
            return []

def key_replace(text, replace_dict=None):
    """关键词替换函数。
    
    Args:
        text (str): 要处理的文本
        replace_dict (dict): 替换规则字典
        
    Returns:
        str: 替换后的文本
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception as e:
            print(u"文本转换失败: {}".format(e))
            return ""
            
    if not replace_dict:
        return text
        
    try:
        for key, value in replace_dict.items():
            text = text.replace(str(key), str(value))
        return text
    except Exception as e:
        print(u"关键词替换失败: {}".format(e))
        return text

def add_pauses(text):
    """为文本中的标点符号添加 Ren'Py 暂停标记。
    
    Args:
        text (str): 要处理的文本
        
    Returns:
        str: 添加暂停标记后的文本
    """
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception as e:
            print(u"文本转换失败: {}".format(e))
            return ""
            
    try:
        # 在主要断句符号后添加长暂停 {p}
        text = re.sub(r'([。！？.!?])\s*', r'\1{p}', text)
        # 在次要断句符号后添加短暂停 {w}
        text = re.sub(r'([，、,;；])\s*', r'\1{w}', text)
        # 在换行符后添加暂停
        text = re.sub(r'(\n+)\s*', r'\1{p}', text)
        return text
    except Exception as e:
        print(u"添加暂停标记失败: {}".format(e))
        return text

class JyacsTextProcessor:
    """JYACS 文本处理器
    
    封装了分句、清理和格式化文本的常用操作。
    提供统一的文本处理接口。
    """
    
    def __init__(self):
        """初始化文本处理器"""
        self.splitter = JyacsTalkSplitV2()
        
    def process_text(self, text):
        """将长文本分割成句子列表。
        
        Args:
            text (str): 要处理的文本
            
        Returns:
            list: 句子列表
        """
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception as e:
                print(u"文本转换失败: {}".format(e))
                return []
                
        try:
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
        except Exception as e:
            print(u"文本处理失败: {}".format(e))
            return [text] if text else []
        
    def clean_text(self, text):
        """清理文本，移除多余的空白字符。
        
        Args:
            text (str): 要清理的文本
            
        Returns:
            str: 清理后的文本
        """
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception as e:
                print(u"文本转换失败: {}".format(e))
                return ""
                
        try:
            # 将多个空白字符替换为单个空格
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        except Exception as e:
            print(u"清理文本失败: {}".format(e))
            return text
        
    def format_for_display(self, text):
        """格式化文本以在 Ren'Py 中显示。
        
        Args:
            text (str): 要格式化的文本
            
        Returns:
            str: 格式化后的文本
        """
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception as e:
                print(u"文本转换失败: {}".format(e))
                return ""
                
        try:
            # 1. 添加暂停标记
            text = add_pauses(text)
            
            # 2. 清理文本
            text = self.clean_text(text)
            
            return text
        except Exception as e:
            print(u"格式化文本失败: {}".format(e))
            return text 
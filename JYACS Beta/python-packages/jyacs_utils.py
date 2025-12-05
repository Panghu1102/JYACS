# -*- coding: utf-8 -*-
# jyacs_utils.py - JYACS 工具模块
# 版本: 1.0.1 (已修复)
# 作者: Panghu1102

import os
import time
import logging
import json
import re
from datetime import datetime

class JyacsLogger:
    """JYACS 日志记录器"""
    
    def __init__(self, log_file="jyacs.log", level=logging.INFO):
        self.logger = logging.getLogger("JYACS")
        self.logger.setLevel(level)
        
        # 避免重复添加handler
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 创建日志目录
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # 文件处理器
        log_path = os.path.join(log_dir, log_file)
        self.file_handler = logging.FileHandler(log_path, encoding='utf-8')
        self.file_handler.setLevel(level)
        
        # 控制台处理器
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(level)
        
        # 格式化器
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.file_handler.setFormatter(formatter)
        self.console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
    
    def __del__(self):
        """析构函数，确保关闭文件处理器"""
        self.close()
            
    def close(self):
        """关闭日志处理器"""
        try:
            if self.file_handler:
                self.file_handler.close()
                self.logger.removeHandler(self.file_handler)
                self.file_handler = None
            
            if self.console_handler:
                self.logger.removeHandler(self.console_handler)
                self.console_handler = None
        except Exception as e:
            # 在关闭失败时，我们只能打印到控制台
            print("关闭日志处理器失败: {}".format(e))
            
    def log(self, level, message):
        """通用日志记录方法"""
        self.logger.log(level, message)
        
    def log_info(self, message):
        """记录信息日志"""
        self.logger.info(message)
        
    def log_warning(self, message):
        """记录警告日志"""
        self.logger.warning(message)
        
    def log_error(self, message):
        """记录错误日志"""
        self.logger.error(message)
        
    def log_debug(self, message):
        """记录调试日志"""
        self.logger.debug(message)
        
    def log_critical(self, message):
        """记录严重错误日志"""
        self.logger.critical(message)

class JyacsConfig:
    """JYACS 配置管理器"""
    
    def __init__(self, config_file="jyacs_config.json"):
        self.config_file = config_file
        self.config = {}
        self.load_config()
        
    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                # 使用utf-8-sig编码处理可能存在的BOM
                with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                    self.config = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print("加载配置失败: {}。将使用空配置。".format(e))
            self.config = {}
            
    def save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print("保存配置失败: {}".format(e))
            
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
        
    def set(self, key, value):
        """设置配置值并保存"""
        self.config[key] = value
        self.save_config()
        
    def has(self, key):
        """检查配置是否存在"""
        return key in self.config

class JyacsFileUtils:
    """JYACS 文件工具"""
    
    @staticmethod
    def ensure_dir(directory):
        """确保目录存在"""
        try:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
        except OSError as e:
            print("创建目录失败: {}".format(e))
            
    @staticmethod
    def safe_write(file_path, content, encoding='utf-8'):
        """安全写入文件"""
        try:
            JyacsFileUtils.ensure_dir(os.path.dirname(file_path))
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except IOError as e:
            print("写入文件 '{}' 失败: {}".format(file_path, e))
            return False
            
    @staticmethod
    def safe_read(file_path, encoding='utf-8'):
        """安全读取文件"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
        except IOError as e:
            print("读取文件 '{}' 失败: {}".format(file_path, e))
        return None
        
    @staticmethod
    def get_file_size(file_path):
        """获取文件大小（字节）"""
        try:
            if os.path.exists(file_path):
                return os.path.getsize(file_path)
        except OSError as e:
            print("获取文件大小 '{}' 失败: {}".format(file_path, e))
        return 0
        
    @staticmethod
    def get_file_modified_time(file_path):
        """获取文件修改时间戳"""
        try:
            if os.path.exists(file_path):
                return os.path.getmtime(file_path)
        except OSError as e:
            print("获取文件修改时间 '{}' 失败: {}".format(file_path, e))
        return 0

class JyacsTimeUtils:
    """JYACS 时间工具"""
    
    @staticmethod
    def get_current_timestamp():
        """获取当前时间戳"""
        return int(time.time())
        
    @staticmethod
    def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
        """格式化时间戳"""
        try:
            return datetime.fromtimestamp(timestamp).strftime(format_str)
        except (ValueError, TypeError):
            return "Invalid Timestamp"
        
    @staticmethod
    def get_time_diff(timestamp1, timestamp2):
        """获取时间差（秒）"""
        try:
            return abs(int(timestamp1) - int(timestamp2))
        except (ValueError, TypeError):
            return 0
        
    @staticmethod
    def is_recent(timestamp, hours=24):
        """检查时间是否在最近几小时内"""
        current_time = JyacsTimeUtils.get_current_timestamp()
        return JyacsTimeUtils.get_time_diff(current_time, timestamp) <= hours * 3600

class JyacsTextUtils:
    """JYACS 文本工具"""
    
    @staticmethod
    def clean_text(text):
        """清理文本中的多余空白"""
        if not isinstance(text, str):
            return ""
        # 将所有空白符（包括换行、制表符等）替换为单个空格
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    @staticmethod
    def truncate_text(text, max_length=100, suffix="..."):
        """按指定长度截断文本"""
        if not isinstance(text, str) or len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
        
    @staticmethod
    def count_words(text):
        """计算文本中的单词数（基于空格分割）"""
        if not isinstance(text, str):
            return 0
        return len(text.split())
        
    @staticmethod
    def extract_keywords(text, max_keywords=10):
        """提取关键词（基于词频的简单实现）"""
        if not isinstance(text, str):
            return []
            
        try:
            # 简单的关键词提取（按词频）
            words = re.findall(r'\w+', text.lower())
            word_count = {}
            
            for word in words:
                if len(word) > 2:  # 忽略太短的词
                    word_count[word] = word_count.get(word, 0) + 1
                    
            # 按频率排序
            sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
            return [word for word, count in sorted_words[:max_keywords]]
        except Exception as e:
            print("提取关键词失败: {}".format(e))
            return []

# 全局单例
# 这些实例将在模块首次导入时创建，
# 建议在主程序逻辑中（如dev.rpy）根据需要进行管理和注册到store。
jyacs_logger = JyacsLogger()
jyacs_config = JyacsConfig() 
# -*- coding: utf-8 -*-
# jyacs_utils.py - JYACS 工具模块
# 版本: 1.0.0
# 作者: Panghu1102

import os
import time
import logging
import json
import re
from datetime import datetime

class JyacsLogger:
    """JYACS 日志记录器
    
    提供统一的日志记录功能，支持文件和控制台输出。
    """
    
    def __init__(self, log_file="jyacs.log", level=logging.INFO):
        """初始化日志记录器
        
        Args:
            log_file (str): 日志文件名
            level (int): 日志级别
        """
        self.logger = logging.getLogger("JYACS")
        self.logger.setLevel(level)
        
        # 避免重复添加handler
        if self.logger.handlers:
            self.logger.handlers = []

        try:
            # 创建日志目录
            log_dir = os.path.join(config.gamedir, "logs")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
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
            
        except Exception as e:
            print(u"初始化日志记录器失败: {}".format(e))
            raise
    
    def __del__(self):
        """析构函数，确保关闭文件处理器"""
        self.close()
            
    def close(self):
        """关闭日志处理器"""
        try:
            if hasattr(self, 'file_handler') and self.file_handler:
                self.file_handler.close()
                self.logger.removeHandler(self.file_handler)
                self.file_handler = None
            
            if hasattr(self, 'console_handler') and self.console_handler:
                self.logger.removeHandler(self.console_handler)
                self.console_handler = None
        except Exception as e:
            print(u"关闭日志处理器失败: {}".format(e))
            
    def log(self, level, message):
        """通用日志记录方法"""
        try:
            self.logger.log(level, message)
        except Exception as e:
            print(u"记录日志失败: {} ({})".format(message, e))
        
    def log_info(self, message):
        """记录信息日志"""
        self.log(logging.INFO, message)
        
    def log_warning(self, message):
        """记录警告日志"""
        self.log(logging.WARNING, message)
        
    def log_error(self, message):
        """记录错误日志"""
        self.log(logging.ERROR, message)
        
    def log_debug(self, message):
        """记录调试日志"""
        self.log(logging.DEBUG, message)
        
    def log_critical(self, message):
        """记录严重错误日志"""
        self.log(logging.CRITICAL, message)

class JyacsConfig:
    """JYACS 配置管理器
    
    处理配置文件的加载、保存和访问。
    """
    
    def __init__(self, config_file="jyacs_config.json"):
        """初始化配置管理器
        
        Args:
            config_file (str): 配置文件路径
        """
        self.config_file = config_file
        self.config = {}
        self.load_config()
        
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                # 使用utf-8-sig编码处理可能存在的BOM
                with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                    self.config = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(u"加载配置失败: {}。将使用空配置。".format(e))
            self.config = {}
            
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(u"保存配置失败: {}".format(e))
            raise
            
    def get(self, key, default=None):
        """获取配置值
        
        Args:
            key (str): 配置键
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        return self.config.get(key, default)
        
    def set(self, key, value):
        """设置配置值并保存
        
        Args:
            key (str): 配置键
            value: 配置值
        """
        self.config[key] = value
        self.save_config()
        
    def has(self, key):
        """检查配置是否存在
        
        Args:
            key (str): 配置键
            
        Returns:
            bool: 是否存在
        """
        return key in self.config

class JyacsFileUtils:
    """JYACS 文件工具
    
    提供文件操作的工具方法。
    """
    
    @staticmethod
    def ensure_dir(directory):
        """确保目录存在
        
        Args:
            directory (str): 目录路径
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError as e:
            print(u"创建目录失败: {}".format(e))
            raise
            
    @staticmethod
    def safe_write(file_path, content, encoding='utf-8'):
        """安全写入文件
        
        Args:
            file_path (str): 文件路径
            content (str): 文件内容
            encoding (str): 编码方式
            
        Returns:
            bool: 是否成功
        """
        try:
            JyacsFileUtils.ensure_dir(os.path.dirname(file_path))
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except IOError as e:
            print(u"写入文件 '{}' 失败: {}".format(file_path, e))
            return False
            
    @staticmethod
    def safe_read(file_path, encoding='utf-8'):
        """安全读取文件
        
        Args:
            file_path (str): 文件路径
            encoding (str): 编码方式
            
        Returns:
            str: 文件内容，失败返回None
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
        except IOError as e:
            print(u"读取文件 '{}' 失败: {}".format(file_path, e))
        return None
        
    @staticmethod
    def get_file_size(file_path):
        """获取文件大小（字节）
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            int: 文件大小
        """
        try:
            if os.path.exists(file_path):
                return os.path.getsize(file_path)
        except OSError as e:
            print(u"获取文件大小 '{}' 失败: {}".format(file_path, e))
        return 0
        
    @staticmethod
    def get_file_modified_time(file_path):
        """获取文件修改时间戳
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            float: 修改时间戳
        """
        try:
            if os.path.exists(file_path):
                return os.path.getmtime(file_path)
        except OSError as e:
            print(u"获取文件修改时间 '{}' 失败: {}".format(file_path, e))
        return 0

class JyacsTimeUtils:
    """JYACS 时间工具
    
    提供时间相关的工具方法。
    """
    
    @staticmethod
    def get_current_timestamp():
        """获取当前时间戳
        
        Returns:
            int: 当前时间戳
        """
        return int(time.time())
        
    @staticmethod
    def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
        """格式化时间戳
        
        Args:
            timestamp (int): 时间戳
            format_str (str): 格式字符串
            
        Returns:
            str: 格式化的时间字符串
        """
        try:
            return datetime.fromtimestamp(timestamp).strftime(format_str)
        except (ValueError, TypeError) as e:
            print(u"格式化时间戳失败: {}".format(e))
            return "Invalid Timestamp"
        
    @staticmethod
    def get_time_diff(timestamp1, timestamp2):
        """获取时间差（秒）
        
        Args:
            timestamp1 (int): 时间戳1
            timestamp2 (int): 时间戳2
            
        Returns:
            int: 时间差（秒）
        """
        try:
            return abs(int(timestamp1) - int(timestamp2))
        except (ValueError, TypeError) as e:
            print(u"计算时间差失败: {}".format(e))
            return 0
        
    @staticmethod
    def is_recent(timestamp, hours=24):
        """检查时间是否在最近几小时内
        
        Args:
            timestamp (int): 时间戳
            hours (int): 小时数
            
        Returns:
            bool: 是否在指定时间内
        """
        try:
            current_time = JyacsTimeUtils.get_current_timestamp()
            return JyacsTimeUtils.get_time_diff(current_time, timestamp) <= hours * 3600
        except Exception as e:
            print(u"检查时间是否最近失败: {}".format(e))
            return False

class JyacsTextUtils:
    """JYACS 文本工具
    
    提供文本处理的工具方法。
    """
    
    @staticmethod
    def clean_text(text):
        """清理文本中的多余空白
        
        Args:
            text (str): 输入文本
            
        Returns:
            str: 清理后的文本
        """
        if not isinstance(text, str):
            return ""
        try:
            # 将所有空白符替换为单个空格
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        except Exception as e:
            print(u"清理文本失败: {}".format(e))
            return text
        
    @staticmethod
    def truncate_text(text, max_length=100, suffix="..."):
        """按指定长度截断文本
        
        Args:
            text (str): 输入文本
            max_length (int): 最大长度
            suffix (str): 后缀
            
        Returns:
            str: 截断后的文本
        """
        if not isinstance(text, str):
            return str(text)
        try:
            if len(text) <= max_length:
                return text
            return text[:max_length - len(suffix)] + suffix
        except Exception as e:
            print(u"截断文本失败: {}".format(e))
            return text
        
    @staticmethod
    def count_words(text):
        """计算文本中的单词数
        
        Args:
            text (str): 输入文本
            
        Returns:
            int: 单词数
        """
        if not isinstance(text, str):
            return 0
        try:
            return len(text.split())
        except Exception as e:
            print(u"计算单词数失败: {}".format(e))
            return 0
        
    @staticmethod
    def extract_keywords(text, max_keywords=10):
        """提取关键词
        
        Args:
            text (str): 输入文本
            max_keywords (int): 最大关键词数
            
        Returns:
            list: 关键词列表
        """
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
            print(u"提取关键词失败: {}".format(e))
            return []

# 全局单例
try:
    jyacs_logger = JyacsLogger()
    jyacs_config = JyacsConfig()
except Exception as e:
    print(u"初始化JYACS工具模块失败: {}".format(e))
    # 在初始化失败时，仍然定义变量但设为None
    jyacs_logger = None
    jyacs_config = None
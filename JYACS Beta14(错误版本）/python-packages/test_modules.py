#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_modules.py - JYACS 模块测试工具
# 版本: 1.0.0
# 作者: Panghu1102

"""
JYACS 模块测试工具
用于测试各个模块的功能是否正常。
提供基本的测试用例和错误检查。
"""

import os
import sys
import json
import logging
import unittest
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("JYACS_Test")

class JyacsTestCase(unittest.TestCase):
    """JYACS 测试基类
    
    提供基本的测试功能和辅助方法。
    """
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_start_time = datetime.now()
        logger.info("开始测试: %s", self._testMethodName)
        
    def tearDown(self):
        """测试后的清理工作"""
        duration = datetime.now() - self.test_start_time
        logger.info("测试完成: %s (耗时: %s)", self._testMethodName, duration)
        
    def assertDictStructure(self, test_dict, required_keys):
        """检查字典是否包含所有必需的键
        
        Args:
            test_dict (dict): 要检查的字典
            required_keys (list): 必需的键列表
        """
        for key in required_keys:
            self.assertIn(key, test_dict, f"缺少必需的键: {key}")

class ConfigTests(JyacsTestCase):
    """配置模块测试"""
    
    def test_config_structure(self):
        """测试配置文件结构"""
        try:
            with open("jyacs_config.json", "r", encoding="utf-8-sig") as f:
                config = json.load(f)
                
            required_keys = [
                "version",
                "prompts",
                "api_config",
                "language",
                "max_history_token",
                "emotion",
                "logging"
            ]
            
            self.assertDictStructure(config, required_keys)
            self.assertIsInstance(config["prompts"], dict)
            self.assertIsInstance(config["api_config"], dict)
            self.assertIsInstance(config["emotion"], dict)
            self.assertIsInstance(config["logging"], dict)
        except Exception as e:
            self.fail(f"测试配置文件结构失败: {e}")

class TextProcessingTests(JyacsTestCase):
    """文本处理模块测试"""
    
    def setUp(self):
        """测试前的准备工作"""
        super().setUp()
        try:
            from jyacs_interface import JyacsTalkSplitV2, JyacsTextProcessor
            self.splitter = JyacsTalkSplitV2()
            self.processor = JyacsTextProcessor()
        except ImportError as e:
            self.skipTest(f"无法导入所需模块: {e}")
            
    def test_text_splitting(self):
        """测试文本分句功能"""
        test_cases = [
            {
                "input": "你好！我是优里。今天天气真好。",
                "expected": ["你好！", "我是优里。", "今天天气真好。"]
            },
            {
                "input": "Hello! This is a test.",
                "expected": ["Hello!", "This is a test."]
            }
        ]
        
        for case in test_cases:
            with self.subTest(input=case["input"]):
                try:
                    self.splitter.add_part(case["input"])
                    result = []
                    while True:
                        sentence = self.splitter.split_present_sentence()
                        if not sentence:
                            break
                        result.append(sentence)
                    result.extend(self.splitter.announce_stop())
                    
                    self.assertEqual(result, case["expected"])
                except Exception as e:
                    self.fail(f"文本分句测试失败: {e}")
                    
    def test_text_cleaning(self):
        """测试文本清理功能"""
        test_cases = [
            {
                "input": "  Hello   World  ",
                "expected": "Hello World"
            },
            {
                "input": "Multiple\n\nLine\n\nBreaks",
                "expected": "Multiple Line Breaks"
            }
        ]
        
        for case in test_cases:
            with self.subTest(input=case["input"]):
                try:
                    result = self.processor.clean_text(case["input"])
                    self.assertEqual(result, case["expected"])
                except Exception as e:
                    self.fail(f"文本清理测试失败: {e}")

class EmotionTests(JyacsTestCase):
    """情绪分析模块测试"""
    
    def setUp(self):
        """测试前的准备工作"""
        super().setUp()
        try:
            from jyacs_emotion import JyacsEmoSelector
            self.selector = JyacsEmoSelector()
        except ImportError as e:
            self.skipTest(f"无法导入所需模块: {e}")
            
    def test_emotion_selection(self):
        """测试情绪选择功能"""
        test_cases = [
            {
                "input": "我很开心！",
                "expected_type": "happy"
            },
            {
                "input": "我爱你。",
                "expected_type": "love"
            }
        ]
        
        for case in test_cases:
            with self.subTest(input=case["input"]):
                try:
                    self.selector.analyze(case["input"])
                    self.assertEqual(self.selector.get_emotion_name(), case["expected_type"])
                except Exception as e:
                    self.fail(f"情绪选择测试失败: {e}")

def main():
    """主函数"""
    try:
        # 添加当前目录到 Python 路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
            
        # 运行测试
        unittest.main(verbosity=2)
    except Exception as e:
        logger.error("测试执行失败: %s", e)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
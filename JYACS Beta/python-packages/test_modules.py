#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JYACS模块测试脚本
用于验证所有Python模块是否正常工作
"""

import os
import sys
import unittest

class TestJyacsModules(unittest.TestCase):
    """JYACS模块测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 导入模块
        from jyacs_utils import JyacsLogger, JyacsConfig, JyacsFileUtils
        from jyacs_emotion import JyacsEmoSelector
        from jyacs_interface import JyacsTalkSplitV2, JyacsTextProcessor
        
        # 创建实例
        self.logger = JyacsLogger()
        self.config = JyacsConfig()
        self.file_utils = JyacsFileUtils()
        self.emotion_selector = JyacsEmoSelector()
        self.text_processor = JyacsTextProcessor()
    
    def test_logger(self):
        """测试日志记录器"""
        self.logger.log_info("测试信息")
        self.logger.log_warning("测试警告")
        self.logger.log_error("测试错误")
        self.assertTrue(os.path.exists("logs/jyacs.log"))
    
    def test_config(self):
        """测试配置管理器"""
        self.config.set("test_key", "test_value")
        self.assertEqual(self.config.get("test_key"), "test_value")
        self.assertTrue(self.config.has("test_key"))
    
    def test_file_utils(self):
        """测试文件工具"""
        test_dir = "test_dir"
        test_file = os.path.join(test_dir, "test.txt")
        test_content = "测试内容"
        
        self.file_utils.ensure_dir(test_dir)
        self.assertTrue(os.path.exists(test_dir))
        
        self.file_utils.safe_write(test_file, test_content)
        self.assertEqual(self.file_utils.safe_read(test_file), test_content)
        
        # 清理测试文件
        os.remove(test_file)
        os.rmdir(test_dir)
    
    def test_emotion_selector(self):
        """测试情绪选择器"""
        test_texts = {
            "我很开心！": "happy",
            "我好难过...": "sad",
            "我生气了！": "angry",
            "这太令人惊讶了": "surprised",
            "我在思考": "thinking",
            "我爱你❤️": "love",
            "我很兴奋": "excited",
            "一切都很普通": "neutral"
        }
        
        for text, expected_emotion in test_texts.items():
            self.emotion_selector.analyze(text)
            emotion = self.emotion_selector.get_emote()
            emotion_name = self.emotion_selector.get_emotion_name()
            
            # 测试情绪名称或确保情绪表情在对应的情绪类别中
            self.assertTrue(
                emotion_name == expected_emotion or 
                emotion in self.emotion_selector.emotion_patterns[expected_emotion]["emotes"],
                f"对于文本'{text}'，期望情绪'{expected_emotion}'，但得到'{emotion_name}'，表情为'{emotion}'"
            )
    
    def test_text_processor(self):
        """测试文本处理器"""
        test_text = "你好！这是一个测试。今天天气很好？"
        sentences = self.text_processor.process_text(test_text)
        
        self.assertEqual(len(sentences), 3)
        self.assertEqual(sentences[0], "你好！")
        self.assertEqual(sentences[1], "这是一个测试。")
        self.assertEqual(sentences[2], "今天天气很好？")
        
        cleaned_text = self.text_processor.clean_text("  测试   文本  ")
        self.assertEqual(cleaned_text, "测试 文本")
        
        formatted_text = self.text_processor.format_for_display("你好。再见。")
        self.assertTrue("{fast}" in formatted_text)

def run_tests():
    """运行所有测试"""
    unittest.main()

if __name__ == "__main__":
    run_tests() 
# -*- coding: utf-8 -*-
# jyacs_emotion.py - JYACS 情绪分析模块
# 版本: 1.0.1 (已修复)
# 作者: Panghu1102

import re
import random

class JyacsEmoSelector:
    """JYACS 情绪选择器
    
    根据输入文本中的关键词，简单地选择一个情绪表情。
    """
    
    def __init__(self):
        self.current_emotion = "1eua"  # 默认情绪：中性
        
        # 情绪关键词和对应的表情列表
        # 使用 re.compile 预编译正则表达式以提高性能
        self.emotion_patterns = {
            # 积极情绪
            "happy": {
                "patterns": [re.compile(p) for p in ['开心', '高兴', '快乐', '愉快', '兴奋', '😊', '😄', '😃']],
                "emotes": ["1eua", "1hub", "1hubsa", "1tub", "1tubsa"]
            },
            "love": {
                "patterns": [re.compile(p) for p in ['爱', '喜欢', '爱慕', '❤️', '💕', '💖']],
                "emotes": ["1hua", "1hub", "1hubsa", "1tub", "1tubsa"]
            },
            "excited": {
                "patterns": [re.compile(p) for p in ['激动', '兴奋', '振奋', '😆', '🤩']],
                "emotes": ["1hub", "1hubsa", "1tub", "1tubsa"]
            },
            
            # 中性情绪
            "neutral": {
                "patterns": [re.compile(p) for p in ['一般', '普通', '正常', '😐', '😑']],
                "emotes": ["1eua", "1eub", "1euc"]
            },
            "thinking": {
                "patterns": [re.compile(p) for p in ['思考', '想', '考虑', '🤔', '💭']],
                "emotes": ["1eub", "1euc", "1lua", "1lub"]
            },
            
            # 消极情绪
            "sad": {
                "patterns": [re.compile(p) for p in ['难过', '伤心', '悲伤', '😢', '😭', '💔']],
                "emotes": ["1sua", "1sub", "1suc", "1hua"]
            },
            "angry": {
                "patterns": [re.compile(p) for p in ['生气', '愤怒', '恼火', '😠', '😡', '💢']],
                "emotes": ["1sua", "1sub", "1suc"]
            },
            "worried": {
                "patterns": [re.compile(p) for p in ['担心', '忧虑', '焦虑', '😰', '😨', '😟']],
                "emotes": ["1lua", "1lub", "1sua", "1sub"]
            },
            "surprised": {
                "patterns": [re.compile(p) for p in ['惊讶', '震惊', '意外', '😲', '😱', '😳']],
                "emotes": ["1sua", "1sub", "1eua", "1eub"]
            }
        }
        
        # 创建情绪表情到情绪名称的映射，用于快速反向查找
        self.emote_to_emotion = {
            emote: emotion_name
            for emotion_name, data in self.emotion_patterns.items()
            for emote in data["emotes"]
        }
        
        # 情绪强度权重，用于调整不同情绪的优先级
        self.emotion_weights = {
            "happy": 1.2, "love": 1.5, "excited": 1.3,
            "neutral": 1.0, "thinking": 1.1,
            "sad": 1.4, "angry": 1.6, "worried": 1.3, "surprised": 1.2
        }
        
    def analyze(self, text):
        """分析文本，并根据结果更新当前情绪。"""
        if not isinstance(text, str) or not text:
            return text # 如果输入不是字符串或为空，则不作处理
            
        try:
            emotion_scores = {}
            
            for emotion_name, data in self.emotion_patterns.items():
                score = 0
                for pattern in data["patterns"]:
                    # 累加每个关键词的出现次数
                    score += len(pattern.findall(text))
                    
                if score > 0:
                    # 应用权重，并存入得分表
                    emotion_scores[emotion_name] = score * self.emotion_weights.get(emotion_name, 1.0)
                    
            if emotion_scores:
                # 选择得分最高的情绪
                best_emotion = max(emotion_scores, key=emotion_scores.get)
                # 从该情绪的表情列表中随机选择一个
                self.current_emotion = random.choice(self.emotion_patterns[best_emotion]["emotes"])
            else:
                # 如果没有匹配到任何情绪，则重置为默认中性情绪
                self.reset_emotion()
                
        except Exception as e:
            print("情绪分析失败: {}。将使用默认情绪。".format(e))
            self.reset_emotion()
            
        return text
        
    def get_emote(self):
        """获取当前选择的表情字符串。"""
        return self.current_emotion
        
    def set_emotion(self, emote_code):
        """手动设置情绪。"""
        # 验证 emote_code 是否存在于映射中，增加稳健性
        if emote_code in self.emote_to_emotion:
            self.current_emotion = emote_code
        else:
            print("警告: 尝试设置一个未知的情绪表情 '{}'。".format(emote_code))

    def get_emotion_name(self):
        """根据当前表情获取其情绪分类名（如 'happy', 'sad'）。"""
        return self.emote_to_emotion.get(self.current_emotion, "neutral")
        
    def reset_emotion(self):
        """重置为默认的中性情绪。"""
        self.current_emotion = "1eua"

class JyacsEmotionAnalyzer:
    """JYACS 情绪分析器
    
    一个高级封装，用于简化情绪分析的调用。
    """
    
    def __init__(self):
        self.selector = JyacsEmoSelector()
        
    def analyze_text_emotion(self, text):
        """分析文本情绪，并返回处理后的文本和所选表情。"""
        processed_text = self.selector.analyze(text)
        emotion = self.selector.get_emote()
        return processed_text, emotion
        
    def get_emotion_from_keywords(self, keywords):
        """根据关键词列表获取一个合适的情绪表情。"""
        if not isinstance(keywords, list) or not keywords:
            return "1eua" # 默认中性表情
            
        # 将关键词列表合并为一个字符串进行分析
        text = " ".join(keywords)
        self.selector.analyze(text)
        return self.selector.get_emote()
        
    def get_emotion_variations(self, base_emotion, count=3):
        """获取一个基础表情的变体列表。"""
        # 通过反向映射找到基础表情所属的情绪分类
        emotion_name = self.selector.emote_to_emotion.get(base_emotion)
        if emotion_name:
            # 获取该分类下的所有表情
            all_emotes = self.selector.emotion_patterns[emotion_name]["emotes"]
            # 返回指定数量的随机样本
            return random.sample(all_emotes, min(count, len(all_emotes)))
        # 如果未找到，则只返回基础表情
        return [base_emotion] 
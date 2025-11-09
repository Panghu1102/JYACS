# ============================================
# 警告: 此文件已废弃 (DEPRECATED)
# ============================================
# 该图片表情系统已被JUSTYURI表情编码系统取代
# 新系统使用表情编码（格式：X-YYYYY-ZZZZ）来动态组合表情
# 而不是使用预定义的静态图片
#
# 这个文件是当初没想好怎么写表情的时候写的，后来因为不理想，又要强制背景，就费了点功夫，现在按照JY的方法来显示。  
# 这个文件现在只供参考使用哈，当然价值不大，有类似项目可以研究。
# ============================================

# jyacs_emotion_images.rpy - JYACS 表情图片管理模块 (已废弃)
# 根据AI回复内容中的关键词，自动切换优里的立绘背景图片
# 使用JUSTYURI的表情系统实现

init -1200 python:
    import os
    import random
    
    class JyacsEmotionImageManager:
        """JYACS 表情图片管理器
        
        根据AI回复内容中的关键词，自动选择合适的优里立绘背景图片
        支持基于JUSTYURI的表情编码系统
        """
        
        def __init__(self):
            """初始化表情图片管理器"""
            self.emotions_path = "mod_assets/images/expressions"
            self.current_emotion = "normal"
            self.current_expression = "A-ACAAA-AAAA"  # 默认表情编码
            
            # 关键词到表情图片的映射
            self.keyword_to_emotion = {
                # 积极情绪
                '开心': 'happy',
                '高兴': 'happy', 
                '快乐': 'happy',
                '愉快': 'happy',
                '兴奋': 'happy',
                '幸福': 'happy',
                '喜欢': 'happy',
                '可爱': 'happy',
                '爱': 'kind',
                '温柔': 'kind',
                '亲切': 'kind',
                
                # 中性/思考
                '思考': 'think and interested',
                '想': 'think and interested',
                '考虑': 'think and interested',
                '觉得': 'think and interested',
                '认为': 'think and interested',
                '可能': 'think and a little worry',
                '担心': 'think and a little worry',
                '忧虑': 'think and a little worry',
                
                # 轻微消极
                '有点': 'a little sad',
                '稍微': 'a little sad',
                '一点点': 'a little sad',
                '难过': 'sad',
                '伤心': 'sad',
                '悲伤': 'sad',
                '沮丧': 'sad',
                '失望': 'sad',
                '害怕': 'sad',
                '恐惧': 'sad',
                
                # 强烈消极
                '生气': 'unhappy',
                '愤怒': 'unhappy',
                '恼火': 'unhappy',
                '讨厌': 'unhappy',
                '不喜欢': 'unhappy',
                
                # 放松状态
                '放松': 'relaxed',
                '平静': 'relaxed',
                '安心': 'relaxed',
                '舒服': 'relaxed',
                '轻松': 'relaxed',
                
                # 复合情绪
                '开心又放松': 'relaxing and happy',
                '愉快又轻松': 'relaxing and happy'
            }
            
            # 正常表情列表（无关键词匹配时随机选择）
            self.normal_emotions = [
                'normal', 'normal2', 'normal3', 'relaxed'
            ]
            
            # 验证表情图片是否存在
            self._validate_emotions()
        
        def _validate_emotions(self):
            """验证表情图片文件是否存在"""
            try:
                base_path = renpy.config.gamedir
                emotions_dir = os.path.join(base_path, "..", self.emotions_path)
                
                if not os.path.exists(emotions_dir):
                    print("警告: 表情图片目录不存在: {}".format(emotions_dir))
                    return
                
                # 获取实际存在的图片文件
                existing_files = []
                for file in os.listdir(emotions_dir):
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        name = os.path.splitext(file)[0]
                        existing_files.append(name)
                
                print("找到的表情图片: {}".format(existing_files))
                
            except Exception as e:
                print("验证表情图片时出错: {}".format(e))
        
        def analyze_text_for_emotion(self, text):
            """分析文本并选择合适的表情图片
            
            Args:
                text (str): AI回复的文本
                
            Returns:
                str: 选择的表情图片名称
            """
            if not text or not isinstance(text, str):
                return self.get_random_normal_emotion()
            
            text_lower = text.lower()
            
            # 检查关键词匹配
            for keyword, emotion in self.keyword_to_emotion.items():
                if keyword in text_lower:
                    # 更新表情编码
                    self.update_expression_code(emotion)
                    return emotion
            
            # 检查复合关键词
            for keywords, emotion in self.keyword_to_emotion.items():
                if ' ' in keywords:
                    parts = keywords.split(' ')
                    if all(part in text_lower for part in parts):
                        # 更新表情编码
                        self.update_expression_code(emotion)
                        return emotion
            
            # 如果没有匹配，返回随机正常表情
            return self.get_random_normal_emotion()
        
        def update_expression_code(self, emotion):
            """根据情绪更新表情编码"""
            # 这里可以实现从情绪名称到JUSTYURI表情编码的映射
            emotion_to_code = {
                'happy': 'A-BCAAA-AAAA',
                'sad': 'A-ADCAA-AAAA',
                'normal': 'A-ACAAA-AAAA',
                'relaxed': 'A-ACAAA-AAAA',
                'kind': 'A-BCAAA-AAAA',
                'a little sad': 'A-ADAAA-AAAA',
                'think and interested': 'A-ACBAA-AAAA',
                'think and a little worry': 'A-ADBAA-AAAA',
                'relaxing and happy': 'A-BCAAA-AAAA',
                'unhappy': 'A-ADCAA-AAAA'
            }
            
            if emotion in emotion_to_code:
                self.current_expression = emotion_to_code[emotion]
            else:
                self.current_expression = 'A-ACAAA-AAAA'  # 默认表情编码
        
        def get_random_normal_emotion(self):
            """获取随机正常表情"""
            emotion = random.choice(self.normal_emotions)
            self.update_expression_code(emotion)
            return emotion
        
        def show_emotion_image(self, emotion_name):
            """显示指定表情的图片"""
            try:
                # 将空格替换为下划线用于显示名称
                display_name = emotion_name.replace(" ", "_")
                
                # 检查图片是否存在
                base_path = renpy.config.gamedir
                image_path = os.path.join(base_path, "..", self.emotions_path, "{}.png".format(emotion_name))
                
                if os.path.exists(image_path):
                    self.current_emotion = emotion_name
                    # 不清除场景，保持原游戏的背景系统
                    # 原游戏使用 jy_bg 动态背景，我们只需要显示优里的表情即可
                    # renpy.show("jyacs_emotion_{}".format(display_name))
                    return True
                else:
                    # 如果特定表情不存在，使用normal
                    print("表情图片不存在: {}，使用normal".format(image_path))
                    # renpy.show("jyacs_emotion_normal")
                    return False
                    
            except Exception as e:
                print("显示表情图片时出错: {}".format(e))
                # renpy.show("jyacs_emotion_normal")
                return False
        
        def get_current_emotion(self):
            """获取当前表情"""
            return self.current_emotion
            
        def get_current_expression(self):
            """获取当前表情编码"""
            return self.current_expression

# 创建全局表情图片管理器实例 (已废弃 - 不再使用)
# init python:
#     if not hasattr(store, 'jyacs_emotion_image_manager'):
#         store.jyacs_emotion_image_manager = JyacsEmotionImageManager()

# 注册表情图片到Renpy（作为全屏背景显示）(已废弃 - 不再需要)
# 新系统使用JUSTYURI表情编码动态组合表情，不再使用静态图片
# init -1100:
#     image jyacs_emotion_happy = Transform("mod_assets/images/expressions/happy.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_sad = Transform("mod_assets/images/expressions/sad.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_normal = Transform("mod_assets/images/expressions/normal.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_normal2 = Transform("mod_assets/images/expressions/normal2.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_normal3 = Transform("mod_assets/images/expressions/normal3.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_relaxed = Transform("mod_assets/images/expressions/relaxed.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_kind = Transform("mod_assets/images/expressions/kind.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_a_little_sad = Transform("mod_assets/images/expressions/a little sad.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_think_and_interested = Transform("mod_assets/images/expressions/think and interested.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_think_and_a_little_worry = Transform("mod_assets/images/expressions/think and a little worry.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_relaxing_and_happy = Transform("mod_assets/images/expressions/relaxing and happy.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_unhappy = Transform("mod_assets/images/expressions/unhappy.png", size=(1280, 720), yalign=1.0)

# 辅助函数 (已废弃 - 使用新的表情系统)
# init python:
#     def jyacs_show_emotion_from_text(text):
#         """从文本分析并显示表情的便捷函数 (已废弃)"""
#         emotion = store.jyacs_emotion_image_manager.analyze_text_for_emotion(text)
#         store.jyacs_emotion_image_manager.show_emotion_image(emotion)
#         return emotion

# 新的辅助函数 - 使用JUSTYURI表情编码系统
init python:
    def jyacs_show_emotion_from_text(text):
        """从文本分析并显示表情的便捷函数
        
        使用JUSTYURI表情编码系统分析文本并显示对应表情
        
        Args:
            text (str): 要分析的文本
            
        Returns:
            str: 表情编码
        """
        expression = get_expression_from_text(text)
        show_chr(expression)
        return expression
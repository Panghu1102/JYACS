# jyacs_emotion_images.rpy - JYACS 表情图片管理模块
# 版本: 1.0.0
# 作者: 基于用户需求的表情图片系统

init -1200 python:
    import os
    import random
    
    class JyacsEmotionImageManager:
        """JYACS 表情图片管理器
        
        根据AI回复内容中的关键词，自动选择合适的表情图片显示
        支持基于文件系统的表情图片管理
        """
        
        def __init__(self):
            """初始化表情图片管理器"""
            self.emotions_path = "mod_assets/images/emotins"
            self.current_emotion = "normal"
            
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
                '爱': 'kind',
                '温柔': 'kind',
                '亲切': 'kind',
                '可爱': 'happy',
                
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
                
                # 强烈消极
                '生气': 'unhappy',
                '愤怒': 'unhappy',
                '恼火': 'unhappy',
                '讨厌': 'unhappy',
                '不喜欢': 'unhappy',
                '害怕': 'sad',
                '恐惧': 'sad',
                
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
                    return emotion
            
            # 检查复合关键词
            for keywords, emotion in self.keyword_to_emotion.items():
                if ' ' in keywords:
                    parts = keywords.split(' ')
                    if all(part in text_lower for part in parts):
                        return emotion
            
            # 如果没有匹配，返回随机正常表情
            return self.get_random_normal_emotion()
        
        def get_random_normal_emotion(self):
            """获取随机正常表情"""
            return random.choice(self.normal_emotions)
        
        def show_emotion_image(self, emotion_name, character="yuri"):
            """显示表情图片（全屏背景）
            
            Args:
                emotion_name (str): 表情名称
                character (str): 角色名称（保留参数，实际用于背景命名）
            """
            try:
                image_path = "{}/{}.png".format(self.emotions_path, emotion_name)
                
                # 检查图片是否存在
                base_path = renpy.config.gamedir
                full_path = os.path.join(base_path, "..", image_path)
                
                if os.path.exists(full_path):
                    self.current_emotion = emotion_name
                    # 改为全屏背景显示
                    renpy.show("jyacs_emotion_{} at truecenter".format(emotion_name))
                    return True
                else:
                    # 如果特定表情不存在，使用normal背景
                    print("表情背景不存在: {}，使用normal".format(full_path))
                    renpy.show("jyacs_emotion_normal at truecenter")
                    return False
                    
            except Exception as e:
                print("显示表情背景时出错: {}".format(e))
                renpy.show("jyacs_emotion_normal at truecenter")
                return False
        
        def get_current_emotion(self):
            """获取当前表情"""
            return self.current_emotion

    # 创建全局表情图片管理器实例
    if not hasattr(store, 'jyacs_emotion_image_manager'):
        store.jyacs_emotion_image_manager = JyacsEmotionImageManager()

# 注册表情图片到Renpy（全屏背景版本）
init -1100:
    python:
        try:
            base_path = "mod_assets/images/emotins"
            emotions = [
                'happy', 'sad', 'normal', 'normal2', 'normal3', 'relaxed',
                'kind', 'a little sad', 'think and interested', 'think and a little worry',
                'relaxing and happy', 'unhappy'
            ]
            
            for emotion in emotions:
                image_file = "{}/{}.png".format(base_path, emotion)
                # 注册为全屏背景图片，处理空格
                image_name = "jyacs_emotion_{}".format(emotion.replace(" ", "_"))
                renpy.image(image_name, im.Scale(image_file, config.screen_width, config.screen_height))
                
        except Exception as e:
            print("注册表情图片时出错: {}".format(e))

# 辅助函数
init -1000 python:
    def jyacs_show_emotion_from_text(text, character="yuri"):
        """根据文本显示对应表情图片的便捷函数
        
        Args:
            text (str): AI回复文本
            character (str): 角色名称
            
        Returns:
            str: 使用的表情名称
        """
        if not hasattr(store, 'jyacs_emotion_image_manager'):
            return "normal"
        
        emotion = store.jyacs_emotion_image_manager.analyze_text_for_emotion(text)
        store.jyacs_emotion_image_manager.show_emotion_image(emotion, character)
        return emotion

    # 注册到store
    if not hasattr(store, 'jyacs_show_emotion_from_text'):
        store.jyacs_show_emotion_from_text = jyacs_show_emotion_from_text
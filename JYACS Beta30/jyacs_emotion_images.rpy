# jyacs_emotion_images.rpy - JYACS 表情图片管理模块
# 根据AI回复内容中的关键词，自动切换优里的立绘背景图片

init -1200 python:
    import os
    import random
    
    class JyacsEmotionImageManager:
        """JYACS 表情图片管理器
        
        根据AI回复内容中的关键词，自动选择合适的优里立绘背景图片
        支持基于文件系统的表情图片管理和关键词匹配
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
                    # 先清除当前场景，再显示为全屏背景，使用下划线格式名称
                    renpy.scene()
                    renpy.show("jyacs_emotion_{}".format(display_name))
                    return True
                else:
                    # 如果特定表情不存在，使用normal
                    print("表情图片不存在: {}，使用normal".format(image_path))
                    renpy.scene()
                    renpy.show("jyacs_emotion_normal")
                    return False
                    
            except Exception as e:
                print("显示表情图片时出错: {}".format(e))
                renpy.scene()
                renpy.show("jyacs_emotion_normal")
                return False
        
        def get_current_emotion(self):
            """获取当前表情"""
            return self.current_emotion

# 创建全局表情图片管理器实例
init python:
    if not hasattr(store, 'jyacs_emotion_image_manager'):
        store.jyacs_emotion_image_manager = JyacsEmotionImageManager()

# 注册表情图片到Renpy（作为全屏背景显示）
init -1100:
    image jyacs_emotion_happy = Transform("mod_assets/images/emotins/happy.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_sad = Transform("mod_assets/images/emotins/sad.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_normal = Transform("mod_assets/images/emotins/normal.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_normal2 = Transform("mod_assets/images/emotins/normal2.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_normal3 = Transform("mod_assets/images/emotins/normal3.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_relaxed = Transform("mod_assets/images/emotins/relaxed.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_kind = Transform("mod_assets/images/emotins/kind.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_a_little_sad = Transform("mod_assets/images/emotins/a little sad.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_think_and_interested = Transform("mod_assets/images/emotins/think and interested.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_think_and_a_little_worry = Transform("mod_assets/images/emotins/think and a little worry.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_relaxing_and_happy = Transform("mod_assets/images/emotins/relaxing and happy.png", size=(1280, 720), yalign=1.0)
    image jyacs_emotion_unhappy = Transform("mod_assets/images/emotins/unhappy.png", size=(1280, 720), yalign=1.0)

# 辅助函数
init python:
    def jyacs_show_emotion_from_text(text):
        """从文本分析并显示表情的便捷函数"""
        emotion = store.jyacs_emotion_image_manager.analyze_text_for_emotion(text)
        store.jyacs_emotion_image_manager.show_emotion_image(emotion)
        return emotion
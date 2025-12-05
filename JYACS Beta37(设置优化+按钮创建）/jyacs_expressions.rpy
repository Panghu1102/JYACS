# jyacs_expressions.rpy - JYACS 表情系统
# 基于JUSTYURI的表情系统实现

init -1200 python:
    import os
    import random
    import re
    
    class yuri_display:
        """
        优里表情显示系统，基于JUSTYURI的实现
        处理表情编码并显示对应的表情
        """
        
        values = {
            "position": "sit",
            "head": "front",
            "eyes": 0,
            "mouth": "a",
            "eyebrows": "a",
            "blush": False,
            "cry": False,
            "both arms": 0,
            "left arm": 0,
            "right arm": 0
        }
        
        @staticmethod
        def position(index):
            position = ["sit", "stand"]
            yuri_display.values["position"] = position[index]
            return yuri_display
        
        @staticmethod
        def head(index):
            head = ["front", "down", "side"]
            yuri_display.values["head"] = head[index]
            return yuri_display
        
        @staticmethod
        def eyes(index):
            yuri_display.values["eyes"] = index
            return yuri_display
        
        @staticmethod
        def mouth(index):
            yuri_display.values["mouth"] = index
            return yuri_display
        
        @staticmethod
        def eyebrows(index):
            yuri_display.values["eyebrows"] = index
            return yuri_display
        
        @staticmethod
        def blush(value):
            yuri_display.values["blush"] = value
            return yuri_display
        
        @staticmethod
        def cry(value):
            yuri_display.values["cry"] = value
            return yuri_display
        
        @staticmethod
        def both_arms(index):
            yuri_display.values["both arms"] = index
            yuri_display.values["left arm"] = 0
            yuri_display.values["right arm"] = 0
            return yuri_display
        
        @staticmethod
        def left_arm(index):
            yuri_display.values["both arms"] = 0
            yuri_display.values["left arm"] = index
            return yuri_display
        
        @staticmethod
        def right_arm(index):
            yuri_display.values["both arms"] = 0
            yuri_display.values["right arm"] = index
            return yuri_display
        
        @staticmethod
        def show():
            """显示当前表情状态"""
            global yuri_sit
            global yuri_stand
            
            # 构建眼睛图像名称
            eyes = "eyes_" + str(yuri_display.values["eyes"]) + "_" + yuri_display.values["head"]
            if eyes == "eyes_13_front": 
                eyes = "eyes_12_front"
                eyes_alpha = "yuri_sit_eyes_standard"
                eyes_beta = "insanepupils"
            elif yuri_display.values["head"] == "front": 
                if yuri_display.values["eyes"] in [0, 3, 7, 8, 9]:
                    eyes_alpha = "yuri_sit_blink_1"
                elif yuri_display.values["eyes"] in [1, 4, 5, 10]:
                    eyes_alpha = "yuri_sit_blink_2"
                else:
                    eyes_alpha = "yuri_sit_eyes_standard"
                eyes_beta = "nothing"
            else: 
                eyes_alpha = "yuri_sit_eyes_standard"
                eyes_beta = "nothing"
            
            # 构建嘴巴图像名称
            mouth = "mouth_" + yuri_display.values["mouth"] + "_" + yuri_display.values["head"]
            
            # 构建眉毛图像名称
            eyebrows = "eyebrows_" + yuri_display.values["eyebrows"] + "_" + yuri_display.values["head"]
            
            # 构建脸红效果
            if yuri_display.values["blush"]:
                head_cover_1 = "blush" + "_" + str(yuri_display.values["head"])
            else:
                head_cover_1 = "nothing"
            
            # 构建哭泣效果
            if yuri_display.values["cry"]:
                tears_type = ["open","open","closed","open","squint","squint","happy","open","open","open","squint","open","open","open"]
                if yuri_display.values["eyes"] >= 0 and yuri_display.values["eyes"] < len(tears_type):
                    head_cover_2 = tears_type[yuri_display.values["eyes"]] + "-eyes-crying"
                else:
                    head_cover_2 = "open-eyes-crying"
            else:
                head_cover_2 = "nothing"
            
            # 构建手臂图像名称
            uparms_exist = False
            downarm_both = ""
            uparm_both = ""
            downarm_left = ""
            uparm_left = ""
            downarm_right = ""
            uparm_right = ""
            
            if yuri_display.values["both arms"]:
                downarm_both = "downarm_both_arms_" + str(yuri_display.values["both arms"])
                
                if yuri_display.values["both arms"] == 2:
                    uparms_exist = True
                else:
                    uparm_both = "uparm_both_1"
            else:
                downarm_left = "downarm_left_" + str(yuri_display.values["left arm"])
                uparm_left = "uparm_left_0"
                downarm_right = "downarm_right_" + str(yuri_display.values["right arm"])
                uparm_right = "uparm_right_0"
            
            # 显示表情图像
            # 在JYACS中，我们使用简化的方式显示表情
            # 将表情编码转换为情绪名称，并显示对应的图像
            emotion_name = "jyacs_emotion_" + get_emotion_from_expression()
            renpy.scene()
            renpy.show(emotion_name)
            
            return yuri_display
    
    def base64_to_index(char):
        """将Base64字符转换为索引"""
        base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        try:
            return base64_chars.index(char)
        except ValueError:
            return 0
    
    def show_chr(expression, chr="yuri_sit", position=["t11"]):
        """
        显示指定表情编码的角色
        参数:
            expression: 表情编码字符串，格式为 X-YYYYY-ZZZZ
            chr: 角色名称
            position: 位置列表
        """
        global yuri_sit
        global yuri_stand
        
        # 处理默认表情
        if expression == "default":
            # 默认表情
            expression = "A-ACAAA-AAAA"
        
        # 处理表情编码格式
        if(expression.count('-') == 1):
            expression = 'A-' + expression
        
        if(list(map(lambda x: len(x), expression.split('-'))) != [1, 5, 4]):
            expression = "A-AAAAA-AAAA"
        
        # 解析头部位置
        if expression[0] == "A":
            head = "front"
            yuri_display.head(0)
        elif expression[0] == "B":
            head = "side"
            yuri_display.head(1)
        else:
            head = "front"
            yuri_display.head(0)
        
        # 解析眼睛
        eyes_index = base64_to_index(expression[2])
        yuri_display.eyes(eyes_index)
        
        # 解析嘴巴
        mouth_index = expression[3].lower()
        yuri_display.mouth(mouth_index)
        
        # 解析眉毛
        eyebrows_index = expression[4].lower()
        yuri_display.eyebrows(eyebrows_index)
        
        # 解析脸红
        blush = expression[5] == "B"
        yuri_display.blush(blush)
        
        # 解析哭泣
        cry = expression[6] == "B"
        yuri_display.cry(cry)
        eyes_index = base64_to_index(expression[2])
        
        # 解析嘴巴
        mouth = expression[3].lower()
        
        # 解析眉毛
        eyebrows = expression[4].lower()
        
        # 解析脸红效果
        blush = (expression[5] == "B")
        
        # 解析哭泣效果
        cry = (expression[6] == "B")
        
        # 解析手臂位置
        botharms = False
        if expression[8:10] == "ZZ":
            # 双臂模式
            botharms = True
            both_arms_index = base64_to_index(expression[10])
        else:
            # 单臂模式
            left_arm_index = base64_to_index(expression[9])
            right_arm_index = base64_to_index(expression[11])
        
        # 设置表情状态
        yuri_display.head(0 if head == "front" else 1)
        yuri_display.eyes(eyes_index)
        yuri_display.mouth(mouth)
        yuri_display.eyebrows(eyebrows)
        yuri_display.blush(blush)
        yuri_display.cry(cry)
        
        if botharms:
            yuri_display.both_arms(both_arms_index)
        else:
            yuri_display.left_arm(left_arm_index)
            yuri_display.right_arm(right_arm_index)
        
        # 显示表情
        yuri_display.show()
        
        return expression
    
    def get_emotion_from_expression():
        """根据当前表情状态返回对应的情绪名称"""
        # 眼睛索引
        eyes = yuri_display.values["eyes"]
        # 嘴巴类型
        mouth = yuri_display.values["mouth"]
        # 眉毛类型
        eyebrows = yuri_display.values["eyebrows"]
        # 是否脸红
        blush = yuri_display.values["blush"]
        # 是否哭泣
        cry = yuri_display.values["cry"]
        
        # 根据表情组合返回情绪名称
        if eyes in [0, 1] and mouth == "a" and eyebrows == "a":
            return "normal"  # 中性/平静表情
        elif eyes in [2, 3] and mouth == "a" and eyebrows == "b":
            return "think_and_interested"  # 思考/感兴趣
        elif eyes in [7, 8, 9] and mouth in ["c", "f"] and eyebrows == "a":
            return "happy"  # 开心/高兴
        elif eyes in [4, 5, 6] and mouth in ["g", "f"] and eyebrows == "a":
            return "relaxing_and_happy"  # 放松且开心
        elif eyes in [10, 11] and mouth == "b" and eyebrows == "a" and blush:
            return "kind"  # 温柔/友善
        elif eyes in [2, 3] and mouth in ["b", "c"] and eyebrows in ["a", "e"] and not blush:
            return "think_and_a_little_worry"  # 思考且略微担忧
        elif eyes in [4, 5] and mouth in ["a", "b"] and eyebrows in ["a", "l"] and not cry:
            return "a_little_sad"  # 轻微悲伤
        elif eyes in [6, 7, 8] and mouth in ["a", "b"] and eyebrows in ["a", "b"] and cry:
            return "sad"  # 悲伤
        elif eyes in [9, 10] and mouth in ["c", "b"] and eyebrows == "b" and blush:
            return "unhappy"  # 不开心/生气
        elif eyes in [0, 1] and mouth == "a" and eyebrows in ["a", "b"]:
            return "relaxed"  # 放松
        else:
            return "normal"  # 默认为中性表情

# 创建全局表情管理器实例
init python:
    if not hasattr(store, 'jyacs_expression_manager'):
        store.jyacs_expression_manager = yuri_display

# 注册表情图像到Renpy (已废弃 - 不再需要预定义图片)
# 新系统使用JUSTYURI表情编码动态组合表情，不再使用静态图片
# init -1100:
#     # 基本表情
#     image jyacs_emotion_normal = Transform("mod_assets/images/expressions/normal.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_happy = Transform("mod_assets/images/expressions/happy.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_sad = Transform("mod_assets/images/expressions/sad.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_relaxed = Transform("mod_assets/images/expressions/relaxed.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_kind = Transform("mod_assets/images/expressions/kind.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_a_little_sad = Transform("mod_assets/images/expressions/a_little_sad.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_think_and_interested = Transform("mod_assets/images/expressions/think_and_interested.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_think_and_a_little_worry = Transform("mod_assets/images/expressions/think_and_a_little_worry.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_relaxing_and_happy = Transform("mod_assets/images/expressions/relaxing_and_happy.png", size=(1280, 720), yalign=1.0)
#     image jyacs_emotion_unhappy = Transform("mod_assets/images/expressions/unhappy.png", size=(1280, 720), yalign=1.0)

# 辅助函数
init python:
    def jyacs_show_emotion_from_text(text):
        """从文本分析并显示表情的便捷函数"""
        expression = get_expression_from_text(text)
        show_chr(expression)
        return get_emotion_from_expression()
    
    def get_expression_from_text(text):
        """根据文本内容分析并返回JUSTYURI表情编码
        
        该函数扫描输入文本中的情绪关键词，并返回对应的JUSTYURI表情编码。
        表情编码格式为 X-YYYYY-ZZZZ，其中：
        - X: 头部位置 (A=正面, B=侧面)
        - YYYYY: 眼睛、嘴巴、眉毛、脸红、哭泣的编码
        - ZZZZ: 手臂位置编码
        
        Args:
            text (str): 要分析的文本内容
            
        Returns:
            str: JUSTYURI表情编码，格式为 X-YYYYY-ZZZZ
                 如果没有匹配到关键词，返回默认中性表情 "A-ACAAA-AAAA"
        
        Examples:
            >>> get_expression_from_text("我很开心！")
            "A-CFGAA-AIAI"
            >>> get_expression_from_text("让我想想...")
            "A-BFAAA-AAAC"
            >>> get_expression_from_text("这是普通的对话")
            "A-ACAAA-AAAA"
        """
        # 输入验证
        if not text or not isinstance(text, (str, unicode)):
            return "A-ACAAA-AAAA"
        
        # 限制文本长度，防止性能问题
        if len(text) > 10000:
            text = text[:10000]
        
        # 默认表情编码（中性/平静）
        default_expression = "A-ACAAA-AAAA"
        
        # 关键词到表情编码的映射
        # 注意：这些映射基于JUSTYURI的表情系统
        keyword_to_expression = {
            # 积极情绪 - 开心/高兴
            '开心': "A-CFGAA-AIAI",
            '高兴': "A-CFGAA-AIAI", 
            '快乐': "A-CFGAA-AIAI",
            
            # 积极情绪 - 愉快/兴奋
            '愉快': "A-GCBAA-AEAB",
            '兴奋': "A-GCBAA-AEAB",
            '幸福': "A-GCBAA-AEAB",
            
            # 积极情绪 - 喜欢/可爱
            '喜欢': "A-CABBA-ALAL",
            '可爱': "A-CABBA-ALAL",
            
            # 温柔情绪
            '爱': "A-CABBA-AMAM",
            '温柔': "A-CABBA-AMAM",
            '亲切': "A-CABBA-AMAM",
            
            # 中性/思考
            '思考': "A-BFAAA-AAAC",
            '想': "A-BFAAA-AAAC",
            '考虑': "A-BFAAA-AAAC",
            '觉得': "A-BFAAA-AAAC",
            '认为': "A-BFAAA-AAAC",
            
            # 担心/忧虑
            '担心': "A-AFBAA-ALAA",
            '忧虑': "A-AFBAA-ALAA",
            
            # 轻微消极
            '有点': "A-HECAA-AEAB",
            '稍微': "A-HECAA-AEAB",
            '一点点': "A-HECAA-AEAB",
            
            # 悲伤情绪
            '难过': "A-DGFAA-ABAB",
            '伤心': "A-DGFAA-ABAB",
            '悲伤': "A-DGFAA-ABAB",
            '沮丧': "A-DGFAA-ABAB",
            '失望': "A-DGFAA-ABAB",
            
            # 害怕/恐惧
            '害怕': "A-KFCAA-ABAB",
            '恐惧': "A-KFCAA-ABAB",
            
            # 强烈消极 - 生气
            '生气': "A-HCBBA-ABAB",
            '愤怒': "A-HCBBA-ABAB",
            '恼火': "A-HCBBA-ABAB",
            '讨厌': "A-HCBBA-ABAB",
            '不喜欢': "A-HCBBA-ABAB",
            
            # 惊讶/震惊
            '惊讶': "A-ICAAA-ALAL",
            '震惊': "A-ICAAA-ALAL",
            '意外': "A-ICAAA-ALAL",
            
            # 平静/中性
            '平静': "A-ACAAA-AAAA",
            '安心': "A-ACAAA-AAAA",
            '舒服': "A-ACAAA-AAAA",
            '轻松': "A-ACAAA-AAAA"
        }
        
        try:
            # 检查文本中是否包含关键词
            for keyword, expression in keyword_to_expression.items():
                if keyword in text:
                    return expression
        except Exception as e:
            # 如果发生任何错误，记录并返回默认表情
            print(u"[JYACS] 表情分析出错: {}".format(e))
            return default_expression
        
        # 如果没有匹配到关键词，返回默认表情
        return default_expression
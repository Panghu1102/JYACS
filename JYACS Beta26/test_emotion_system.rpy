# test_emotion_system.rpy - 表情背景系统测试
# 用于验证表情背景系统是否正常工作（全屏背景版本）

label test_emotion_images:
    scene black  # 先清空背景
    
    "现在开始测试表情背景系统..."
    
    "测试1: 开心情绪"
    show jyacs_emotion_happy at truecenter
    "显示开心背景"
    
    "测试2: 悲伤情绪"
    show jyacs_emotion_sad at truecenter
    "显示悲伤背景"
    
    "测试3: 思考情绪"
    show jyacs_emotion_think_and_interested at truecenter
    "显示思考背景"
    
    "测试4: 正常情绪"
    show jyacs_emotion_normal at truecenter
    "显示正常背景"
    
    "测试5: 放松情绪"
    show jyacs_emotion_relaxed at truecenter
    "显示放松背景"
    
    "测试6: 通过文本自动识别"
    python:
        test_text = "我今天真的很开心，见到你让我感到快乐！"
        emotion = store.jyacs_emotion_image_manager.analyze_text_for_emotion(test_text)
        # 将空格替换为下划线用于显示
        display_emotion = emotion.replace(" ", "_")
    
    "文本: [test_text]"
    "检测到情绪: [emotion]"
    show expression "jyacs_emotion_{}".format(display_emotion) at truecenter
    "显示对应背景"
    
    "表情背景系统测试完成！"
    
    return
# JYACS 表情背景系统使用指南

## 概述

JYACS现在支持基于AI回复内容的关键词自动切换**全屏背景**图片。系统会根据AI回复中的情绪关键词，从`mod_assets/images/emotins/`文件夹中选择合适的表情背景图片。

## 文件结构

```
mod_assets/images/emotins/
├── happy.png              # 开心/高兴背景
├── sad.png                # 悲伤/难过背景
├── normal.png             # 正常背景
├── normal2.png            # 正常背景变体2
├── normal3.png            # 正常背景变体3
├── relaxed.png            # 放松背景
├── kind.png               # 温柔/亲切背景
├── a little sad.png       # 轻微悲伤背景
├── think and interested.png  # 思考且感兴趣背景
├── think and a little worry.png  # 思考且轻微担心背景
├── relaxing and happy.png # 放松且开心背景
└── unhappy.png            # 不开心/生气背景
```

## 关键词映射

系统会根据以下关键词自动选择背景：

### 积极情绪
- **happy.png**: "开心", "高兴", "快乐", "愉快", "兴奋", "幸福", "喜欢", "可爱"
- **kind.png**: "爱", "温柔", "亲切"
- **relaxing and happy.png**: "开心又放松", "愉快又轻松"

### 中性/思考情绪
- **think and interested.png**: "思考", "想", "考虑", "觉得", "认为"
- **think and a little worry.png**: "可能", "担心", "忧虑"

### 消极情绪
- **sad.png**: "难过", "伤心", "悲伤", "沮丧", "失望", "害怕", "恐惧"
- **a little sad.png**: "有点", "稍微", "一点点"
- **unhappy.png**: "生气", "愤怒", "恼火", "讨厌", "不喜欢"

### 放松状态
- **relaxed.png**: "放松", "平静", "安心", "舒服", "轻松"

## 使用方式

### 自动使用
系统在AI回复时会自动分析文本并选择合适的**全屏背景**图片。如果没有匹配到任何关键词，会从`normal.png`, `normal2.png`, `normal3.png`中随机选择一个。

### 手动测试
可以使用以下代码测试系统：

```renpy
# 测试特定文本的情绪识别
$ emotion = jyacs_show_emotion_from_text("我今天真的很开心！")
"检测到情绪: [emotion]"

# 显示特定表情背景（注意空格替换为下划线）
show jyacs_emotion_happy at truecenter
show jyacs_emotion_sad at truecenter
show jyacs_emotion_think_and_interested at truecenter
```

### 背景显示说明
表情图片现在作为**全屏背景**显示，而不是角色立绘。使用以下格式：

```renpy
show jyacs_emotion_[表情名] at truecenter
```

如果表情名包含空格，显示时需要将空格替换为下划线：
- `think and interested` → `show jyacs_emotion_think_and_interested at truecenter`
- `a little sad` → `show jyacs_emotion_a_little_sad at truecenter`

## 自定义背景

要添加新的表情背景图片：

1. 将PNG格式的图片放入`mod_assets/images/emotins/`目录
2. 文件名应该描述情绪状态（如"excited.png"）
3. 图片应该与游戏分辨率匹配（全屏背景）
4. 在`jyacs_emotion_images.rpy`中的`keyword_to_emotion`字典添加对应的关键词映射

## 故障排除

如果表情背景不显示：
1. 检查图片文件是否存在于指定目录
2. 确认图片格式为PNG
3. 检查图片分辨率是否与游戏分辨率匹配
4. 查看游戏日志获取错误信息
5. 使用测试脚本验证系统是否正常工作

## 配置文件

可以在`jyacs_config.json`中配置表情系统：
```json
{
    "emotion": {
        "enable": true,
        "default_emotion": "normal",
        "use_image_emotions": true,
        "emotions_path": "mod_assets/images/emotins",
        "fallback_emotion": "normal"
    }
}
```
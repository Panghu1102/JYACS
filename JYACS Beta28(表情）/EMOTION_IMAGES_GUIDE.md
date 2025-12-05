# JYACS 表情图片系统使用指南

## 概述

JYACS现在支持基于AI回复内容的关键词自动切换优里的立绘背景图片。系统会根据AI回复中的情绪关键词，从`mod_assets/images/emotins/`文件夹中选择合适的表情图片。

## 文件结构

```
mod_assets/images/emotins/
├── happy.png              # 开心/高兴
├── sad.png                # 悲伤/难过
├── normal.png             # 正常状态
├── normal2.png            # 正常状态变体2
├── normal3.png            # 正常状态变体3
├── relaxed.png            # 放松状态
├── kind.png               # 温柔/亲切
├── a little sad.png       # 轻微悲伤
├── think and interested.png  # 思考且感兴趣
├── think and a little worry.png  # 思考且轻微担心
├── relaxing and happy.png # 放松且开心
└── unhappy.png            # 不开心/生气
```

## 关键词映射

系统会根据以下关键词自动选择表情：

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
系统在AI回复时会自动分析文本并选择合适的表情图片。如果没有匹配到任何关键词，会从`normal.png`, `normal2.png`, `normal3.png`中随机选择一个。

### 手动测试
可以使用以下代码测试系统：

```renpy
# 测试特定文本的情绪识别
$ emotion = jyacs_show_emotion_from_text("我今天真的很开心！")
"检测到情绪: [emotion]"

# 显示特定表情
show yuri happy
show yuri sad
show yuri think_and_interested
```

## 自定义表情

要添加新的表情图片：

1. 将PNG格式的图片放入`mod_assets/images/emotins/`目录
2. 文件名应该描述情绪状态（如"excited.png"）
3. 在`jyacs_emotion_images.rpy`中的`keyword_to_emotion`字典添加对应的关键词映射

## 故障排除

如果表情图片不显示：
1. 检查图片文件是否存在于指定目录
2. 确认图片格式为PNG
3. 检查文件名是否包含特殊字符
4. 查看游戏日志获取错误信息
5. 使用测试脚本验证系统是否正常工作

## 配置文件

可以在`jyacs_config.json`中配置表情系统：
```json
{
    "emotion": {
        "enable": true,
        "default_emotion": "normal",
        "use_image_emotions": true
    }
}
```
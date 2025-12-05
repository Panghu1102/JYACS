# Design Document

## Overview

本设计文档描述如何将JYACS项目中的两套表情系统合并为一套统一的JUSTYURI表情编码系统。设计目标是废弃旧的图片表情系统，让所有表情显示都通过表情编码系统实现，同时保持代码的可维护性和性能。

## Architecture

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Response Text                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         analyze_text_for_expression(text)                    │
│         - 关键词扫描                                          │
│         - 情绪识别                                            │
│         - 表情编码映射                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
              Expression Code (X-YYYYY-ZZZZ)
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              show_chr(expression_code)                       │
│              - 解析编码                                       │
│              - 设置yuri_display状态                          │
│              - 显示组合表情                                   │
└─────────────────────────────────────────────────────────────┘
```

### 数据流

1. **输入**: AI返回的文本内容
2. **处理**: 文本分析 → 关键词匹配 → 表情编码生成
3. **输出**: JUSTYURI表情编码
4. **显示**: 编码解析 → 表情组件组合 → Renpy显示

## Components and Interfaces

### 1. 表情分析模块 (jyacs_expressions.rpy)

#### 新增函数: analyze_text_for_expression()

```python
def analyze_text_for_expression(text):
    """
    分析文本内容，返回对应的JUSTYURI表情编码
    
    Args:
        text (str): 要分析的文本内容
        
    Returns:
        str: JUSTYURI表情编码，格式为 X-YYYYY-ZZZZ
    """
    # 实现逻辑见下文
```

**功能**:
- 扫描文本中的情绪关键词
- 根据关键词优先级和权重选择最合适的表情
- 返回标准的JUSTYURI表情编码

**关键词映射表** (基于现有代码 `get_expression_from_text()`):

| 情绪类型 | 关键词 | 表情编码 | 编码解析 |
|---------|--------|---------|---------|
| 开心/高兴 | 开心、高兴、快乐 | A-CFGAA-AIAI | eyes=2, mouth=g, eyebrows=a |
| 愉快/兴奋 | 愉快、兴奋、幸福 | A-GCBAA-AEAB | eyes=6, mouth=b, eyebrows=a |
| 喜欢/可爱 | 喜欢、可爱 | A-CABBA-ALAL | eyes=2, mouth=b, blush=B |
| 温柔/爱 | 爱、温柔、亲切 | A-CABBA-AMAM | eyes=2, mouth=b, blush=B |
| 思考 | 思考、想、考虑、觉得、认为 | A-BFAAA-AAAC | eyes=1, mouth=a |
| 担心/忧虑 | 担心、忧虑 | A-AFBAA-ALAA | eyes=0, mouth=b, eyebrows=a |
| 轻微消极 | 有点、稍微、一点点 | A-HECAA-AEAB | eyes=7, mouth=c, eyebrows=a |
| 悲伤 | 难过、伤心、悲伤、沮丧、失望 | A-DGFAA-ABAB | eyes=3, mouth=g, cry=B |
| 害怕/恐惧 | 害怕、恐惧 | A-KFCAA-ABAB | eyes=10, mouth=c, cry=B |
| 生气/愤怒 | 生气、愤怒、恼火、讨厌、不喜欢 | A-HCBBA-ABAB | eyes=7, mouth=b, blush=B, cry=B |
| 惊讶/震惊 | 惊讶、震惊、意外 | A-ICAAA-ALAL | eyes=8, mouth=a, eyebrows=a |
| 平静/放松 | 平静、安心、舒服、轻松 | A-ACAAA-AAAA | 默认中性表情 |

**编码说明**:
- 位置1 (X): A=正面, B=侧面
- 位置2 (Y1): 眼睛索引 (Base64: A=0, B=1, C=2, ..., K=10)
- 位置3 (Y2): 嘴巴类型 (a-z)
- 位置4 (Y3): 眉毛类型 (a-z)
- 位置5 (Y4): 脸红 (A=无, B=有)
- 位置6 (Y5): 哭泣 (A=无, B=有)
- 位置7-10 (ZZZZ): 手臂位置 (默认AAAA)

#### 修改函数: get_expression_from_text()

**当前问题**: 该函数已存在但映射不完整，需要重构。

**解决方案**: 
- 保留该函数作为向后兼容
- 内部调用新的analyze_text_for_expression()
- 或直接重构该函数的实现

### 2. API核心模块 (jyacs_api.rpy)

#### 修改: JyacsAi.chat() 方法

**当前代码**:
```python
# 使用新的图片表情系统
if hasattr(store, 'jyacs_emotion_image_manager'):
    emote = store.jyacs_emotion_image_manager.analyze_text_for_emotion(reply)
else:
    emote = "normal"  # 默认表情

self.message_queue.append((emote, reply))
```

**修改后**:
```python
# 使用JUSTYURI表情编码系统
if hasattr(store, 'analyze_text_for_expression'):
    expression_code = store.analyze_text_for_expression(reply)
else:
    expression_code = "A-ACAAA-AAAA"  # 默认表情编码

self.message_queue.append((expression_code, reply))
```

**变更点**:
1. 移除对jyacs_emotion_image_manager的依赖
2. 调用analyze_text_for_expression()获取表情编码
3. 消息队列存储表情编码而不是情绪名称

### 3. 主聊天循环 (jyacs_main.rpy)

#### 修改: submod_jyacs_talking 标签

**当前代码**:
```python
# 使用新的图片表情系统 - 显示为全屏背景
emotion_name = message[0]
display_name = emotion_name.replace(" ", "_")
# 先隐藏当前背景，再显示新的表情背景
renpy.scene()
renpy.show("jyacs_emotion_{}".format(display_name))
```

**修改后**:
```python
# 使用JUSTYURI表情编码系统
expression_code = message[0]
# 显示表情
show_chr(expression_code)
```

**变更点**:
1. 移除renpy.scene()和renpy.show()调用
2. 直接调用show_chr()函数显示表情
3. 表情编码自动解析和显示

#### 修改: show_expression() 函数

**当前实现**: 已经支持DDLC到JUSTYURI的转换，保持不变。

**确保**: 该函数继续正常工作，用于兼容性。

### 4. 废弃模块处理

#### jyacs_emotion_images.rpy

**处理方案**:
1. 在文件顶部添加废弃警告注释
2. 保留文件但不再使用
3. 移除对JyacsEmotionImageManager的实例化

**添加注释**:
```python
# ============================================
# 警告: 此文件已废弃
# 该图片表情系统已被JUSTYURI表情编码系统取代
# 保留此文件仅用于向后兼容
# 请勿在新代码中使用此模块
# ============================================
```

#### 移除图片注册代码

**位置**: jyacs_expressions.rpy 和 jyacs_emotion_images.rpy 的 init -1100 块

**处理**: 
- 注释掉或删除所有 `image jyacs_emotion_xxx` 的定义
- 这些图片不再需要，因为使用组合式表情

## Data Models

### 表情编码数据结构

```python
# 表情编码字符串格式
expression_code = "X-YYYYY-ZZZZ"

# 示例
"A-HFCAA-AAAA"  # 开心表情
"A-KABBA-AAAA"  # 温柔表情
"A-DGFAB-AAAA"  # 悲伤表情
```

### 关键词映射数据结构

**注意**: 以下映射来自现有代码 `get_expression_from_text()` 函数，保持与原有逻辑一致。

```python
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
```

### 消息队列数据结构

```python
# 修改前
message_queue = [
    ("happy", "我很开心！"),
    ("sad", "我有点难过..."),
]

# 修改后
message_queue = [
    ("A-HFCAA-AAAA", "我很开心！"),
    ("A-DGFAB-AAAA", "我有点难过..."),
]
```

## Error Handling

### 1. 表情编码无效

**场景**: analyze_text_for_expression() 返回无效编码

**处理**:
```python
def show_chr(expression, chr="yuri_sit", position=["t11"]):
    try:
        # 验证编码格式
        if not expression or not isinstance(expression, str):
            expression = "A-ACAAA-AAAA"
        
        # 处理默认表情
        if expression == "default":
            expression = "A-ACAAA-AAAA"
        
        # 验证编码格式
        if expression.count('-') == 1:
            expression = 'A-' + expression
        
        if list(map(lambda x: len(x), expression.split('-'))) != [1, 5, 4]:
            expression = "A-ACAAA-AAAA"
        
        # 继续处理...
    except Exception as e:
        # 记录错误并使用默认表情
        store.jyacs_log("表情编码解析失败: {}".format(e), "ERROR")
        expression = "A-ACAAA-AAAA"
```

### 2. 关键词匹配失败

**场景**: 文本中没有任何情绪关键词

**处理**:
```python
def analyze_text_for_expression(text):
    # ... 关键词匹配逻辑 ...
    
    # 如果没有匹配到任何关键词
    if not matched:
        return "A-ACAAA-AAAA"  # 返回默认中性表情
```

### 3. 函数不存在

**场景**: analyze_text_for_expression 函数未定义

**处理**:
```python
# 在 jyacs_api.rpy 中
if hasattr(store, 'analyze_text_for_expression'):
    expression_code = store.analyze_text_for_expression(reply)
else:
    expression_code = "A-ACAAA-AAAA"
    store.jyacs_log("表情分析函数不存在，使用默认表情", "WARNING")
```

### 4. 多个关键词冲突

**场景**: 文本中包含多个不同情绪的关键词

**处理策略**:
1. 使用情绪优先级（强烈情绪 > 轻微情绪）
2. 使用情绪权重（负面情绪权重更高）
3. 选择第一个匹配的关键词

```python
# 情绪优先级定义
emotion_priority = {
    'angry': 10,      # 生气（最高优先级）
    'sad': 9,         # 悲伤
    'worried': 8,     # 担心
    'surprised': 7,   # 惊讶
    'happy': 6,       # 开心
    'kind': 5,        # 温柔
    'thinking': 4,    # 思考
    'relaxed': 3,     # 放松
    'neutral': 1      # 中性（最低优先级）
}
```

## Testing Strategy

### 1. 单元测试

**测试函数**: analyze_text_for_expression()

```python
# 测试用例
test_cases = [
    ("我很开心！", "A-HFCAA-AAAA"),
    ("我有点难过...", "A-DGFAB-AAAA"),
    ("让我想想...", "A-CFAAA-AAAA"),
    ("我很担心你", "A-CFBAA-AAAA"),
    ("这是普通的对话", "A-ACAAA-AAAA"),
]

for text, expected in test_cases:
    result = analyze_text_for_expression(text)
    assert result == expected, f"Failed: {text} -> {result} (expected {expected})"
```

### 2. 集成测试

**测试场景**: 完整的对话流程

1. 启动聊天
2. 发送包含情绪关键词的消息
3. 验证AI回复后表情正确显示
4. 验证表情切换流畅

### 3. 回归测试

**确保不破坏现有功能**:

1. MoodStatus (JyacsEmoSelector) 仍然工作
2. show_expression() 函数仍然工作
3. DDLC风格表情代码转换正常
4. 聊天功能正常运行

### 4. 边界测试

**测试边界情况**:

1. 空文本
2. 超长文本
3. 特殊字符
4. 多语言文本
5. 无效编码

## Performance Considerations

### 1. 关键词匹配优化

**当前方案**: 遍历所有关键词

**优化方案**:
- 使用字典查找而不是列表遍历
- 预编译正则表达式
- 缓存常见文本的结果

```python
# 优化示例
import re

# 预编译正则表达式
emotion_patterns = {
    'happy': re.compile(r'开心|高兴|快乐|愉快|兴奋|幸福'),
    'sad': re.compile(r'难过|伤心|悲伤|沮丧|失望'),
    # ...
}

def analyze_text_for_expression(text):
    for emotion, pattern in emotion_patterns.items():
        if pattern.search(text):
            return emotion_to_expression[emotion]
    return "A-ACAAA-AAAA"
```

### 2. 表情显示性能

**考虑因素**:
- show_chr() 函数的执行时间
- Renpy图像加载时间
- 表情切换的流畅度

**优化**:
- 预加载常用表情组件
- 避免不必要的renpy.scene()调用
- 使用Transform缓存

## Migration Plan

### 阶段1: 准备工作
1. 备份现有代码
2. 创建测试用例
3. 文档化当前行为

### 阶段2: 实现新功能
1. 实现analyze_text_for_expression()
2. 更新JyacsAi.chat()
3. 更新主聊天循环

### 阶段3: 清理废弃代码
1. 标记jyacs_emotion_images.rpy为废弃
2. 移除图片注册代码
3. 移除对jyacs_emotion_image_manager的引用

### 阶段4: 测试验证
1. 运行单元测试
2. 运行集成测试
3. 手动测试对话流程

### 阶段5: 部署
1. 合并代码
2. 更新文档
3. 发布新版本

## Backward Compatibility

### 保留的功能

1. **show_expression()**: 继续支持DDLC风格表情代码
2. **MoodStatus**: JyacsEmoSelector继续工作
3. **show_chr()**: 保持API不变

### 废弃的功能

1. **JyacsEmotionImageManager**: 不再使用
2. **jyacs_emotion_image_manager**: 全局实例移除
3. **预定义表情图片**: 不再注册

### 迁移指南

如果有外部代码依赖旧系统:

```python
# 旧代码
emotion = jyacs_emotion_image_manager.analyze_text_for_emotion(text)
jyacs_emotion_image_manager.show_emotion_image(emotion)

# 新代码
expression = analyze_text_for_expression(text)
show_chr(expression)
```

## Security Considerations

### 输入验证

```python
def analyze_text_for_expression(text):
    # 验证输入
    if not text or not isinstance(text, (str, unicode)):
        return "A-ACAAA-AAAA"
    
    # 限制文本长度，防止性能问题
    if len(text) > 10000:
        text = text[:10000]
    
    # 继续处理...
```

### 编码验证

```python
def show_chr(expression, chr="yuri_sit", position=["t11"]):
    # 验证编码格式，防止注入攻击
    if not re.match(r'^[AB]-[A-Za-z]{5}-[A-Za-z]{4}$', expression):
        expression = "A-ACAAA-AAAA"
    
    # 继续处理...
```

## Future Enhancements

### 1. 动态表情生成

根据文本情感强度动态调整表情参数。

### 2. 表情动画

添加表情切换的过渡动画。

### 3. 上下文感知

根据对话历史选择更合适的表情。

### 4. 机器学习

使用ML模型进行更准确的情感分析。

### 5. 自定义表情

允许用户自定义关键词到表情的映射。

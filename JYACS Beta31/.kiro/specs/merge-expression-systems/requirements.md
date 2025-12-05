# Requirements Document

## Introduction

本需求文档描述了将JYACS项目中的两套表情系统合并的需求。当前项目存在两套并行的表情系统：
1. JUSTYURI表情编码系统（基于编码的组合式表情系统）
2. 图片表情系统（基于预定义图片的简单系统）

目标是以JUSTYURI表情编码系统为主，废弃旧的图片表情系统，让所有情绪关键词映射到表情编码，由编码系统统一处理表情显示。

## Requirements

### Requirement 1: 统一表情系统架构

**User Story:** 作为开发者，我希望项目只使用一套表情系统（JUSTYURI编码系统），以便代码更清晰、维护更简单。

#### Acceptance Criteria

1. WHEN 系统初始化 THEN 只加载JUSTYURI表情编码系统，不再初始化JyacsEmotionImageManager
2. WHEN AI返回文本 THEN 系统使用关键词映射到表情编码，而不是情绪图片名称
3. WHEN 显示表情 THEN 使用show_chr()函数和表情编码，而不是显示预定义图片
4. IF 代码中存在对jyacs_emotion_image_manager的引用 THEN 应该被移除或重构

### Requirement 2: 关键词到表情编码的映射

**User Story:** 作为系统，我需要将文本中的情绪关键词映射到JUSTYURI表情编码，以便正确显示角色表情。

#### Acceptance Criteria

1. WHEN 分析包含情绪关键词的文本 THEN 系统返回对应的JUSTYURI表情编码（格式：X-YYYYY-ZZZZ）
2. WHEN 关键词为"开心"、"高兴"、"快乐" THEN 返回开心表情编码
3. WHEN 关键词为"难过"、"伤心"、"悲伤" THEN 返回悲伤表情编码
4. WHEN 关键词为"思考"、"想"、"考虑" THEN 返回思考表情编码
5. WHEN 关键词为"担心"、"忧虑" THEN 返回担忧表情编码
6. WHEN 关键词为"温柔"、"亲切"、"爱" THEN 返回温柔表情编码
7. WHEN 关键词为"生气"、"愤怒" THEN 返回生气表情编码
8. WHEN 关键词为"惊讶"、"震惊" THEN 返回惊讶表情编码
9. WHEN 关键词为"放松"、"轻松" THEN 返回放松表情编码
10. WHEN 没有匹配到任何关键词 THEN 返回默认中性表情编码（A-ACAAA-AAAA）

### Requirement 3: 重构JyacsAi类的表情处理

**User Story:** 作为JyacsAi类，我需要在收到AI回复后，使用表情编码系统而不是图片系统来处理表情。

#### Acceptance Criteria

1. WHEN JyacsAi.chat()方法收到AI回复 THEN 调用表情分析函数获取表情编码
2. WHEN 表情编码获取成功 THEN 将编码添加到消息队列（而不是情绪名称）
3. WHEN 消息队列返回消息 THEN 返回格式为(expression_code, text)的元组
4. IF 表情分析失败 THEN 使用默认表情编码"A-ACAAA-AAAA"

### Requirement 4: 更新主聊天循环的表情显示

**User Story:** 作为主聊天循环，我需要使用show_chr()函数显示表情编码，而不是显示预定义的图片。

#### Acceptance Criteria

1. WHEN 从消息队列获取消息 THEN 提取表情编码（第一个元素）
2. WHEN 显示表情 THEN 调用show_chr(expression_code)而不是renpy.show("jyacs_emotion_xxx")
3. WHEN show_chr()执行 THEN 正确解析编码并显示对应的组合表情
4. WHEN 显示对话文本 THEN 在表情显示后正常显示文本内容

### Requirement 5: 清理废弃代码

**User Story:** 作为开发者，我希望移除所有与旧图片表情系统相关的废弃代码，保持代码库整洁。

#### Acceptance Criteria

1. WHEN 重构完成 THEN jyacs_emotion_images.rpy文件应该被标记为废弃或删除
2. WHEN 检查代码 THEN 不应存在对JyacsEmotionImageManager的实例化
3. WHEN 检查代码 THEN 不应存在对jyacs_emotion_image_manager的调用
4. WHEN 检查图片注册 THEN 移除init -1100中的旧表情图片注册代码
5. IF 需要保留向后兼容性 THEN 添加注释说明这些代码已废弃

### Requirement 6: 创建统一的表情分析函数

**User Story:** 作为系统，我需要一个统一的函数来分析文本并返回表情编码，以便在各处调用。

#### Acceptance Criteria

1. WHEN 创建函数analyze_text_for_expression(text) THEN 函数接受文本参数
2. WHEN 函数执行 THEN 扫描文本中的情绪关键词
3. WHEN 找到关键词 THEN 返回对应的JUSTYURI表情编码
4. WHEN 找到多个关键词 THEN 根据优先级或权重选择最合适的表情
5. WHEN 没有找到关键词 THEN 返回默认表情编码
6. WHEN 函数被调用 THEN 性能应该足够快，不影响对话流畅度

### Requirement 7: 保持与现有代码的兼容性

**User Story:** 作为系统，我需要确保重构后的代码与现有的其他模块兼容，不破坏现有功能。

#### Acceptance Criteria

1. WHEN 重构完成 THEN MoodStatus（JyacsEmoSelector）仍然正常工作
2. WHEN 调用show_expression(emote) THEN DDLC风格代码仍能转换为JUSTYURI编码
3. WHEN 系统初始化 THEN 所有表情相关的全局变量正确初始化
4. WHEN 运行聊天功能 THEN 不应出现AttributeError或其他错误
5. IF 存在其他模块依赖旧系统 THEN 提供适配层或迁移指南

### Requirement 8: 测试和验证

**User Story:** 作为QA，我需要验证新的表情系统能正确工作，所有情绪都能正确显示。

#### Acceptance Criteria

1. WHEN 输入包含"开心"的文本 THEN 显示开心表情
2. WHEN 输入包含"难过"的文本 THEN 显示悲伤表情
3. WHEN 输入包含"思考"的文本 THEN 显示思考表情
4. WHEN 输入不包含情绪关键词的文本 THEN 显示默认中性表情
5. WHEN 连续对话 THEN 表情能正确切换
6. WHEN 表情编码无效 THEN 系统应该优雅降级到默认表情
7. WHEN 运行完整对话流程 THEN 不应出现崩溃或错误

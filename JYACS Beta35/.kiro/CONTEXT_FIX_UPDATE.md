# 对话上下文保持修复 - 更新

## 🎯 问题

之前的修复虽然解决了卡死问题，但引入了新问题：**每轮对话都是全新的开始，AI 不记得之前的对话内容**。

## 🔍 根本原因

在 `jyacs_api.rpy` 的 `chat()` 方法中，每次发送消息时只包含：
1. 系统提示
2. 当前用户消息

**没有包含对话历史**，导致 AI 无法保持上下文。

## 🛠️ 修复方案

### 1. 添加对话历史管理

在 `JyacsAi` 类中添加对话历史变量：

```python
# 对话历史管理
self.conversation_history = []  # 存储对话历史
self.max_history_length = 20  # 最多保留 20 轮对话（40 条消息）
```

### 2. 在发送消息时包含历史

修改 `chat()` 方法，在构建消息数组时添加历史：

```python
# 构建消息数组
messages = []

# 1. 系统提示
messages.append({"role": "system", "content": self.system_prompt})

# 2. 对话历史（保持上下文）
if self.conversation_history:
    messages.extend(self.conversation_history)
    
# 3. 当前用户消息
user_content = self.user_prompt_template.format(message=message)
messages.append({"role": "user", "content": user_content})
```

### 3. 在收到响应后保存历史

在收到 API 响应后，将本轮对话添加到历史：

```python
# 将本轮对话添加到历史中
self.conversation_history.append({"role": "user", "content": user_content})
self.conversation_history.append({"role": "assistant", "content": reply})

# 限制历史长度，避免超出 token 限制
if len(self.conversation_history) > self.max_history_length * 2:
    self.conversation_history = self.conversation_history[2:]
```

### 4. 在对话结束时清空历史

添加 `clear_conversation_history()` 方法，并在对话结束时调用：

```python
def clear_conversation_history(self):
    """清空对话历史（当用户退出对话时调用）"""
    history_length = len(self.conversation_history)
    self.conversation_history = []
    self.content_func("对话历史已清空（共 {} 条消息）".format(history_length), "INFO")
    return history_length
```

在 `label submod_jyacs_talking.end` 中调用：

```python
python:
    # 清空对话历史（对话会话结束）
    if hasattr(store.jyacs, 'clear_conversation_history'):
        cleared_count = store.jyacs.clear_conversation_history()
        store.jyacs_log("对话会话结束，已清空 {} 条历史消息".format(cleared_count), "INFO")
```

## 📊 修改的文件

### 1. jyacs_api.rpy

**修改位置 1**：`__init__` 方法（第 83-88 行）
- 添加 `conversation_history` 列表
- 添加 `max_history_length` 配置

**修改位置 2**：`chat()` 方法（第 330-340 行）
- 在构建消息数组时添加对话历史

**修改位置 3**：`chat()` 方法（第 380-395 行）
- 在收到响应后保存对话历史
- 限制历史长度

**修改位置 4**：`close_wss_session()` 方法后（第 295-300 行）
- 添加 `clear_conversation_history()` 方法

### 2. jyacs_main.rpy

**修改位置**：`label submod_jyacs_talking.end`（第 552-560 行）
- 在对话结束时清空对话历史

## ✅ 修复效果

### 修复前
```
用户: 你好
AI: 你好！我是优里。

用户: 我刚才说了什么？
AI: 我不知道你刚才说了什么。（❌ 不记得上下文）
```

### 修复后
```
用户: 你好
AI: 你好！我是优里。

用户: 我刚才说了什么？
AI: 你刚才说"你好"。（✅ 记得上下文）
```

## 🎯 对话历史管理策略

### 历史长度限制

- **最大历史长度**: 20 轮对话（40 条消息）
- **为什么限制**: 避免超出 API 的 token 限制
- **如何限制**: 当历史超过限制时，移除最旧的一轮对话

### 历史清空时机

- **对话结束时**: 用户输入 "nevermind" 或主动退出
- **连接断开时**: 不清空（保持会话）
- **游戏重启时**: 自动清空（Python 对象重新初始化）

### 历史内容

每轮对话包含 2 条消息：
1. **用户消息**: `{"role": "user", "content": "..."}`
2. **AI 响应**: `{"role": "assistant", "content": "..."}`

## 📝 日志输出

### 发送消息时
```
[DEBUG] 添加对话历史: 4 条消息
[DEBUG] 用户消息: 我刚才说了什么？
[DEBUG] 总消息数（含系统提示）: 6
```

### 收到响应后
```
[DEBUG] 对话已添加到历史，当前历史长度: 6 条消息
```

### 历史满时
```
[DEBUG] 对话历史已满，移除最旧的一轮对话
```

### 对话结束时
```
[INFO] 对话会话结束，已清空 6 条历史消息
```

## 🧪 测试验证

### 测试步骤

1. **启动对话**
   ```
   输入: "你好"
   预期: AI 正常响应
   ```

2. **第二轮对话（测试上下文）**
   ```
   输入: "我刚才说了什么？"
   预期: AI 回答 "你刚才说'你好'"
   ```

3. **第三轮对话（继续测试上下文）**
   ```
   输入: "那你叫什么名字？"
   预期: AI 回答 "我叫优里"
   ```

4. **第四轮对话（测试多轮上下文）**
   ```
   输入: "总结一下我们刚才的对话"
   预期: AI 能够总结之前的对话内容
   ```

5. **退出对话**
   ```
   输入: "nevermind"
   预期: 对话结束，历史清空
   ```

6. **重新开始对话**
   ```
   输入: "我们之前聊了什么？"
   预期: AI 回答不记得（因为历史已清空）
   ```

### 预期结果

✅ **成功标志**:
- AI 能够记住之前的对话内容
- 多轮对话保持连贯性
- 对话结束后历史正确清空
- 新对话不会受旧对话影响

❌ **失败标志**:
- AI 仍然不记得之前的对话
- 日志中没有 "添加对话历史" 的记录
- 对话结束后历史没有清空

## 🔧 技术细节

### OpenAI API 消息格式

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "system", "content": "你是优里..."},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！我是优里。"},
    {"role": "user", "content": "我刚才说了什么？"}
  ]
}
```

### 历史管理逻辑

```python
# 添加新对话
conversation_history.append({"role": "user", "content": "..."})
conversation_history.append({"role": "assistant", "content": "..."})

# 限制长度（保留最近 20 轮）
if len(conversation_history) > 40:  # 20 轮 × 2 条消息
    conversation_history = conversation_history[2:]  # 移除最旧的一轮
```

### Token 估算

假设平均每条消息 50 tokens：
- 系统提示: ~500 tokens
- 20 轮对话: 40 条消息 × 50 tokens = 2000 tokens
- 当前消息: ~50 tokens
- **总计**: ~2550 tokens

这在大多数 API 的限制内（通常 4096 或 8192 tokens）。

## 📚 相关文档

- **主修复文档**: `.kiro/AUTOPILOT_FIX_SUMMARY.md`
- **测试指南**: `.kiro/QUICK_TEST_GUIDE.md`
- **完整报告**: `.kiro/FINAL_FIX_REPORT.md`

## 🎉 总结

这次更新修复了对话上下文丢失的问题，现在：

✅ **卡死问题已解决**（之前的修复）
✅ **上下文保持已实现**（本次更新）

AI 现在能够：
- 记住之前的对话内容
- 保持多轮对话的连贯性
- 在对话结束时正确清空历史
- 避免超出 token 限制

**下一步**：测试验证！

---

**更新日期**: 2025-10-11
**更新者**: Kiro AI Assistant
**版本**: v2.1

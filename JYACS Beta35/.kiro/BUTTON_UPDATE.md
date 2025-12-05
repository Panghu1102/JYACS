# JYACS 按钮动态切换功能

## 🎯 功能说明

实现了动态按钮切换功能：
- **初始状态**：按钮显示 "JYACS"
- **对话中**：按钮变为 "退出"
- **点击退出**：结束对话，按钮恢复为 "JYACS"

## 🔧 实现细节

### 1. 状态管理

添加了两个全局变量来跟踪对话状态：

```python
# jyacs_ui_hooks.rpy
store.jyacs_is_chatting = False      # 是否正在对话中
store.jyacs_exit_requested = False   # 用户是否请求退出
```

### 2. 动态按钮

修改了 `free_chat_overlay` 屏幕，根据状态显示不同的按钮：

```python
if not store.jyacs_is_chatting:
    # 未在对话中，显示 "JYACS" 按钮
    textbutton _("JYACS"):
        action [
            SetVariable("store.jyacs_is_chatting", True),
            Call("submod_jyacs_chat_start")
        ]
else:
    # 正在对话中，显示 "退出" 按钮
    textbutton _("退出"):
        action [
            SetVariable("store.jyacs_is_chatting", False),
            SetVariable("store.jyacs_exit_requested", True),
            NullAction()
        ]
```

### 3. 退出检测

在对话循环中检查退出请求：

```python
# jyacs_main.rpy - 外层循环中
if store.jyacs_exit_requested:
    store.jyacs_log("用户点击退出按钮，结束对话", "INFO")
    store.jyacs_exit_requested = False  # 重置标志
    _return = "user_exit"
    break
```

### 4. 状态重置

在对话开始和结束时重置状态：

```python
# 对话开始时
label submod_jyacs_chat_start:
    python:
        store.jyacs_exit_requested = False

# 对话结束时
label submod_jyacs_talking.end:
    python:
        store.jyacs_is_chatting = False
        store.jyacs_exit_requested = False
```

## 📊 修改的文件

### 1. jyacs_ui_hooks.rpy

**修改内容**：
- 添加状态变量初始化
- 修改 `free_chat_overlay` 屏幕，实现动态按钮切换

**修改行数**：~20 行

### 2. jyacs_main.rpy

**修改内容**：
- 在对话开始时重置退出标志
- 在对话循环中检查退出请求
- 在对话结束时重置对话状态

**修改行数**：~10 行

## 🎬 用户体验流程

### 场景 1：正常对话流程

```
1. 用户看到 "JYACS" 按钮
   ↓
2. 点击 "JYACS" 按钮
   ↓
3. 按钮变为 "退出"
   ↓
4. 进入对话界面
   ↓
5. 进行多轮对话
   ↓
6. 输入 "nevermind" 退出
   ↓
7. 按钮恢复为 "JYACS"
```

### 场景 2：使用退出按钮

```
1. 用户看到 "JYACS" 按钮
   ↓
2. 点击 "JYACS" 按钮
   ↓
3. 按钮变为 "退出"
   ↓
4. 进入对话界面
   ↓
5. 进行几轮对话
   ↓
6. 点击 "退出" 按钮 ← 新功能！
   ↓
7. 对话立即结束
   ↓
8. 按钮恢复为 "JYACS"
   ↓
9. 回到正常游戏流程
```

## 🔍 技术细节

### 为什么需要两个变量？

1. **`jyacs_is_chatting`**：
   - 用于控制按钮显示
   - 在点击按钮时立即更新
   - 在对话结束时重置

2. **`jyacs_exit_requested`**：
   - 用于通知对话循环用户想要退出
   - 在点击"退出"按钮时设置
   - 在对话循环检测到后重置

### 为什么不能直接使用 Return()?

在 Ren'Py 中，当我们在 Python 块内运行循环时，`Return()` action 无法立即中断循环。我们需要：
1. 设置一个标志（`jyacs_exit_requested`）
2. 在循环中定期检查这个标志
3. 检测到标志后，主动退出循环

### 按钮位置

按钮位于屏幕右上方（"右中上部"）：
- `xalign 1.0` - 水平右对齐
- `yalign 0.2` - 垂直位置在 20% 处
- `xoffset -20` - 向左偏移 20 像素
- `yoffset 20` - 向下偏移 20 像素

## 🧪 测试验证

### 测试步骤

1. **测试按钮初始状态**
   ```
   启动游戏
   预期：看到 "JYACS" 按钮
   ```

2. **测试按钮切换**
   ```
   点击 "JYACS" 按钮
   预期：按钮变为 "退出"
   ```

3. **测试正常退出**
   ```
   进行对话
   输入 "nevermind"
   预期：对话结束，按钮恢复为 "JYACS"
   ```

4. **测试退出按钮**
   ```
   点击 "JYACS" 按钮
   进行几轮对话
   点击 "退出" 按钮
   预期：对话立即结束，按钮恢复为 "JYACS"
   ```

5. **测试多次切换**
   ```
   重复点击 "JYACS" → 对话 → "退出" 多次
   预期：每次都能正常切换
   ```

### 预期结果

✅ **成功标志**：
- 按钮初始显示 "JYACS"
- 点击后变为 "退出"
- 点击"退出"能立即结束对话
- 对话结束后按钮恢复为 "JYACS"
- 可以多次重复使用

❌ **失败标志**：
- 按钮不切换
- 点击"退出"没有反应
- 对话结束后按钮不恢复
- 按钮状态混乱

## 📝 日志输出

### 对话开始时
```
[DEBUG] 对话状态已重置，按钮恢复为 JYACS
```

### 用户点击退出时
```
[INFO] 用户点击退出按钮，结束对话
```

### 对话结束时
```
[INFO] 对话会话结束，已清空 X 条历史消息
[DEBUG] 对话状态已重置，按钮恢复为 JYACS
```

## 🎨 按钮样式

按钮使用默认的 Ren'Py 文本按钮样式，可以通过修改样式来自定义外观：

```python
# 示例：自定义按钮样式
style jyacs_button is button:
    background "#7C4A4A"
    hover_background "#8C5A5A"
    padding (15, 8)

style jyacs_button_text is button_text:
    size 18
    color "#FFFFFF"
```

## 🔄 状态转换图

```
[游戏开始]
    ↓
[JYACS 按钮] ← 初始状态
    ↓ (点击)
[退出 按钮] + [对话界面]
    ↓ (点击退出 或 输入 nevermind)
[JYACS 按钮] ← 恢复初始状态
    ↓ (可以再次点击)
[循环...]
```

## 💡 使用建议

### 对于玩家

1. **开始对话**：点击右上角的 "JYACS" 按钮
2. **进行对话**：正常输入消息，AI 会回复
3. **退出对话**：
   - 方法 1：输入 "nevermind"
   - 方法 2：点击右上角的 "退出" 按钮 ← 新功能！

### 对于开发者

1. **检查对话状态**：使用 `store.jyacs_is_chatting`
2. **请求退出**：设置 `store.jyacs_exit_requested = True`
3. **重置状态**：在对话结束时确保重置两个变量

## 🐛 已知问题

### 无

目前没有已知问题。

## 🚀 未来改进

### 可能的增强功能

1. **按钮动画**：添加淡入淡出效果
2. **确认对话框**：点击"退出"时显示确认对话框
3. **快捷键**：添加键盘快捷键（如 ESC）退出对话
4. **按钮图标**：使用图标而不是文字
5. **按钮提示**：鼠标悬停时显示提示信息

## 📚 相关文档

- **上下文修复**: `.kiro/CONTEXT_FIX_UPDATE.md`
- **主修复文档**: `.kiro/AUTOPILOT_FIX_SUMMARY.md`
- **测试指南**: `.kiro/QUICK_TEST_GUIDE.md`

## 🎉 总结

这次更新实现了动态按钮切换功能，提升了用户体验：

✅ **按钮状态清晰**：一目了然是否在对话中
✅ **退出方便**：点击按钮即可退出，无需输入命令
✅ **状态管理完善**：自动重置，不会出现状态混乱

现在玩家可以更方便地控制对话流程！

---

**更新日期**: 2025-10-11
**更新者**: Kiro AI Assistant
**版本**: v2.2

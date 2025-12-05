# JYACS 设置显示问题紧急修复

## 🚨 问题描述

用户报告在 JYACS 设置区域看到：
```
API 状态: <function jyacs_get_connection_status_display at 0x072575780>
消息队列: <function jyacs_get_queue_length_display at 0x0727557F0>
```

这表明函数对象被直接显示，而不是函数的返回值。

## 🔍 根本原因

### 问题 1: 文本插值语法错误

**错误代码**:
```renpy
text "API 状态: [jyacs_get_connection_status_display()]"
```

在 Ren'Py 中，方括号 `[]` 内的内容会被求值，但：
- `[function_name()]` 在某些情况下会显示函数对象
- `[function_name!t]` 在某些 Ren'Py 版本中不起作用

### 问题 2: Ren'Py 版本兼容性

不同版本的 Ren'Py 对文本插值的处理可能不同，导致：
- 函数调用语法不一致
- 后缀操作符支持不同
- 求值行为差异

## ✅ 最终解决方案

### 使用 Python 块预先调用函数

**文件**: `jyacs_ui_hooks.rpy`
**位置**: 第 836-848 行

**修改后的代码**:
```renpy
# 状态显示
python:
    # 调用函数获取显示文本
    api_status_text = jyacs_get_connection_status_display()
    queue_length_text = jyacs_get_queue_length_display()

hbox:
    spacing 30
    
    text "API 状态: [api_status_text]":
        style "jyacs_status_text"
    
    text "消息队列: [queue_length_text]":
        style "jyacs_status_text"
```

### 为什么这个方案有效？

1. **明确的函数调用**: 在 Python 块中显式调用函数
2. **变量存储**: 将返回值存储在变量中
3. **简单的变量插值**: 文本中只使用变量名，不涉及函数调用
4. **跨版本兼容**: 这种方式在所有 Ren'Py 版本中都能正常工作

## 🔧 修复步骤

### 步骤 1: 定位问题代码

在 `jyacs_ui_hooks.rpy` 中找到 JYACS 设置区域（约第 836 行）

### 步骤 2: 添加 Python 块

在状态显示之前添加 Python 块：
```python
python:
    api_status_text = jyacs_get_connection_status_display()
    queue_length_text = jyacs_get_queue_length_display()
```

### 步骤 3: 修改文本插值

将：
```renpy
text "API 状态: [jyacs_get_connection_status_display!t]"
```

改为：
```renpy
text "API 状态: [api_status_text]"
```

### 步骤 4: 验证修复

1. 保存文件
2. 重启游戏
3. 打开设置界面
4. 检查显示是否正常

## 🧪 测试验证

### 预期结果

**修复前**:
```
API 状态: <function jyacs_get_connection_status_display at 0x...>
消息队列: <function jyacs_get_queue_length_display at 0x...>
```

**修复后**:
```
API 状态: 未连接
消息队列: 0
```

### 测试步骤

1. **启动游戏**
   ```
   运行游戏
   ```

2. **打开设置**
   ```
   按 ESC -> 选择 Settings
   ```

3. **滚动到 JYACS 设置区域**
   ```
   滚动到页面底部
   ```

4. **验证显示**
   ```
   检查是否显示:
   - "API 状态: 未连接" (或其他状态)
   - "消息队列: 0" (或其他数字)
   ```

5. **测试功能**
   ```
   点击 "详细设置" 按钮
   验证是否能打开详细设置界面
   ```

## 📝 技术说明

### Ren'Py 文本插值的正确用法

#### 方法 1: 变量插值（推荐）
```renpy
python:
    status = get_status()

text "状态: [status]"
```

#### 方法 2: 简单表达式
```renpy
text "总数: [count + 1]"
```

#### 方法 3: 字符串格式化
```renpy
python:
    status = get_status()

text "状态: {}".format(status)
```

#### ❌ 避免的用法
```renpy
# 不要这样做 - 可能显示函数对象
text "状态: [get_status()]"

# 不要这样做 - 兼容性问题
text "状态: [get_status!t]"
```

### 为什么函数对象会被显示？

在 Python 中：
- `function_name` 是函数对象的引用
- `function_name()` 是函数调用，返回结果

在 Ren'Py 文本插值中：
- `[variable]` 会显示变量的值
- `[expression]` 会求值并显示结果
- 但函数调用的求值行为在不同版本中可能不一致

## 🎯 最佳实践

### 在 Ren'Py 中显示动态内容

1. **使用 Python 块预处理**
   ```renpy
   python:
       display_text = process_data()
   
   text "[display_text]"
   ```

2. **使用 DynamicDisplayable**
   ```renpy
   text DynamicDisplayable(get_status)
   ```

3. **使用 timer 更新**
   ```renpy
   timer 1.0 repeat True action Function(update_status)
   ```

### 避免的做法

1. ❌ 在文本插值中直接调用函数
2. ❌ 使用不兼容的后缀操作符
3. ❌ 依赖版本特定的行为

## 🔄 相关修复

### 其他可能需要修复的地方

检查项目中是否还有类似的问题：

```bash
# 搜索可能的问题模式
grep -r "\[.*().*\]" *.rpy
```

如果发现类似的代码，使用相同的方法修复。

## 📚 相关文档

- **完整修复文档**: `.kiro/SETTINGS_FIX.md`
- **按钮更新**: `.kiro/BUTTON_UPDATE.md`
- **上下文修复**: `.kiro/CONTEXT_FIX_UPDATE.md`

## 🎉 总结

这次修复使用了最可靠的方法：

✅ **在 Python 块中调用函数** - 明确且可控
✅ **使用变量存储结果** - 简单且可靠
✅ **简单的变量插值** - 跨版本兼容
✅ **避免复杂的文本插值** - 减少问题

现在设置界面应该能够正确显示状态信息了！

---

**修复日期**: 2025-10-11
**修复者**: Kiro AI Assistant
**版本**: v2.3.1
**优先级**: 🚨 紧急

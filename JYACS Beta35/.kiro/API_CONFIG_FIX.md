# JYACS API 配置选项添加

## 🎯 问题描述

用户报告在 JYACS 设置区域只看到：
```
API 状态: 未连接
消息队列: 0
```

但是**没有任何地方可以输入**：
- API 密钥
- API 地址
- 模型名称

这导致用户无法配置 JYACS 的基本设置。

## 🔍 问题原因

主设置界面（preferences screen）中的 JYACS 设置区域只包含：
1. 状态显示
2. 快速操作按钮（连接、断开、详细设置）

但**缺少了最基本的 API 配置输入选项**。

虽然这些选项在"详细设置"界面中存在，但用户需要能够在主界面直接配置这些基本信息。

## ✅ 解决方案

在主设置界面的 JYACS 设置区域添加三个配置选项：

### 1. API 密钥输入

```renpy
hbox:
    spacing 15
    
    text "API 密钥:":
        style "jyacs_text"
        min_width 100
    
    python:
        api_key = persistent.jyacs_setting_dict.get('api_key', '')
        api_key_display = ("*" * min(len(api_key), 20)) if api_key else "未设置"
    
    textbutton "[api_key_display]":
        style "jyacs_check_button"
        text_style "jyacs_check_button_text"
        action Show("jyacs_text_input", 
                  prompt_text="请输入 API 密钥:", 
                  dict_obj=persistent.jyacs_setting_dict, 
                  key_name="api_key",
                  is_password=True)
        xsize 300
```

**功能**:
- 显示 API 密钥状态（显示为星号或"未设置"）
- 点击按钮打开输入对话框
- 输入的密钥会被保存到 `persistent.jyacs_setting_dict`

### 2. API 地址输入

```renpy
hbox:
    spacing 15
    
    text "API 地址:":
        style "jyacs_text"
        min_width 100
    
    python:
        api_url_display = persistent.jyacs_setting_dict.get('api_url', '') or "未设置"
        if len(api_url_display) > 40:
            api_url_display = api_url_display[:37] + "..."
    
    textbutton "[api_url_display]":
        style "jyacs_check_button"
        text_style "jyacs_check_button_text"
        action Show("jyacs_text_input", 
                  prompt_text="请输入 API 地址:", 
                  dict_obj=persistent.jyacs_setting_dict, 
                  key_name="api_url")
        xsize 300
```

**功能**:
- 显示 API 地址（如果太长则截断）
- 点击按钮打开输入对话框
- 输入的地址会被保存

### 3. 模型名称输入

```renpy
hbox:
    spacing 15
    
    text "模型名称:":
        style "jyacs_text"
        min_width 100
    
    python:
        model_name_display = persistent.jyacs_setting_dict.get('model_name', '') or "未设置"
    
    textbutton "[model_name_display]":
        style "jyacs_check_button"
        text_style "jyacs_check_button_text"
        action Show("jyacs_text_input", 
                  prompt_text="请输入模型名称:", 
                  dict_obj=persistent.jyacs_setting_dict, 
                  key_name="model_name")
        xsize 300
```

**功能**:
- 显示模型名称
- 点击按钮打开输入对话框
- 输入的模型名称会被保存

### 4. 添加"保存设置"按钮

```renpy
textbutton "保存设置":
    style "jyacs_check_button"
    text_style "jyacs_check_button_text"
    action Function(jyacs_apply_setting)
    xsize 100
```

**功能**:
- 应用所有设置更改
- 验证必填字段
- 显示保存结果通知

## 📊 修改的文件

**文件**: `jyacs_ui_hooks.rpy`
**位置**: 第 850-920 行
**修改内容**: 添加 API 配置输入区域

## 🎨 界面布局

### 修改后的 JYACS 设置区域

```
┌─────────────────────────────────────────────┐
│ JYACS 设置                                   │
├─────────────────────────────────────────────┤
│ API 状态: 未连接    消息队列: 0             │
├─────────────────────────────────────────────┤
│ API 密钥:  [********************]  ← 点击输入│
│ API 地址:  [https://api.example.com]        │
│ 模型名称:  [gpt-3.5-turbo]                  │
├─────────────────────────────────────────────┤
│ [保存设置] [连接] [断开] [详细设置]         │
└─────────────────────────────────────────────┘
```

## 🔧 使用流程

### 首次配置

1. **打开设置**
   ```
   按 ESC -> 选择 Settings
   ```

2. **滚动到 JYACS 设置区域**
   ```
   滚动到页面底部
   ```

3. **配置 API 密钥**
   ```
   点击 API 密钥按钮
   输入密钥
   点击确定
   ```

4. **配置 API 地址**
   ```
   点击 API 地址按钮
   输入地址（如 https://api.openai.com/v1/chat/completions）
   点击确定
   ```

5. **配置模型名称**
   ```
   点击模型名称按钮
   输入模型（如 gpt-3.5-turbo）
   点击确定
   ```

6. **保存设置**
   ```
   点击"保存设置"按钮
   等待"基础设置已保存"通知
   ```

7. **连接 API**
   ```
   点击"连接"按钮
   等待连接成功
   ```

### 修改配置

1. 打开设置
2. 点击要修改的配置按钮
3. 输入新值
4. 点击"保存设置"
5. 如果需要，点击"断开"再"连接"

## 🧪 测试验证

### 测试步骤

1. **验证界面显示**
   ```
   打开设置 -> 滚动到 JYACS 设置区域
   
   预期看到:
   ✅ API 密钥: 未设置（或星号）
   ✅ API 地址: 未设置（或地址）
   ✅ 模型名称: 未设置（或模型名）
   ✅ 四个按钮: 保存设置、连接、断开、详细设置
   ```

2. **测试 API 密钥输入**
   ```
   点击 API 密钥按钮
   
   预期:
   ✅ 弹出输入对话框
   ✅ 提示文本: "请输入 API 密钥:"
   ✅ 可以输入文本
   ✅ 点击确定后保存
   ✅ 按钮显示为星号
   ```

3. **测试 API 地址输入**
   ```
   点击 API 地址按钮
   输入: https://api.openai.com/v1/chat/completions
   点击确定
   
   预期:
   ✅ 地址被保存
   ✅ 按钮显示地址（如果太长则截断）
   ```

4. **测试模型名称输入**
   ```
   点击模型名称按钮
   输入: gpt-3.5-turbo
   点击确定
   
   预期:
   ✅ 模型名称被保存
   ✅ 按钮显示模型名称
   ```

5. **测试保存设置**
   ```
   配置好所有选项后
   点击"保存设置"按钮
   
   预期:
   ✅ 显示"基础设置已保存"通知
   ✅ 设置被应用
   ```

6. **测试连接功能**
   ```
   点击"连接"按钮
   
   预期:
   ✅ 显示"正在连接 API..."通知
   ✅ API 状态变为"连接中..."
   ✅ 连接成功后状态变为"已连接"
   ```

## 📝 技术细节

### 输入对话框

使用 `jyacs_text_input` 屏幕来处理输入：

```renpy
screen jyacs_text_input(prompt_text, dict_obj, key_name, is_password=False):
    modal True
    zorder 250
    
    # 显示输入对话框
    # 支持普通文本和密码输入
    # 自动保存到指定的字典
```

**参数**:
- `prompt_text`: 提示文本
- `dict_obj`: 要保存到的字典对象
- `key_name`: 字典中的键名
- `is_password`: 是否为密码输入（显示为星号）

### 数据存储

所有配置都保存在 `persistent.jyacs_setting_dict` 中：

```python
persistent.jyacs_setting_dict = {
    "api_key": "sk-...",
    "api_url": "https://api.openai.com/v1/chat/completions",
    "model_name": "gpt-3.5-turbo",
    # ... 其他设置
}
```

### 设置应用

点击"保存设置"按钮会调用 `jyacs_apply_setting()` 函数：

```python
def jyacs_apply_setting():
    # 验证必填字段
    # 应用设置到 JYACS 实例
    # 如果启用自动重连，重新连接
    # 显示通知
```

## 🎯 设计考虑

### 为什么在主界面添加这些选项？

1. **用户体验**: 用户不应该需要点击"详细设置"才能配置基本信息
2. **首次使用**: 新用户需要快速配置才能开始使用
3. **便捷性**: 常用设置应该容易访问
4. **一致性**: 其他设置也在主界面中

### 为什么保留"详细设置"按钮？

1. **高级选项**: 超参数等高级设置仍在详细界面
2. **界面简洁**: 主界面不应该太拥挤
3. **分层设计**: 基础设置在主界面，高级设置在详细界面

### 为什么添加"保存设置"按钮？

1. **明确操作**: 用户知道何时设置被应用
2. **验证时机**: 可以在保存时验证所有字段
3. **用户控制**: 用户可以修改多个设置后一次性保存

## 🐛 可能的问题和解决方案

### 问题 1: 输入对话框不显示

**原因**: `jyacs_text_input` 屏幕未定义或有错误

**解决**: 检查 `jyacs_ui_hooks.rpy` 中的屏幕定义（约第 158 行）

### 问题 2: 设置不保存

**原因**: `persistent.jyacs_setting_dict` 未初始化

**解决**: 检查 `header.rpy` 中的初始化代码（约第 30 行）

### 问题 3: 保存后无法连接

**原因**: API 配置格式错误

**解决**: 
- 检查 API 地址格式（应包含完整 URL）
- 检查 API 密钥格式
- 查看日志文件获取详细错误

## 📚 相关文档

- **显示修复**: `.kiro/SETTINGS_DISPLAY_FIX.md`
- **完整设置文档**: `.kiro/SETTINGS_FIX.md`
- **按钮更新**: `.kiro/BUTTON_UPDATE.md`

## 🎉 总结

这次修复添加了三个关键的配置选项：

✅ **API 密钥输入** - 安全的密码输入
✅ **API 地址输入** - 完整的 URL 输入
✅ **模型名称输入** - 模型标识符输入
✅ **保存设置按钮** - 应用所有更改

现在用户可以直接在主设置界面配置 JYACS 的基本信息，无需进入详细设置！

---

**修复日期**: 2025-10-11
**修复者**: Kiro AI Assistant
**版本**: v2.4
**优先级**: 🚨 紧急

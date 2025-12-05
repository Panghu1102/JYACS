# JYACS 设置界面集成设计文档

## 概述

本设计文档描述如何将 JYACS 子 mod 的设置界面集成到 JY 1.10.11 的原生设置系统中。目标是在保持 JY 原有设置界面风格和布局的基础上，在设置页面底部添加 JYACS 专属的设置区域，实现无缝集成。

### 设计目标

1. **视觉一致性**: 采用与 JY 1.10.11 完全相同的视觉风格、字体、颜色和布局
2. **非侵入性**: 不修改 JY 1.10.11 的原始文件，通过 Ren'Py 的覆盖机制实现
3. **功能完整性**: 保留 JYACS 现有的所有设置功能
4. **用户体验**: 提供直观、易用的设置界面

## 架构设计

### 1. 集成策略

采用 Ren'Py 的 `screen` 覆盖机制，通过更高优先级的 `init` 块重新定义 `preferences` screen。

```
JY 1.10.11 preferences screen (init -501)
    ↓ 被覆盖
JYACS preferences screen (init -500)
    ├── 保留所有 JY 原有设置项
    ├── 添加分隔线
    └── 添加 JYACS 设置区域
```

### 2. 文件结构

```
项目根目录/
├── JY1.10.11/                    # 游戏本体（只读）
│   └── DDLC-1.1.1-pc/
│       └── game/
│           ├── screens.rpy       # 原始设置界面
│           └── gui.rpy           # GUI 样式定义
├── jyacs_settings.rpy            # JYACS 设置界面（需重构）
├── jyacs_init.rpy                # JYACS 初始化
└── jyacs_ui_hooks.rpy            # UI 钩子（新建）
```

### 3. 技术栈

- **Ren'Py Screen Language**: 用于界面定义
- **Python**: 用于逻辑处理
- **Ren'Py Styles**: 用于样式定义

## 组件设计

### 1. 主设置界面 (preferences screen)

#### 1.1 布局结构

```
preferences screen (init -500)
├── game_menu wrapper
│   └── vbox (主容器)
│       ├── hbox (原 JY 设置区域)
│       │   ├── Display (显示模式)
│       │   ├── Skip (跳过设置)
│       │   └── Custom Assets (自定义资源)
│       ├── null height (间距)
│       ├── hbox (音量和滑块设置)
│       │   ├── vbox (左侧)
│       │   │   ├── Idle Frequency (待机频率)
│       │   │   ├── Text Speed (文本速度)
│       │   │   └── Auto-Forward Time (自动前进时间)
│       │   └── vbox (右侧)
│       │       ├── Music Volume (音乐音量)
│       │       ├── Sound Volume (音效音量)
│       │       ├── Voice Volume (语音音量)
│       │       ├── Mute All (全部静音)
│       │       └── Space BG Bloom (空间背景光晕)
│       ├── null height (分隔)
│       └── frame (JYACS 设置区域 - 新增)
│           └── vbox
│               ├── label "JYACS 设置"
│               ├── hbox (基础设置)
│               │   ├── API 连接状态
│               │   └── 快速操作按钮
│               └── textbutton "详细设置" (打开独立设置界面)
└── text "v[config.version]" (版本号)
```

#### 1.2 样式继承

所有 JYACS 设置项将使用 JY 原有的样式系统：

- **标签样式**: `pref_label` 和 `pref_label_text`
- **按钮样式**: `radio_button`, `check_button`
- **滑块样式**: `slider_slider`, `slider_button`
- **字体**: `gui/font/RifficFree-Bold.ttf` (标签), `gui/font/Halogen.ttf` (按钮)
- **颜色**: `#fff` (文本), `#a679ff` (轮廓/强调色)

### 2. JYACS 设置区域

#### 2.1 简化视图（集成在 preferences screen 中）

显示在原 JY 设置界面底部，提供快速访问：

```
┌─────────────────────────────────────────────┐
│ JYACS 设置                                   │
├─────────────────────────────────────────────┤
│ API 状态: [已连接/未连接]                    │
│ 消息队列: [数量]                             │
│                                              │
│ [连接] [断开] [详细设置]                     │
└─────────────────────────────────────────────┘
```

**组件**:
- 状态显示文本（使用 `pref_label_text` 样式）
- 操作按钮（使用 `check_button` 样式）

#### 2.2 详细设置界面（独立 screen）

点击"详细设置"按钮后打开的模态对话框：

```
┌─────────────────────────────────────────────┐
│              JYACS 详细设置                  │
├─────────────────────────────────────────────┤
│ [基础设置] [高级设置]                        │
├─────────────────────────────────────────────┤
│                                              │
│ API 配置                                     │
│ ├─ API 密钥: [********]  [修改]             │
│ ├─ API 地址: [url]       [修改]             │
│ └─ 模型名称: [model]     [修改]             │
│                                              │
│ 连接设置                                     │
│ ├─ □ 自动连接                               │
│ ├─ □ 自动重连                               │
│ └─ □ 启用触发器                             │
│                                              │
│ 功能设置                                     │
│ ├─ □ 启用情绪识别                           │
│ ├─ □ 回复时显示控制台                       │
│ └─ 目标语言: [zh_cn] ▼                      │
│                                              │
├─────────────────────────────────────────────┤
│        [保存] [验证配置] [返回]              │
└─────────────────────────────────────────────┘
```

**标签页**:
1. **基础设置**: API 配置、连接设置、功能设置
2. **高级设置**: 超参数配置（Temperature, Top P, Max Tokens 等）

### 3. 输入对话框

用于修改 API 密钥、地址等文本输入：

```
┌─────────────────────────────────────────────┐
│              请输入 API 密钥                 │
├─────────────────────────────────────────────┤
│                                              │
│ [_________________________________]          │
│                                              │
├─────────────────────────────────────────────┤
│              [确定] [取消]                   │
└─────────────────────────────────────────────┘
```

**特性**:
- 模态对话框（阻止背景交互）
- 使用 JY 的输入框样式
- 支持字典值的直接修改

## 数据模型

### 1. 持久化数据结构

```python
# 基础设置
persistent.jyacs_setting_dict = {
    "api_key": str,              # API 密钥
    "api_url": str,              # API 地址
    "model_name": str,           # 模型名称
    "auto_connect": bool,        # 自动连接
    "auto_reconnect": bool,      # 自动重连
    "enable_triggers": bool,     # 启用触发器
    "enable_emotion": bool,      # 启用情绪识别
    "show_console_when_reply": bool,  # 回复时显示控制台
    "target_lang": str,          # 目标语言
    "use_custom_model_config": bool,  # 使用自定义模型配置
    "mspire_enable": bool,       # Mspire 启用
    "strict_mode": bool,         # 严格模式
    "log_level": str,            # 日志级别
    "log_conlevel": str          # 控制台日志级别
}

# 高级设置
persistent.jyacs_advanced_setting = {
    "temperature": float,        # 温度 (0.0-1.0)
    "top_p": float,              # Top P (0.0-1.0)
    "max_tokens": int,           # 最大令牌数
    "frequency_penalty": float,  # 频率惩罚 (0.0-1.0)
    "presence_penalty": float,   # 存在惩罚 (0.0-1.0)
    "mf_aggressive": bool,       # MF 激进模式
    "sfe_aggressive": bool,      # SFE 激进模式
    "esc_aggressive": bool,      # ESC 激进模式
    "nsfw_acceptive": bool,      # NSFW 接受
    "seed": int,                 # 随机种子
    "_seed": str                 # 随机种子（字符串）
}
```

### 2. 运行时状态

```python
# JYACS 连接状态
store.jyacs.status = str  # "connected", "disconnected", "connecting"
store.jyacs.message_queue_length = int  # 消息队列长度
```

## 样式系统

### 1. 样式继承关系

```
JY 原生样式
├── pref_label (标签容器)
│   └── pref_label_text (标签文本)
├── radio_button (单选按钮)
│   └── radio_button_text (单选按钮文本)
├── check_button (复选按钮)
│   └── check_button_text (复选按钮文本)
└── slider_slider (滑块)
    └── slider_button (滑块按钮)

JYACS 扩展样式（继承自 JY）
├── jyacs_pref_label (继承 pref_label)
├── jyacs_check_button (继承 check_button)
└── jyacs_slider (继承 slider_slider)
```

### 2. 关键样式定义

```python
# 标签样式
init -1 style jyacs_pref_label is pref_label
init -1 style jyacs_pref_label_text is pref_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size 24
    color "#fff"
    outlines [(3, "#a679ff", 0, 0), (1, "#a679ff", 1, 1)]

# 按钮样式
init -1 style jyacs_check_button is check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

init -1 style jyacs_check_button_text is check_button_text:
    font "gui/font/Halogen.ttf"
    outlines []

# 滑块样式
init -1 style jyacs_slider is slider_slider:
    xsize 350
```

### 3. 颜色方案

遵循 JY 1.10.11 的颜色系统：

- **主色调**: `#a679ff` (紫色)
- **文本颜色**: `#ffffff` (白色)
- **悬停颜色**: `#d5bdff` (浅紫色)
- **选中颜色**: `#9584b3` (深紫色)
- **禁用颜色**: `#aaaaaa7f` (半透明灰色)

## 接口设计

### 1. Screen 接口

#### 1.1 preferences (主设置界面)

```renpy
init -500 screen preferences():
    tag menu
    use game_menu(_("Settings"), scroll="viewport"):
        vbox:
            # JY 原有设置项...
            
            # JYACS 设置区域
            null height (2 * gui.pref_spacing)
            frame:
                style_prefix "jyacs_pref"
                vbox:
                    label "JYACS 设置"
                    # 状态显示和快速操作
```

#### 1.2 jyacs_detailed_settings (详细设置界面)

```renpy
init 15 screen jyacs_detailed_settings():
    modal True
    zorder 200
    
    # 标签页导航
    # 设置内容区域
    # 操作按钮
```

#### 1.3 jyacs_text_input (文本输入对话框)

```renpy
init 15 screen jyacs_text_input(prompt, dict_obj, key_name):
    modal True
    zorder 250
    
    # 输入框
    # 确定/取消按钮
```

### 2. Python 函数接口

#### 2.1 设置应用函数

```python
def jyacs_apply_setting():
    """应用基础设置"""
    # 验证设置
    # 保存到持久化存储
    # 触发相关更新
    pass

def jyacs_apply_advanced_setting():
    """应用高级设置"""
    # 验证超参数范围
    # 保存到持久化存储
    pass
```

#### 2.2 配置验证函数

```python
def jyacs_verify_api_config():
    """验证 API 配置"""
    # 检查必填字段
    # 测试连接
    # 返回验证结果
    pass
```

#### 2.3 状态查询函数

```python
def jyacs_get_connection_status():
    """获取连接状态"""
    return store.jyacs.get_status()

def jyacs_get_queue_length():
    """获取消息队列长度"""
    return store.jyacs.len_message_queue()
```

## 错误处理

### 1. 配置验证

- **API 密钥为空**: 显示警告消息，禁用连接按钮
- **API 地址格式错误**: 显示错误提示，要求重新输入
- **模型名称为空**: 使用默认值 "jyacs_main"

### 2. 连接错误

- **连接失败**: 显示错误消息，提供重试选项
- **连接超时**: 显示超时提示，建议检查网络
- **认证失败**: 提示检查 API 密钥

### 3. 输入验证

- **超参数范围**: 自动限制在有效范围内
- **非法字符**: 过滤或拒绝输入
- **空值处理**: 使用默认值或保持原值

## 测试策略

### 1. 视觉测试

- [ ] 验证 JYACS 设置区域与 JY 原有设置的视觉一致性
- [ ] 检查不同分辨率下的布局适配
- [ ] 测试悬停和选中状态的视觉反馈

### 2. 功能测试

- [ ] 测试所有设置项的保存和加载
- [ ] 验证 API 连接功能
- [ ] 测试配置验证逻辑
- [ ] 检查错误处理和提示

### 3. 集成测试

- [ ] 验证不覆盖 JY 原有设置
- [ ] 测试与 JY 其他功能的兼容性
- [ ] 检查游戏重启后设置的持久化

### 4. 用户体验测试

- [ ] 测试设置流程的直观性
- [ ] 验证错误提示的清晰度
- [ ] 检查操作响应速度

## 实现注意事项

### 1. 优先级管理

- JY 原始 preferences screen: `init -501`
- JYACS 覆盖 preferences screen: `init -500`
- JYACS 详细设置 screen: `init 15`
- JYACS 样式定义: `init -1`

### 2. 命名约定

- Screen 名称: `jyacs_*`
- 样式前缀: `jyacs_*`
- 函数名称: `jyacs_*`
- 变量名称: `jyacs_*`

### 3. 兼容性考虑

- 不修改 JY1.10.11 目录下的任何文件
- 使用 `hasattr` 检查避免重复定义
- 提供降级方案处理缺失依赖

### 4. 性能优化

- 延迟加载非关键组件
- 缓存状态查询结果
- 避免频繁的持久化写入

## 部署计划

### 阶段 1: 样式系统重构
- 创建 JYACS 样式定义，继承 JY 样式
- 测试样式在不同场景下的表现

### 阶段 2: preferences screen 覆盖
- 复制 JY 原有 preferences screen 内容
- 在底部添加 JYACS 设置区域
- 测试与原有设置的兼容性

### 阶段 3: 详细设置界面
- 实现独立的详细设置 screen
- 添加标签页导航
- 实现所有设置项

### 阶段 4: 输入和验证
- 实现文本输入对话框
- 添加配置验证逻辑
- 实现错误处理

### 阶段 5: 集成测试
- 完整功能测试
- 视觉一致性验证
- 性能测试

## 附录

### A. JY 1.10.11 设置界面分析

**原始结构**:
- 使用 `game_menu` wrapper
- 采用 `vbox` + `hbox` 布局
- 使用 `box_wrap True` 实现自动换行
- 滑块使用 `FieldValue` 和 `Preference`

**样式特点**:
- 标签使用粗体字体 (RifficFree-Bold)
- 按钮使用细体字体 (Halogen)
- 紫色主题 (#a679ff)
- 带轮廓的文本效果

### B. 现有 JYACS 设置功能清单

**基础设置**:
- API 密钥、地址、模型名称
- 自动连接、自动重连
- 启用触发器、情绪识别
- 目标语言、日志级别

**高级设置**:
- Temperature, Top P, Max Tokens
- Frequency Penalty, Presence Penalty
- 各种激进模式开关
- NSFW 接受、随机种子

**操作功能**:
- 连接/断开 API
- 验证配置
- 保存设置

### C. 技术参考

- Ren'Py Screen Language: https://www.renpy.org/doc/html/screens.html
- Ren'Py Style System: https://www.renpy.org/doc/html/style.html
- DDLC Modding Guide: https://doki-doki-literature-club.fandom.com/wiki/Modding

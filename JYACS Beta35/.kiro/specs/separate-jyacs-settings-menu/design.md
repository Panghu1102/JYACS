# Design Document

## Overview

本设计文档描述如何将JYACS设置从游戏的preferences界面中独立出来，创建一个专门的JYACS设置菜单入口。主要改动包括：

1. 修改`jyacs_ui_hooks.rpy`，移除preferences screen中的JYACS设置集成代码
2. 修改`jyacs_ui_hooks.rpy`，在game_menu的navigation区域添加"JYACS设置"按钮
3. 创建独立的JYACS设置screen，复用现有的`jyacs_detailed_settings` screen

## Architecture

### 文件结构

```
jyacs_ui_hooks.rpy
├── 样式定义 (保持不变)
├── 辅助函数 (保持不变)
├── jyacs_text_input screen (保持不变)
├── jyacs_detailed_settings screen (保持不变)
├── jyacs_basic_settings_content screen (保持不变)
├── jyacs_advanced_settings_content screen (保持不变)
├── preferences screen (移除JYACS设置部分)
└── game_menu screen (添加JYACS设置按钮)
```

### 组件关系

```
game_menu
├── navigation (原有菜单项)
├── Return按钮 (ypos 420)
└── JYACS设置按钮 (ypos 460, 新增)
    └── 打开 jyacs_detailed_settings screen
```

## Components and Interfaces

### 1. 修改preferences Screen

**位置**: `jyacs_ui_hooks.rpy` 中的 `init 10 screen preferences()` 定义

**改动内容**:
- 移除整个JYACS设置区域的代码块（从 `# ========== JYACS 设置区域 ==========` 到对应的结束位置）
- 保持其他游戏设置不变

**代码结构**:
```python
init 10 screen preferences():
    tag menu
    
    # ... 原有的游戏设置代码 ...
    
    # 移除以下部分:
    # null height (3 * gui.pref_spacing)
    # frame: # JYACS设置容器
    #     ...
    
    # 保留版本号显示
    text "v[config.version]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"
```

### 2. 修改game_menu Screen添加JYACS设置按钮

**位置**: `jyacs_ui_hooks.rpy` 中的 `init 10 screen game_menu()` 定义

**改动内容**:
- 在Return按钮（ypos 420）下方添加JYACS设置按钮（ypos 460）
- 按钮样式与其他navigation按钮保持一致
- 点击后打开`jyacs_detailed_settings` screen

**代码结构**:
```python
init 10 screen game_menu(title, scroll=None):
    # ... 原有代码 ...
    
    use navigation
    
    # ... 原有的随机背景代码 ...
    
    # 返回按钮 (原有)
    vbox:
        xpos 30
        ypos 420
        style_prefix "navigation"
        hbox:
            textbutton _("Return") action Return()
    
    # JYACS设置按钮 (新增)
    vbox:
        xpos 30
        ypos 460
        style_prefix "navigation"
        hbox:
            textbutton _("JYACS设置") action Show("jyacs_detailed_settings")
    
    label title
    
    # ... 原有代码 ...
```

### 3. 独立的JYACS设置界面

**位置**: `jyacs_ui_hooks.rpy` 中的 `jyacs_detailed_settings` screen

**改动内容**: 无需改动，直接复用现有实现

**功能说明**:
- 模态对话框形式
- 包含基础设置和高级设置两个标签页
- 显示API状态和消息队列信息
- 提供连接/断开、保存设置、验证配置等功能
- 支持ESC键关闭

## Data Models

### Persistent数据

无需修改，继续使用现有的persistent数据结构：

```python
persistent.jyacs_setting_dict = {
    'api_key': '',
    'api_url': '',
    'model_name': '',
    # ... 其他设置 ...
}
```

## Error Handling

### 1. 按钮点击错误处理

- 如果`jyacs_detailed_settings` screen未定义，Ren'Py会显示错误
- 解决方案：确保screen定义在按钮之前加载（使用适当的init优先级）

### 2. 界面兼容性

- 确保移除JYACS设置后，preferences界面布局不会出现空白或错位
- 确保新按钮不会与其他UI元素重叠

### 3. 功能完整性

- 确保所有JYACS功能在新界面中正常工作
- 确保设置保存和加载机制不受影响

## Testing Strategy

### 单元测试

1. **preferences界面测试**
   - 打开preferences界面，确认没有JYACS相关内容
   - 验证其他游戏设置功能正常

2. **game_menu按钮测试**
   - 在游戏内打开菜单，确认"JYACS设置"按钮显示
   - 验证按钮位置正确（在Return按钮下方）
   - 验证按钮样式与其他按钮一致

3. **JYACS设置界面测试**
   - 点击"JYACS设置"按钮，确认界面正常打开
   - 验证所有设置选项正常显示
   - 验证连接/断开功能正常
   - 验证设置保存功能正常
   - 验证ESC键关闭功能正常

### 集成测试

1. **完整流程测试**
   - 从游戏菜单 → 点击JYACS设置 → 修改配置 → 保存 → 返回
   - 验证设置是否正确保存
   - 重新打开JYACS设置，验证设置是否正确加载

2. **兼容性测试**
   - 在主菜单和游戏内菜单分别测试
   - 验证在不同场景下按钮都能正常显示和工作

### 用户验收测试

1. **界面美观性**
   - 确认preferences界面更加简洁
   - 确认JYACS设置按钮位置合理
   - 确认JYACS设置界面布局清晰

2. **易用性**
   - 确认用户能够轻松找到JYACS设置入口
   - 确认设置流程直观易懂

## Implementation Notes

### Init优先级

- `jyacs_detailed_settings` screen: `init 15` (已存在)
- `game_menu` screen override: `init 10` (新增)
- `preferences` screen override: `init 10` (新增)

这样可以确保JYACS的screen定义先于game_menu和preferences的override。

### 代码组织

所有改动都在`jyacs_ui_hooks.rpy`文件中完成，不需要修改原游戏的`screens.rpy`文件，保持mod的独立性。

### 向后兼容

- 保持所有persistent数据结构不变
- 保持所有JYACS功能接口不变
- 只改变UI的组织方式

## Design Decisions

### 决策1: 使用screen override而不是修改原文件

**理由**: 
- 保持mod的独立性
- 便于维护和更新
- 避免与原游戏文件冲突

### 决策2: 复用jyacs_detailed_settings而不是创建新screen

**理由**:
- 避免代码重复
- 保持功能一致性
- 减少维护成本

### 决策3: 按钮位置选择ypos 460

**理由**:
- Return按钮在ypos 420
- 按钮间距40像素与其他菜单按钮保持一致
- 不会与其他UI元素重叠

### 决策4: 使用"JYACS设置"作为按钮文本

**理由**:
- 清晰表达功能
- 与其他菜单项命名风格一致
- 易于理解

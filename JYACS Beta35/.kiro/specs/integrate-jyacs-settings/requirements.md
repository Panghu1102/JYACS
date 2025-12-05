# Requirements Document

## Introduction

本功能旨在将 JYACS（Just Yuri AI Chat System）的设置界面完全集成到 JY 1.10.11 的原生设置系统中。目标是在保持 JY 原有设置界面风格和技术规格的基础上，在其设置页面下方添加 JYACS 的专属设置区域，实现无缝融合。这将为用户提供统一、美观且功能完整的设置体验。

## Requirements

### Requirement 1: 研究和分析 JY 1.10.11 设置系统

**User Story:** 作为开发者，我需要深入理解 JY 1.10.11 的设置系统实现方式，以便能够完美复制其技术规格和视觉风格。

#### Acceptance Criteria

1. WHEN 开始集成工作 THEN 系统 SHALL 完整分析 JY 1.10.11 的 screens.rpy 中的 preferences screen 实现
2. WHEN 分析设置界面 THEN 系统 SHALL 识别所有使用的样式定义（style）、布局结构（vbox/hbox）和组件类型
3. WHEN 研究技术规格 THEN 系统 SHALL 记录字体、颜色、间距、边框等视觉参数
4. WHEN 分析交互逻辑 THEN 系统 SHALL 理解 bar、textbutton、label 等组件的使用方式
5. IF 发现自定义组件 THEN 系统 SHALL 记录其实现细节和使用场景

### Requirement 2: 设计 JYACS 设置区域布局

**User Story:** 作为用户，我希望 JYACS 设置能够自然地融入 JY 的设置界面，看起来就像原生功能一样。

#### Acceptance Criteria

1. WHEN 设计布局 THEN 系统 SHALL 将 JYACS 设置区域放置在 JY 原有设置内容的下方
2. WHEN 组织设置项 THEN 系统 SHALL 使用与 JY 相同的分组和层级结构
3. WHEN 设计视觉效果 THEN 系统 SHALL 采用与 JY 完全一致的字体、颜色方案和间距
4. WHEN 设计交互元素 THEN 系统 SHALL 使用与 JY 相同的按钮样式、滑块样式和输入框样式
5. IF 需要新的视觉元素 THEN 系统 SHALL 确保其风格与 JY 原有元素协调一致

### Requirement 3: 实现 API 配置设置

**User Story:** 作为用户，我需要在设置界面中配置 API 密钥、API 地址和模型名称，以便连接到 AI 服务。

#### Acceptance Criteria

1. WHEN 显示 API 设置 THEN 系统 SHALL 创建"API 配置"分组标签
2. WHEN 显示 API 密钥 THEN 系统 SHALL 使用星号遮蔽显示，保护隐私
3. WHEN 用户点击 API 密钥输入框 THEN 系统 SHALL 显示输入对话框允许修改
4. WHEN 显示 API 地址 THEN 系统 SHALL 提供文本输入功能
5. WHEN 显示模型名称 THEN 系统 SHALL 提供文本输入功能
6. WHEN 用户修改任何 API 配置 THEN 系统 SHALL 将值保存到 persistent.jyacs_setting_dict
7. IF API 配置未设置 THEN 系统 SHALL 显示"未设置"提示文本

### Requirement 4: 实现连接状态显示和控制

**User Story:** 作为用户，我需要查看 JYACS 的连接状态，并能够手动连接或断开连接。

#### Acceptance Criteria

1. WHEN 显示连接状态 THEN 系统 SHALL 创建"连接状态"分组标签
2. WHEN 显示状态信息 THEN 系统 SHALL 实时显示当前连接状态
3. WHEN 显示消息队列 THEN 系统 SHALL 实时显示消息队列长度
4. WHEN 用户点击"连接"按钮 THEN 系统 SHALL 调用 store.jyacs.init_connect() 函数
5. WHEN 用户点击"断开"按钮 THEN 系统 SHALL 调用 store.jyacs.close_wss_session() 函数
6. WHEN 用户点击"验证配置"按钮 THEN 系统 SHALL 调用 store.jyacs_verify_api_config() 函数
7. IF 操作成功或失败 THEN 系统 SHALL 提供适当的视觉反馈

### Requirement 5: 实现高级设置入口

**User Story:** 作为高级用户，我需要访问超参数设置（temperature、top_p 等），以便精细调整 AI 行为。

#### Acceptance Criteria

1. WHEN 显示 JYACS 设置区域 THEN 系统 SHALL 提供"高级设置"按钮
2. WHEN 用户点击"高级设置"按钮 THEN 系统 SHALL 打开独立的高级设置界面
3. WHEN 显示高级设置界面 THEN 系统 SHALL 使用与主设置相同的视觉风格
4. WHEN 显示超参数 THEN 系统 SHALL 为每个参数提供滑块控制
5. WHEN 显示参数值 THEN 系统 SHALL 实时显示当前数值
6. WHEN 用户调整参数 THEN 系统 SHALL 将值保存到 persistent.jyacs_advanced_setting
7. IF 用户点击"返回" THEN 系统 SHALL 关闭高级设置界面返回主设置

### Requirement 6: 实现超参数设置界面

**User Story:** 作为高级用户，我需要调整 Temperature、Top P、Max Tokens、Frequency Penalty 和 Presence Penalty 等参数。

#### Acceptance Criteria

1. WHEN 显示 Temperature 设置 THEN 系统 SHALL 提供 0-1.0 范围的滑块，步长 0.01
2. WHEN 显示 Top P 设置 THEN 系统 SHALL 提供 0.1-0.9 范围的滑块，步长 0.01
3. WHEN 显示 Max Tokens 设置 THEN 系统 SHALL 提供 0-2048 范围的滑块，步长 1
4. WHEN 显示 Frequency Penalty 设置 THEN 系统 SHALL 提供 0-1.0 范围的滑块，步长 0.01
5. WHEN 显示 Presence Penalty 设置 THEN 系统 SHALL 提供 0-1.0 范围的滑块，步长 0.01
6. WHEN 用户调整任何参数 THEN 系统 SHALL 实时更新显示的数值
7. WHEN 用户保存设置 THEN 系统 SHALL 调用 store.jyacs_apply_advanced_setting() 函数

### Requirement 7: 保持现有功能完整性

**User Story:** 作为用户，我期望所有现有的 JYACS 设置功能都能正常工作，不会因为界面改变而丢失任何功能。

#### Acceptance Criteria

1. WHEN 集成完成后 THEN 系统 SHALL 保留所有原有的 API 配置功能
2. WHEN 集成完成后 THEN 系统 SHALL 保留所有原有的连接控制功能
3. WHEN 集成完成后 THEN 系统 SHALL 保留所有原有的高级设置功能
4. WHEN 用户保存设置 THEN 系统 SHALL 正确调用 store.jyacs_apply_setting() 函数
5. WHEN 用户修改高级设置 THEN 系统 SHALL 正确调用 store.jyacs_apply_advanced_setting() 函数
6. IF 存在其他设置相关函数 THEN 系统 SHALL 确保它们都能正常调用

### Requirement 8: 优化用户体验

**User Story:** 作为用户，我希望设置界面响应迅速、操作直观，并提供清晰的反馈信息。

#### Acceptance Criteria

1. WHEN 设置界面加载 THEN 系统 SHALL 在 1 秒内完成渲染
2. WHEN 用户进行任何操作 THEN 系统 SHALL 提供即时的视觉反馈
3. WHEN 显示设置项 THEN 系统 SHALL 使用清晰的中文标签
4. WHEN 设置项过多 THEN 系统 SHALL 提供滚动功能确保所有内容可访问
5. IF 操作失败 THEN 系统 SHALL 显示友好的错误提示
6. IF 操作成功 THEN 系统 SHALL 显示成功确认信息

### Requirement 9: 确保代码质量和可维护性

**User Story:** 作为开发者，我需要代码结构清晰、注释完整，以便未来维护和扩展。

#### Acceptance Criteria

1. WHEN 编写代码 THEN 系统 SHALL 遵循 Ren'Py 最佳实践
2. WHEN 定义样式 THEN 系统 SHALL 使用清晰的命名约定
3. WHEN 实现功能 THEN 系统 SHALL 添加适当的中文注释
4. WHEN 组织代码 THEN 系统 SHALL 保持逻辑分组和层次清晰
5. IF 需要修改现有代码 THEN 系统 SHALL 最小化对原有代码的影响
6. IF 创建新文件 THEN 系统 SHALL 遵循项目的文件组织结构

### Requirement 10: 测试和验证

**User Story:** 作为开发者，我需要确保集成后的设置界面在各种情况下都能正常工作。

#### Acceptance Criteria

1. WHEN 测试界面显示 THEN 系统 SHALL 验证所有设置项正确显示
2. WHEN 测试数据持久化 THEN 系统 SHALL 验证设置能够正确保存和加载
3. WHEN 测试交互功能 THEN 系统 SHALL 验证所有按钮和输入框正常工作
4. WHEN 测试边界情况 THEN 系统 SHALL 验证空值、极值等情况的处理
5. WHEN 测试兼容性 THEN 系统 SHALL 验证与 JY 原有功能不冲突
6. IF 发现问题 THEN 系统 SHALL 记录并修复所有发现的缺陷

# JYACS 设置菜单独立化 - 部署指南

## 部署概述
本指南说明如何将更新后的 `jyacs_ui_hooks.rpy` 文件部署到游戏中。

## 部署前检查

### 1. 确认文件完整性
确认以下文件存在：
- [x] `jyacs_ui_hooks.rpy` - 更新后的主文件
- [x] `jyacs_ui_hooks.rpy.backup` - 备份文件

### 2. 确认代码更新
确认 `jyacs_ui_hooks.rpy` 包含以下新增内容：
- [x] `init -500 screen game_menu()` 定义
- [x] JYACS 设置按钮（在 ypos 460 位置）

## 部署步骤

### 方案 A: 直接部署（推荐用于开发测试）

#### 步骤 1: 复制文件到游戏目录
```bash
# 如果 jyacs_ui_hooks.rpy 已经在游戏目录中，则无需操作
# 如果不在，则复制到游戏的 game 目录
```

当前文件位置：
- 源文件：`D:\dokiproject\cursor\jyacs_ui_hooks.rpy`
- 目标位置：`JY1.10.11/DDLC-1.1.1-pc/game/jyacs_ui_hooks.rpy`

#### 步骤 2: 启动游戏测试
1. 启动游戏
2. 按照 `TESTING_GUIDE.md` 进行测试

### 方案 B: 打包部署（推荐用于发布）

#### 步骤 1: 准备部署包
创建一个部署文件夹，包含以下文件：
```
JYACS_Settings_Menu_Update/
├── jyacs_ui_hooks.rpy
├── README.md (安装说明)
└── CHANGELOG.md (更新日志)
```

#### 步骤 2: 创建安装说明
在 README.md 中说明：
1. 备份原有的 `jyacs_ui_hooks.rpy` 文件
2. 将新的 `jyacs_ui_hooks.rpy` 复制到游戏的 game 目录
3. 启动游戏测试

#### 步骤 3: 创建更新日志
在 CHANGELOG.md 中记录：
- 新增功能：JYACS 设置菜单独立化
- 改动内容：在游戏菜单添加 JYACS 设置按钮
- 影响范围：UI 界面

## 部署验证

### 快速验证清单
部署后进行以下快速验证：

1. [ ] 游戏能正常启动
2. [ ] 打开游戏菜单，看到 JYACS 设置按钮
3. [ ] 点击按钮，JYACS 设置界面正常打开
4. [ ] 基础设置和高级设置标签页正常切换
5. [ ] 保存设置功能正常
6. [ ] 返回和 ESC 关闭功能正常

如果以上验证都通过，则部署成功！

## 回滚步骤

如果部署后出现问题，可以按以下步骤回滚：

### 步骤 1: 恢复备份文件
```bash
# 将备份文件恢复
Copy-Item jyacs_ui_hooks.rpy.backup jyacs_ui_hooks.rpy
```

### 步骤 2: 重启游戏
重新启动游戏，确认恢复到之前的状态。

## 部署到生产环境

### 准备工作
1. 完成所有测试（参考 `TESTING_GUIDE.md`）
2. 确认没有已知问题
3. 准备发布说明

### 发布清单
- [ ] 代码审查完成
- [ ] 测试通过
- [ ] 文档更新完成
- [ ] 备份文件准备完成
- [ ] 发布说明准备完成

### 发布步骤
1. 创建发布版本标签（如 v2.1.0）
2. 打包部署文件
3. 发布到相应渠道
4. 通知用户更新

## 兼容性说明

### 游戏版本
- 目标游戏：Just Yuri (JY) 1.10.11
- 基于：DDLC 1.1.1

### 依赖项
- Ren'Py 引擎
- 原游戏的 `screens.rpy` 文件
- JYACS 框架的其他组件

### 已知兼容性问题
目前没有已知的兼容性问题。

## 故障排除

### 问题 1: 游戏启动失败
**症状**: 游戏启动时显示错误信息

**解决方案**:
1. 检查错误信息，定位问题代码
2. 确认 `jyacs_ui_hooks.rpy` 文件没有语法错误
3. 如果无法解决，回滚到备份文件

### 问题 2: JYACS 设置按钮不显示
**症状**: 游戏菜单中看不到 JYACS 设置按钮

**解决方案**:
1. 确认 `jyacs_ui_hooks.rpy` 文件已正确部署
2. 确认文件包含 `init -500 screen game_menu()` 定义
3. 检查是否有其他 mod 冲突

### 问题 3: 点击按钮无反应
**症状**: 点击 JYACS 设置按钮后没有任何反应

**解决方案**:
1. 检查控制台是否有错误信息
2. 确认 `jyacs_detailed_settings` screen 已定义
3. 确认 action 设置正确

## 技术支持

### 日志文件位置
如果遇到问题，可以查看以下日志文件：
- `log.txt` - 游戏运行日志
- `errors.txt` - 错误日志
- `traceback.txt` - 详细错误追踪

### 联系方式
如果需要技术支持，请提供：
1. 问题描述
2. 错误信息（如果有）
3. 日志文件
4. 游戏版本和 JYACS 版本

## 附录

### 文件清单
部署涉及的所有文件：

| 文件名 | 位置 | 说明 |
|--------|------|------|
| jyacs_ui_hooks.rpy | game/ | 主要实现文件 |
| jyacs_ui_hooks.rpy.backup | 备份位置 | 备份文件 |
| IMPLEMENTATION_SUMMARY.md | .kiro/specs/separate-jyacs-settings-menu/ | 实现总结 |
| TESTING_GUIDE.md | .kiro/specs/separate-jyacs-settings-menu/ | 测试指南 |
| DEPLOYMENT_GUIDE.md | .kiro/specs/separate-jyacs-settings-menu/ | 部署指南 |

### 版本历史
- v2.1.0 (2025-01-18): JYACS 设置菜单独立化
  - 新增：game_menu override
  - 新增：JYACS 设置按钮
  - 改进：UI 组织结构

### 相关文档
- `requirements.md` - 需求文档
- `design.md` - 设计文档
- `tasks.md` - 任务列表
- `IMPLEMENTATION_SUMMARY.md` - 实现总结
- `TESTING_GUIDE.md` - 测试指南

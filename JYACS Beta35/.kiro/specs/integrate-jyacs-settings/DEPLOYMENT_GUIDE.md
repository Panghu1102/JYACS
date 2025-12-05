# JYACS 设置界面集成 - 部署指南

## 快速部署

### 前提条件

确保你有以下文件：
- ✅ JY 1.10.11 游戏本体（在 `JY1.10.11/` 目录）
- ✅ JYACS 子 mod 文件（在项目根目录）

### 部署步骤

#### 1. 复制文件到游戏目录

将以下文件复制到 `JY1.10.11/DDLC-1.1.1-pc/game/` 目录：

```
项目根目录/
├── jyacs_ui_hooks.rpy       → 复制到 game/
├── jyacs_settings.rpy       → 复制到 game/
├── jyacs_init.rpy           → 复制到 game/
├── jyacs_api.rpy            → 复制到 game/
├── jyacs_main.rpy           → 复制到 game/
├── jyacs_framework.rpy      → 复制到 game/
├── jyacs_expressions.rpy    → 复制到 game/
├── jyacs_emotion_images.rpy → 复制到 game/
├── jyacs_stub.rpy           → 复制到 game/
├── dev.rpy                  → 复制到 game/
├── header.rpy               → 复制到 game/
└── python-packages/         → 复制整个目录到 game/
```

#### 2. 启动游戏

1. 运行 `JY1.10.11/DDLC-1.1.1-pc/DDLC.exe`
2. 等待游戏加载完成
3. 检查控制台是否有错误信息

#### 3. 验证安装

1. 按 `ESC` 键打开菜单
2. 选择 "Settings"
3. 滚动到底部
4. 确认看到 "JYACS 设置" 区域

如果看到 JYACS 设置区域，说明安装成功！

---

## 详细部署说明

### Windows 部署

#### 方法 1: 手动复制（推荐）

1. 打开文件资源管理器
2. 导航到项目根目录
3. 选择所有 `.rpy` 文件
4. 复制（Ctrl+C）
5. 导航到 `JY1.10.11/DDLC-1.1.1-pc/game/`
6. 粘贴（Ctrl+V）
7. 如果提示覆盖，选择"替换"

#### 方法 2: 使用批处理脚本

创建 `deploy.bat` 文件：

```batch
@echo off
echo 正在部署 JYACS 到 JY 1.10.11...

set SOURCE=.
set TARGET=JY1.10.11\DDLC-1.1.1-pc\game

echo 复制 .rpy 文件...
copy /Y "%SOURCE%\*.rpy" "%TARGET%\"

echo 复制 python-packages 目录...
xcopy /E /I /Y "%SOURCE%\python-packages" "%TARGET%\python-packages"

echo 复制 mod_assets 目录...
xcopy /E /I /Y "%SOURCE%\mod_assets" "%TARGET%\mod_assets"

echo 部署完成！
pause
```

运行 `deploy.bat` 即可自动部署。

### Linux/Mac 部署

创建 `deploy.sh` 文件：

```bash
#!/bin/bash
echo "正在部署 JYACS 到 JY 1.10.11..."

SOURCE="."
TARGET="JY1.10.11/DDLC-1.1.1-pc/game"

echo "复制 .rpy 文件..."
cp -f $SOURCE/*.rpy $TARGET/

echo "复制 python-packages 目录..."
cp -rf $SOURCE/python-packages $TARGET/

echo "复制 mod_assets 目录..."
cp -rf $SOURCE/mod_assets $TARGET/

echo "部署完成！"
```

运行：
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 配置说明

### 首次配置

1. 启动游戏
2. 按 `ESC` → "Settings" → 滚动到底部
3. 点击 "详细设置"
4. 在 "基础设置" 标签页中配置：
   - **API 密钥**: 你的 API 密钥
   - **API 地址**: API 服务器地址（如 `https://api.example.com`）
   - **模型名称**: 模型名称（如 `jyacs_main`）
5. 点击 "保存设置"
6. 点击 "验证配置" 测试连接

### 推荐配置

#### 基础设置
- ✅ 自动连接: 开启
- ✅ 自动重连: 开启
- ✅ 启用触发器: 开启
- ✅ 启用情绪识别: 开启
- ⬜ 回复时显示控制台: 关闭（调试时开启）
- ✅ 启用 Mspire: 开启
- ⬜ 严格模式: 关闭

#### 高级设置
- **Temperature**: 0.7（创造性和一致性的平衡）
- **Top P**: 0.9（推荐值）
- **Max Tokens**: 2048（根据需要调整）
- **Frequency Penalty**: 0.0（默认）
- **Presence Penalty**: 0.0（默认）

---

## 故障排除

### 问题 1: 看不到 JYACS 设置区域

**可能原因**:
- 文件未正确复制
- 游戏缓存未清除

**解决方案**:
1. 删除 `game/cache/` 目录
2. 重新启动游戏
3. 确认 `jyacs_ui_hooks.rpy` 存在于 `game/` 目录

### 问题 2: 点击"详细设置"无反应

**可能原因**:
- Screen 定义有错误
- 依赖文件缺失

**解决方案**:
1. 检查控制台错误信息
2. 确认所有 `.rpy` 文件都已复制
3. 检查 `jyacs_ui_hooks.rpy` 的语法

### 问题 3: 设置无法保存

**可能原因**:
- 持久化数据未初始化
- 写入权限问题

**解决方案**:
1. 确认 `jyacs_init.rpy` 已正确加载
2. 检查游戏目录的写入权限
3. 尝试以管理员身份运行游戏

### 问题 4: API 连接失败

**可能原因**:
- API 配置错误
- 网络问题
- API 服务器不可达

**解决方案**:
1. 检查 API 密钥是否正确
2. 检查 API 地址格式（需要包含 `http://` 或 `https://`）
3. 测试网络连接
4. 查看控制台的详细错误信息

### 问题 5: 游戏启动变慢

**可能原因**:
- Python 包加载时间
- 初始化逻辑复杂

**解决方案**:
1. 这是正常现象，首次启动会稍慢
2. 后续启动会使用缓存，速度会提升
3. 如果持续很慢，检查 `python-packages/` 目录大小

### 问题 6: 字体显示异常

**可能原因**:
- JY 字体文件缺失
- 字体路径错误

**解决方案**:
1. 确认 `gui/font/RifficFree-Bold.ttf` 存在
2. 确认 `gui/font/Halogen.ttf` 存在
3. 如果字体缺失，从 JY 原版复制

---

## 卸载说明

如需卸载 JYACS 设置界面集成：

### 完全卸载

1. 删除以下文件：
   ```
   game/jyacs_ui_hooks.rpy
   game/jyacs_ui_hooks.rpyc
   game/jyacs_settings.rpy
   game/jyacs_settings.rpyc
   game/jyacs_init.rpy
   game/jyacs_init.rpyc
   game/jyacs_api.rpy
   game/jyacs_api.rpyc
   game/jyacs_main.rpy
   game/jyacs_main.rpyc
   game/jyacs_framework.rpy
   game/jyacs_framework.rpyc
   game/jyacs_expressions.rpy
   game/jyacs_expressions.rpyc
   game/jyacs_emotion_images.rpy
   game/jyacs_emotion_images.rpyc
   game/jyacs_stub.rpy
   game/jyacs_stub.rpyc
   game/dev.rpy
   game/dev.rpyc
   game/header.rpy
   game/header.rpyc
   ```

2. 删除目录：
   ```
   game/python-packages/
   game/mod_assets/
   ```

3. 删除缓存：
   ```
   game/cache/
   ```

4. 重新启动游戏

### 仅卸载设置界面

如果只想移除设置界面集成，保留其他 JYACS 功能：

1. 删除 `game/jyacs_ui_hooks.rpy` 和 `.rpyc`
2. 恢复 `game/jyacs_settings.rpy` 到 v1.0.0 版本
3. 删除缓存并重启游戏

---

## 更新说明

### 从 v1.0.0 更新到 v2.0.0

1. **备份设置**:
   - 记录当前的 API 配置
   - 记录当前的高级设置

2. **更新文件**:
   - 复制新的 `jyacs_ui_hooks.rpy`
   - 复制新的 `jyacs_settings.rpy`
   - 覆盖其他更新的文件

3. **清除缓存**:
   - 删除 `game/cache/` 目录

4. **重新配置**:
   - 启动游戏
   - 重新输入 API 配置
   - 验证设置是否正常工作

### 未来更新

当有新版本发布时：

1. 查看 CHANGELOG 了解变更
2. 备份当前配置
3. 按照新版本的部署指南操作
4. 测试所有功能

---

## 性能优化

### 减少启动时间

1. **清理不需要的 Python 包**:
   ```
   python-packages/
   ├── 保留必需的包
   └── 删除未使用的包
   ```

2. **禁用不需要的功能**:
   - 如果不需要情绪识别，在设置中关闭
   - 如果不需要 Mspire，在设置中关闭

### 减少内存占用

1. **调整 Max Tokens**:
   - 如果不需要长回复，降低 Max Tokens 值
   - 推荐值: 1024-2048

2. **关闭调试功能**:
   - 关闭"回复时显示控制台"
   - 设置日志级别为 WARNING 或 ERROR

---

## 安全建议

### 保护 API 密钥

1. **不要分享存档**:
   - 存档中包含 API 密钥
   - 分享前先删除或重置密钥

2. **定期更换密钥**:
   - 建议每月更换一次 API 密钥
   - 如果怀疑泄露，立即更换

3. **使用环境变量**（高级）:
   - 可以修改代码从环境变量读取密钥
   - 避免在存档中存储明文密钥

### 网络安全

1. **使用 HTTPS**:
   - 确保 API 地址使用 `https://`
   - 避免使用不安全的 `http://`

2. **验证证书**:
   - 确保 API 服务器证书有效
   - 不要忽略证书警告

---

## 开发者部署

### 开发环境设置

1. **使用符号链接**（推荐）:
   ```bash
   # Linux/Mac
   ln -s /path/to/project/*.rpy /path/to/game/
   
   # Windows (需要管理员权限)
   mklink /H "game\jyacs_ui_hooks.rpy" "project\jyacs_ui_hooks.rpy"
   ```

2. **使用版本控制**:
   - 将 `game/` 目录加入 `.gitignore`
   - 只跟踪项目根目录的源文件

3. **自动部署脚本**:
   - 使用 `deploy.bat` 或 `deploy.sh`
   - 配置 IDE 的构建后事件

### 调试技巧

1. **启用开发者模式**:
   - 在 `options.rpy` 中设置 `config.developer = True`
   - 可以使用 Shift+D 打开开发者菜单

2. **查看日志**:
   - 日志文件位于 `game/log.txt`
   - 错误信息位于 `game/traceback.txt`

3. **使用控制台**:
   - 开启"回复时显示控制台"
   - 可以实时查看 JYACS 的运行状态

---

## 生产环境部署

### 发布前检查清单

- [ ] 所有文件已复制
- [ ] 缓存已清除
- [ ] 设置界面正常显示
- [ ] JY 原有功能正常
- [ ] API 连接测试通过
- [ ] 设置保存和加载正常
- [ ] 游戏重启后设置保持
- [ ] 无控制台错误
- [ ] 性能测试通过
- [ ] 文档已更新

### 发布包准备

1. **创建发布目录**:
   ```
   JYACS-v2.0.0/
   ├── README.md
   ├── CHANGELOG.md
   ├── LICENSE
   ├── game/
   │   ├── jyacs_ui_hooks.rpy
   │   ├── jyacs_settings.rpy
   │   ├── jyacs_init.rpy
   │   ├── jyacs_api.rpy
   │   ├── jyacs_main.rpy
   │   ├── jyacs_framework.rpy
   │   ├── jyacs_expressions.rpy
   │   ├── jyacs_emotion_images.rpy
   │   ├── jyacs_stub.rpy
   │   ├── dev.rpy
   │   ├── header.rpy
   │   ├── python-packages/
   │   └── mod_assets/
   └── docs/
       ├── INSTALLATION.md
       ├── CONFIGURATION.md
       └── TROUBLESHOOTING.md
   ```

2. **创建安装说明**:
   - 简明的安装步骤
   - 配置示例
   - 常见问题解答

3. **打包发布**:
   ```bash
   zip -r JYACS-v2.0.0.zip JYACS-v2.0.0/
   ```

---

## 支持和反馈

### 获取帮助

1. **查看文档**:
   - README.md
   - TESTING_GUIDE.md
   - 本文档

2. **检查已知问题**:
   - 查看 IMPLEMENTATION_SUMMARY.md 的"已知限制"部分

3. **联系开发者**:
   - 提供详细的错误信息
   - 包含 `log.txt` 和 `traceback.txt`
   - 说明重现步骤

### 报告问题

提交问题时请包含：

1. **环境信息**:
   - 操作系统和版本
   - JY 版本
   - JYACS 版本

2. **问题描述**:
   - 详细的问题描述
   - 预期行为
   - 实际行为

3. **重现步骤**:
   - 一步步的操作步骤
   - 截图或视频（如果可能）

4. **日志文件**:
   - `game/log.txt`
   - `game/traceback.txt`
   - 控制台输出

---

## 总结

按照本指南，你应该能够成功部署 JYACS 设置界面集成。如果遇到问题，请参考故障排除部分或联系支持。

祝你使用愉快！🎉

# JYACS 部署指南

## 概述

JYACS (JustYuriAIChatSubmod) 是一个为 Doki Doki Literature Club 设计的AI聊天子模组。本指南将帮助您正确部署和配置JYACS系统。

## 文件结构

```
DDLC_JYACS/
├── game/
│   ├── python-packages/          # Python模块包
│   │   ├── jyacs_core.py         # JYACS核心模块
│   │   ├── jyacs_interface.py    # JYACS接口模块
│   │   ├── jyacs_emotion.py      # JYACS情绪分析模块
│   │   ├── jyacs_trigger.py      # JYACS触发器模块
│   │   ├── jyacs_utils.py        # JYACS工具模块
│   │   └── [其他依赖包...]
│   ├── script.rpy                # 主脚本文件
│   ├── options.rpy               # 配置文件
│   ├── mas_framework.rpy         # MAS框架模拟
│   ├── header.rpy                # JYACS主界面
│   ├── jyacs_api.rpy             # JYACS API核心
│   ├── dev.rpy                   # 文本处理模块
│   ├── main.rpy                  # 主要功能实现
│   └── mod_assets/               # 资源文件夹
│       ├── font/                 # 字体文件
│       ├── images/               # 图像资源
│       └── audio/                # 音频资源
├── README.md                     # 项目说明
└── DEPLOYMENT.md                 # 部署指南
```

## 部署步骤

### 1. 准备DDLC基础环境

1. **下载DDLC原版**
   - 从官方网站下载 Doki Doki Literature Club
   - 确保版本为最新稳定版

2. **备份原版文件**
   - 复制整个DDLC文件夹作为备份
   - 重命名备份文件夹为 `DDLC_Backup`

### 2. 安装JYACS文件

1. **复制核心文件**
   ```bash
   # 将以下文件复制到DDLC的game目录
   cp script.rpy DDLC/game/
   cp options.rpy DDLC/game/
   cp mas_framework.rpy DDLC/game/
   cp header.rpy DDLC/game/
   cp jyacs_api.rpy DDLC/game/
   cp dev.rpy DDLC/game/
   cp main.rpy DDLC/game/
   ```

2. **安装Python包**
   ```bash
   # 创建python-packages目录
   mkdir -p DDLC/game/python-packages
   
   # 复制所有Python模块
   cp python-packages/* DDLC/game/python-packages/
   ```

3. **安装资源文件**
   ```bash
   # 创建mod_assets目录
   mkdir -p DDLC/game/mod_assets
   
   # 复制字体文件
   cp font/SarasaMonoTC-SemiBold.ttf DDLC/game/mod_assets/font/
   
   

### 3. 配置JYACS

1. **启动游戏**
   - 运行 `DDLC.exe`
   - 进入游戏主菜单

2. **访问JYACS设置**
   - 在游戏菜单中选择 "设置"
   - 找到 "JYACS AI聊天" 选项
   - 点击进入JYACS设置界面

3. **配置API设置**
   - **API密钥**: 输入您的AI服务API密钥
   - **API地址**: 输入API服务地址
   - **模型名称**: 选择使用的AI模型

4. **高级设置** (可选)
   - **温度**: 控制AI回复的随机性 (0.0-1.0)
   - **Top P**: 控制词汇选择的多样性 (0.0-1.0)
   - **最大令牌数**: 限制回复长度
   - **频率惩罚**: 减少重复词汇
   - **存在惩罚**: 减少重复主题

### 4. 验证安装

1. **检查模块加载**
   - 查看游戏控制台输出
   - 确认没有模块导入错误
   - 检查日志文件 `jyacs.log`

2. **测试连接**
   - 在JYACS设置中点击 "测试连接"
   - 确认API配置正确
   - 验证网络连接正常

3. **测试聊天功能**
   - 进入聊天界面
   - 发送测试消息
   - 确认AI能够正常回复

## 配置选项

### API配置

| 选项 | 说明 | 默认值 |
|------|------|--------|
| API密钥 | AI服务的访问密钥 | 空 |
| API地址 | AI服务的API地址 | 空 |
| 模型名称 | 使用的AI模型 | jyacs_main |

### 高级设置

| 选项 | 说明 | 范围 | 默认值 |
|------|------|------|--------|
| 温度 | 控制回复随机性 | 0.0-1.0 | 0.7 |
| Top P | 控制词汇多样性 | 0.0-1.0 | 0.9 |
| 最大令牌数 | 回复最大长度 | 1-4096 | 2048 |
| 频率惩罚 | 减少重复词汇 | 0.0-1.0 | 0.0 |
| 存在惩罚 | 减少重复主题 | 0.0-1.0 | 0.0 |

### 功能开关

| 功能 | 说明 | 默认状态 |
|------|------|----------|
| 自动连接 | 启动时自动连接API | 开启 |
| 自动重连 | 连接断开时自动重连 | 开启 |
| 触发器 | 启用文本触发器 | 开启 |
| 情绪分析 | 启用情绪分析 | 开启 |

## 故障排除

### 常见问题

1. **模块导入失败**
   ```
   错误: JYACS模块导入失败，使用模拟模式
   ```
   **解决方案**: 
   - 检查 `python-packages` 目录是否存在
   - 确认所有Python文件已正确复制
   - 检查Python版本兼容性

2. **API连接失败**
   ```
   错误: 无法连接服务器，请检查网络
   ```
   **解决方案**:
   - 检查网络连接
   - 验证API地址是否正确
   - 确认API密钥有效
   - 检查防火墙设置

3. **游戏崩溃**
   ```
   错误: Ren'Py脚本错误
   ```
   **解决方案**:
   - 检查所有.rpy文件语法
   - 确认文件编码为UTF-8
   - 查看错误日志获取详细信息

4. **字体显示异常**
   ```
   错误: 字体文件未找到
   ```
   **解决方案**:
   - 确认字体文件已复制到正确位置
   - 检查字体文件名是否正确
   - 验证字体文件完整性

### 日志文件

JYACS会生成详细的日志文件，位置：
- `DDLC/game/jyacs.log` - 主要日志文件
- `DDLC/game/jyacs_config.json` - 配置文件
- `DDLC/game/jyacs_triggers.json` - 触发器配置

### 调试模式

启用调试模式以获取更详细的错误信息：

1. 编辑 `jyacs_utils.py`
2. 将日志级别设置为 `DEBUG`
3. 重启游戏
4. 查看控制台输出和日志文件

## 性能优化

### 内存优化

1. **限制历史记录**
   - 设置合理的最大历史记录数量
   - 定期清理旧消息

2. **优化文本处理**
   - 调整分句器参数
   - 限制单次处理文本长度

### 网络优化

1. **连接池管理**
   - 复用WebSocket连接
   - 实现连接超时机制

2. **请求优化**
   - 批量处理请求
   - 实现请求缓存

## 安全注意事项

1. **API密钥保护**
   - 不要在代码中硬编码API密钥
   - 使用环境变量或配置文件
   - 定期更换API密钥

2. **数据隐私**
   - 本地存储聊天记录
   - 不向第三方分享用户数据
   - 实现数据加密

3. **网络安全**
   - 使用HTTPS/WSS连接
   - 验证API服务器证书
   - 实现请求签名验证

## 更新和维护

### 版本更新

1. **备份当前配置**
   ```bash
   cp DDLC/game/jyacs_config.json backup/
   cp DDLC/game/jyacs_triggers.json backup/
   ```

2. **更新文件**
   - 下载新版本文件
   - 替换旧版本文件
   - 保留用户配置

3. **验证更新**
   - 测试所有功能
   - 检查配置兼容性
   - 更新文档

### 定期维护

1. **日志清理**
   - 定期清理旧日志文件
   - 压缩历史日志

2. **配置备份**
   - 定期备份用户配置
   - 验证备份完整性

3. **性能监控**
   - 监控内存使用
   - 检查网络连接状态
   - 分析错误日志

## 技术支持

如果您遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查日志文件获取错误详情
3. 在GitHub Issues中搜索类似问题
4. 创建新的Issue并提供详细信息

### 有用的链接

- [JYACS GitHub仓库](https://github.com/panghu1102/JYACS)
- [DDLC官方网站](https://ddlc.moe/)
- [Ren'Py文档](https://www.renpy.org/doc/html/)

---

**注意**: 本部署指南适用于JYACS 1.0.0版本。如果您使用其他版本，请参考对应版本的文档。 
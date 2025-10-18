# JYACS Python Packages

这个目录包含了JYACS所需的所有Python模块。

## 模块说明

- `jyacs_utils.py`: 工具模块，提供日志记录、配置管理等功能
- `jyacs_emotion.py`: 情绪分析模块，处理文本情绪和表情选择
- `jyacs_interface.py`: 接口模块，提供文本处理和分句功能

## 依赖说明

JYACS需要以下Python包：

- `chardet`: 用于字符编码检测
- `logging`: Python标准库，用于日志记录
- `json`: Python标准库，用于JSON处理
- `os`, `sys`, `time`: Python标准库，用于系统操作

## 安装说明

1. 这些模块已经包含在JYACS发布包中，无需额外安装
2. 所有依赖都是Python标准库或已包含在Ren'Py中
3. `chardet`库已经包含在Ren'Py中，无需额外安装

## 使用说明

1. 这些模块会在游戏启动时自动加载
2. 所有功能都通过`store`注册到Ren'Py中
3. 可以通过`store.jyacs_*`访问相关功能

## 注意事项

1. 不要直接修改这些文件，除非你知道自己在做什么
2. 所有配置都应该通过游戏内的设置界面进行
3. 如果遇到问题，请查看日志文件了解详情 
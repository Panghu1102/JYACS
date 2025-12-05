# System Prompt 加载问题修复 - 设计文档

## 概述

本设计文档描述了修复 JYACS system prompt 加载问题的技术方案。问题的根本原因是配置被多次加载，且在加载失败时使用了简化版的默认提示词，导致新的完整版提示词没有被应用。

## 问题根本原因分析

### 场景 C：配置被覆盖

经过分析，确定问题属于"场景 C"：

1. **重复加载问题**
   - `JyacsAi.__init__()` 中调用 `_load_config()`
   - `init -750` 阶段创建实例后又调用 `reload_config()`
   - `set_api()` 方法中也会调用 `_load_config()`
   - 多次加载可能导致后续加载失败并覆盖之前成功加载的配置

2. **默认提示词问题**
   - 配置加载失败时使用的默认提示词是简化版：
     ```python
     "你是优里，来自心跳文学部。你现在独自与玩家在太空教室中对话..."
     ```
   - 而不是配置文件中的完整版（包含 Role、Skills、Background、Rules 等）

3. **路径解析问题**
   - 使用 `__file__` 在 Ren'Py 环境中可能不可靠
   - 应该使用 `renpy.config.gamedir` 或 `renpy.config.basedir`

4. **日志覆盖问题**
   - 日志文件使用 `"w"` 模式，每次写入都会覆盖之前的内容
   - 导致无法看到完整的加载过程

## 架构设计

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                    JyacsAi 类                           │
├─────────────────────────────────────────────────────────┤
│ 属性:                                                   │
│  - system_prompt: str                                   │
│  - user_prompt_template: str                            │
│  - _config_loaded: bool  [新增]                         │
│                                                         │
│ 方法:                                                   │
│  - __init__()                                           │
│  - _load_config()           [改进]                      │
│  - _use_default_config()    [新增]                      │
│  - reload_config(force)     [改进]                      │
│  - set_api()                [改进]                      │
│  - chat()                   [增强日志]                  │
└─────────────────────────────────────────────────────────┘
```

### 配置加载流程

```
游戏启动
    │
    ├─> init -1400: 定义 JyacsAi 类
    │   └─> 定义 DEFAULT_SYSTEM_PROMPT 常量
    │
    ├─> init -750: 创建 store.jyacs 实例
    │   └─> JyacsAi.__init__()
    │       └─> _load_config()
    │           ├─> 尝试从文件加载
    │           │   ├─> 成功: 设置 _config_loaded = True
    │           │   └─> 失败: 调用 _use_default_config()
    │           │
    │           └─> _use_default_config()
    │               └─> 使用 DEFAULT_SYSTEM_PROMPT
    │
    └─> 验证配置加载状态
        └─> 输出详细日志
```

### 配置重载机制

```
用户调用 reload_config()
    │
    ├─> 检查 _config_loaded 标志
    │   ├─> 已加载 && !force: 跳过
    │   └─> 未加载 || force: 继续
    │
    └─> 调用 _load_config()
        └─> 重新加载配置
```

## 数据模型

### 配置文件结构

```json
{
    "version": "1.0.0",
    "prompts": {
        "system_prompt": "完整的系统提示词...",
        "user_prompt_template": "用户消息模板..."
    },
    "api_config": {
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 2048
    }
}
```

### 默认配置常量

```python
DEFAULT_SYSTEM_PROMPT = """
Role: Yuri (《Doki Doki Literature Club》中的角色)
Profile
...
[完整的提示词内容]
"""

DEFAULT_USER_PROMPT_TEMPLATE = "[player]说：{message}..."
```

## 关键修改点

### 1. 添加配置加载状态标志

```python
class JyacsAi:
    def __init__(self):
        # ...
        self._config_loaded = False  # 新增标志
```

**目的**: 防止重复加载导致的覆盖问题

### 2. 改进路径解析逻辑

**修改前**:
```python
current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, "python-packages", "jyacs_config.json")
```

**修改后**:
```python
config_path = os.path.join(renpy.config.gamedir, "python-packages", "jyacs_config.json")
```

**原因**: `__file__` 在 Ren'Py 环境中不可靠，应使用 Ren'Py 提供的路径配置

### 3. 使用完整的默认提示词

**修改前**:
```python
self.system_prompt = "你是优里，来自心跳文学部。你现在独自与玩家在太空教室中对话..."
```

**修改后**:
```python
self.system_prompt = DEFAULT_SYSTEM_PROMPT  # 完整版提示词
```

**原因**: 确保即使配置加载失败，也使用与配置文件相同的完整提示词

### 4. 创建独立的默认配置方法

```python
def _use_default_config(self):
    """使用默认配置（与配置文件中的完整版本一致）"""
    self.content_func("使用默认系统提示词（完整版）", "INFO")
    self.system_prompt = DEFAULT_SYSTEM_PROMPT
    self.user_prompt_template = DEFAULT_USER_PROMPT_TEMPLATE
    self._config_loaded = True
```

**目的**: 统一默认配置的使用，避免代码重复

### 5. 改进 reload_config 方法

```python
def reload_config(self, force=False):
    if self._config_loaded and not force:
        self.content_func("配置已加载，跳过重复加载", "DEBUG")
        return "配置已加载"
    
    self.content_func("重新加载配置文件...", "INFO")
    self._load_config()
    return "配置文件已重新加载"
```

**目的**: 防止意外的重复加载

### 6. 移除 set_api 中的自动重载

**修改前**:
```python
def set_api(self, key, url, model):
    # ...
    self._load_config()  # 自动重新加载
```

**修改后**:
```python
def set_api(self, key, url, model):
    # ...
    # 不再自动重新加载配置文件
```

**原因**: 避免设置 API 时意外覆盖已加载的配置

### 7. 修复日志文件写入模式

**修改前**:
```python
with open(log_file, "w", encoding="utf-8") as f:  # 覆盖模式
    f.write(log_entry)
```

**修改后**:
```python
with open(log_file, "a", encoding="utf-8") as f:  # 追加模式
    f.write(log_entry)
```

**原因**: 保留完整的日志历史，便于诊断问题

### 8. 增强日志输出

在关键位置添加详细的日志：

- 初始化完成时输出配置状态
- 加载配置时输出路径和结果
- 发送 API 请求时输出实际使用的 system_prompt

## 错误处理策略

### 配置加载失败的处理流程

```
尝试加载配置文件
    │
    ├─> FileNotFoundError
    │   └─> 记录警告 + 使用默认配置
    │
    ├─> json.JSONDecodeError
    │   └─> 记录错误 + 使用默认配置
    │
    └─> Exception (其他错误)
        └─> 记录错误 + 详细堆栈 + 使用默认配置
```

### 日志级别使用

- **INFO**: 正常操作（配置加载成功、API 设置更新）
- **DEBUG**: 调试信息（路径尝试、配置内容预览）
- **WARNING**: 警告信息（配置文件不存在、使用默认配置）
- **ERROR**: 错误信息（JSON 解析失败、异常捕获）

## 测试策略

### 单元测试场景

1. **配置文件存在且格式正确**
   - 预期: 成功加载，`_config_loaded = True`
   - 验证: `system_prompt` 长度 > 2000 字符

2. **配置文件不存在**
   - 预期: 使用默认配置，`_config_loaded = True`
   - 验证: `system_prompt == DEFAULT_SYSTEM_PROMPT`

3. **配置文件格式错误**
   - 预期: 捕获异常，使用默认配置
   - 验证: 日志包含 "JSON 解析失败"

4. **重复调用 reload_config()**
   - 预期: 第二次调用被跳过
   - 验证: 日志包含 "跳过重复加载"

5. **强制重新加载**
   - 预期: `reload_config(force=True)` 成功重新加载
   - 验证: 日志包含 "重新加载配置文件"

### 集成测试场景

1. **游戏启动流程**
   - 启动游戏
   - 检查日志文件
   - 验证配置加载状态

2. **API 请求验证**
   - 发送聊天消息
   - 检查日志中的 system_prompt 内容
   - 验证 AI 响应符合新提示词要求

3. **配置重载测试**
   - 修改配置文件
   - 调用 `reload_config(force=True)`
   - 验证新配置生效

## 性能考虑

### 配置加载优化

- 配置只在初始化时加载一次
- 使用 `_config_loaded` 标志避免重复加载
- 文件读取使用缓冲 I/O

### 日志性能

- 日志写入使用追加模式，避免读取整个文件
- 日志级别可配置，生产环境可关闭 DEBUG 日志

## 安全考虑

### 路径安全

- 使用 Ren'Py 提供的配置路径，避免路径遍历攻击
- 不接受用户输入的配置文件路径

### 配置验证

- 验证配置文件结构
- 验证 API URL 格式
- 敏感信息（API 密钥）在日志中脱敏

## 部署注意事项

### 文件位置

配置文件必须位于以下位置之一：
- `{game_dir}/python-packages/jyacs_config.json`
- `{base_dir}/game/python-packages/jyacs_config.json`
- `{base_dir}/python-packages/jyacs_config.json`

### 日志文件

日志文件位置：`{game_dir}/../JYACS console.txt`

### 兼容性

- 支持 Python 2.7 和 Python 3.x
- 支持 Windows、macOS、Linux
- 兼容 Ren'Py 6.99+ 和 7.x

## 回滚计划

如果修复导致问题：

1. **立即回滚**: 恢复 `jyacs_api.rpy` 到修改前的版本
2. **保留日志**: 保存 `JYACS console.txt` 用于分析
3. **问题报告**: 记录具体的错误信息和复现步骤

## 后续改进建议

1. **配置 UI**: 添加游戏内配置查看和编辑界面
2. **配置验证**: 添加配置文件格式验证工具
3. **热重载**: 支持不重启游戏的配置热重载
4. **配置备份**: 自动备份配置文件
5. **诊断工具**: 添加配置诊断命令

## 成功标准

修复完成后，系统应该满足：

✅ 游戏启动时成功加载完整的 system_prompt  
✅ 日志文件清楚显示配置加载过程  
✅ 发送到 API 的请求包含完整的新版 system_prompt  
✅ AI 的响应符合新提示词的要求（只输出台词，无动作描写）  
✅ 配置加载失败时使用完整的默认提示词  
✅ 避免重复加载导致的配置覆盖问题  
✅ 日志文件保留完整的历史记录  

## 总结

本次修复通过以下关键改进解决了 system prompt 加载问题：

1. 使用完整的默认提示词常量
2. 改进路径解析逻辑（使用 Ren'Py 配置路径）
3. 添加配置加载状态标志，防止重复加载
4. 修复日志文件写入模式（追加而非覆盖）
5. 增强错误处理和日志输出
6. 移除不必要的自动重载逻辑

这些改进确保了即使在配置加载失败的情况下，系统也能使用与配置文件相同的完整提示词，从而保证 AI 的响应质量。

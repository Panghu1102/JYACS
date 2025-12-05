# System Prompt 加载问题 - 详细诊断计划

## 执行摘要

这不是一个简单的"创建几个文件"就能解决的问题。这是一个**系统性的配置加载失败问题**，需要：
1. 深入理解 Ren'Py 的文件系统和初始化机制
2. 追踪配置加载的完整生命周期
3. 识别多个可能的失败点
4. 实施针对性的修复方案

## 问题分析

### 已知事实
1. ✅ `jyacs_config.json` 文件存在且格式正确
2. ✅ 代码中有 `_load_config()` 方法来加载配置
3. ✅ 代码中有日志记录配置加载状态
4. ❌ 实际运行时使用的是旧版简易提示词
5. ❌ 新版提示词没有被应用到 API 请求中

### 关键疑点

#### 疑点 1: `__file__` 在 Ren'Py 中的行为
```python
# jyacs_api.rpy 第 103 行
current_dir = os.path.dirname(__file__)
```

**问题**: 
- 在 Ren'Py 的 `init python` 块中，`__file__` 可能未定义
- 即使定义了，它可能指向 `.rpyc` 编译文件而不是源文件
- 这会导致路径解析完全错误

**验证方法**:
```python
print("DEBUG: __file__ = {}".format(__file__ if '__file__' in dir() else 'UNDEFINED'))
print("DEBUG: current_dir = {}".format(os.path.dirname(__file__) if '__file__' in dir() else 'N/A'))
```

#### 疑点 2: 配置文件路径解析失败
```python
# 当前逻辑
config_path = os.path.join(current_dir, "python-packages", "jyacs_config.json")

# 备用路径
alt_paths = [
    os.path.join(current_dir, "..", "python-packages", "jyacs_config.json"),
    os.path.abspath("python-packages/jyacs_config.json"),
    os.path.join(os.getcwd(), "python-packages", "jyacs_config.json")
]
```

**问题**:
- 如果 `current_dir` 是错误的，所有路径都会错误
- `os.getcwd()` 在 Ren'Py 中可能指向游戏根目录或其他位置
- 备用路径可能都无法找到文件

**正确的 Ren'Py 路径应该是**:
```python
# 使用 Ren'Py 的配置对象
config_path = os.path.join(renpy.config.gamedir, "python-packages", "jyacs_config.json")
# 或者
config_path = os.path.join(renpy.config.basedir, "game", "python-packages", "jyacs_config.json")
```

#### 疑点 3: 异常被静默捕获
```python
except Exception as e:
    self.content_func("加载配置文件失败: {}".format(str(e)), "ERROR")
    # 使用默认系统提示
    self.system_prompt = "你是优里，来自心跳文学部..."
```

**问题**:
- 异常被捕获后，使用了默认提示词
- 用户可能没有看到错误日志
- 日志文件可能没有被正确写入

#### 疑点 4: 日志文件写入问题
```python
def jyacs_log(message, level="INFO"):
    try:
        log_file = os.path.join(renpy.config.gamedir, "..", "JYACS console.txt")
        with open(log_file, "w", encoding="utf-8") as f:  # ⚠️ 注意这里是 "w" 模式
            f.write(log_entry)
```

**严重问题**:
- 使用 `"w"` 模式会**覆盖**整个日志文件
- 每次写入都会删除之前的所有日志
- 这导致我们无法看到完整的加载过程

#### 疑点 5: 初始化顺序问题
```python
# jyacs_api.rpy
init -1400 python:
    class JyacsAi:
        def __init__(self):
            self._load_config()  # 在 __init__ 中加载

# jyacs_api.rpy
init -750 python:
    if not hasattr(store, 'jyacs'):
        store.jyacs = JyacsAi()
        store.jyacs.reload_config()  # 又重新加载一次
```

**问题**:
- 配置被加载了两次
- 第二次加载可能失败并使用默认值
- 初始化顺序可能导致依赖问题

#### 疑点 6: JSON 文件格式问题
虽然文件看起来格式正确，但可能存在：
- 隐藏的 BOM 字符
- 不可见的控制字符
- 换行符问题（Windows vs Unix）
- 编码问题（虽然指定了 UTF-8）

## 诊断步骤

### 步骤 1: 创建增强的诊断版本（不破坏现有代码）

创建一个独立的诊断脚本 `jyacs_diagnostic.rpy`：

```python
init -1350 python:
    def jyacs_diagnose_config():
        """诊断配置加载问题"""
        import os
        import json
        
        print("\n" + "="*60)
        print("JYACS 配置诊断开始")
        print("="*60)
        
        # 1. 检查 __file__ 变量
        print("\n[1] 检查 __file__ 变量:")
        try:
            print("  __file__ = {}".format(__file__))
            print("  dirname(__file__) = {}".format(os.path.dirname(__file__)))
        except NameError:
            print("  ⚠️ __file__ 未定义!")
        
        # 2. 检查 Ren'Py 路径
        print("\n[2] 检查 Ren'Py 路径:")
        print("  renpy.config.gamedir = {}".format(renpy.config.gamedir))
        print("  renpy.config.basedir = {}".format(renpy.config.basedir))
        print("  os.getcwd() = {}".format(os.getcwd()))
        
        # 3. 尝试所有可能的配置文件路径
        print("\n[3] 尝试查找配置文件:")
        possible_paths = [
            os.path.join(renpy.config.gamedir, "python-packages", "jyacs_config.json"),
            os.path.join(renpy.config.basedir, "game", "python-packages", "jyacs_config.json"),
            os.path.join(renpy.config.basedir, "python-packages", "jyacs_config.json"),
            os.path.abspath("python-packages/jyacs_config.json"),
            os.path.join(os.getcwd(), "python-packages", "jyacs_config.json"),
        ]
        
        found_path = None
        for i, path in enumerate(possible_paths, 1):
            exists = os.path.exists(path)
            print("  [{}] {} - {}".format(i, "✓" if exists else "✗", path))
            if exists and found_path is None:
                found_path = path
        
        # 4. 尝试加载配置文件
        if found_path:
            print("\n[4] 尝试加载配置文件: {}".format(found_path))
            try:
                with open(found_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print("  ✓ 文件读取成功，大小: {} 字节".format(len(content)))
                
                config = json.loads(content)
                print("  ✓ JSON 解析成功")
                
                if "prompts" in config:
                    print("  ✓ 找到 'prompts' 部分")
                    if "system_prompt" in config["prompts"]:
                        prompt = config["prompts"]["system_prompt"]
                        print("  ✓ 找到 'system_prompt'，长度: {} 字符".format(len(prompt)))
                        print("  前 100 个字符: {}...".format(prompt[:100]))
                    else:
                        print("  ✗ 缺少 'system_prompt'")
                else:
                    print("  ✗ 缺少 'prompts' 部分")
                    
            except Exception as e:
                print("  ✗ 加载失败: {}".format(e))
                import traceback
                traceback.print_exc()
        else:
            print("\n[4] ✗ 未找到配置文件!")
        
        # 5. 检查当前 jyacs 实例的配置
        print("\n[5] 检查当前 jyacs 实例:")
        if hasattr(store, 'jyacs'):
            print("  ✓ store.jyacs 存在")
            print("  system_prompt 长度: {}".format(len(store.jyacs.system_prompt)))
            print("  前 100 个字符: {}...".format(store.jyacs.system_prompt[:100]))
            print("  user_prompt_template: {}".format(store.jyacs.user_prompt_template[:100] if len(store.jyacs.user_prompt_template) > 100 else store.jyacs.user_prompt_template))
        else:
            print("  ✗ store.jyacs 不存在")
        
        print("\n" + "="*60)
        print("诊断完成")
        print("="*60 + "\n")

# 在 jyacs 实例创建后立即运行诊断
init -740 python:
    if hasattr(store, 'jyacs'):
        jyacs_diagnose_config()
```

### 步骤 2: 修复日志文件写入问题

```python
def jyacs_log(message, level="INFO"):
    """将日志写入文件"""
    try:
        import os
        log_dir = os.path.join(renpy.config.gamedir, "..")
        log_file = os.path.join(log_dir, "JYACS console.txt")
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = "[{}] [JYACS-{}] {}\n".format(timestamp, level, message)
        
        # ⚠️ 改为追加模式 "a" 而不是覆盖模式 "w"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(u"[JYACS-LOGFAIL] [{}]: {} ({})".format(level, message, e))
```

### 步骤 3: 修复路径解析问题

```python
def _load_config(self):
    """加载配置文件"""
    try:
        # ⚠️ 使用 Ren'Py 的配置路径而不是 __file__
        config_path = os.path.join(renpy.config.gamedir, "python-packages", "jyacs_config.json")
        
        self.content_func("尝试加载配置文件: {}".format(config_path), "INFO")
        
        if not os.path.exists(config_path):
            # 尝试备用路径
            alt_path = os.path.join(renpy.config.basedir, "game", "python-packages", "jyacs_config.json")
            self.content_func("主路径不存在，尝试备用路径: {}".format(alt_path), "INFO")
            if os.path.exists(alt_path):
                config_path = alt_path
            else:
                raise FileNotFoundError("配置文件不存在于任何已知路径")
        
        self.content_func("找到配置文件: {}".format(config_path), "INFO")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # ... 其余加载逻辑
```

### 步骤 4: 增强错误处理和日志

```python
def _load_config(self):
    """加载配置文件"""
    try:
        # ... 加载逻辑
        
        # 验证加载的内容
        if self.system_prompt:
            self.content_func("✓ 成功加载系统提示，长度: {} 字符".format(len(self.system_prompt)), "INFO")
            self.content_func("✓ 系统提示前 200 字符: {}...".format(self.system_prompt[:200]), "DEBUG")
        else:
            self.content_func("⚠️ 警告: 系统提示为空", "WARNING")
            raise ValueError("系统提示为空")
            
    except FileNotFoundError as e:
        self.content_func("✗ 配置文件不存在: {}".format(e), "ERROR")
        self._use_default_config()
    except json.JSONDecodeError as e:
        self.content_func("✗ JSON 解析失败: {}".format(e), "ERROR")
        self._use_default_config()
    except Exception as e:
        self.content_func("✗ 加载配置文件失败: {}".format(e), "ERROR")
        import traceback
        self.content_func("完整错误信息:\n{}".format(traceback.format_exc()), "ERROR")
        self._use_default_config()

def _use_default_config(self):
    """使用默认配置"""
    self.content_func("使用默认配置", "WARNING")
    self.system_prompt = "你是优里，来自心跳文学部..."
    self.user_prompt_template = "{message}"
```

### 步骤 5: 在 API 请求时记录实际内容

```python
def chat(self, message):
    """发送聊天消息"""
    try:
        # ... 构建消息
        
        messages = []
        messages.append({"role": "system", "content": self.system_prompt})
        
        # ⚠️ 记录实际发送的内容
        self.content_func("=" * 60, "DEBUG")
        self.content_func("发送 API 请求", "DEBUG")
        self.content_func("System Prompt 长度: {} 字符".format(len(self.system_prompt)), "DEBUG")
        self.content_func("System Prompt 前 200 字符: {}...".format(self.system_prompt[:200]), "DEBUG")
        self.content_func("User Message: {}".format(message), "DEBUG")
        self.content_func("=" * 60, "DEBUG")
        
        # ... 发送请求
```

## 预期的诊断结果

运行诊断后，我们应该能看到：

### 场景 A: 路径问题
```
[1] 检查 __file__ 变量:
  ⚠️ __file__ 未定义!

[3] 尝试查找配置文件:
  [1] ✗ D:/dokiproject/cursor/game/python-packages/jyacs_config.json
  [2] ✓ D:/dokiproject/cursor/python-packages/jyacs_config.json
```
**解决方案**: 修改路径解析逻辑，使用 `renpy.config.basedir`

### 场景 B: JSON 解析问题
```
[4] 尝试加载配置文件:
  ✓ 文件读取成功
  ✗ JSON 解析失败: Expecting property name enclosed in double quotes
```
**解决方案**: 修复 JSON 文件格式

### 场景 C: 配置被覆盖
```
[5] 检查当前 jyacs 实例:
  ✓ store.jyacs 存在
  system_prompt 长度: 67
  前 100 个字符: 你是优里，来自心跳文学部。你现在独自与玩家在太空教室中对话...
```
**解决方案**: 检查初始化顺序，确保配置不被覆盖

## 修复优先级

1. **P0 - 立即修复**: 日志文件写入模式（从 "w" 改为 "a"）
2. **P0 - 立即修复**: 路径解析逻辑（使用 `renpy.config.gamedir`）
3. **P1 - 高优先级**: 增强错误处理和日志记录
4. **P1 - 高优先级**: 添加诊断工具
5. **P2 - 中优先级**: 验证 JSON 文件格式
6. **P2 - 中优先级**: 检查初始化顺序
7. **P3 - 低优先级**: 添加配置验证 UI

## 下一步行动

1. **立即执行**: 创建诊断脚本并运行
2. **收集信息**: 查看诊断输出，确定根本原因
3. **实施修复**: 根据诊断结果应用针对性修复
4. **验证修复**: 测试配置加载和 API 请求
5. **文档更新**: 记录问题原因和解决方案

## 注意事项

⚠️ **不要低估这个问题的复杂性**

这不是简单的"文件不存在"问题，而是涉及：
- Ren'Py 的文件系统抽象
- Python 模块加载机制
- 初始化顺序依赖
- 错误处理和日志记录
- 跨平台路径处理

需要系统性的诊断和修复，不能仓促行事。

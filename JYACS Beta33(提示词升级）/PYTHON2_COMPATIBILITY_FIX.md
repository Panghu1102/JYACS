# Python 2 兼容性修复

## 问题描述

游戏启动时出现以下错误：
```
AttributeError: 'module' object has no attribute 'JSONDecodeError'
```

## 根本原因

**Ren'Py 7.3.5 使用 Python 2.7**，而 `json.JSONDecodeError` 是 Python 3.5+ 才引入的异常类。

在 Python 2 中：
- `json.loads()` 解析失败时抛出 `ValueError`
- 没有 `json.JSONDecodeError` 这个类

在 Python 3.5+ 中：
- `json.loads()` 解析失败时抛出 `json.JSONDecodeError`
- `json.JSONDecodeError` 继承自 `ValueError`

## 修复内容

### 1. jyacs_api.rpy (第 166-170 行)

**修复前：**
```python
except json.JSONDecodeError as e:
    self.content_func("JSON 解析失败: {}，使用默认配置".format(str(e)), "ERROR")
    self._use_default_config()
```

**修复后：**
```python
except ValueError as e:
    # Python 2 中 json.loads 抛出 ValueError 而不是 JSONDecodeError
    self.content_func("JSON 解析失败: {}，使用默认配置".format(str(e)), "ERROR")
    self._use_default_config()
```

### 2. python-packages/jyacs_utils.py (第 132 行)

**修复前：**
```python
except (IOError, json.JSONDecodeError) as e:
```

**修复后：**
```python
except (IOError, ValueError) as e:
    # Python 2 兼容性: json.loads 抛出 ValueError 而不是 JSONDecodeError
```

### 3. python-packages/fix_json.py (第 115-118 行)

**修复前：**
```python
except json.JSONDecodeError as e:
    logger.error("解析配置文件失败: %s", e)
    return None
```

**修复后：**
```python
except ValueError as e:
    # Python 2 兼容性: json.loads 抛出 ValueError 而不是 JSONDecodeError
    logger.error("解析配置文件失败: %s", e)
    return None
```

## 为什么使用 ValueError 是安全的

1. **向后兼容**: 在 Python 2 中，`json.loads()` 抛出 `ValueError`
2. **向前兼容**: 在 Python 3 中，`json.JSONDecodeError` 继承自 `ValueError`，所以 `except ValueError` 也能捕获 `JSONDecodeError`
3. **最佳实践**: 对于需要同时支持 Python 2 和 3 的代码，使用 `ValueError` 是标准做法

## 验证

修复后，游戏应该能够正常启动，并且：
- 如果配置文件存在且格式正确，会成功加载
- 如果配置文件格式错误，会捕获异常并使用默认配置
- 不会再出现 `AttributeError` 错误

## 下一步

现在错误已修复，可以继续诊断原始问题：**为什么新的 system prompt 没有被应用**。

建议：
1. 启动游戏，查看日志输出
2. 检查配置文件是否被成功加载
3. 验证实际发送到 API 的 system_prompt 内容

## 相关文件

- `jyacs_api.rpy` - 主要的 API 类
- `python-packages/jyacs_utils.py` - 工具函数
- `python-packages/fix_json.py` - 配置文件生成器
- `python-packages/jyacs_config.json` - 配置文件（包含新的 system prompt）

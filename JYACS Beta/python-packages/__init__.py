# python-packages/__init__.py
# JYACS Python 包初始化文件
# 版本: 1.0.0
# 作者: Panghu1102

"""
JYACS Python 包

这个包包含了 JYACS (JustYuriAIChatSubmod) 的核心 Python 模块：

- jyacs_interface: 文本处理和分句功能
- jyacs_emotion: 情绪分析功能  
- jyacs_utils: 日志记录和工具函数

使用示例:
    from jyacs_interface import JyacsTalkSplitV2, key_replace
    from jyacs_emotion import JyacsEmoSelector
    from jyacs_utils import jyacs_logger
"""

__version__ = "1.0.0"
__author__ = "Panghu1102"

# 设置默认值，以防导入失败
JyacsTalkSplitV2 = None
key_replace = None
add_pauses = None
JyacsTextProcessor = None
JyacsEmoSelector = None
JyacsEmotionAnalyzer = None
JyacsLogger = None
JyacsConfig = None
JyacsFileUtils = None
JyacsTimeUtils = None
JyacsTextUtils = None
jyacs_logger = None
jyacs_config = None

# 导入主要模块
try:
    from .jyacs_interface import JyacsTalkSplitV2, key_replace, add_pauses, JyacsTextProcessor
    from .jyacs_emotion import JyacsEmoSelector, JyacsEmotionAnalyzer
    from .jyacs_utils import JyacsLogger, JyacsConfig, JyacsFileUtils, JyacsTimeUtils, JyacsTextUtils, jyacs_logger, jyacs_config
except ImportError as e:
    import sys
    print(f"JYACS Python 包导入错误: {e}")
    print(f"Python 路径: {sys.path}")
    
    # 尝试单独导入每个模块，以便更好地定位问题
    try:
        from .jyacs_interface import JyacsTalkSplitV2, key_replace, add_pauses, JyacsTextProcessor
    except ImportError as e:
        print(f"jyacs_interface 导入错误: {e}")
        
    try:
        from .jyacs_emotion import JyacsEmoSelector, JyacsEmotionAnalyzer
    except ImportError as e:
        print(f"jyacs_emotion 导入错误: {e}")
        
    try:
        from .jyacs_utils import JyacsLogger, JyacsConfig, JyacsFileUtils, JyacsTimeUtils, JyacsTextUtils, jyacs_logger, jyacs_config
    except ImportError as e:
        print(f"jyacs_utils 导入错误: {e}")

# 导出主要类和函数
__all__ = [
    # jyacs_interface
    'JyacsTalkSplitV2',
    'key_replace', 
    'add_pauses',
    'JyacsTextProcessor',
    
    # jyacs_emotion
    'JyacsEmoSelector',
    'JyacsEmotionAnalyzer',
    
    # jyacs_utils
    'JyacsLogger',
    'JyacsConfig', 
    'JyacsFileUtils',
    'JyacsTimeUtils',
    'JyacsTextUtils',
    'jyacs_logger',
    'jyacs_config'
] 
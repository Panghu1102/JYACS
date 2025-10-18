# -*- coding: utf-8 -*-
# __init__.py - JYACS Python 包初始化
# 版本: 1.0.0
# 作者: Panghu1102

"""
JYACS Python 包
提供 JYACS (Just Yuri AI Chat Submod) 的核心功能。
"""

__version__ = "1.0.0"
__author__ = "Panghu1102"

from .jyacs_utils import JyacsLogger, JyacsConfig
from .jyacs_emotion import JyacsEmoSelector
from .jyacs_interface import JyacsTalkSplitV2, JyacsTextProcessor, key_replace, add_pauses

__all__ = [
    "JyacsLogger",
    "JyacsConfig",
    "JyacsEmoSelector",
    "JyacsTalkSplitV2",
    "JyacsTextProcessor",
    "key_replace",
    "add_pauses"
] 
# Copyright 2025 Panghu1102
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# __init__.py - JYACS Python 包初始化
# 版本: 1.0.1
# 作者: Panghu1102

"""
JYACS Python 包
提供 JYACS (Just Yuri AI Chat Submod) 的核心功能。
"""

__version__ = "1.0.1"
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
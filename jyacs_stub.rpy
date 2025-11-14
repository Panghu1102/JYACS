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
# jyacs_stub.rpy – JYACS依赖
# 开发人员注意，这玩意是为了兼容jy写的，不是必要的开发文件，如果你想做jn或者fae的话

# 使用更低的优先级以确保不会干扰主游戏初始化
init -1500 python:
    # Import required modules inside init block to prevent early execution
    import types
    import logging
    import store

    # Python 2.7 compatible SimpleNamespace
    try:
        from types import SimpleNamespace
    except ImportError:
        class SimpleNamespace(object):
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
            def __repr__(self):
                keys = sorted(self.__dict__)
                items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
                return "{}({})".format(type(self).__name__, ", ".join(items))
            def __eq__(self, other):
                return self.__dict__ == other.__dict__

    # ------------------------------------------------------------------
    # Generic no-op helpers ------------------------------------------------
    # ------------------------------------------------------------------
    def _noop(*_args, **_kwargs):
        """A do-nothing placeholder function."""
        return None

    def _decorator_noop(*_dargs, **_dkwargs):
        """Return a decorator that leaves the wrapped function untouched."""
        def _wrap(fn):
            return fn
        return _wrap

    # ------------------------------------------------------------------
    # 兼容JY......我恨jy，以及我之前半夜瞎写的代码----------------------------------------
    # ------------------------------------------------------------------
    if not hasattr(store, "jyacs_submod_utils"):
        store.jyacs_submod_utils = SimpleNamespace()
        store.jyacs_submod_utils.Submod = _noop
        store.jyacs_submod_utils.getAndRunFunctions = _noop
        store.jyacs_submod_utils.functionplugin = _decorator_noop
        store.jyacs_submod_utils.submod_log = SimpleNamespace()
        store.jyacs_submod_utils.submod_log.level = logging.INFO
        store.jyacs_submod_utils.isSubmodInstalled = lambda name: False

    # ------------------------------------------------------------------
    # 创建JY相关的命名空间
    # ------------------------------------------------------------------
    if not hasattr(store, "jy_submod_utils"):
        store.jy_submod_utils = store.jyacs_submod_utils

    # 提供JY相关的UI对象
    if not hasattr(store, "jy_ptod"):
        store.jy_ptod = SimpleNamespace()
        store.jy_ptod.font = "mod_assets/font/SarasaMonoTC-SemiBold.ttf"

    if not hasattr(store, "jy_ui"):
        store.jy_ui = SimpleNamespace()
        store.jy_ui.MONO_FONT = "mod_assets/font/SarasaMonoTC-SemiBold.ttf"

# 确保游戏标题正确设置，使用更低的优先级
init -1600 python:
    # 确保游戏标题正确设置
    # 许多Ren'Py项目（包括Just Yuri）在options.rpy中通过config.name或gui.window_title设置显示标题。
    # 如果初始化早期的错误阻止options.rpy执行，窗口会回退到通用的"A Ren'Py Game"字符串。
    # 在这里设置一个安全的默认值，确保即使其他脚本错误发生，标题也保持正确。
    # 为什么会覆盖标题呀！真无语了，老子真服气了，谁写的renpy...
    # 我们只在尚未定义名称时设置它，以避免在已存在时覆盖真实值。
    if not getattr(config, "name", None):
        config.name = "Just Yuri with JYACS 1.0.0"
        print("JYACS: 已设置游戏标题为 'Just Yuri'")
    
    if not getattr(config, "window_title", None):
        config.window_title = "Just Yuri"
        print("JYACS: 已设置窗口标题为 'Just Yuri'")

# 添加更多的兼容性函数和变量
init -1400 python:
    if not hasattr(store, "getAPIKey"):
        store.getAPIKey = lambda *_args, **_kwargs: ""

    # JY辅助函数-------------------
    jy_helpers = {
        "_jy_getAffection": (lambda *_a, **_k: 0),
        "jy_getAffection": (lambda *_a, **_k: 0),
        "jy_getEV": (lambda *_a, **_k: None),
        "jy_inEVL": (lambda *_a, **_k: False),
    }
    
    # 将每个辅助函数添加到store中
    for _name, _default in jy_helpers.items():
        if not hasattr(store, _name):
            setattr(store, _name, _default)

    if not hasattr(store, "jy_rev_unseen"):
        store.jy_rev_unseen = []
        
    if not hasattr(store, "player"):
        store.player = "Player"
        
    def getEV(name):
        """Placeholder for event access function"""
        return None
        
    if not hasattr(store, "getEV"):
        store.getEV = getEV
        
    if not hasattr(store, "jyacs_chat_history"):
        store.jyacs_chat_history = []
        
    if not hasattr(store, "jyacs_log"):
        def jyacs_log(message, level="INFO"):
            """Simple logging function"""
            print("[JYACS-{}] {}".format(level, message))
        store.jyacs_log = jyacs_log
        
    # 确保基本变量存在
    if not hasattr(store, "jyacs_chr_exist"):
        store.jyacs_chr_exist = False
        
    if not hasattr(store, "jyacs_chr_changed"):
        store.jyacs_chr_changed = False
        
    # 确保jyacs_confont变量存在
    if not hasattr(store, "jyacs_confont"):
        store.jyacs_confont = "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
        
    # 确保基本函数存在
    if not hasattr(store, "_jyacs_verify_token"):
        def _jyacs_verify_token():
            """验证令牌的占位函数"""
            return True
        store._jyacs_verify_token = _jyacs_verify_token
        
    # 确保登录变量存在
    if not hasattr(store, "_jyacs_LoginAcc"):
        store._jyacs_LoginAcc = ""
    if not hasattr(store, "_jyacs_LoginPw"):
        store._jyacs_LoginPw = ""
    if not hasattr(store, "_jyacs_LoginEmail"):
        store._jyacs_LoginEmail = ""

# 防止覆盖原游戏的标签
init -1300 python:
    # 确保不会覆盖原游戏的start标签
    if renpy.has_label("start"):
        print("JYACS: 检测到原游戏start标签，不会覆盖")
    else:
        print("JYACS: 未检测到原游戏start标签，这可能是个问题")
        
    # 检查并报告其他关键标签
    for label in ["splashscreen", "after_load", "quit"]:
        if renpy.has_label(label):
            print(u"JYACS: 检测到原游戏{}标签".format(label)) 
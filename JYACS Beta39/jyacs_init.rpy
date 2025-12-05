# jyacs_init.rpy - JYACS 初始化文件
# 版本: 1.0.0
# 作者: Panghu1102

# 使用更低的初始化优先级以避免干扰主游戏
init -1700 python:
    import sys
    import os
    import traceback

    # 1. 路径设置 (更稳健的方式)
    python_packages_path = os.path.join(config.gamedir, "python-packages")
    if not os.path.isdir(python_packages_path):
        python_packages_path = os.path.join(config.basedir, "python-packages")

    if os.path.isdir(python_packages_path):
        if python_packages_path not in sys.path:
            sys.path.insert(0, python_packages_path)
            print(u"JYACS: 已添加python-packages路径: {}".format(python_packages_path))
    else:
        # 如果路径不存在，尝试创建
        try:
            os.makedirs(python_packages_path, exist_ok=True)
            if python_packages_path not in sys.path:
                sys.path.insert(0, python_packages_path)
            print(u"JYACS: 'python-packages' 目录已创建于: {}".format(python_packages_path))
        except Exception as e:
            print(u"JYACS: 创建 'python-packages' 目录失败: {}".format(e))

init -1650 python:
    # 2. 基础持久化数据设置
    # 使用 hasattr 检查，避免重复定义
    if not hasattr(persistent, 'jyacs_setting_dict'):
        persistent.jyacs_setting_dict = {
            "api_key": "", "api_url": "", "model_name": "jyacs_main",
            "auto_connect": True, "auto_reconnect": True, "enable_triggers": True,
            "enable_emotion": True, "show_console_when_reply": False,
            "target_lang": "zh_cn", "use_custom_model_config": False,
            "strict_mode": False,
            "log_level": "INFO", "log_conlevel": "INFO"
        }
    
    if not hasattr(persistent, 'jyacs_advanced_setting'):
        persistent.jyacs_advanced_setting = {
            "temperature": 0.7, "top_p": 0.9, "max_tokens": 2048,
            "frequency_penalty": 0.0, "presence_penalty": 0.0,
            "mf_aggressive": False, "sfe_aggressive": False, "esc_aggressive": True,
            "nsfw_acceptive": True, "seed": 0, "_seed": "0"
        }
    
    if not hasattr(persistent, 'jyacs_advanced_setting_status'):
        persistent.jyacs_advanced_setting_status = {}
    
    if not hasattr(persistent, 'jyacs_log_history'):
        persistent.jyacs_log_history = []
    
    if not hasattr(persistent, '_jyacs_send_or_received_mpostals'):
        persistent._jyacs_send_or_received_mpostals = []
    
    # 确保玩家信息存在
    if not hasattr(persistent, 'jyacs_player_additions'):
        persistent.jyacs_player_additions = []

init -1600 python:
    # 3. 兼容性函数定义
    import logging
    
    # 进度条函数
    if not hasattr(store, 'jyacs_progress_bar'):
        def jyacs_progress_bar(percentage, current=None, total=None, bar_length=20):
            """进度条显示函数"""
            filled_length = int(round(bar_length * percentage / 100.0))
            bar = u'▇' * filled_length + u' ' * (bar_length - filled_length)
            
            if total is not None:
                return u'|{}| {}% | {} / {}'.format(bar, int(percentage), current, total)
            else:
                return u'|{}| {}%'.format(bar, int(percentage))
        store.jyacs_progress_bar = jyacs_progress_bar
    
    # 基本日志函数
    if not hasattr(store, 'jyacs_basic_log'):
        def jyacs_basic_log(message, level="INFO"):
            """基本日志记录函数"""
            try:
                print(u"[JYACS-{}] {}".format(level, message))
            except:
                print("[JYACS-{}] <encoding error>".format(level))
        store.jyacs_basic_log = jyacs_basic_log

    # 初始化函数
    def jyacs_late_init():
        """执行依赖于其他模块的初始化"""
        try:
            # 初始化情绪分析器
            try:
                from jyacs_emotion import JyacsEmotionAnalyzer
                store.emotion_analyzer = JyacsEmotionAnalyzer()
                print("JYACS: 情绪分析器已初始化")
                if hasattr(store, 'jyacs_logger') and store.jyacs_logger:
                    store.jyacs_logger.log_info("情绪分析器已初始化")
            except ImportError as e:
                print("JYACS: 无法导入情绪分析模块: {}".format(e))
                store.emotion_analyzer = None
            
            # 这里的代码依赖于 dev.rpy 和 jyacs_api.rpy 中加载的模块和函数
            if hasattr(store, 'jyacs_logger') and store.jyacs_logger:
                log_level_str = persistent.jyacs_setting_dict.get("log_level", "INFO").upper()
                log_level = getattr(logging, log_level_str, logging.INFO)
                store.jyacs_logger.logger.setLevel(log_level)
                store.jyacs_logger.log_info("JYACS 初始化完成")
            else:
                print("JYACS: Logger尚未初始化，跳过日志级别设置。")
        except Exception as e:
            print(u"JYACS 晚期初始化失败: {}".format(e))
            traceback.print_exc()

# 使用自定义标签，避免覆盖原游戏的after_load
label jyacs_after_load:
    python:
        jyacs_late_init()
    return

# 添加after_load钩子，但不覆盖原始标签
init 1500 python:
    # 安全地添加after_load钩子
    def jyacs_after_load_hook():
        """JYACS加载后钩子"""
        jyacs_late_init()
        return
    
    # 如果原始after_load存在，不要覆盖它
    if renpy.has_label("after_load"):
        print("JYACS: 检测到原始after_load标签，添加钩子")
        # 这里可以添加钩子代码，但我们使用更安全的方式
    else:
        print("JYACS: 未检测到原始after_load标签，创建新标签")
        
        # 定义一个安全的after_load标签
        @renpy.register_label("after_load")
        def _jyacs_after_load_label():
            jyacs_late_init()
            return
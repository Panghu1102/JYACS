# JYACS 逻辑文件
# 版本: 1.0.0
# 作者: Panghu1102

# 基础配置和路径设置
init -999 python:
    import store
    import os
    import sys
    import logging
    import json
    import copy
    import time
    import random
    import traceback
    import hashlib
    try:
        import chardet
    except ImportError:
        chardet = None

    # 版本信息
    JYACS_VERSION = "1.0.0"
    JYACS_AUTHOR = "Panghu1102"

# 持久化数据初始化
init -950 python:
    # 初始化默认设置
    if not hasattr(persistent, 'jyacs_setting_dict'):
        persistent.jyacs_setting_dict = {
            "api_key": "",
            "api_url": "",
            "model_name": "jyacs_main",
            "auto_connect": True,
            "auto_reconnect": True,
            "enable_triggers": True,
            "enable_emotion": True,
            "console": True,
            "show_console_when_reply": False,
            "target_lang": "zh_cn",
            "use_custom_model_config": False,
            "mspire_enable": True,
            "strict_mode": False,
            "console_font": "mod_assets/font/SarasaMonoTC-SemiBold.ttf",
            "log_level": "INFO",
            "log_conlevel": "INFO"
        }

    if not hasattr(persistent, 'jyacs_advanced_setting'):
        persistent.jyacs_advanced_setting = {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2048,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "seed": 0,
            "_seed": "0"
        }

    if not hasattr(persistent, 'jyacs_log_history'):
        persistent.jyacs_log_history = []

    if not hasattr(persistent, '_jyacs_send_or_received_mpostals'):
        persistent._jyacs_send_or_received_mpostals = []

# 检查JyacsProviderManager是否可用
init -800 python:
    if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'jyacs') and hasattr(store.jyacs.jyacs, 'JyacsProviderManager'):
        JyacsProviderManager = store.jyacs.jyacs.JyacsProviderManager
    else:
        # 创建默认的提供商管理器
        JyacsProviderManager = type(str('obj'), (object,), {
            'servers': [
                {'id': 1, 'name': 'JYACS官方服务器', 'deviceName': 'JYACS Official', 'servingModel': 'JYACS-Main', 'isOfficial': True},
                {'id': 2, 'name': '备用服务器', 'deviceName': 'Backup Server', 'servingModel': 'JYACS-Core', 'isOfficial': False}
            ],
            'get_server_by_id': lambda self, server_id: {'name': 'Unknown', 'deviceName': 'Unknown', 'servingModel': 'Unknown'},
            'get_provider': lambda self: []
        })

    def jyacs_reset_setting():
        """重置JYACS设置到默认值"""
        persistent.jyacs_setting_dict = jyacs_default_dict.copy()
        if hasattr(store, 'jyacs_log'):
            store.jyacs_log("JYACS设置已重置", "INFO")

    def _jyacs_verify_api_config():
        """验证API配置"""
        if not hasattr(store, 'jyacs') or not hasattr(store.jyacs, 'jyacs'):
            return {"success": False, "exception": "JYACS模块未加载"}

        res = store.jyacs.jyacs._verify_token()
        if res.get("success"):
            renpy.show_screen("jyacs_message", message=_("API配置验证成功"))
        else:
            renpy.show_screen("jyacs_message", message=renpy.substitute(_("API配置验证失败, 请检查API密钥和地址")) + "\n" + renpy.substitute(_("失败原因:")) + res.get("exception"))
        return res

    def _upload_persistent_dict():
        """上传持久化数据到JYACS"""
        if not hasattr(store, 'jyacs') or not hasattr(store.jyacs, 'jyacs'):
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("JYACS模块不可用，跳过数据上传", "WARNING")
            return

        maxlen = 1000
        import copy
        d = copy.deepcopy(persistent.__dict__)

        # 清理MAS特有的数据 - 保留清理逻辑但简化
        keys_to_clear = [
            '_seen_ever', '_mas_event_init_lockdb', '_changed', 'event_database',
            'farewell_database', 'greeting_database', '_mas_apology_database',
            'mas_compliments_database', '_mas_fun_facts_database', '_mas_mood_database',
            '_mas_songs_database', '_mas_story_database', '_mas_affection_backups'
        ]

        for key in keys_to_clear:
            if key in d:
                if isinstance(d[key], (list, dict)):
                    d[key].clear()
                else:
                    d[key] = None

        # 移除偏好设置
        if '_preferences' in d:
            del d['_preferences']

        # 添加玩家信息 - 简化处理
        if hasattr(store, 'player'):
            d['playername'] = store.player

        # 过滤数据 - 简化处理
        keys_to_remove = []
        for i in d.keys():
            try:
                json.dumps(d[i])
                if isinstance(d[i], (list, dict, str)) and len(d[i]) > maxlen:
                    d[i] = "REMOVED|TOO_LONG"
            except:
                try:
                    if len(str(d[i])) > maxlen:
                        d[i] = "REMOVED|TOO_LONG"
                except:
                    d[i] = "REMOVED"

        for key in keys_to_remove:
            del d[key]

        # 上传数据
        res = store.jyacs.jyacs.upload_save(d)
        if not res.get("success", False):
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("ERROR: upload save failed: {}".format(res.get("exception", "unknown")), "ERROR")
        renpy.notify(_("JYACS: 存档上传成功") if res.get("success", False) else _("JYACS: 存档上传失败"))

    def reset_session():
        """重置聊天会话"""
        if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'jyacs'):
            store.jyacs.jyacs.reset_chat_session()
        renpy.notify(_("JYACS: 会话已重置"))

    def output_chat_history():
        """导出聊天历史"""
        if not hasattr(store, 'jyacs') or not hasattr(store.jyacs, 'jyacs'):
            renpy.notify(_("JYACS: 模块不可用"))
            return

        import json
        try:
            os.makedirs(os.path.join(renpy.config.basedir, "game", "Submods", "JYACS_ChatSubmod"), exist_ok=True)
            with open(os.path.join(renpy.config.basedir, "game", "Submods", "JYACS_ChatSubmod", "chat_history.txt"), 'w', encoding='utf-8') as f:
                f.write(json.dumps(store.jyacs.jyacs.get_history().get("history", []), ensure_ascii=False, indent=2))
            renpy.notify(_("JYACS: 历史已导出至game/Submods/JYACS_ChatSubmod/chat_history.txt"))
        except Exception as e:
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("导出聊天历史失败: {}".format(e), "ERROR")
            renpy.notify(_("JYACS: 导出失败"))

    def upload_chat_history():
        """上传聊天历史"""
        if not hasattr(store, 'jyacs') or not hasattr(store.jyacs, 'jyacs'):
            renpy.notify(_("JYACS: 模块不可用"))
            return

        import json
        history_file = os.path.join(renpy.config.basedir, "game", "Submods", "JYACS_ChatSubmod", "chat_history.txt")
        if not os.path.exists(history_file):
            renpy.notify(_("JYACS: 未找到历史文件"))
            return
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            res = store.jyacs.jyacs.upload_history(history)
            renpy.notify(_("JYACS: 历史上传成功") if res.get("success", False) else _("JYACS: 历史上传失败, {}".format(res.get("exception", "未知错误"))))
        except Exception as e:
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("上传聊天历史失败: {}".format(e), "ERROR")
            renpy.notify(_("JYACS: 上传失败"))

    def process_user_message(message):
        """处理用户消息，包括关键词替换和日志记录"""
        # 使用 store.key_replace 进行关键词替换
        processed_message = process_user_input(message)

        # 使用 store.jyacs_log 记录处理过程
        if hasattr(store, 'jyacs_log'):
            store.jyacs_log("用户消息处理: '{}' -> '{}'".format(message, processed_message), "DEBUG")

        return processed_message

    def jyacs_apply_setting(ininit=False):
        """应用JYACS设置"""
        if not hasattr(store, 'jyacs') or not hasattr(store.jyacs, 'jyacs'):
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("JYACS模块不可用，跳过设置应用", "WARNING")
            return

        # 使用 store.jyacs_log 记录设置应用过程
        if hasattr(store, 'jyacs_log'):
            store.jyacs_log("开始应用JYACS设置", "INFO")

        # --- 新增：直接从字典获取并应用API设置 ---
        api_key = persistent.jyacs_setting_dict.get("api_key", "")
        api_url = persistent.jyacs_setting_dict.get("api_url", "")
        model_name = persistent.jyacs_setting_dict.get("model_name", "jyacs_main")
        store.jyacs.set_api(api_key, api_url, model_name)
        # --- 新增结束 ---

        if persistent.jyacs_setting_dict["mspire_interval"] <= 10:
            persistent.jyacs_setting_dict["mspire_interval"] = 10

        store.jyacs.jyacs.auto_reconnect = persistent.jyacs_setting_dict["auto_reconnect"]
        if persistent.jyacs_setting_dict["use_custom_model_config"]:
            jyacs_apply_advanced_setting()
        else:
            store.jyacs.jyacs.modelconfig = {}

        if persistent.jyacs_setting_dict["42seed"]:
            persistent.jyacs_advanced_setting_status["seed"] = False
            persistent.jyacs_advanced_setting['seed'] = 42
            store.jyacs.jyacs.modelconfig.update({"seed":42})
        store.jyacs.jyacs.sf_extraction = persistent.jyacs_setting_dict["sf_extraction"]
        store.jyacs.jyacs.chat_session = persistent.jyacs_setting_dict["chat_session"]
        store.jyacs.jyacs.model = persistent.jyacs_setting_dict["jyacs_model"]
        store.jyacs.jyacs.mspire_use_cache = persistent.jyacs_setting_dict["mspire_use_cache"]

        # 设置控制台字体（安全地检查对象是否存在）
        if hasattr(store, 'jyacs_console') and hasattr(store.jyacs_console, 'font'):
            store.jyacs_console.font = persistent.jyacs_setting_dict["console_font"]

        store.jyacs.jyacs.target_lang = persistent.jyacs_setting_dict["target_lang"]
        store.jyacs.jyacs.mspire_category = persistent.jyacs_setting_dict["mspire_category"]
        store.jyacs.jyacs.mspire_type = persistent.jyacs_setting_dict["mspire_search_type"]

        # 设置日志级别（安全地检查对象是否存在）
        if hasattr(store, 'jyacs_submod_utils') and hasattr(store.jyacs_submod_utils, 'submod_log'):
            store.jyacs_submod_utils.submod_log.level = persistent.jyacs_setting_dict["log_level"]
        if hasattr(store.jyacs.jyacs, 'console_logger'):
            store.jyacs.jyacs.console_logger.level = persistent.jyacs_setting_dict["log_conlevel"]

        store.jyacs.jyacs.mspire_session = 0
        store.jyacs.jyacs.provider_id = persistent.jyacs_setting_dict["provider_id"]
        store.jyacs.jyacs.max_history_token = persistent.jyacs_setting_dict["max_history_token"]
        store.jyacs.jyacs.enable_strict_mode = persistent.jyacs_setting_dict["strict_mode"]

        if hasattr(store.jyacs.jyacs, 'mtrigger_manager'):
            store.persistent.jyacs_mtrigger_status = store.jyacs.jyacs.mtrigger_manager.output_settings()

        # 运行函数（安全地检查对象是否存在）
        if hasattr(store, 'jyacs_submod_utils') and hasattr(store.jyacs_submod_utils, 'getAndRunFunctions'):
            store.jyacs_submod_utils.getAndRunFunctions()

        # 设置表情翻译
        if store.jyacs.jyacs.target_lang == store.jyacs.jyacs.JyacsAiLang.zh_cn:
            store.jyacs.jyacs.MoodStatus.emote_translate = {}
        elif store.jyacs.jyacs.target_lang == store.jyacs.jyacs.JyacsAiLang.en:
            try:
                import json_exporter
                store.jyacs.jyacs.MoodStatus.emote_translate = json_exporter.emotion_etz
            except ImportError:
                store.jyacs.jyacs.MoodStatus.emote_translate = {}

        if not ininit:
            success = store.jyacs.jyacs.send_settings()
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("设置上传{}".format('成功' if success else '失败'), "INFO")
            renpy.notify(_("JYACS: 已上传设置") if success else _("JYACS: 请等待连接就绪后手动上传"))

    def jyacs_apply_advanced_setting():
        """应用高级设置"""
        if not hasattr(store, 'jyacs') or not hasattr(store.jyacs, 'jyacs'):
            return

        settings_dict = {}
        for k, v in persistent.jyacs_advanced_setting_status.items():
            if v:
                settings_dict[k] = persistent.jyacs_advanced_setting[k]
        store.jyacs.jyacs.modelconfig.update(settings_dict)
        # 确保重新加载配置文件中的系统提示词
        store.jyacs.reload_config()
        if hasattr(store, 'jyacs_log'):
            store.jyacs_log("Applying advanced settings: {}".format(settings_dict), "INFO")

    def change_chatsession():
        """切换聊天会话"""
        persistent.jyacs_setting_dict["chat_session"] += 1
        if persistent.jyacs_setting_dict["chat_session"] not in range(0, 10):
            persistent.jyacs_setting_dict["chat_session"] = 0

    def reset_player_information():
        """重置玩家信息"""
        # 将mas_player_additions改为jyacs_player_additions
        persistent.jyacs_player_additions = []
        if hasattr(store, 'jyacs_log'):
            store.jyacs_log("玩家信息已重置", "INFO")

    def export_player_information():
        """导出玩家信息"""
        try:
            os.makedirs(os.path.join(renpy.config.basedir, "game", "Submods", "JYACS_ChatSubmod"), exist_ok=True)
            with open(os.path.join(renpy.config.basedir, "game", "Submods", "JYACS_ChatSubmod", "player_info.txt"), 'w', encoding='utf-8') as f:
                # 将mas_player_additions改为jyacs_player_additions
                f.write(json.dumps(persistent.jyacs_player_additions, ensure_ascii=False, indent=2))
            renpy.notify("JYACS: 信息已导出至game/Submods/JYACS_ChatSubmod/player_info.txt")
        except Exception as e:
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("导出玩家信息失败: {}".format(e), "ERROR")
            renpy.notify("JYACS: 导出失败")

    def update_model_setting(ininit = False):
        """更新模型设置"""
        if not hasattr(store, 'jyacs') or not hasattr(store.jyacs, 'jyacs'):
            return

        import os, json
        try:
            config_file = os.path.join(renpy.config.basedir, "game", "Submods", "JYACS_ChatSubmod", "custom_modelconfig.json")
            if os.path.exists(config_file):
                with open(config_file, "r", encoding='utf-8') as f:
                    store.jyacs.jyacs.modelconfig = json.load(f)
        except Exception as e:
            if not ininit:
                renpy.notify(_("JYACS: 加载高级参数失败, 查看submod_log.log获取详细原因"))
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("Failed to load custom model config: {}".format(e), "ERROR")

    def change_loglevel():
        """切换日志级别"""
        import logging
        l = [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        curr = l.index(persistent.jyacs_setting_dict["log_level"])
        persistent.jyacs_setting_dict["log_level"] = l[(curr + 1) % len(l)]
        # 安全地检查对象是否存在
        if hasattr(store, 'jyacs_submod_utils') and hasattr(store.jyacs_submod_utils, 'submod_log'):
            store.jyacs_submod_utils.submod_log.level = persistent.jyacs_setting_dict["log_level"]

    def change_conloglevel():
        """切换控制台日志级别"""
        import logging
        l = [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        curr = l.index(persistent.jyacs_setting_dict["log_conlevel"])
        persistent.jyacs_setting_dict["log_conlevel"] = l[(curr + 1) % len(l)]
        if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'jyacs') and hasattr(store.jyacs.jyacs, 'console_logger'):
            store.jyacs.jyacs.console_logger.level = persistent.jyacs_setting_dict["log_conlevel"]

    def try_eval(str_):
        """安全执行eval"""
        try:
            return eval(str_)
        except Exception as e:
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("Failed to eval: {}|param: '{}'".format(e, str_), "ERROR")
            return None

    def log_eventstat():
        """记录事件统计"""
        try:
            def get_conditional(name):
                try:
                    # 替换mas_getEV为更通用的getEV
                    if hasattr(store, 'getEV') and store.getEV(name):
                        return store.getEV(name).conditional
                except Exception as e:
                    if hasattr(store, 'jyacs_log'):
                        store.jyacs_log("Failed to get conditional: {}".format(e), "ERROR")
                    return None

            # 安全地记录事件状态
            if hasattr(store, 'jyacs_log'):
                # 使用安全的条件检查，避免不存在的标签
                try:
                    store.jyacs_log("jyacs_greeting.conditional:{}|seen:{}".format(
                        try_eval(get_conditional('jyacs_greeting')), 
                        renpy.seen_label('jyacs_greeting') if renpy.has_label('jyacs_greeting') else False
                    ), "INFO")
                except:
                    pass

                # 对其他标签也做类似处理
                for label in ['jyacs_chr2', 'jyacs_chr_gone', 'jyacs_chr_corrupted2', 
                             'jyacs_wants_preferences2', 'jyacs_wants_mspire', 
                             'jyacs_mspire', 'jyacs_wants_mpostal']:
                    try:
                        store.jyacs_log("{}.conditional:{}|seen:{}".format(
                            label,
                            try_eval(get_conditional(label)), 
                            renpy.seen_label(label) if renpy.has_label(label) else False
                        ), "INFO")
                    except:
                        pass

        except Exception as e:
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("Failed to get event stat: {}".format(e), "ERROR")

# 工具函数

# 应用设置并记录事件统计
init -700 python:
    def create_sentence_splitter():
        """创建分句器，使用 store.TalkSplitV2"""
        if hasattr(store, 'TalkSplitV2'):
            return store.TalkSplitV2()
        return None

    def process_ai_reply_with_splitter(reply_text):
        """使用 store.TalkSplitV2 处理AI回复的分句显示"""
        if not hasattr(store, 'TalkSplitV2'):
            return [reply_text]

        splitter = store.TalkSplitV2()
        sentences = []

        for char in reply_text:
            splitter.add_part(char)
            sentence = splitter.split_present_sentence()
            if sentence:
                sentences.append(sentence)

        remaining = splitter.announce_stop()
        sentences.extend(remaining)

        return sentences
    
    jyacs_apply_setting(True)
    log_eventstat()

    # 注册兼容性函数到store，供其他模块调用
    process_user_input = lambda text: store.key_replace(text) if hasattr(store, 'key_replace') else text
    store.process_user_input = process_user_input
    store.create_sentence_splitter = create_sentence_splitter
    store.process_ai_reply_with_splitter = process_ai_reply_with_splitter
    store.process_user_message = process_user_message
    store.jyacs_apply_setting = jyacs_apply_setting
    store.jyacs_apply_advanced_setting = jyacs_apply_advanced_setting
    store.reset_session = reset_session
    store.output_chat_history = output_chat_history
    store.upload_chat_history = upload_chat_history
    store.change_chatsession = change_chatsession
    store.reset_player_information = reset_player_information
    store.export_player_information = export_player_information
    store.update_model_setting = update_model_setting
    store.change_loglevel = change_loglevel
    store.change_conloglevel = change_conloglevel
    store.log_eventstat = log_eventstat

# 子模组注册和基础函数
init -900 python:
    # 安全的日志记录函数
    def jyacs_log(message, level="INFO"):
        """简化的日志记录函数"""
        try:
            log_message = u"[JYACS-{}] {}".format(level, message)
            renpy.log(log_message)
        except Exception as e:
            print(u"[JYACS-LOGFAIL] [{}]: {} ({})".format(level, message, e))

    # 进度条函数
    def jyacs_progress_bar(percentage, current=None, total=None, bar_length=20):
        """进度条显示函数"""
        filled_length = int(round(bar_length * percentage / 100.0))
        bar = u'▇' * filled_length + u' ' * (bar_length - filled_length)

        if total is not None:
            return u'|{}| {}% | {} / {}'.format(bar, int(percentage), current, total)
        else:
            return u'|{}| {}%'.format(bar, int(percentage))

    # 注册到store
    if not hasattr(store, 'jyacs_log'):
        store.jyacs_log = jyacs_log
    if not hasattr(store, 'jyacs_progress_bar'):
        store.jyacs_progress_bar = jyacs_progress_bar

# 子模组注册
init -900 python:
    # 子模组信息 - 使用安全的调用方式
    if hasattr(store, 'jyacs_submod_utils') and hasattr(store.jyacs_submod_utils, 'Submod'):
        store.jyacs_submod_utils.Submod(
            author="Panghu1102",
            name="JustYuriAIChatSubmod",
            description="基于API的AI聊天系统",
            version="1.0.0",
            settings_pane="jyacs_setting_pane"
        )

# 核心功能初始化
init -800 python:
    # 初始化函数重写为安全版本
    def jyacs_init():
        """JYACS初始化"""
        try:
            if hasattr(store, 'jyacs_console'):
                store.jyacs_console.font = store.persistent.jyacs_setting_dict.get("console_font", "SarasaMonoTC-SemiBold.ttf")

            # 安全地设置日志级别
            if hasattr(store, 'jyacs_submod_utils') and hasattr(store.jyacs_submod_utils, 'submod_log'):
                log_level = persistent.jyacs_setting_dict.get("log_level", "INFO")
                store.jyacs_submod_utils.submod_log.level = getattr(logging, log_level, logging.INFO)

                # 安全地运行函数
                if hasattr(store.jyacs_submod_utils, 'getAndRunFunctions'):
                    store.jyacs_submod_utils.getAndRunFunctions()

            # 安全地设置API密钥
            if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'jyacs') and hasattr(store, 'getAPIKey'):
                store.jyacs.jyacs.ciphertext = store.getAPIKey("Jyacs_Token")
            return True
        except Exception as e:
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("JYACS初始化失败: {}".format(e), "ERROR")
            else:
                print("[JYACS-ERROR] JYACS初始化失败: {}".format(e))
            return False

    def save_player_additions():
        """保存玩家补充信息"""
        try:
            with open("player_additions.json", "w", encoding="utf-8") as f:
                json.dump(persistent.jyacs_player_additions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("保存玩家补充信息失败: {}".format(e), "ERROR")
            else:
                print("[JYACS-ERROR] 保存玩家补充信息失败: {}".format(e))

    def get_event_conditional(name):
        """安全地获取事件条件"""
        try:
            if hasattr(store, 'getEV') and store.getEV(name):
                return store.getEV(name).conditional
        except Exception:
            pass
        return None

    def get_build_timescamp():
        """获取构建时间戳"""
        return 0  # 默认返回0，避免错误

# 默认设置和配置
init 10 python:
    # 检查jyacs模块是否可用
    if not hasattr(store, 'jyacs') or not hasattr(store.jyacs, 'jyacs'):
        # 如果jyacs模块不可用，使用默认值
        jyacs_default_dict = {
            "auto_reconnect": False,
            "jyacs_model": "jyacs_main",
            "use_custom_model_config": False,
            "sf_extraction": True,
            "chat_session": 1,
            "console": True,
            "console_font": "mod_assets/font/SarasaMonoTC-SemiBold.ttf",
            "target_lang": "zh_cn" if config.language == "chinese" else "en",
            "mspire_enable": True,
            "mspire_category": [],
            "mspire_interval": 60,
            "mspire_search_type": "in_fuzzy_all",
            "mspire_session": 0,
            "mspire_use_cache": True,
            "log_level": logging.DEBUG,
            "log_conlevel": logging.INFO,
            "provider_id": 1 if not renpy.android else 2,
            "max_history_token": 4096,
            "status_update_time": 0.25,
            "strict_mode": False,
            "show_console_when_reply": False,
            "mpostal_default_reply_time": 60*60*12,
            "42seed": False,
            "use_anim_background": False  # 移除MAS特有的动态背景
        }
    else:
        # 使用jyacs模块的值
        jyacs_default_dict = {
            "auto_reconnect": False,
            "jyacs_model": store.jyacs.jyacs.JyacsAiModel.jyacs_main,
            "use_custom_model_config": False,
            "sf_extraction": True,
            "chat_session": 1,
            "console": True,
            "console_font": "mod_assets/font/SarasaMonoTC-SemiBold.ttf",
            "target_lang": store.jyacs.jyacs.JyacsAiLang.zh_cn if config.language == "chinese" else store.jyacs.jyacs.JyacsAiLang.en,
            "mspire_enable": True,
            "mspire_category": [],
            "mspire_interval": 60,
            "mspire_search_type": "in_fuzzy_all",
            "mspire_session": 0,
            "mspire_use_cache": True,
            "log_level": logging.DEBUG,
            "log_conlevel": logging.INFO,
            "provider_id": 1 if not renpy.android else 2,
            "max_history_token": 4096,
            "status_update_time": 0.25,
            "strict_mode": False,
            "show_console_when_reply": False,
            "mpostal_default_reply_time": 60*60*12,
            "42seed": False,
            "use_anim_background": False  # 移除MAS特有的动态背景
        }

    # 高级设置
    jyacs_advanced_setting = {
        "top_p": 0.7,
        "temperature": 0.2,
        "max_tokens": 1600,
        "frequency_penalty": 0.4,
        "presence_penalty": 0.4,
        "seed": 0,
        "mf_aggressive": False,
        "sfe_aggressive": False,
        "tnd_aggressive": 1,
        "esc_aggressive": True,
        "nsfw_acceptive": True,
        "pre_additive": 0,
        "post_additive": 1,
        "amt_aggressive": True,
        "tz": None,
        "_seed": "0"
    }





init python:
    def scr_nullfunc():
        return            

screen jyacs_setting_pane():
    python:
        import store.jyacs as jyacs
        stat = _("未连接") if not jyacs.jyacs.wss_session else _("已连接") if jyacs.jyacs.is_connected() else _("已断开")
        # 安全地获取API密钥
        if hasattr(store, 'getAPIKey'):
            store.jyacs.jyacs.ciphertext = store.getAPIKey("Jyacs_Token")

    vbox:
        xmaximum 800
        xfill True
        style_prefix "check"

        timer persistent.jyacs_setting_dict.get('status_update_time', 1.0) repeat True action Function(scr_nullfunc, _update_screens=True)
        
        # 定义安全的版本检查函数
        python:
            def safe_version_check():
                # 默认返回False，避免显示不必要的警告
                return False
                
        # 使用安全的版本检查
        if safe_version_check():
            text _("> 你当前的版本过旧, 可能影响正常运行, 请升级至最新版本"):
                xalign 1.0 yalign 0.0
                xoffset -10
                style "main_menu_version"
                
        if store.jyacs.jyacs.is_outdated is None:
            text _("> 无法验证版本号, 如果出现问题请更新至最新版"):
                xalign 1.0 yalign 0.0
                xoffset -10
                style "main_menu_version"
        elif store.jyacs.jyacs.is_outdated is True:
            text _("> 当前版本已不再支持, 请更新至最新版"):
                xalign 1.0 yalign 0.0
                xoffset -10
                style "main_menu_version"

        # 安全地检查子模组
        if hasattr(store, 'jyacs_submod_utils') and hasattr(store.jyacs_submod_utils, 'isSubmodInstalled'):
            if store.jyacs_submod_utils.isSubmodInstalled("Better Loading"):
                text _("> 警告: 与 Better Loading 不兼容"):
                    xalign 1.0 yalign 0.0
                    xoffset -10
                    style "main_menu_version"
            if store.jyacs_submod_utils.isSubmodInstalled("Log Screen"):
                text _("> 警告: 与 Log Screen 一起使用时, 请将'submod_log'的详细程度提高至info及以上"):
                    xalign 1.0 yalign 0.0
                    xoffset -10
                    style "main_menu_version"
                    
        text _("> JYACS通信状态: [jyacs.jyacs.status]|[jyacs.jyacs.JyacsAiStatus.get_description(jyacs.jyacs.status)]"):
            xalign 1.0 yalign 0.0
            xoffset -10
            style "main_menu_version"

        text renpy.substitute(_("> Websocket:")) + renpy.substitute(stat):
            xalign 1.0 yalign 0.0
            xoffset -10
            style "main_menu_version"
        if not jyacs.jyacs.is_accessable():
            textbutton _("> 生成令牌")  
        elif not jyacs.jyacs.is_connected():
            textbutton _("> 生成令牌"):
                action Show("jyacs_login")
            
        if jyacs.jyacs.has_token() and not jyacs.jyacs.is_connected():
            textbutton _("> 使用已保存令牌连接"):
                action Call("submod_jyacs_chat_start")

            
        elif jyacs.jyacs.is_connected():
            if jyacs.jyacs.is_ready_to_input():
                textbutton _("> 手动上传设置"):
                    action Function(jyacs_apply_setting)
            else:
                textbutton _("> 手动上传设置 [[请先使JYACS完成连接]")
                    

            textbutton _("> 重置当前对话"):
                action Function(reset_session)

            textbutton _("> 导出当前对话"):
                action Function(output_chat_history)
            
            textbutton _("> 上传对话历史到会话 '[store.jyacs.jyacs.chat_session]' "):
                action Function(upload_chat_history)

            textbutton renpy.substitute(_("> 退出当前DCC账号")) + " " + renpy.substitute(_("{size=-10}* 如果对话卡住了, 点我断开连接")):
                action Function(store.jyacs.jyacs.close_wss_session)

        else:
            textbutton _("> 使用已保存令牌连接")
    
        textbutton _("> JYACS对话设置 {size=-10}*部分选项重新连接生效"):
            action Show("jyacs_setting")

screen jyacs_node_setting():
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")

        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None
        def set_provider(id):
            persistent.jyacs_setting_dict["provider_id"] = id

    modal True
    zorder 215
    
    style_prefix "check"

    frame:
        vbox:
            xmaximum 1100
            spacing 5
            viewport:
                id "viewport"
                scrollbars "vertical"
                ymaximum 600
                xmaximum 1100
                xfill True
                yfill False
                mousewheel True
                draggable True
                
                vbox:
                    xmaximum 1100
                    xfill True
                    yfill False

                    for provider in JyacsProviderManager.servers:
                        text str(provider.get('id')) + ' | ' + provider.get('name')
                        

                        hbox:
                            text renpy.substitute(_("设备: ")) + provider.get('deviceName', 'Device not provided')
                        hbox:
                            text renpy.substitute(_("当前模型: ")) + provider.get('servingModel', 'No model provided')


                        hbox:
                            textbutton _("> 使用该节点"):
                                action [
                                    Function(set_provider, provider.get('id')),
                                    Hide("jyacs_node_setting")
                                ]
                            
                            if provider.get("isOfficial", False):
                                textbutton _(" √ JYACS 官方服务器")
                    
                    hbox:
                        textbutton _("更新节点列表"):
                            style_prefix "confirm"
                            action Function(store.jyacs.jyacs.JyacsProviderManager.get_provider)

                        textbutton _("关闭"):
                            style_prefix "confirm"
                            action Hide("jyacs_node_setting")

screen jyacs_triggers():
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")
        jyacs_triggers = store.jyacs.jyacs.mtrigger_manager
        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None

    modal True
    zorder 215
    
    style_prefix "check"

    frame:
        vbox:
            xmaximum 1100
            spacing 5
            viewport:
                id "viewport"
                scrollbars "vertical"
                ymaximum 600
                xmaximum 1100
                xfill True
                yfill False
                mousewheel True
                draggable True
                
                vbox:
                    xmaximum 1100
                    xfill True
                    yfill False

                    text _("MTrigger空间使用情况: ")
                    text "request: " + str(jyacs_triggers.get_length(0)) + " / " + str(jyacs_triggers.MAX_LENGTH_REQUEST):
                        color ("#FF0000" if jyacs_triggers.get_length(0) > jyacs_triggers.MAX_LENGTH_REQUEST * 0.75 else gui.interface_text_color)
                    text "table: " + str(jyacs_triggers.get_length(1)) + " / " + str(jyacs_triggers.MAX_LENGTH_TABLE):
                        color ("#FF0000" if jyacs_triggers.get_length(1) > jyacs_triggers.MAX_LENGTH_TABLE * 0.9 else gui.interface_text_color)
                    if jyacs_triggers.get_length(0) > jyacs_triggers.MAX_LENGTH_REQUEST * 0.75 or jyacs_triggers.get_length(1) > jyacs_triggers.MAX_LENGTH_TABLE * 0.9:
                        text _("> 注意: 当空间不足时将自动关闭部分MTrigger!"):
                            color "#ff0000"
                            size 15

                    for trigger in jyacs_triggers.triggers:
                        label trigger.name
                        if not jyacs_triggers.trigger_status(trigger.name) or not trigger.condition():
                            hbox:
                                text _("空间占用: -"):
                                    size 15
                        elif trigger.method == 0:
                            hbox:
                                text _("空间占用: request"):
                                    size 15
                                text str(len(trigger)):
                                    size 15
                        elif trigger.method == 1:
                            hbox:
                                text _("空间占用: table"):
                                    size 15
                                text str(len(trigger)):
                                    size 15
                        text trigger.description:
                            size 15
                        
                        
                        
                        hbox:
                            if jyacs_triggers.trigger_status(trigger.name):
                                textbutton _("√ 已启用"):
                                    action Function(jyacs_triggers.disable_trigger, trigger.name)
                                    selected jyacs_triggers.trigger_status(trigger.name)
                            else:
                                textbutton _("× 已禁用"):
                                    action Function(jyacs_triggers.enable_trigger, trigger.name)
                                    selected jyacs_triggers.trigger_status(trigger.name)
                            
                            if not trigger.condition():
                                textbutton _("※ 当前不满足触发条件")

            hbox:
                style_prefix "confirm"
                textbutton _("关闭"):
                    action Hide("jyacs_triggers")

screen jyacs_mpostals():
    python:
        import time
        submods_screen = store.renpy.get_screen("submods", "screens")
        jyacs_triggers = store.jyacs.jyacs.mtrigger_manager
        preview_len = 200
        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None

        # 定义安全的角色名变量
        character_name = "Yuri" if not hasattr(store, "m_name") else store.m_name

        def _delect_portal(title):
            for item in persistent._jyacs_send_or_received_mpostals:
                if title == item["raw_title"]:
                    persistent._jyacs_send_or_received_mpostals.remove(item)
                    break

    modal True
    zorder 215
    
    style_prefix "check"

    frame:
        vbox:
            xmaximum 1100
            spacing 5
            viewport:
                id "viewport"
                scrollbars "vertical"
                ymaximum 600
                xmaximum 1100
                xfill True
                yfill False
                mousewheel True
                draggable True
                
                vbox:
                    xmaximum 1100
                    xfill True
                    yfill False
                    hbox:
                        # 修改对"太空教室"的引用，使其更通用
                        textbutton _("{size=15}因能力有限, 阅读信件后信件列表将在返回主界面后重新显示.")
                            

                    hbox:
                        text ""
                    for postal in persistent._jyacs_send_or_received_mpostals:
                        label postal["raw_title"]
                        text renpy.substitute(_("信件状态: ")) + postal["responsed_status"]:
                            size 10                       
                        text renpy.substitute(_("寄信时间: ")) + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(postal["time"].split(".")[0]))):
                            size 10
                        text renpy.substitute(_("\n[player]: \n")) + postal["raw_content"][:preview_len].replace("\n", "") + ("..." if len(postal["raw_content"]) > preview_len else  "") + "\n":
                            size 15
                        if postal["responsed_content"] != "":
                            # 使用安全的角色名变量
                            text renpy.substitute(_("\n[character_name]: \n")) + postal["responsed_content"][:preview_len].replace("\n", "")  + ("..." if len(postal["responsed_content"]) > preview_len else  ""):
                                size 15
                        hbox:
                            textbutton _("阅读[player]写的信"):
                                action [
                                        Hide("jyacs_mpostals"),
                                        Hide("jyacs_setting"),
                                        Function(store.jyacs_apply_setting),
                                        Function(renpy.call, "jyacs_mpostal_show_backtoscreen", content = postal["raw_content"])
                                ]
                            if postal["responsed_content"] != "":
                                # 使用安全的角色名变量
                                textbutton _("阅读[character_name]的回信"):
                                    action [
                                            Hide("jyacs_mpostals"),
                                            Hide("jyacs_setting"),
                                            Function(store.jyacs_apply_setting),
                                            Function(renpy.call, "jyacs_mpostal_show_backtoscreen", content = postal["responsed_content"])
                                    ]
                            
                            if postal["responsed_status"] in ("fatal"):
                                textbutton _("重新寄信"):
                                    action SetDict(postal, "responsed_status", "delaying")
                            hbox:
                                textbutton _("删除"):
                                    action Function(_delect_portal, postal["raw_title"])
                            
            hbox:
                style_prefix "confirm"
                textbutton _("关闭"):
                    action Hide("jyacs_mpostals")

screen jyacs_tz_setting():
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")
        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None

        def get_gmt_offset_timezone():
            import time
            if time.localtime().tm_isdst:
                offset_sec = -time.altzone
            else:
                offset_sec = -time.timezone

            offset_hours = offset_sec // 3600

            if offset_hours == 0:
                return "Etc/GMT"
            elif offset_hours > 0:
                return "Etc/GMT-{}".format(offset_hours)
            else:
                return "Etc/GMT+{}".format(-offset_hours)

        current_tz = get_gmt_offset_timezone()

    modal True
    zorder 215
    
    style_prefix "check"

    frame:
        vbox:
            xmaximum 1100
            spacing 5
            viewport:
                id "viewport"
                scrollbars "vertical"
                ymaximum 600
                xmaximum 1100
                xfill True
                yfill False
                mousewheel True
                draggable True
                
                vbox:
                    xmaximum 1100
                    xfill True
                    yfill False
                    text _("{size=-10}如果这里没有你的时区, 请根据你当地的UTC时间选择")

                    hbox:
                        textbutton _("根据语言自动选择"):
                            action SetDict(persistent.jyacs_advanced_setting, "tz", None)
                    
                    hbox:
                        textbutton _("根据系统时区自动选择"):
                            action SetDict(persistent.jyacs_advanced_setting, "tz", current_tz)

                    hbox:
                        textbutton "UTC-12|Etc/GMT+12":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Etc/GMT+12")

                    hbox:
                        textbutton "UTC-11|Pacific/Midway":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Pacific/Midway")

                    hbox:
                        textbutton "UTC-10|Pacific/Honolulu":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Pacific/Honolulu")

                    hbox:
                        textbutton "UTC-9|America/Anchorage":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "America/Anchorage")

                    hbox:
                        textbutton "UTC-8|America/Los_Angeles":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "America/Los_Angeles")

                    hbox:
                        textbutton "UTC-7|America/Denver":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "America/Denver")

                    hbox:
                        textbutton "UTC-6|America/Chicago":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "America/Chicago")

                    hbox:
                        textbutton "UTC-5|America/New_York":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "America/New_York")

                    hbox:
                        textbutton "UTC-4|America/Santiago":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "America/Santiago")

                    hbox:
                        textbutton "UTC-3|America/Argentina/Buenos_Aires":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "America/Argentina/Buenos_Aires")

                    hbox:
                        textbutton "UTC-2|Atlantic/South_Georgia":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Atlantic/South_Georgia")

                    hbox:
                        textbutton "UTC-1|Atlantic/Azores":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Atlantic/Azores")

                    hbox:
                        textbutton "UTC+0|Europe/London":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Europe/London")

                    hbox:
                        textbutton "UTC+1|Europe/Berlin":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Europe/Berlin")

                    hbox:
                        textbutton "UTC+2|Europe/Kaliningrad":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Europe/Kaliningrad")

                    hbox:
                        textbutton "UTC+3|Europe/Moscow":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Europe/Moscow")

                    hbox:
                        textbutton "UTC+4|Asia/Dubai":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Asia/Dubai")

                    hbox:
                        textbutton "UTC+5|Asia/Karachi":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Asia/Karachi")

                    hbox:
                        textbutton "UTC+6|Asia/Dhaka":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Asia/Dhaka")

                    hbox:
                        textbutton "UTC+7|Asia/Bangkok":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Asia/Bangkok")

                    hbox:
                        textbutton "UTC+8|Asia/Shanghai":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Asia/Shanghai")

                    hbox:
                        textbutton "UTC+9|Asia/Tokyo":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Asia/Tokyo")

                    hbox:
                        textbutton "UTC+10|Australia/Sydney":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Australia/Sydney")

                    hbox:
                        textbutton "UTC+11|Pacific/Noumea":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Pacific/Noumea")

                    hbox:
                        textbutton "UTC+12|Pacific/Auckland":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Pacific/Auckland")

                    hbox:
                        textbutton "UTC+13|Pacific/Tongatapu":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Pacific/Tongatapu")

                    hbox:
                        textbutton "UTC+14|Pacific/Kiritimati":
                            action SetDict(persistent.jyacs_advanced_setting, "tz", "Pacific/Kiritimati")
            hbox:
                textbutton _("关闭"):
                    style_prefix "confirm"
                    action [
                        SetDict(persistent.jyacs_advanced_setting_status, "tz", persistent.jyacs_advanced_setting['tz']),
                        Hide("jyacs_tz_setting")
                        ]

screen jyacs_advance_setting():
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")

        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None
    modal True
    zorder 215
    
    style_prefix "check"

    frame:
        vbox:
            xmaximum 1100
            spacing 5
            viewport:
                id "viewport"
                scrollbars "vertical"
                ymaximum 600
                xmaximum 1100
                xfill True
                yfill False
                mousewheel True
                draggable True
                
                vbox:
                    xmaximum 1100
                    xfill True
                    yfill False
                    hbox:
                        text _("{a=https://github.com/Mon1-innovation/JYACS/blob/main/document/API%20Document.txt}{i}{u}JYACS 官方文档{/i}{/u}{/a}")
                    hbox:
                        text _("{a=https://www.openaidoc.com.cn/api-reference/chat}{i}{u}OPENAI 中文文档{/i}{/u}{/a}")
                    hbox:
                        text _("{size=-10}注意: 只有已被勾选(标记了X)的高级设置才会被使用, 未使用的设置将使用服务端的默认设置")
                    hbox:
                        if not persistent.jyacs_setting_dict.get('use_custom_model_config'):
                            text _("{size=-10}你当前未启用'使用高级参数', 该页的所有设置都不会生效!")

                    hbox:
                        text ""
                    hbox:
                        text _("{size=-10}================超参数================")

                    hbox:
                        textbutton "top_p":
                            action ToggleDict(persistent.jyacs_advanced_setting_status, "top_p")
                            hovered SetField(_tooltip, "value", _("模型选择的范围, 模型考虑概率质量值在前 top_p 的标记的结果, 因此，0.1 意味着仅考虑概率质量值前 10% 的标记"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        
                        if persistent.jyacs_advanced_setting_status.get("top_p", False):
                            bar:
                                value DictValue(persistent.jyacs_advanced_setting, "top_p", 0.9, step=0.01,offset=0.1 ,style="slider")
                                xsize 200
                            
                            textbutton "[persistent.jyacs_advanced_setting.get('top_p', 'None')]"

                    hbox:
                        textbutton "temperature":
                            action ToggleDict(persistent.jyacs_advanced_setting_status, "temperature")
                            hovered SetField(_tooltip, "value", _("模型输出的随机性, 较高的值会使输出更随机, 而较低的值则会使其更加专注和确定"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        if persistent.jyacs_advanced_setting_status.get("temperature", False):
                            bar:
                                value DictValue(persistent.jyacs_advanced_setting, "temperature", 1.0, step=0.01,offset=0 ,style="slider")
                                xsize 200
                            textbutton "[persistent.jyacs_advanced_setting.get('temperature', 'None')]"
                    
                    hbox:
                        textbutton "max_tokens":
                            action ToggleDict(persistent.jyacs_advanced_setting_status, "max_tokens")
                            hovered SetField(_tooltip, "value", _("模型输出的长度限制, 较高的值会使输出更长"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        if persistent.jyacs_advanced_setting_status.get("max_tokens", False):
                            bar:
                                value DictValue(persistent.jyacs_advanced_setting, "max_tokens", 2048, step=1,offset=0 ,style="slider")
                                xsize 200
                            textbutton "[persistent.jyacs_advanced_setting.get('max_tokens', 'None')]"
                    
                    hbox:
                        textbutton "frequency_penalty":
                            action ToggleDict(persistent.jyacs_advanced_setting_status, "frequency_penalty")
                            hovered SetField(_tooltip, "value", _("频率惩罚, 正值基于新标记在文本中的现有频率对其进行惩罚, 降低模型重复相同行的可能性"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        
                        if persistent.jyacs_advanced_setting_status.get("frequency_penalty", False):
                            bar:
                                value DictValue(persistent.jyacs_advanced_setting, "frequency_penalty", 1.0, step=0.01,offset=0 ,style="slider")
                                xsize 200
                            textbutton "[persistent.jyacs_advanced_setting.get('frequency_penalty', 'None')]"
                    
                    hbox:
                        textbutton "presence_penalty":
                            action ToggleDict(persistent.jyacs_advanced_setting_status, "presence_penalty")
                            hovered SetField(_tooltip, "value", _("重现惩罚, 正值基于新标记出现在文本中的情况对其进行惩罚, 增加模型谈论新话题的可能性"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        
                        if persistent.jyacs_advanced_setting_status.get("presence_penalty", False):
                            bar:
                                value DictValue(persistent.jyacs_advanced_setting, "presence_penalty", 1.0, step=0.01,offset=0 ,style="slider")
                                xsize 200
                            textbutton "[persistent.jyacs_advanced_setting.get('presence_penalty', 'None')]"
 
                    hbox:
                        if not persistent.jyacs_setting_dict.get('42seed'):
                            textbutton "seed":
                                action ToggleDict(persistent.jyacs_advanced_setting_status, "seed")
                            
                            if persistent.jyacs_advanced_setting_status.get("seed", False):
                                textbutton "[persistent.jyacs_advanced_setting.get('seed', 'None')]/99999 ":
                                    action Show("jyacs_seed_input")

                                textbutton "+1000":
                                    action SetDict(persistent.jyacs_advanced_setting, "seed", persistent.jyacs_advanced_setting["seed"] + 1000 if persistent.jyacs_advanced_setting["seed"] + 1000 < 99999 else 0)

                                textbutton "+100":
                                    action SetDict(persistent.jyacs_advanced_setting, "seed", persistent.jyacs_advanced_setting["seed"] + 100 if persistent.jyacs_advanced_setting["seed"] + 100 < 99999 else 0)

                                textbutton "+25":
                                    action SetDict(persistent.jyacs_advanced_setting, "seed", persistent.jyacs_advanced_setting["seed"] + 25 if persistent.jyacs_advanced_setting["seed"] + 25 < 99999 else 0)

                                textbutton "+1":
                                    action SetDict(persistent.jyacs_advanced_setting, "seed", persistent.jyacs_advanced_setting["seed"] + 1 if persistent.jyacs_advanced_setting["seed"] + 1 < 99999 else 0)

                                textbutton "-1":
                                    action SetDict(persistent.jyacs_advanced_setting, "seed", persistent.jyacs_advanced_setting["seed"] - 1 if persistent.jyacs_advanced_setting["seed"] - 1 > 0 else 99999)
                                
                                textbutton "-25":
                                    action SetDict(persistent.jyacs_advanced_setting, "seed", persistent.jyacs_advanced_setting["seed"] - 25 if persistent.jyacs_advanced_setting["seed"] - 25 > 0 else 99999)
                                
                                textbutton "-100":
                                    action SetDict(persistent.jyacs_advanced_setting, "seed", persistent.jyacs_advanced_setting["seed"] - 100 if persistent.jyacs_advanced_setting["seed"] - 100 > 0 else 99999)
                                
                                textbutton "-1000":
                                    action SetDict(persistent.jyacs_advanced_setting, "seed", persistent.jyacs_advanced_setting["seed"] - 1000 if persistent.jyacs_advanced_setting["seed"] - 1000 > 0 else 99999)

                        else:
                            textbutton "seed ":
                                action NullAction()
                                selected persistent.jyacs_advanced_setting_status.get('seed', False)

                            textbutton "[persistent.jyacs_advanced_setting.get('seed', 'None')]"

                            textbutton _("!已启用最佳实践")


                    hbox:
                        text _("{size=-10}================偏好================")

                    hbox:
                        textbutton "tnd_aggressive":
                            action ToggleDict(persistent.jyacs_advanced_setting_status, "tnd_aggressive")
                            hovered SetField(_tooltip, "value", _("当其为0时只调用MFocus直接选择的工具. 为1时总是会调用时间与节日工具. 为2时还会额外调用日期工具.\n当其为2且mas_geolocation存在时, tnd_aggressive还会额外调用当前天气工具.\n越高越可能补偿MFocus命中率低下的问题, 但也越可能会干扰模型对部分问题的判断."))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        
                        if persistent.jyacs_advanced_setting_status.get("tnd_aggressive", False):
                            bar:
                                value DictValue(persistent.jyacs_advanced_setting, "tnd_aggressive", 2, step=1,offset=0 ,style="slider")
                                xsize 100
                            textbutton "[persistent.jyacs_advanced_setting.get('tnd_aggressive', 'None')]"
                    hbox:
                        textbutton "mf_aggressive:[persistent.jyacs_advanced_setting.get('mf_aggressive', 'None')]":
                            action [ToggleDict(persistent.jyacs_advanced_setting_status, "mf_aggressive"),
                                ToggleDict(persistent.jyacs_advanced_setting, "mf_aggressive")]
                            hovered SetField(_tooltip, "value", _("总是尽可能使用MFocus的最终输出替代指导构型信息.\n启用可能提升模型的复杂信息梳理能力, 但也可能会造成速度下降或专注扰乱"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        textbutton "sfe_aggressive:[persistent.jyacs_advanced_setting.get('sfe_aggressive', 'None')]":
                            action [ToggleDict(persistent.jyacs_advanced_setting_status, "sfe_aggressive"),
                                ToggleDict(persistent.jyacs_advanced_setting, "sfe_aggressive")]
                            hovered SetField(_tooltip, "value", _("总是以用户的真名替代prompt中的[[player]字段.\n启用此功能可能有利于模型理解玩家的姓名, 但也可能会造成总体拟合能力的下降和信息编造"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        textbutton "esc_aggressive:[persistent.jyacs_advanced_setting.get('esc_aggressive', 'None')]":
                            action [ToggleDict(persistent.jyacs_advanced_setting_status, "esc_aggressive"),
                                ToggleDict(persistent.jyacs_advanced_setting, "esc_aggressive")]
                            hovered SetField(_tooltip, "value", _("调用agent模型对MFocus联网搜集的信息整理一次.\n启用此功能会改善模型对联网检索信息的专注能力, 但也会降低涉及联网搜索query的响应速度."))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        textbutton "amt_aggressive: [persistent.jyacs_advanced_setting.get('amt_aggressive', 'None')]":
                            action [ToggleDict(persistent.jyacs_advanced_setting_status, "amt_aggressive"),
                                ToggleDict(persistent.jyacs_advanced_setting, "amt_aggressive")]
                            hovered SetField(_tooltip, "value", _("要求MFocus预检MTrigger内容(若存在), 以告知核心模型要求是否可以完成. \n启用此功能会改善MTrigger与核心模型的表现失步问题, 但也会降低涉及MTrigger对话的响应速度.\n当对话未使用MTrigger或仅有好感触发器, 此功能不会生效."))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                    hbox:
                        textbutton "nsfw_acceptive:[persistent.jyacs_advanced_setting.get('nsfw_acceptive', 'None')]":
                            action [ToggleDict(persistent.jyacs_advanced_setting_status, "nsfw_acceptive"),
                                ToggleDict(persistent.jyacs_advanced_setting, "nsfw_acceptive")]
                            hovered SetField(_tooltip, "value", _("改变system指引, 使模型对NSFW场景更为宽容.\n经测试启用此功能对模型总体表现(意外地)有利, 但也存在降低模型专注能力和造成混乱的风险."))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                    hbox:
                        textbutton "pre_additive":
                            action ToggleDict(persistent.jyacs_advanced_setting_status, "pre_additive")
                            hovered SetField(_tooltip, "value", _("相当于pre_additive数值轮次的历史对话将被加入MFocus.\n此功能强度越高, 越可能提高MFocus在自然对话中的触发率, 但也越可能干扰MFocus的判断或导致其表现异常."))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        
                        if persistent.jyacs_advanced_setting_status.get("pre_additive", False):
                            bar:
                                value DictValue(persistent.jyacs_advanced_setting, "pre_additive", 5, step=1,offset=0 ,style="slider")
                                xsize 50
                            textbutton "[persistent.jyacs_advanced_setting.get('pre_additive', 'None')]"

                        textbutton "post_additive":
                            action ToggleDict(persistent.jyacs_advanced_setting_status, "post_additive")
                            hovered SetField(_tooltip, "value", _("相当于post_additive数值轮次的历史对话将被加入MTrigger.\n此功能强度越高, 越可能提高MTrigger在自然对话中的触发率, 但也越可能干扰MTrigger的判断或导致其表现异常."))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        
                        if persistent.jyacs_advanced_setting_status.get("post_additive", False):
                            bar:
                                value DictValue(persistent.jyacs_advanced_setting, "post_additive", 5, step=1,offset=0 ,style="slider")
                                xsize 50
                            textbutton "[persistent.jyacs_advanced_setting.get('post_additive', 'None')]"

                    hbox:
                        textbutton _("选择时区: [persistent.jyacs_advanced_setting.get('tz') or 'Asia/Shanghai' if store.jyacs.jyacs.target_lang == store.jyacs.jyacs.JyacsAiLang.zh_cn else 'America/Indiana/Vincennes']"):
                            action Show("jyacs_tz_setting")
                            selected persistent.jyacs_advanced_setting_status.get('tz')




            hbox:
                style_prefix "confirm"
                textbutton _("保存设置"):
                    action [
                        Function(jyacs_apply_advanced_setting),
                        Hide("jyacs_advance_setting")
                    ]

screen jyacs_setting():
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")

        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None
        store.len = len
        
    modal True
    zorder 215
    
    style_prefix "check"

    frame:
        vbox:
            xmaximum 1100
            spacing 5
            viewport:
                id "viewport"
                scrollbars "vertical"
                ymaximum 600
                xmaximum 1100
                xfill True
                yfill False
                mousewheel True
                draggable True
                
                vbox:
                    xmaximum 1100
                    xfill True
                    yfill False
                    if renpy.config.debug:
                        hbox:
                            text "=====JyacsAi()====="
                        hbox:
                            text "ai.is_responding: [store.jyacs.jyacs.is_responding()]":
                                size 15
                        hbox:
                            text "ai.is_failed: [store.jyacs.jyacs.is_failed()]":
                                size 15
                        hbox:
                            text "ai.is_connected: [store.jyacs.jyacs.is_connected()]":
                                size 15
                        hbox:
                            text "ai.is_ready_to_input: [store.jyacs.jyacs.is_ready_to_input()]":
                                size 15
                        hbox:
                            text "ai.JyacsAiStatus.is_submod_exception: [store.jyacs.jyacs.JyacsAiStatus.is_submod_exception(store.jyacs.jyacs.status)]":
                                size 15
                        hbox:
                            text "ai.len_message_queue(): [store.jyacs.jyacs.len_message_queue()]":
                                size 15
                        hbox:
                            text "jyacs_chr_exist: [jyacs_chr_exist]":
                                size 15
                        hbox:
                            text "jyacs_chr_changed: [jyacs_chr_changed]":
                                size 15
                        
                        # 安全地处理未定义的变量
                        python:
                            # 定义安全的函数和变量
                            def safe_len(obj):
                                if obj is None:
                                    return 0
                                try:
                                    return len(obj)
                                except:
                                    return 0
                                    
                            # 检查mas_rev_unseen是否存在
                            has_rev_unseen = hasattr(store, 'mas_rev_unseen')
                            rev_unseen_len = safe_len(getattr(store, 'mas_rev_unseen', []))
                            rev_unseen_str = str(getattr(store, 'mas_rev_unseen', []))
                            
                            # 安全的邮件检查函数
                            def safe_mail_check():
                                try:
                                    if hasattr(store, 'has_mail_waitsend'):
                                        mail_waiting = store.has_mail_waitsend()
                                    else:
                                        mail_waiting = False
                                        
                                    # 使用通用的好感度检查
                                    affection_check = True
                                    
                                    # 安全地检查标签是否存在
                                    label_checks = []
                                    for label in ['jyacs_wants_mspire', 'jyacs_wants_mpostal']:
                                        label_checks.append(renpy.has_label(label) and renpy.seen_label(label))
                                    
                                    # 安全地检查事件状态
                                    event_checks = []
                                    for event in ['jyacs_mpostal_received', 'jyacs_mpostal_read']:
                                        if hasattr(store, 'mas_inEVL'):
                                            event_checks.append(not store.mas_inEVL(event))
                                        else:
                                            event_checks.append(True)
                                    
                                    return mail_waiting and affection_check and all(label_checks) and all(event_checks)
                                except:
                                    return False
                                    
                            # 安全的事件检查函数
                            def safe_event_check():
                                try:
                                    # 安全地检查标签是否存在
                                    greeting_check = renpy.has_label('jyacs_greeting') and renpy.seen_label('jyacs_greeting')
                                    mspire_check = not (renpy.has_label('jyacs_wants_mspire') and renpy.seen_label('jyacs_wants_mspire'))
                                    random_ask_check = renpy.has_label('mas_random_ask') and renpy.seen_label('mas_random_ask')
                                    
                                    return greeting_check and mspire_check and random_ask_check
                                except:
                                    return False
                        
                        hbox:
                            # 使用安全的变量引用
                            text "未读消息: [rev_unseen_len] | [rev_unseen_str]":
                                size 15
                        hbox:
                            # 使用安全的函数
                            text "邮件状态检查: [safe_mail_check()]":
                                size 15
                        hbox:
                            # 使用安全的函数
                            text "事件状态检查: [safe_event_check()]":
                                size 15
                        hbox:
                            textbutton "输出Event信息到日志":
                                action Function(log_eventstat)
                        
                        # 安全地处理事件推送
                        python:
                            def safe_push_event(event_name):
                                """安全地推送事件"""
                                try:
                                    # 如果MASEventList存在，使用它
                                    if hasattr(store, 'MASEventList') and hasattr(store.MASEventList, 'push'):
                                        store.MASEventList.push(event_name)
                                    # 否则尝试使用renpy.jump
                                    elif renpy.has_label(event_name):
                                        renpy.hide_screen("jyacs_setting")
                                        store.jyacs_apply_setting()
                                        renpy.jump(event_name)
                                    # 如果都不行，尝试使用call
                                    elif "." in event_name and renpy.has_label(event_name.split(".")[-1]):
                                        renpy.hide_screen("jyacs_setting")
                                        store.jyacs_apply_setting()
                                        renpy.call(event_name.split(".")[-1])
                                except Exception as e:
                                    if hasattr(store, 'jyacs_log'):
                                        store.jyacs_log("推送事件失败: {}".format(e), "ERROR")
                        
                        hbox:
                            textbutton "推送分句测试":
                                action [
                                    Hide("jyacs_setting"),
                                    Function(store.jyacs_apply_setting),
                                    Function(safe_push_event, "text_split")
                                ]
                        hbox:
                            textbutton "推送聊天loop":
                                action [
                                    Hide("jyacs_setting"),
                                    Function(store.jyacs_apply_setting),
                                    Function(safe_push_event, "jyacs_main.talking_start")
                                    ]
                            textbutton "推送MSpire":
                                action [
                                    Hide("jyacs_setting"),
                                    Function(store.jyacs_apply_setting),
                                    Function(safe_push_event, "jyacs_mspire")
                                    ]
                            textbutton "推送jyacs_mpostal_read":
                                action [
                                        Hide("jyacs_setting"),
                                        Function(store.jyacs_apply_setting),
                                        Function(safe_push_event, "jyacs_mpostal_read")
                                    ]
                            textbutton "推送jyacs_mpostal_load":
                                action [
                                        Hide("jyacs_setting"),
                                        Function(store.jyacs_apply_setting),
                                        Function(safe_push_event, "jyacs_mpostal_load")
                                    ]

                    # 剩余的设置界面内容保持不变
                    hbox:
                        text _("累计对话轮次: [store.jyacs.jyacs.stat.get('message_count')] ")

                    hbox:
                        text _("累计MSpire轮次: [store.jyacs.jyacs.stat.get('mspire_count')] ")

                    hbox:
                        text _("累计收到Token: [store.jyacs.jyacs.stat.get('received_token')] ")
                    
                    hbox:
                        text _("每个会话累计Token: [store.jyacs.jyacs.stat.get('received_token_by_session')] ")
                    
                    hbox:
                        text _("累计发信数: [store.jyacs.jyacs.stat.get('mpostal_count')] ")

                    hbox:
                        text _("当前用户: [store.jyacs.jyacs.user_acc]")

                    hbox:
                        textbutton _("重置统计数据"):
                            action Function(store.jyacs.jyacs.reset_stat)

                    hbox:
                        textbutton _("服务提供节点: [JyacsProviderManager.get_server_by_id(persistent.jyacs_setting_dict.get('provider_id')).get('name', 'Unknown')] "):
                            action Show("jyacs_node_setting")
                            hovered SetField(_tooltip, "value", _("设置服务器节点"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                    hbox: 
                        textbutton _("自动重连: [persistent.jyacs_setting_dict.get('auto_reconnect')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "auto_reconnect", True, False)
                            hovered SetField(_tooltip, "value", _("连接断开时自动重连"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        textbutton _("严格反劫持: [persistent.jyacs_setting_dict.get('strict_mode')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "strict_mode", True, False)
                            hovered SetField(_tooltip, "value", _("严格模式下, 将会在每次发送时携带cookie信息"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                    hbox:
                        textbutton _("当前JYACS模型: [persistent.jyacs_setting_dict.get('jyacs_model')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "jyacs_model", store.jyacs.jyacs.JyacsAiModel.jyacs_main, store.jyacs.jyacs.JyacsAiModel.jyacs_core)
                            hovered SetField(_tooltip, "value", _("jyacs_main：完全能力模型，jyacs_core: 核心能力模型\n完全能力的前置响应延迟偏高"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                    hbox:
                        textbutton _("目标语言: [persistent.jyacs_setting_dict.get('target_lang')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "target_lang", store.jyacs.jyacs.JyacsAiLang.zh_cn, store.jyacs.jyacs.JyacsAiLang.en)
                            hovered SetField(_tooltip, "value", _("你与优里的沟通语言\n通过system prompt实现, 不能保证输出语言严格正确"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                    hbox:
                        textbutton _("使用高级参数: [persistent.jyacs_setting_dict.get('use_custom_model_config')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "use_custom_model_config", True, False)    
                            hovered SetField(_tooltip, "value", _("高级参数会大幅影响模型的表现"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        textbutton _("设置高级参数"):
                            action Show("jyacs_advance_setting")

                        textbutton _("锁定最佳实践"):
                            action ToggleDict(persistent.jyacs_setting_dict, "42seed", True, False)
                            hovered SetField(_tooltip, "value", _("锁定seed为42, 该设置覆盖高级参数中的seed\n启用会完全排除生成中的随机性, 在统计学上稳定性更佳"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                    hbox:
                        textbutton _("使用存档数据: [persistent.jyacs_setting_dict.get('sf_extraction')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "sf_extraction", True, False)
                            hovered SetField(_tooltip, "value", _("关闭时, 模型将不会使用存档数据\n每次重启游戏将自动上传存档"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                    hbox:
                        textbutton _("当前使用会话: [persistent.jyacs_setting_dict.get('chat_session')] "):
                            action Function(store.change_chatsession)
                            hovered SetField(_tooltip, "value", _("chat_session为0为单轮对话模式, 不同的对话之间相互独立, 需要分别上传存档"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        textbutton _("会话长度: "):
                            action NullAction()
                        bar:
                            value DictValue(persistent.jyacs_setting_dict, "max_history_token", 28672-512,step=10,offset=512 ,style="slider")
                            xsize 375
                            hovered SetField(_tooltip, "value", _("此参数意在缓解对话历史累积导致的响应速度过慢问题. 请避免将其设置得过小, 否则可能影响模型的正常语言能力."))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        textbutton _("[persistent.jyacs_setting_dict.get('max_history_token')] ")

                    hbox:
                        textbutton _("输出到控制台: [persistent.jyacs_setting_dict.get('console')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "console", True, False)
                            hovered SetField(_tooltip, "value", _("在对话期间是否使用console显示相关信息"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        # 定义默认等宽字体，避免依赖mas_ui
                        python:
                            default_mono_font = "DejaVuSansMono.ttf"
                            if hasattr(store, 'mas_ui') and hasattr(store.mas_ui, 'MONO_FONT'):
                                default_mono_font = store.mas_ui.MONO_FONT
                                
                        textbutton _("控制台字体: [persistent.jyacs_setting_dict.get('console_font')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "console_font", store.jyacs_confont, default_mono_font)
                            hovered SetField(_tooltip, "value", _("console使用的字体\nDejaVuSansMono.ttf为默认字体\nSarasaMonoTC-SemiBold.ttf对于非英文字符有更好的显示效果"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                    hbox:
                        textbutton _("清除玩家补充信息: 当前共有[len(persistent.jyacs_player_additions)]条"):
                            action Function(reset_player_information)
                            hovered SetField(_tooltip, "value", _("由你补充的一些数据, 增删后需要重新上传存档"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        textbutton _("编辑信息"):
                            action [
                                Hide("jyacs_setting"),
                                Function(store.jyacs_apply_setting),
                                Function(renpy.jump, "jyacs_mods_preferences")
                                ]

                        textbutton _("导出至根目录"):
                            action Function(export_player_information)
                            hovered SetField(_tooltip, "value", _("导出至game/Submods/JYACS_ChatSubmod/player_information.txt"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                    hbox:
                        textbutton _("MSpire: [persistent.jyacs_setting_dict.get('mspire_enable')] "):
                            action ToggleDict(persistent.jyacs_setting_dict, "mspire_enable", True, False)
                            hovered SetField(_tooltip, "value", _("是否允许由MSpire生成的对话, MSpire不受MFocus影响, 需要关闭重复对话"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        textbutton _("对话范围编辑"):
                            action [
                                Hide("jyacs_setting"),
                                Function(store.jyacs_apply_setting),
                                Function(renpy.jump, "mspire_mods_preferences")
                                ]
                        textbutton _("间隔"):
                            action NullAction()
                        bar:
                            value DictValue(persistent.jyacs_setting_dict, "mspire_interval", 200, step=1,offset=10 ,style="slider")
                            xsize 150
                            hovered SetField(_tooltip, "value", _("MSpire对话的最低间隔分钟"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        textbutton _("[persistent.jyacs_setting_dict.get('mspire_interval')]分钟")

                        textbutton _("搜索方式: [persistent.jyacs_setting_dict.get('mspire_search_type')] "):
                            action [
                                Hide("jyacs_setting"),
                                Function(store.jyacs_apply_setting),
                                Function(renpy.jump, "mspire_type")
                            ]
                        
                    hbox:
                        textbutton _("MSpire 使用缓存"):
                            action ToggleDict(persistent.jyacs_setting_dict, "mspire_use_cache", True, False)
                            hovered SetField(_tooltip, "value", _("启用MSpire缓存, 且使用默认高级参数并固定种子为42\n"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                    # 安全处理日志级别显示
                    python:
                        def safe_get_log_level():
                            """安全获取日志级别"""
                            import logging
                            try:
                                if hasattr(store, 'mas_submod_utils') and hasattr(store.mas_submod_utils, 'submod_log'):
                                    return logging.getLevelName(store.mas_submod_utils.submod_log.level)
                                else:
                                    return "INFO"
                            except:
                                return "INFO"
                                
                    hbox:
                        textbutton _("日志等级:[safe_get_log_level()] "):
                            action Function(store.change_loglevel)
                            hovered SetField(_tooltip, "value", _("这将影响日志文件中每条log的等级, 低于该等级的log将不会记录\n这也会影响其他子模组"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        textbutton _("控制台log等级: [logging.getLevelName(store.jyacs.jyacs.console_logger.level)] "):
                            action Function(store.change_conloglevel)
                            hovered SetField(_tooltip, "value", _("这将影响控制台中每条log的等级, 低于该等级的log将不会记录"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        
                        textbutton _("状态码更新速度"):
                            action NullAction()
                        bar:
                            value DictValue(persistent.jyacs_setting_dict, "status_update_time", 3.0, step=0.1, offset=0.1,style="slider")
                            xsize 150
                            hovered SetField(_tooltip, "value", _("在Submod界面处的状态码更新频率"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)
                        
                        textbutton "[persistent.jyacs_setting_dict.get('status_update_time')]s"

                    hbox:
                        textbutton _("MTrigger 列表"):
                            action Show("jyacs_triggers")
                        
                        textbutton _("查看MPostals往来信件"):
                            action Show("jyacs_mpostals")
                        
                        textbutton _("回信时显示控制台"):
                            action ToggleDict(persistent.jyacs_setting_dict, "show_console_when_reply", True, False)
                    
                    hbox:
                        textbutton _("信件回复时间"):
                            action NullAction()
                        bar:
                            value DictValue(persistent.jyacs_setting_dict, "mpostal_default_reply_time", 50000, step=1, offset=3600, style="slider")
                            xsize 150
                            hovered SetField(_tooltip, "value", _("回信所需要的最低时间"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

                        textbutton "[persistent.jyacs_setting_dict.get('mpostal_default_reply_time', 0) / 3600]h"

                    hbox:
                        textbutton _("查看后端负载"):
                            action Show("jyacs_workload_stat")
                        
                        textbutton _("动态的天堂树林"):
                            action ToggleDict(persistent.jyacs_setting_dict, "use_anim_background", True, False)
                            hovered SetField(_tooltip, "value", _("使用动态摇曳和改良光影的天堂树林, 略微增加渲染压力. 重启生效\n如果产生显存相关错误, 删减精灵包或禁用此选项"))
                            unhovered SetField(_tooltip, "value", _tooltip.default)

            hbox:
                style_prefix "confirm"
                textbutton _("保存设置"):
                    action [
                        Function(store.jyacs_apply_setting),
                        Hide("jyacs_setting")
                        ]
                textbutton _("重置设置"):
                    action [
                        Function(store.jyacs_reset_setting),
                        Function(store.jyacs_apply_setting, ininit = True),
                        Function(renpy.notify, _("JYACS: 设置已重置")),
                        Hide("jyacs_setting")
                    ]
                
                 

default use_email = True
screen jyacs_login():
    modal True
    zorder 215

    style_prefix "confirm"

    frame:
        vbox:
            xfill False
            yfill False
            spacing 5

            hbox:
                style_prefix "check"
                if use_email:
                    textbutton _("改为用户名登录"):
                        action [ToggleVariable("use_email"), Function(_jyacs_clear)]
                        selected False

                else:
                    textbutton _("改为邮箱登录"):
                        action [ToggleVariable("use_email"), Function(_jyacs_clear)]
                        selected False
                        
            hbox:
                if use_email:
                    textbutton _("输入 DCC 账号邮箱"):
                        action Show("jyacs_login_input",message = _("请输入DCC 账号邮箱"),returnto = "_jyacs_LoginEmail")
                else:
                    textbutton _("输入 DCC 账号用户名"):
                        action Show("jyacs_login_input",message = _("请输入DCC 账号用户名") ,returnto = "_jyacs_LoginAcc")

            hbox:
                textbutton _("输入 DCC 账号密码"):
                    action Show("jyacs_login_input",message = _("请输入DCC 账号密码"),returnto = "_jyacs_LoginPw")
            hbox:
                text ""
            hbox:
                textbutton _("连接至服务器生成JYACS令牌"):
                    action [
                        Function(store.jyacs.jyacs._gen_token, store._jyacs_LoginAcc, store._jyacs_LoginPw, "", store._jyacs_LoginEmail if store._jyacs_LoginEmail != "" else None),
                        Function(_jyacs_verify_token),
                        Function(_jyacs_clear), 
                        Hide("jyacs_login")
                        ]
                textbutton _("取消"):
                    action [Function(_jyacs_clear), Hide("jyacs_login")]
            hbox:
                text _("{size=-10}※ 使用JYACS，即认为你同意服务条款")
            hbox:
                text _("{size=-10}※ 访问 https://github.com/Panghu1102/JYACS 了解更多")

screen jyacs_login_input(message, returnto, ok_action = Hide("jyacs_login_input")):
    modal True
    zorder 225

    style_prefix "confirm"

    frame:
        vbox:
            ymaximum 300
            xmaximum 800
            xfill True
            yfill False
            spacing 5

            label _(message):
                style "confirm_prompt"
                xalign 0.5
            hbox:
                input default "" value VariableInputValue(returnto) length 64

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen jyacs_seed_input():
    python:
        def apply_seed():
            seed = int(persistent.jyacs_advanced_setting['_seed'])
            if seed < 0 or seed > 99999:
                renpy.show_screen("jyacs_message", message=_("seed范围错误, 请重新输入种子"))
                persistent.jyacs_advanced_setting['_seed'] = str(persistent.jyacs_advanced_setting['seed'])
            else:
                persistent.jyacs_advanced_setting['seed'] = seed
                
    modal True
    zorder 225

    style_prefix "confirm"

    frame:
        vbox:
            ymaximum 300
            xmaximum 800
            xfill True
            yfill False
            spacing 5

            label _("请输入种子, 范围为0-99999"):
                style "confirm_prompt"
                xalign 0.5
            hbox:
                input default str(persistent.jyacs_advanced_setting['_seed']) value DictInputValue(persistent.jyacs_advanced_setting, "_seed") length 5 allow "0123456789"

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action [
                    Function(apply_seed),
                    Hide("jyacs_seed_input")
                ]

screen jyacs_message(message = "Non Message", ok_action = Hide("jyacs_message")):
    modal True
    zorder 225

    style_prefix "confirm"

    frame:
        vbox:
            ymaximum 300
            xmaximum 800
            xfill True
            yfill False
            spacing 5

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen jyacs_input_screen(prompt):
    default jyacs_input = store.jyacs.JyacsInputValue()
    style_prefix "input"

    window:
        hbox:
            style_prefix "quick"
            xalign 0.5
            yalign 0.995

            textbutton _("就这样吧"):
                selected False
                action Return("nevermind")

            textbutton _("粘贴"):
                selected False
                action [Function(jyacs_input.set_text, pygame.scrap.get(pygame.SCRAP_TEXT).strip()),Function(jyacs_input.set_text, pygame.scrap.get(pygame.SCRAP_TEXT).strip())]
            
        vbox:
            align (0.5, 0.5)
            spacing 30

            text prompt style "input_prompt"
            input:
                id "input"
                value jyacs_input

screen jyacs_workload_stat():
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")
        stat = store.jyacs.jyacs.workload_raw
        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None
        store.update_interval = 15
        def check_and_update(use_none = False):
            import time
            last = store.jyacs.last_workload_update + update_interval - time.time()
            if last < 0:
                store.jyacs.last_workload_update = time.time()
                store.jyacs.jyacs.update_workload()
            return last if not use_none else None

    modal True
    zorder 215
    
    style_prefix "check"

    frame:
        vbox:
            xmaximum 1100
            spacing 5
            viewport:
                id "viewport"
                scrollbars "vertical"
                ymaximum 600
                xmaximum 1100
                xfill True
                yfill False
                mousewheel True
                draggable True
                
                vbox:
                    xmaximum 1100
                    xfill True
                    yfill False

                    for server in stat:
                        text server:
                            size 20
                        text "========================================"
                        for card in stat[server]:
                            hbox:
                                text stat[server][card]["name"]:
                                    size 15
                                text store.jyacs.progress_bar(stat[server][card]["mean_utilization"]):
                                    size 10

                                text "VRAM: " + str(stat[server][card]["mean_memory"]) + " / " + str(stat[server][card]["vram"]):
                                    size 10
                                text renpy.substitute(_("平均功耗: ")) + str(stat[server][card]["mean_consumption"]) + "W":
                                    size 10
                        text ""

            hbox:
                text renpy.substitute(_("下次更新数据")) + store.jyacs.progress_bar(((check_and_update() / store.update_interval)) * 100, bar_length = 90):
                    size 15
                timer 0.15 repeat True action Function(check_and_update, use_none = True)

            hbox:
                textbutton _("关闭"):
                    style_prefix "confirm"
                    action Hide("jyacs_workload_stat")

screen jyacs_outdated_notice():
    frame:
        style "jyacs_frame"
        vbox:
            style_prefix "jyacs"
            spacing 20
            text _("> 你当前的生成版本过旧, 可能影响正常运行, 请升级至最新生成版本")
            textbutton _("确定") action Return()

# 添加在文件的适当位置，例如在init -1500 python块之后
init -999 python:
    # 定义清理函数，避免未定义错误
    def _jyacs_clear():
        """清理登录信息"""
        if not hasattr(store, '_jyacs_LoginAcc'):
            store._jyacs_LoginAcc = ""
        if not hasattr(store, '_jyacs_LoginPw'):
            store._jyacs_LoginPw = ""
        if not hasattr(store, '_jyacs_LoginEmail'):
            store._jyacs_LoginEmail = ""
        store._jyacs_LoginAcc = ""
        store._jyacs_LoginPw = ""
        store._jyacs_LoginEmail = ""

# 样式定义
init 20 python:
    # 确保不覆盖已有样式
    if not hasattr(style, 'jyacs_frame'):
        style.jyacs_frame = Style(style.frame)
        style.jyacs_frame.background = "#2A2A2A"
        style.jyacs_frame.padding = (20, 20)
        style.jyacs_frame.xfill = True
        style.jyacs_frame.yfill = True

    if not hasattr(style, 'jyacs_vbox'):
        style.jyacs_vbox = Style(style.vbox)
        style.jyacs_vbox.spacing = 20
        style.jyacs_vbox.xfill = True

    if not hasattr(style, 'jyacs_title'):
        style.jyacs_title = Style(style.text)
        style.jyacs_title.color = "#FFFFFF"
        style.jyacs_title.size = 36
        style.jyacs_title.xalign = 0.5

    if not hasattr(style, 'jyacs_section_frame'):
        style.jyacs_section_frame = Style(style.frame)
        style.jyacs_section_frame.background = "#1A1A1A"
        style.jyacs_section_frame.padding = (20, 20)
        style.jyacs_section_frame.margin = (0, 10)

    if not hasattr(style, 'jyacs_section_vbox'):
        style.jyacs_section_vbox = Style(style.vbox)
        style.jyacs_section_vbox.spacing = 15
        style.jyacs_section_vbox.xfill = True

    if not hasattr(style, 'jyacs_section_title'):
        style.jyacs_section_title = Style(style.text)
        style.jyacs_section_title.color = "#FFFFFF"
        style.jyacs_section_title.size = 24

    if not hasattr(style, 'jyacs_option_vbox'):
        style.jyacs_option_vbox = Style(style.vbox)
        style.jyacs_option_vbox.spacing = 10
        style.jyacs_option_vbox.xfill = True

    if not hasattr(style, 'jyacs_option_hbox'):
        style.jyacs_option_hbox = Style(style.hbox)
        style.jyacs_option_hbox.spacing = 10
        style.jyacs_option_hbox.xfill = True

    if not hasattr(style, 'jyacs_label'):
        style.jyacs_label = Style(style.text)
        style.jyacs_label.color = "#FFFFFF"
        style.jyacs_label.size = 18
        style.jyacs_label.min_width = 150

    if not hasattr(style, 'jyacs_input'):
        style.jyacs_input = Style(style.input)
        style.jyacs_input.background = "#404040"
        style.jyacs_input.color = "#FFFFFF"
        style.jyacs_input.size = 18

    if not hasattr(style, 'jyacs_bar'):
        style.jyacs_bar = Style(style.bar)
        style.jyacs_bar.left_bar = "#4A7C59"
        style.jyacs_bar.right_bar = "#404040"
        style.jyacs_bar.thumb = "#5A8C69"
        style.jyacs_bar.hover_thumb = "#6A9C79"

    if not hasattr(style, 'jyacs_button_hbox'):
        style.jyacs_button_hbox = Style(style.hbox)
        style.jyacs_button_hbox.spacing = 20
        style.jyacs_button_hbox.xalign = 0.5

    if not hasattr(style, 'jyacs_button'):
        style.jyacs_button = Style(style.button)
        style.jyacs_button.background = "#4A7C59"
        style.jyacs_button.hover_background = "#5A8C69"
        style.jyacs_button.padding = (20, 10)

    if not hasattr(style, 'jyacs_button_text'):
        style.jyacs_button_text = Style(style.text)
        style.jyacs_button_text.color = "#FFFFFF"
        style.jyacs_button_text.size = 18

# 注册到store的函数
init 25 python:
    # 安全地注册函数到store
    functions_to_register = {
        "process_user_input": process_user_input,
        "create_sentence_splitter": create_sentence_splitter,
        "process_ai_reply_with_splitter": process_ai_reply_with_splitter,
        "process_user_message": process_user_message,
        "jyacs_apply_setting": jyacs_apply_setting,
        "jyacs_apply_advanced_setting": jyacs_apply_advanced_setting,
        "reset_session": reset_session,
        "output_chat_history": output_chat_history,
        "upload_chat_history": upload_chat_history,
        "change_chatsession": change_chatsession,
        "reset_player_information": reset_player_information,
        "export_player_information": export_player_information,
        "update_model_setting": update_model_setting,
        "change_loglevel": change_loglevel,
        "change_conloglevel": change_conloglevel,
        "log_eventstat": log_eventstat
    }

    for func_name, func in functions_to_register.items():
        if not hasattr(store, func_name):
            setattr(store, func_name, func)

# 子模组标签定义
label submod_jyacs_init:
    jump submod_jyacs_init_impl

# 子模组初始化标签
label submod_jyacs_init_impl:
    python:
        # 安全地初始化子模组
        success = jyacs_init()
        if not success and hasattr(store, 'jyacs_log'):
            store.jyacs_log("子模组初始化失败", "ERROR")
    return

# 子模组设置标签
label submod_jyacs_settings:
    python:
        # 安全地显示设置界面
        if hasattr(store, 'jyacs_log'):
            store.jyacs_log("显示设置界面", "INFO")
        renpy.show_screen("jyacs_settings")
    return

# 子模组高级设置标签
label submod_jyacs_advanced_settings:
    python:
        # 安全地显示高级设置界面
        if hasattr(store, 'jyacs_log'):
            store.jyacs_log("显示高级设置界面", "INFO")
        renpy.show_screen("jyacs_advanced_settings")
    return

# 子模组重置标签
label submod_jyacs_reset:
    python:
        # 安全地重置子模组
        if hasattr(store, 'jyacs_log'):
            store.jyacs_log("重置子模组", "INFO")
        reset_session()
        reset_player_information()
    return

# 界面定义
init 15 screen submod_jyacs_settings():
    modal True
    zorder 200
    
    add "#000000AA"
    
    frame:
        style "jyacs_frame"
        
        vbox:
            style "jyacs_vbox"
            
            text "JYACS 设置" style "jyacs_title"
            
            frame:
                style "jyacs_section_frame"
                
                viewport:
                    scrollbars "vertical"
                    ysize 480
                    xsize 780
                    
                    vbox:
                        style "jyacs_section_vbox"
                        
                        # API配置区域
                        frame:
                            style "jyacs_section_frame"
                            
                            vbox:
                                style "jyacs_option_vbox"
                                
                                text "API 配置" style "jyacs_section_title"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "API 密钥:" style "jyacs_label"
                                    input:
                                        value VariableInputValue("persistent.jy_ai_api_key")
                                        length 50
                                        style "jyacs_input"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "API 地址:" style "jyacs_label"
                                    input:
                                        value VariableInputValue("persistent.jy_ai_api_url")
                                        length 80
                                        style "jyacs_input"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "模型名称:" style "jyacs_label"
                                    input:
                                        value VariableInputValue("persistent.jy_ai_model_name")
                                        length 30
                                        style "jyacs_input"
                        
                        # 基础设置区域
                        frame:
                            style "jyacs_section_frame"
                            
                            vbox:
                                style "jyacs_option_vbox"
                                
                                text "基础设置" style "jyacs_section_title"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "自动连接:" style "jyacs_label"
                                    textbutton "开启" action ToggleDict(persistent.jyacs_setting_dict, "auto_connect") style "jyacs_button"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "自动重连:" style "jyacs_label"
                                    textbutton "开启" action ToggleDict(persistent.jyacs_setting_dict, "auto_reconnect") style "jyacs_button"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "启用触发器:" style "jyacs_label"
                                    textbutton "开启" action ToggleDict(persistent.jyacs_setting_dict, "enable_triggers") style "jyacs_button"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "启用情感系统:" style "jyacs_label"
                                    textbutton "开启" action ToggleDict(persistent.jyacs_setting_dict, "enable_emotion") style "jyacs_button"
            
            # 底部按钮
            hbox:
                style "jyacs_button_hbox"
                
                textbutton "保存设置" action [Function(store.jyacs_apply_setting), Hide("submod_jyacs_settings")] style "jyacs_button"
                
                textbutton "高级设置" action Show("submod_jyacs_advanced_settings") style "jyacs_button"
                
                textbutton "关闭" action Hide("submod_jyacs_settings") style "jyacs_button"

# 标签定义
init 10 python:
    # 注册标签到store
    def submod_jyacs_init_connect(use_pause_instand_wait=False):
        store.jyacs.content_func = store.jyacs_log
        store.jyacs_log("\n" * 25 + store.jyacs.ascii_icon, "INFO")
        
        if not store.jyacs.is_connected():
            store.jyacs.init_connect()
        
        while True:
            if not store.jyacs.is_connected():
                store.jyacs_log("正在初始化连接...", "INFO")
                renpy.pause(0.3, True)
                if not store.jyacs.is_failed():
                    continue
            
            if not store.jyacs.is_ready_to_input() and not store.jyacs.is_failed():
                store.jyacs_log("等待登录...", "INFO")
                if use_pause_instand_wait:
                    renpy.pause(1.0)
                else:
                    renpy.say(y, ".{w=0.3}.{w=0.3}.{w=0.3}{nw}")
                    if len(_history_list):
                        _history_list.pop()
                continue
            
            if store.jyacs.is_ready_to_input():
                store.jyacs_log("登录成功，准备开始聊天！", "INFO")
                return "success"
            elif store.jyacs.is_failed():
                store.jyacs_log("登录失败，请检查配置。", "ERROR")
                renpy.pause(2.0)
                return "disconnected"
    
    # 注册函数到store
    if not hasattr(store, 'submod_jyacs_init_connect'):
        store.submod_jyacs_init_connect = submod_jyacs_init_connect

# 高级设置屏幕
init 15 screen submod_jyacs_advanced_settings():
    modal True
    zorder 201
    
    add "#000000AA"
    
    frame:
        style "jyacs_frame"
        
        vbox:
            style "jyacs_vbox"
            
            text "JYACS 高级设置" style "jyacs_title"
            
            frame:
                style "jyacs_section_frame"
                
                viewport:
                    scrollbars "vertical"
                    ysize 480
                    xsize 780
                    
                    vbox:
                        style "jyacs_section_vbox"
                        
                        # 模型参数设置
                        frame:
                            style "jyacs_section_frame"
                            
                            vbox:
                                style "jyacs_option_vbox"
                                
                                text "模型参数" style "jyacs_section_title"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "Temperature:" style "jyacs_label"
                                    bar:
                                        value DictValue(persistent.jyacs_advanced_setting, "temperature", 1.0, step=0.1, offset=0.0)
                                        style "jyacs_bar"
                                        xsize 200
                                    text "[persistent.jyacs_advanced_setting.get('temperature', 0.7)]"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "Top P:" style "jyacs_label"
                                    bar:
                                        value DictValue(persistent.jyacs_advanced_setting, "top_p", 1.0, step=0.1, offset=0.0)
                                        style "jyacs_bar"
                                        xsize 200
                                    text "[persistent.jyacs_advanced_setting.get('top_p', 0.9)]"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "Max Tokens:" style "jyacs_label"
                                    bar:
                                        value DictValue(persistent.jyacs_advanced_setting, "max_tokens", 4096, step=256, offset=256)
                                        style "jyacs_bar"
                                        xsize 200
                                    text "[persistent.jyacs_advanced_setting.get('max_tokens', 2048)]"
                        
                        # 日志设置
                        frame:
                            style "jyacs_section_frame"
                            
                            vbox:
                                style "jyacs_option_vbox"
                                
                                text "日志设置" style "jyacs_section_title"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "日志级别:" style "jyacs_label"
                                    textbutton "[persistent.jyacs_setting_dict.get('log_level', 'INFO')]" action [
                                        SetDict(persistent.jyacs_setting_dict, "log_level", 
                                            {"INFO": "DEBUG", "DEBUG": "WARNING", "WARNING": "ERROR", "ERROR": "INFO"}[
                                                persistent.jyacs_setting_dict.get("log_level", "INFO")
                                            ]
                                        )
                                    ] style "jyacs_button"
                                
                                hbox:
                                    style "jyacs_option_hbox"
                                    text "控制台日志级别:" style "jyacs_label"
                                    textbutton "[persistent.jyacs_setting_dict.get('log_conlevel', 'INFO')]" action [
                                        SetDict(persistent.jyacs_setting_dict, "log_conlevel", 
                                            {"INFO": "DEBUG", "DEBUG": "WARNING", "WARNING": "ERROR", "ERROR": "INFO"}[
                                                persistent.jyacs_setting_dict.get("log_conlevel", "INFO")
                                            ]
                                        )
                                    ] style "jyacs_button"
            
            # 底部按钮
            hbox:
                style "jyacs_button_hbox"
                
                textbutton "保存设置" action [Function(store.jyacs_apply_setting), Hide("submod_jyacs_advanced_settings")] style "jyacs_button"
                
                textbutton "返回" action [Hide("submod_jyacs_advanced_settings"), Show("submod_jyacs_settings")] style "jyacs_button"

# 注册函数到store
init -700 python:
    # 注册所有公开函数到store
    _public_functions = {
        "jyacs_apply_setting": jyacs_apply_setting,
        "jyacs_verify_api_config": jyacs_verify_api_config,
        "calculate_sha256": calculate_sha256,
        "find_mail_files": find_mail_files,
        "get_user_api_token": get_user_api_token,
        "get_user_api_url": get_user_api_url,
        "get_user_model_name": get_user_model_name
    }
    for name, func in _public_functions.items():
        if not hasattr(store, name):
            setattr(store, name, func)

# ... existing code ...

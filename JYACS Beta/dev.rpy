# dev.rpy - JustYuriAIChatSubmod 文本处理核心逻辑
# 版本: 1.1.0 (重构版)
# 作者: Panghu1102

init -950 python:
    import sys
    import os
    import traceback

    # 1. 路径设置 (统一)
    # 此部分逻辑已移至 jyacs_init.rpy 以确保最先执行

    # 2. 模块导入与函数注册 (合并)
    try:
        # 统一导入所有需要的模块
        from jyacs_interface import JyacsTalkSplitV2, key_replace, add_pauses
        from jyacs_emotion import JyacsEmoSelector
        from jyacs_utils import jyacs_logger

        # 定义并注册基于模块的函数
        if not hasattr(store, 'jyacs_log'):
            def jyacs_log(message, level="INFO"):
                try:
                    log_map = {
                        "ERROR": jyacs_logger.log_error,
                        "WARNING": jyacs_logger.log_warning,
                        "DEBUG": jyacs_logger.log_debug
                    }
                    log_map.get(level, jyacs_logger.log_info)(message)
                except Exception as e:
                    print(u"[JYACS-LOGFAIL] [{}]: {} ({})".format(level, message, e))
            store.jyacs_log = jyacs_log

        if not hasattr(store, 'key_replace'): store.key_replace = key_replace
        if not hasattr(store, 'TalkSplitV2'): store.TalkSplitV2 = JyacsTalkSplitV2
        if not hasattr(store, 'add_pauses'): store.add_pauses = add_pauses
        if not hasattr(store, 'jyacs_emotion_selector'):
            store.jyacs_emotion_selector = JyacsEmoSelector()
        
        store.jyacs_log("JYACS文本处理模块加载成功", "INFO")

    except ImportError as e:
        # 降级处理: 如果模块导入失败，定义并注册模拟函数
        print(u"JYACS模块导入失败，使用模拟(mock)模式: {}".format(e))
        traceback.print_exc()
        
        if not hasattr(store, 'jyacs_log'):
            def jyacs_log_mock(message, level="INFO"):
                print(u"[JYACS-MOCK-{}] {}".format(level, message))
            store.jyacs_log = jyacs_log_mock
        
        if not hasattr(store, 'key_replace'):
            def key_replace_mock(text, replace_dict=None):
                if not replace_dict: return text
                for k, v in replace_dict.items():
                    text = text.replace(str(k), str(v))
                return text
            store.key_replace = key_replace_mock

        if not hasattr(store, 'TalkSplitV2'): store.TalkSplitV2 = lambda: None
        if not hasattr(store, 'add_pauses'): store.add_pauses = lambda text: text
        if not hasattr(store, 'jyacs_emotion_selector'): store.jyacs_emotion_selector = None

    # 3. 文本处理核心函数 (使用hasattr保护)
    if not hasattr(store, 'process_user_message'):
        def process_user_message(message):
            """处理用户消息，替换关键词"""
            try:
                player_name = store.player if hasattr(store, 'player') else "Player"
                # 确保是unicode字符串
                processed = unicode(message)
                return store.key_replace(processed, {
                    u"[player]": player_name,
                    u"{player}": player_name
                })
            except Exception as e:
                store.jyacs_log(u"处理用户消息失败: {}".format(e), "ERROR")
                return message
        store.process_user_message = process_user_message

    if not hasattr(store, 'process_ai_reply_with_splitter'):
        def process_ai_reply_with_splitter(ai_reply):
            """使用分句器处理AI回复"""
            try:
                if not ai_reply: return []
                # 确保 TalkSplitV2 可用
                if not store.TalkSplitV2: return [ai_reply]
                splitter = store.TalkSplitV2()
                
                splitter.add_part(ai_reply)
                sentences = []
                while True:
                    sentence = splitter.split_present_sentence()
                    if sentence is None: break
                    sentences.append(sentence)
                sentences.extend(splitter.announce_stop())
                
                return sentences
            except Exception as e:
                store.jyacs_log(u"AI回复分句失败: {}".format(e), "ERROR")
                return [ai_reply]
        store.process_ai_reply_with_splitter = process_ai_reply_with_splitter
        
    if not hasattr(store, 'apply_emotion_analysis'):
        def apply_emotion_analysis(text):
            """应用情绪分析"""
            try:
                if store.jyacs_emotion_selector:
                    text, emote = store.jyacs_emotion_selector.analyze(text), store.jyacs_emotion_selector.get_emote()
                    return text, emote
            except Exception as e:
                store.jyacs_log(u"情绪分析失败: {}".format(e), "ERROR")
            return text, "1eua"
        store.apply_emotion_analysis = apply_emotion_analysis

    # 4. 辅助函数
    if not hasattr(store, 'clean_text_for_display'):
        def clean_text_for_display(text):
            """清理文本用于显示，移除Ren'Py特殊字符"""
            try:
                return store.key_replace(unicode(text), {u"[": u"", u"]": u"", u"{": u"", u"}": u"", u"%": u"%%"})
            except Exception as e:
                store.jyacs_log(u"清理文本失败: {}".format(e), "ERROR")
                return text
        store.clean_text_for_display = clean_text_for_display

    if not hasattr(store, 'process_chat_history'):
        def process_chat_history(history, max_messages=50):
            """处理聊天历史，限制长度并清理"""
            try:
                if not history: return []
                cleaned = []
                for msg in history[-max_messages:]:
                    if isinstance(msg, (list, tuple)) and len(msg) >= 2:
                        cleaned.append((msg[0], clean_text_for_display(msg[1])))
                    elif isinstance(msg, basestring):
                        cleaned.append(("1eua", clean_text_for_display(msg)))
                return cleaned
            except Exception as e:
                store.jyacs_log(u"处理聊天历史失败: {}".format(e), "ERROR")
                return []
        store.process_chat_history = process_chat_history

# 5. 最终加载日志
init 1000 python:
    # 确保 jyacs_log 在store中，如果不在则使用print
    log_func = store.jyacs_log if hasattr(store, 'jyacs_log') else print
    log_func("dev.rpy: 文本处理模块已加载", "INFO")



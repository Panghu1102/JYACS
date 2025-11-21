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
# dev.rpy - JustYuriAIChatSubmod 文本处理核心逻辑
# 版本: 1.0.1
# 作者: Panghu1102

init -900 python:
    import sys
    import os
    import traceback

    sys.path.append(config.basedir + "/game/python-packages")

    # 1. 基础日志函数 (确保最基本的日志功能可用)
    if not hasattr(store, 'jyacs_basic_log'):
        def jyacs_basic_log(message, level="INFO"):
            """基础日志函数，在完整日志系统可用前使用"""
            try:
                print(u"[JYACS-{}] {}".format(level, message))
            except Exception as e:
                print(u"[JYACS-LOGFAIL] Basic log failed: {}".format(e))
        store.jyacs_basic_log = jyacs_basic_log

    # 2. 模块导入与函数注册
    try:
        # 统一导入所需模块
        from jyacs_interface import JyacsTalkSplitV2, key_replace, add_pauses, JyacsTextProcessor
        from jyacs_emotion import JyacsEmoSelector, JyacsEmotionAnalyzer
        from jyacs_utils import jyacs_logger, JyacsConfig

        # 注册核心组件
        if not hasattr(store, 'jyacs_text_processor'):
            store.jyacs_text_processor = JyacsTextProcessor()
        if not hasattr(store, 'jyacs_emotion_analyzer'):
            store.jyacs_emotion_analyzer = JyacsEmotionAnalyzer()
        if not hasattr(store, 'jyacs_config'):
            store.jyacs_config = JyacsConfig()
            
        # 确保表情系统初始化
        if hasattr(store, 'show_chr') and hasattr(store, 'get_expression_from_text'):
            store.jyacs_basic_log("JUSTYURI表情系统已加载", "INFO")
        else:
            store.jyacs_basic_log("警告：JUSTYURI表情系统未加载", "WARNING")

        # 定义并注册日志函数
        if not hasattr(store, 'jyacs_log'):
            def jyacs_log(message, level="INFO"):
                try:
                    log_map = {
                        "ERROR": jyacs_logger.log_error,
                        "WARNING": jyacs_logger.log_warning,
                        "DEBUG": jyacs_logger.log_debug,
                        "CRITICAL": jyacs_logger.log_critical
                    }
                    log_func = log_map.get(level.upper(), jyacs_logger.log_info)
                    log_func(message)
                except Exception as e:
                    store.jyacs_basic_log(u"日志记录失败: {} ({})".format(message, e), "ERROR")
            store.jyacs_log = jyacs_log

        # 注册工具函数
        if not hasattr(store, 'key_replace'): store.key_replace = key_replace
        if not hasattr(store, 'add_pauses'): store.add_pauses = add_pauses
        if not hasattr(store, 'jyacs_emotion_selector'):
            store.jyacs_emotion_selector = JyacsEmoSelector()
        if not hasattr(store, 'TalkSplitV2'):
            store.TalkSplitV2 = JyacsTalkSplitV2
        
        store.jyacs_log("JYACS文本处理模块加载成功", "INFO")

    except ImportError as e:
        store.jyacs_basic_log(u"JYACS模块导入失败，使用降级模式: {}".format(e), "ERROR")
        traceback.print_exc()
        
        # 降级处理：提供基本功能的模拟实现
        if not hasattr(store, 'jyacs_log'):
            store.jyacs_log = store.jyacs_basic_log
        
        if not hasattr(store, 'key_replace'):
            def key_replace_mock(text, replace_dict=None):
                if not isinstance(text, (str, unicode)) or not replace_dict:
                    return text
                try:
                    for k, v in replace_dict.items():
                        text = text.replace(str(k), str(v))
                    return text
                except Exception as e:
                    store.jyacs_basic_log(u"关键词替换失败: {}".format(e), "ERROR")
                    return text
            store.key_replace = key_replace_mock

        if not hasattr(store, 'add_pauses'):
            store.add_pauses = lambda text: text
        if not hasattr(store, 'jyacs_emotion_selector'):
            store.jyacs_emotion_selector = None

    # 3. 文本处理核心函数
    if not hasattr(store, 'process_user_message'):
        def process_user_message(message):
            """处理用户消息，替换关键词并进行清理"""
            try:
                if not isinstance(message, (str, unicode)):
                    return str(message)

                player_name = store.player if hasattr(store, 'player') else "Player"
                processed = unicode(message)
                
                # 基础替换
                processed = store.key_replace(processed, {
                    u"[player]": player_name,
                    u"{player}": player_name,
                    u"[Player]": player_name,
                    u"{Player}": player_name
                })
                
                # 清理特殊字符
                processed = store.clean_text_for_display(processed)
                
                return processed
            except Exception as e:
                store.jyacs_log(u"处理用户消息失败: {}".format(e), "ERROR")
                return message
        store.process_user_message = process_user_message

    if not hasattr(store, 'process_ai_reply'):
        def process_ai_reply(ai_reply):
            """处理AI回复，包括分句和情绪分析"""
            try:
                if not ai_reply:
                    return [], "1eua"

                # 文本处理
                if hasattr(store, 'jyacs_text_processor'):
                    sentences = store.jyacs_text_processor.process_text(ai_reply)
                else:
                    sentences = [ai_reply]

                # 情绪分析
                if hasattr(store, 'jyacs_emotion_analyzer'):
                    final_text = " ".join(sentences)
                    processed_text, emotion = store.jyacs_emotion_analyzer.analyze_text_emotion(final_text)
                    return [processed_text], emotion
                
                return sentences, "1eua"
            except Exception as e:
                store.jyacs_log(u"处理AI回复失败: {}".format(e), "ERROR")
                return [ai_reply], "1eua"
        store.process_ai_reply = process_ai_reply

    # 4. 辅助函数
    if not hasattr(store, 'clean_text_for_display'):
        def clean_text_for_display(text):
            """清理文本用于显示，移除特殊字符并处理转义"""
            try:
                if not isinstance(text, (str, unicode)):
                    return str(text)
                    
                # 转换为unicode
                text = unicode(text)
                
                # 移除Ren'Py特殊字符
                replacements = {
                    u"[": u"",
                    u"]": u"",
                    u"{": u"",
                    u"}": u"",
                    u"%": u"%%",
                    u"\\": u"\\\\",
                    u"\n": u" "
                }
                return store.key_replace(text, replacements)
            except Exception as e:
                store.jyacs_log(u"清理文本失败: {}".format(e), "ERROR")
                return text
        store.clean_text_for_display = clean_text_for_display

    if not hasattr(store, 'process_chat_history'):
        def process_chat_history(history, max_messages=50):
            """处理聊天历史，限制长度并清理文本"""
            try:
                if not history:
                    return []
                    
                cleaned = []
                for msg in history[-max_messages:]:
                    try:
                        if isinstance(msg, (list, tuple)) and len(msg) >= 2:
                            cleaned.append((
                                msg[0],
                                store.clean_text_for_display(msg[1])
                            ))
                        elif isinstance(msg, (str, unicode)):
                            cleaned.append((
                                "1eua",
                                store.clean_text_for_display(msg)
                            ))
                    except Exception as e:
                        store.jyacs_log(u"处理单条历史记录失败: {}".format(e), "WARNING")
                        continue
                        
                return cleaned
            except Exception as e:
                store.jyacs_log(u"处理聊天历史失败: {}".format(e), "ERROR")
                return []
        store.process_chat_history = process_chat_history

# 5. 最终加载确认
init 20 python:
    try:
        store.jyacs_log("dev.rpy: 文本处理模块已完成加载", "INFO")
    except Exception as e:
        print(u"警告: python-packages 路径不存在或模块加载失败")



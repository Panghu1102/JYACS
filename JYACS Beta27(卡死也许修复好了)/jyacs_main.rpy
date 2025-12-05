# jyacs_main.rpy - JYACS 主要游戏脚本
# 版本: 1.0.0
# 作者: Panghu1102

image jy_bg = "mod_assets/images/jy_bg.png"

# 样式定义 - 降低优先级
init 50 python:
    # 确保不覆盖已有样式


    style.jyacs_input_text = Style(style.text)
    style.jyacs_input_text.font = "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    style.jyacs_input_text.size = 16
    style.jyacs_input_text.color = "#FFFFFF"
    style.jyacs_input_text.outlines = [(1, "#000000", 0, 0)]

# 初始化变量 - 降低优先级
init -890 python:
    # 创建空的消息列表
    if not hasattr(store, 'jyacs_messages'):
        store.jyacs_messages = []
    
    # 创建空的日志历史
    if not hasattr(store, 'jyacs_log_history'):
        store.jyacs_log_history = []
    
    # 发送消息的函数
    def jyacs_send_message(message):
        """发送消息到JYACS"""
        if not message or not message.strip():
            return
        
        # 添加到消息列表
        store.jyacs_messages.append(message)
        
        # 如果JYACS可用，发送消息
        if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'chat'):
            store.jyacs.chat(message)
    
    # 进度条函数(如果不存在)
    if not hasattr(store, 'jyacs_progress_bar'):
        def jyacs_progress_bar(percentage, current=None, total=None, bar_length=20):
            """进度条显示函数"""
            filled_length = int(round(bar_length * percentage / 100.0))
            bar = '▇' * filled_length + ' ' * (bar_length - filled_length)
            
            if total is not None:
                return '|{}| {}% | {} / {}'.format(bar, int(percentage), current, total)
            elif current is not None:
                return '|{}| {}% | {}'.format(bar, int(percentage), current)
            else:
                return '|{}| {}%'.format(bar, int(percentage))
        
        store.jyacs_progress_bar = jyacs_progress_bar

# 聊天界面
init 5 python:
    def show_expression(emote):
        """显示优里的表情"""
        renpy.show("yuri {} at t11".format(emote))

# 错误处理
init 5 python:
    def handle_mspire_error():
        """处理MSpire错误"""
        renpy.say("优里", "MSpire暂时无法使用。")
        return "error"
    
    def handle_mail_error():
        """处理邮件错误"""
        renpy.say("优里", "邮件处理暂时无法使用。")
        return "error"

# 聊天界面标签 - 添加submod_前缀
label submod_jyacs_chat_start:
    scene jy_bg
    
    python:
        # 确保应用最新的JYACS设置
        if hasattr(store, 'jyacs_apply_setting'):
            store.jyacs_apply_setting()
    
    show yuri 1eua at t11
    y "你好！我是优里，很高兴见到你。"
    y "我们可以开始聊天了。"
    
    jump submod_jyacs_talking

label submod_jyacs_chat_end:
    y "再见！希望我们下次还能聊天。"
    return "normal"

# 聊天界面屏幕
# 状态界面
init 15 screen jyacs_status_overlay():
    zorder 100
    
    if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'is_responding') and store.jyacs.is_responding:
        frame:
            background "#000000B2"
            xalign 1.0
            yalign 0.0
            padding (10, 5)
            
            text "思考中..." style "jyacs_console_text"
    use free_chat_overlay





# MSpire功能 - 添加submod_前缀
label submod_jyacs_mspire:
    python:
        store.jyacs_mspire_response = None
        if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'is_ready_to_input') and store.jyacs.is_ready_to_input:
            if hasattr(store.jyacs, 'start_MSpire'):
                store.jyacs.start_MSpire()
                if hasattr(store.jyacs, 'get_message'):
                    response_data = store.jyacs.get_message()
                    if response_data:
                        emote, response_text = response_data
                        if hasattr(store, 'emotion_analyzer'):
                            analyzed_text, final_emote = store.emotion_analyzer.analyze_text_emotion(response_text)
                        else:
                            analyzed_text, final_emote = response_text, emote
                        store.jyacs_mspire_response = (final_emote, analyzed_text)

    if store.jyacs_mspire_response:
        $ emote, text = store.jyacs_mspire_response
        show yuri [emote]
        y "[text]"
    else:
        y "MSpire暂时无法使用。"
    return "normal"

# 邮件功能 - 添加submod_前缀
label submod_jyacs_mpostal_read:
    python:
        store.jyacs_mpostal_response = None
        if store.jyacs.is_ready_to_input:
            # 模拟邮件内容
            mail_content = "这是一封来自[player]的邮件。"
            store.jyacs.start_MPostal(mail_content, "问候邮件")
            response_data = store.jyacs.get_message()
            if response_data:
                emote, response_text = response_data
                analyzed_text, final_emote = store.emotion_analyzer.analyze_text_emotion(response_text)
                store.jyacs_mpostal_response = (final_emote, analyzed_text)

    if store.jyacs_mpostal_response:
        $ emote, text = store.jyacs_mpostal_response
        show yuri [emote]
        y "[text]"
    else:
        y "邮件处理暂时无法使用。"
    return "normal"

# 修改主聊天功能 - 添加submod_前缀
label submod_jyacs_talking(mspire=False):
    show yuri at t11
    
    show screen jyacs_status_overlay
    
    call submod_jyacs_init_connect(use_pause_instand_wait=True)
    if _return == "disconnected":
        hide screen jyacs_status_overlay
        return "disconnected"
    
    python:
        import time
        import copy
        from jyacs_utils import JyacsLogger
        from jyacs_emotion import JyacsEmoSelector
        import traceback
        
        # 设置日志记录器
        store.jyacs.content_func = store.jyacs_log
        store.action = {}
        
        # 设置对话超时保护
        if not hasattr(store, '_jyacs_dialogue_start_time'):
            store._jyacs_dialogue_start_time = time.time()
        else:
            store._jyacs_dialogue_start_time = time.time()  # 重置开始时间
        
        if mspire:
            store.jyacs_log("<submod> MSpire init...", "INFO")
            renpy.pause(2.3)
        
        printed = False
        is_retry_before_sendmessage = False
        question = False
        max_dialogue_time = 300  # 5分钟最大对话时间
        
        while True:
            # 全局超时检查
            current_time = time.time()
            if current_time - store._jyacs_dialogue_start_time > max_dialogue_time:
                store.jyacs_log("对话超时保护触发，强制退出", "WARNING")
                _return = "disconnected"
                break
            
            if is_retry_before_sendmessage:
                store.jyacs.chat(is_retry_before_sendmessage)
                question = is_retry_before_sendmessage
                is_retry_before_sendmessage = False
            
            renpy.show("yuri {}".format(store.jyacs.MoodStatus.get_emote()))
            
            if store.jyacs.is_ready_to_input:
                if not mspire:
                    if "stop" in store.action:
                        if store.action["stop"]:
                            store.action = {}
                            _return = "canceled"
                            break
                    
                    # 获取用户输入 - 使用标准Renpy对话输入
                    question = renpy.input(
                        _("说吧, [persistent.playername]"),
                        default="",
                        length=75 if not config.language == "english" else 375
                    ).strip(' \t\n\r')
                    
                    if question == "":
                        continue
                    if question == "nevermind":
                        _return = "canceled"
                        store.jyacs.content_func = None
                        break
                    
                    # 添加到历史记录
                    to_history = copy.deepcopy(_history_list[-1])
                    to_history.who = persistent.playername
                    to_history.what = question
                    _history_list.append(to_history)
                    
                    # 发送消息
                    store.jyacs.chat(question)
                    is_retry_before_sendmessage = False
                else:
                    store.jyacs.start_MSpire()
            
            elif not store.jyacs.is_connected and persistent.jyacs_setting_dict.get('auto_reconnect', True):
                # 限制重连尝试次数，避免无限重连
                if not hasattr(store, '_jyacs_reconnect_count'):
                    store._jyacs_reconnect_count = 0
                
                if store._jyacs_reconnect_count < 3:  # 最多重连3次
                    store.jyacs.init_connect()
                    renpy.pause(1.0, True)  # 给重连更多时间
                    store.jyacs_log("WebSocket已断开，正在重新连接... (尝试 %d/3)" % (store._jyacs_reconnect_count + 1), "WARNING")
                    store._jyacs_reconnect_count += 1
                    is_retry_before_sendmessage = question if question else False
                    continue
                else:
                    store.jyacs_log("重连失败次数过多，放弃重连", "ERROR")
                    store._jyacs_reconnect_count = 0  # 重置计数器
                    _return = "disconnected"
                    break
            else:
                _return = "disconnected"
                store.jyacs_log("jyacs_talking::断开连接，可能是意外情况", "WARNING")
                break
            
            # 处理响应
            start_time = time.time()
            start_token = store.jyacs.stat.get("received_token", 0)
            received_message = ""
            gentime = 0.0
            max_wait_time = 60  # 最大等待时间60秒
            
            while True:
                current_time = time.time()
                elapsed_time = current_time - start_time
                
                if store.jyacs.is_responding:
                    gentime = current_time
                else:
                    gentime = store.jyacs._gen_time
                
                # 超时检查
                if elapsed_time > max_wait_time:
                    store.jyacs_log("消息处理超时，强制退出", "WARNING")
                    _return = "disconnected"
                    break
                
                # 只在连接断开时尝试重连一次，避免无限重连
                if not store.jyacs.is_connected and persistent.jyacs_setting_dict.get('auto_reconnect', True):
                    if elapsed_time < 10:  # 只在10秒内尝试重连
                        store.jyacs.init_connect()
                        store.jyacs_log("WebSocket已断开，正在重新连接...", "WARNING")
                        renpy.pause(1.0, hard=True)  # 给重连一些时间
                    else:
                        store.jyacs_log("重连超时，放弃重连", "WARNING")
                        _return = "disconnected"
                        break
                
                # 显示状态
                store.jyacs_log("JYACS状态:%s | 消息队列: %d/%dtoken | 时间: %.1fs" % (
                    store.jyacs.status,
                    store.jyacs.len_message_queue,
                    store.jyacs.stat.get("received_token", 0) - start_token,
                    elapsed_time
                ), "INFO")
                
                if store.jyacs.is_failed:
                    if store.jyacs.len_message_queue == 0:
                        y(_("好像出了什么问题..."))
                        _return = "disconnected"
                        break
                
                # 检查是否有消息需要处理
                if store.jyacs.len_message_queue > 0:
                    # 获取并显示消息
                    message = store.jyacs.get_message()
                    if message:
                        store.jyacs_log("jyacs_talking::message:'%s', '%s'" % (message[0], message[1]), "DEBUG")
                        received_message += message[1]

                        # 使用新的表情背景系统
                        emotion_name = message[0]
                        display_name = emotion_name.replace(" ", "_")
                        renpy.show("jyacs_emotion_{} at truecenter".format(display_name))
                        try:
                            y(message[1])
                        except Exception as e:
                            store.jyacs_log("jyacs_talking::renpy.say error:{}".format(traceback.format_exc()), "ERROR")
                            store.jyacs_log("!!SUBMOD ERROR when chatting: {}".format(e), "ERROR")
                    
                    # 检查是否还有更多消息
                    if not store.jyacs.is_responding and store.jyacs.len_message_queue == 0:
                        break
                else:
                    # 等待消息，但避免无限等待
                    if store.jyacs.is_responding:
                        store.jyacs_log("等待消息...", "INFO")
                        y(".{w=0.3}.{w=0.3}.{w=0.3}{nw}")
                        if len(_history_list):
                            _history_list.pop()
                    
                    # 使用较短的等待时间，避免长时间阻塞
                    renpy.pause(0.3, hard=True)
                    
                    # 确保正确退出循环
                    if not store.jyacs.is_responding and store.jyacs.len_message_queue == 0:
                        break
                    
                    # 如果长时间没有响应，强制退出
                    if elapsed_time > 30 and not store.jyacs.is_responding:
                        store.jyacs_log("长时间无响应，强制退出", "WARNING")
                        _return = "disconnected"
                        break

            store.jyacs_log("jyacs_talking::RESPONSE :'%s'" % received_message, "DEBUG")
            _return = "mtrigger_triggering"
            
            # 处理触发器
            store.action = store.jyacs.mtrigger_manager.run_trigger("post")
            store.jyacs_log("<chat_action> {}".format(store.action), "DEBUG")
            
            if store.action.get('stop', False):
                _return = "canceled"
                break
            
            if mspire:
                _return = "canceled"
                afm_pref = renpy.game.preferences.afm_enable
                renpy.game.preferences.afm_enable = False
                break

label submod_jyacs_init_connect(use_pause_instand_wait=False):
    python:
        import time
        store.jyacs.content_func = store.jyacs_log
        store.jyacs_log("\n" * 25 + "=== JYACS AI Chat Submod ===", "INFO")
        
        if not store.jyacs.is_connected:
            store.jyacs.init_connect()
        
        while True:
            if not store.jyacs.is_connected:
                store.jyacs_log("正在初始化连接...", "INFO")
                renpy.pause(0.3, True)
                if not store.jyacs.is_failed:
                    continue
            
            if not store.jyacs.is_ready_to_input() and not store.jyacs.is_failed:
                store.jyacs_log("等待登录...", "INFO")
                if use_pause_instand_wait:
                    renpy.pause(1.0)
                else:
                    time.sleep(1.0)
            else:
                break
        
        if store.jyacs.is_failed:
            _return = "disconnected"
        else:
            _return = "connected"
    return _return

label submod_jyacs_talking_end:
    if persistent.jyacs_setting_dict.get('console', True):
        $ store.jyacs_log("清理控制台...", "INFO")
        hide screen jyacs_console_teaching
        show yuri at t11
    
    # 重置重连计数器
    python:
        if hasattr(store, '_jyacs_reconnect_count'):
            store._jyacs_reconnect_count = 0
    
    hide screen jyacs_status_overlay
    return _return
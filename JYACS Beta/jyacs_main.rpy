# jyacs_main.rpy - JYACS 主要游戏脚本
# 版本: 1.0.0
# 作者: Panghu1102

# 在文件开头添加样式定义
style jyacs_console_text:
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    size 14
    color "#FFFFFF"
    outlines [(1, "#000000", 0, 0)]

style jyacs_input_text:
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    size 16
    color "#FFFFFF"
    outlines [(1, "#000000", 0, 0)]

# 初始化变量
init -10 python:
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
label jyacs_chat_start:
    scene bg bedroom
    with dissolve
    
    python:
        # 确保JYACS已初始化
        if not hasattr(store, 'jyacs') or not store.jyacs:
            # 修正: 使用正确的类引用
            if hasattr(store, 'JyacsAi'):
                store.jyacs = store.JyacsAi(
                    store.persistent.jy_ai_api_key,
                    store.persistent.jy_ai_api_url,
                    store.persistent.jy_ai_model_name
                )
            else:
                # 如果JyacsAi不存在，尝试从jyacs模块导入
                from store.jyacs import JyacsAi
                store.jyacs = JyacsAi(
                    store.persistent.jy_ai_api_key,
                    store.persistent.jy_ai_api_url,
                    store.persistent.jy_ai_model_name
                )
    
    show yuri 1eua at t11
    y "你好！我是优里，很高兴见到你。"
    y "我们可以开始聊天了。"
    
    jump jyacs_chat_loop

label jyacs_chat_loop:
    python:
        # 检查JYACS状态
        if hasattr(store, 'jyacs'):
            if hasattr(store.jyacs, 'is_ready_to_input'):
                if not store.jyacs.is_ready_to_input():
                    if hasattr(store.jyacs, 'is_failed') and store.jyacs.is_failed():
                        renpy.notify("JYACS连接失败，请检查配置")
                        renpy.jump("jyacs_chat_start")
                    else:
                        renpy.notify("JYACS正在连接中，请稍候...")
                        renpy.pause(1.0)
                        renpy.jump("jyacs_chat_loop")
    
    # 显示聊天界面
    call screen jyacs_chat_screen
    
    # 处理用户输入
    $ user_input = _return
    
    if user_input == "quit":
        jump jyacs_chat_end
    elif user_input == "nevermind":
        y "好的，我们继续聊天吧。"
        jump jyacs_chat_loop
    elif user_input and user_input.strip():
        # 处理用户消息
        $ processed_input = store.process_user_message(user_input) if hasattr(store, 'process_user_message') else user_input
        
        # 发送到AI
        $ jyacs_send_message(processed_input)
        
        # 等待响应
        $ response_data = store.jyacs.get_message() if hasattr(store.jyacs, 'get_message') else None
        
        if response_data:
            $ emote, response_text = response_data
            
            # 应用情绪分析
            $ analyzed_text, final_emote = store.apply_emotion_analysis(response_text) if hasattr(store, 'apply_emotion_analysis') else (response_text, emote)
            
            # 显示优里的回复
            $ show_expression(final_emote)
            y "[analyzed_text]"
        else:
            y "抱歉，我现在无法回应。请稍后再试。"
    
    jump jyacs_chat_loop

label jyacs_chat_end:
    y "再见！希望我们下次还能聊天。"
    return

# 显示表情的函数
init python:
    def show_expression(emote):
        """显示优里的表情"""
        if emote == "1eua":
            renpy.show("yuri 1eua at t11")
        elif emote == "1hub":
            renpy.show("yuri 1hub at t11")
        elif emote == "1sua":
            renpy.show("yuri 1sua at t11")
        elif emote == "1lua":
            renpy.show("yuri 1lua at t11")
        else:
            renpy.show("yuri 1eua at t11")

# 聊天界面屏幕
init 5 screen jyacs_chat_screen():
    style_prefix "jyacs"
    
    default jyacs_input_value = ""  # 初始化输入变量
    
    frame:
        style "jyacs_frame"
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        
        vbox:
            style "jyacs_vbox"
            xfill True
            spacing 20
            
            # 聊天区域
            frame:
                style "jyacs_chat_frame"
                xfill True
                yfill True
                
                viewport:
                    style "jyacs_viewport"
                    mousewheel True
                    scrollbars "vertical"
                    
                    vbox:
                        style "jyacs_message_vbox"
                        for message in store.jyacs_messages:
                            text message style "jyacs_message_text"
            
            # 输入区域
            hbox:
                style "jyacs_input_hbox"
                spacing 10
                
                input:
                    style "jyacs_input"
                    value ScreenVariableInputValue("jyacs_input_value")
                    length 200
                
                textbutton "发送":
                    style "jyacs_button"
                    action [Function(jyacs_send_message, jyacs_input_value), SetScreenVariable("jyacs_input_value", "")]

# 错误处理
init 5 python:
    def handle_mspire_error():
        """处理MSpire错误"""
        renpy.say("优里", "MSpire暂时无法使用。")
    
    def handle_mail_error():
        """处理邮件错误"""
        renpy.say("优里", "邮件处理暂时无法使用。")

# 样式定义
style jyacs_frame:
    background "#2A2A2A"
    padding (40, 40)

style jyacs_vbox:
    spacing 20
    xfill True

style jyacs_chat_frame:
    background "#1A1A1A"
    padding (20, 20)

style jyacs_viewport:
    xfill True
    yfill True

style jyacs_message_vbox:
    spacing 10
    xfill True

style jyacs_message_text:
    color "#FFFFFF"
    size 18

style jyacs_input_hbox:
    spacing 10
    xfill True

style jyacs_input:
    background "#404040"
    color "#FFFFFF"
    size 18
    xfill True

style jyacs_button:
    background "#4A7C59"
    hover_background "#5A8C69"
    padding (20, 10)
    color "#FFFFFF"

# MSpire功能
label jyacs_mspire:
    python:
        store.jyacs_mspire_response = None
        if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'is_ready_to_input') and store.jyacs.is_ready_to_input():
            if hasattr(store.jyacs, 'start_MSpire'):
                store.jyacs.start_MSpire()
                if hasattr(store.jyacs, 'get_message'):
                    response_data = store.jyacs.get_message()
                    if response_data:
                        emote, response_text = response_data
                        if hasattr(store, 'apply_emotion_analysis'):
                            analyzed_text, final_emote = store.apply_emotion_analysis(response_text)
                        else:
                            analyzed_text, final_emote = response_text, emote
                        store.jyacs_mspire_response = (final_emote, analyzed_text)

    if store.jyacs_mspire_response:
        $ emote, text = store.jyacs_mspire_response
        show yuri expression emote
        y "[text]"
    else:
        y "MSpire暂时无法使用。"
    return

# 邮件功能
label jyacs_mpostal_read:
    python:
        store.jyacs_mpostal_response = None
        if store.jyacs.is_ready_to_input():
            # 模拟邮件内容
            mail_content = "这是一封来自[player]的邮件。"
            store.jyacs.start_MPostal(mail_content, "问候邮件")
            response_data = store.jyacs.get_message()
            if response_data:
                emote, response_text = response_data
                analyzed_text, final_emote = store.apply_emotion_analysis(response_text)
                store.jyacs_mpostal_response = (final_emote, analyzed_text)

    if store.jyacs_mpostal_response:
        $ emote, text = store.jyacs_mpostal_response
        show yuri expression emote
        y "[text]"
    else:
        y "邮件处理暂时无法使用。"
    return

# 测试功能
label jyacs_test:
    python:
        # 测试文本处理
        test_text = "你好[player]，今天天气怎么样？"
        processed = store.process_user_message(test_text)
        store.jyacs_log("测试文本处理: {} -> {}".format(test_text, processed), "DEBUG")
        
        # 测试分句
        test_reply = "今天天气很好。我很开心能和你聊天。"
        sentences = store.process_ai_reply_with_splitter(test_reply)
        store.jyacs_log("测试分句: {} -> {}".format(test_reply, sentences), "DEBUG")
        
        # 测试情绪分析
        emotion_text, emotion = store.apply_emotion_analysis("我很开心！")
        store.jyacs_log("测试情绪分析: 开心 -> {}".format(emotion), "DEBUG")
    
    y "测试完成！请查看日志文件了解详细信息。"
    return 

# 添加状态界面
screen jyacs_status_overlay():
    zorder 100
    
    if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'is_responding') and store.jyacs.is_responding():
        frame:
            background "#000000B2"
            xalign 1.0
            yalign 0.0
            padding (10, 5)
            
            text "思考中..." style "jyacs_console_text"

# 修改主聊天功能
label jyacs_talking(mspire=False):
    if persistent.jyacs_setting_dict['console']:
        show yuri at t22
        show screen jyacs_console_teaching
    
    show screen jyacs_status_overlay
    
    call jyacs_init_connect(use_pause_instand_wait=True)
    if _return == "disconnected":
        hide screen jyacs_status_overlay
        return "disconnected"
    
    python:
        import time
        import copy
        from store.jyacs_utils import jyacs_logger
        from store.jyacs_emotion import JyacsEmoSelector
        import traceback
        
        # 设置日志记录器
        store.jyacs.content_func = store.jyacs_log
        store.action = {}
        
        if mspire:
            jyacs_logger.log_info("<submod> MSpire init...")
            renpy.pause(2.3)
        
        printed = False
        is_retry_before_sendmessage = False
        question = False
        
        while True:
            if is_retry_before_sendmessage:
                store.jyacs.chat(is_retry_before_sendmessage)
                question = is_retry_before_sendmessage
                is_retry_before_sendmessage = False
            
            renpy.show("yuri {}".format(store.jyacs.MoodStatus.get_emote()))
            
            if store.jyacs.is_ready_to_input():
                if not mspire:
                    if "stop" in store.action:
                        if store.action["stop"]:
                            store.action = {}
                            _return = "canceled"
                            break
                    
                    # 获取用户输入
                    question = renpy.input(
                        _("说吧, [player]"),
                        default="",
                        length=75 if not config.language == "english" else 375,
                        screen="jyacs_input_screen"
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
            
            elif not store.jyacs.is_connected() and persistent.jyacs_setting_dict['auto_reconnect']:
                store.jyacs.init_connect()
                renpy.pause(0.3, True)
                store.jyacs_log("WebSocket已断开，正在重新连接...", "WARNING")
                is_retry_before_sendmessage = question if question else False
                continue
            else:
                _return = "disconnected"
                store.jyacs_log("jyacs_talking::断开连接，可能是意外情况", "WARNING")
                break
            
            # 处理响应
            start_time = time.time()
            start_token = store.jyacs.stat.get("received_token", 0)
            received_message = ""
            gentime = 0.0
            
            while store.jyacs.is_responding() or store.jyacs.len_message_queue() > 0:
                if store.jyacs.is_responding():
                    gentime = time.time()
                else:
                    gentime = store.jyacs._gen_time
                
                if not store.jyacs.is_connected() and persistent.jyacs_setting_dict['auto_reconnect']:
                    store.jyacs.init_connect()
                    store.jyacs_log("WebSocket已断开，正在重新连接...", "WARNING")
                
                # 显示状态
                store.jyacs_log("JYACS状态:{} | 消息队列: {}/{}token | 时间: {}".format(
                    store.jyacs.status,
                    store.jyacs.len_message_queue(),
                    store.jyacs.stat.get("received_token", 0) - start_token,
                    round(gentime - start_time)
                ), "INFO")
                
                if store.jyacs.is_failed():
                    if store.jyacs.len_message_queue() == 0:
                        y(_("好像出了什么问题..."))
                        _return = "disconnected"
                        break
                
                if store.jyacs.len_message_queue() == 0:
                    store.jyacs_log("等待消息...", "INFO")
                    y(".{w=0.3}.{w=0.3}.{w=0.3}{nw}")
                    if len(_history_list):
                        _history_list.pop()
                    continue
                
                # 获取并显示消息
                message = store.jyacs.get_message()
                store.jyacs_log("jyacs_talking::message:'{}', '{}'".format(message[0], message[1]), "DEBUG")
                received_message += message[1]
                
                renpy.show("yuri {}".format(message[0]))
                try:
                    y(message[1])
                except Exception as e:
                    store.jyacs_log("jyacs_talking::renpy.say error:{}".format(traceback.format_exc()), "ERROR")
                    store.jyacs_log("!!SUBMOD ERROR when chatting: {}".format(e), "ERROR")
            
            store.jyacs_log("jyacs_talking::RESPONSE :'{}'".format(received_message), "DEBUG")
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

label jyacs_talking.end:
    if persistent.jyacs_setting_dict['console']:
        $ store.jyacs_log("清理控制台...", "INFO")
        hide screen jyacs_console_teaching
        show yuri at t11
    hide screen jyacs_status_overlay
    return _return

# 控制台显示/隐藏
label jyacs_show_console:
    if persistent.jyacs_setting_dict['console']:
        show screen jyacs_console_teaching
        show yuri at t22
    return

label jyacs_hide_console:
    if persistent.jyacs_setting_dict['console']:
        hide screen jyacs_console_teaching
        show yuri at t11
    return

# 重新连接
label jyacs_reconnect:
    python:
        store.jyacs.close_wss_session()
    return

# 邮件处理
label jyacs_mpostal_load:
    python:
        if store.mail_exist():
            import time
            _postals = store.find_mail_files()
            for item in _postals:
                persistent._jyacs_send_or_received_mpostals.append({
                    "raw_title": item[0],
                    "raw_content": item[1],
                    "time": str(time.time()),
                    "responsed_content": "",
                    "responsed_status": "delaying",
                    "failed_count": 0
                })
    return

# 初始化连接
label jyacs_init_connect(use_pause_instand_wait=False):
    python:
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
                    y(".{w=0.3}.{w=0.3}.{w=0.3}{nw}")
                    if len(_history_list):
                        _history_list.pop()
                continue
            
            if store.jyacs.is_ready_to_input():
                store.jyacs_log("登录成功，准备开始聊天！", "INFO")
                _return = "success"
                break
            elif store.jyacs.is_failed():
                if store.jyacs.status == store.jyacs.JyacsAiStatus.API_KEY_FAILED:
                    store.jyacs_log("登录失败，请检查API密钥。", "ERROR")
                elif store.jyacs.status == store.jyacs.JyacsAiStatus.CONFIG_NOTFOUND:
                    store.jyacs_log("配置文件未找到，请检查设置。", "ERROR")
                else:
                    store.jyacs_log("jyacs_talking:: 未知错误: jyacs.is_failed() = {}, jyacs.status = {}, jyacs.is_connected() = {}".format(
                        store.jyacs.is_failed(),
                        store.jyacs.status,
                        store.jyacs.is_connected()
                    ), "ERROR")
                    store.jyacs_log("发生错误，请检查日志文件", "ERROR")
                renpy.pause(2.0)
                _return = "disconnected"
                break
    
    call show_workload
    return _return

# 邮件阅读
label jyacs_mpostal_read:
    if persistent.jyacs_setting_dict.get("show_console_when_reply", False):
        call jyacs_show_console
    else:
        window hide
    
    call jyacs_mpostal_load
    call jyacs_init_connect(use_pause_instand_wait=True)
    
    if _return == "disconnected":
        jump jyacs_mpostal_read.failed
    
    python:
        import time
        for cur_postal in persistent._jyacs_send_or_received_mpostals:
            if cur_postal["responsed_status"] != "notupload":
                continue
            
            start_time = time.time()
            store.jyacs.start_MPostal(cur_postal["raw_content"], title=cur_postal["raw_title"])
            
            not_uploaded_count = sum(1 for postal in persistent._jyacs_send_or_received_mpostals if postal["responsed_status"] == "notupload")
            current_index = persistent._jyacs_send_or_received_mpostals.index(cur_postal) + 1
            
            store.jyacs_log("<submod> Processing mpostal {} ({}/{})".format(
                cur_postal["raw_title"],
                current_index,
                not_uploaded_count
            ), "INFO")
            
            cur_postal["responsed_status"] = "failed"
            
            while store.jyacs.is_responding() or store.jyacs.len_message_queue() > 0:
                if store.jyacs.is_responding():
                    gentime = time.time()
                else:
                    gentime = store.jyacs._gen_time
                
                store.jyacs_log("JYACS状态:{} | 时间: {}".format(
                    store.jyacs.status,
                    round(gentime - start_time)
                ), "INFO")
                
                if store.jyacs.is_failed():
                    if store.jyacs.len_message_queue() == 0:
                        cur_postal["responsed_status"] = "failed"
                        cur_postal["responsed_content"] = cur_postal["responsed_content"] + renpy.substitute(_("无法回复信件, 查看日志以获取详细原因\n错误码: [store.jyacs.status] | [store.jyacs.JyacsAiStatus.get_description(store.jyacs.status)]" + "\nt{}".format(time.time()))) + ("\n" if len(cur_postal["responsed_content"]) else "")
                        
                        _return = "failed"
                        store.jyacs_log("jyacs_mpostal_read: failed!", "ERROR")
                        break
                
                if store.jyacs.len_message_queue() == 0:
                    store.jyacs_log("等待消息...", "INFO")
                    renpy.pause(1.0)
                    continue
                
                message = store.jyacs.get_message(add_pause=False)
                store.jyacs_log("jyacs_mpostal_read::message:'{}', '{}'".format(message[0], message[1]), "DEBUG")
                
                cur_postal["responsed_content"] = store.key_replace(message[1], {})
                cur_postal["responsed_status"] = "received"
                _return = "success"
            
            if cur_postal.get("failed_count", 0) >= 3:
                cur_postal["responsed_status"] = "fatal"
                cur_postal["responsed_content"] = renpy.substitute(_("无法回复信件, 因失败次数过多, 该信件将不会再回复")) + "\n" + cur_postal["responsed_content"]
                store.jyacs_log("jyacs_mpostal_read: failed after 3 times!!!", "ERROR")
                break
            else:
                if "failed_count" not in cur_postal:
                    cur_postal["failed_count"] = 0
                cur_postal["failed_count"] += 1

label jyacs_mpostal_read.failed:
    call jyacs_hide_console
    if not persistent.jyacs_setting_dict.get("show_console_when_reply", False):
        window show
    return _return

# 显示工作负载
label show_workload:
    python:
        data = store.jyacs.get_workload_lite()
        if data["total_inuse_vmem"] and data["total_vmem"] and data["avg_usage"]:
            store.jyacs_log("<DISABLE_VERBOSITY><JYACS LLM Server> Current Workload", "INFO")
            store.jyacs_log("<DISABLE_VERBOSITY>VRAM " + store.jyacs_progress_bar(
                data["total_inuse_vmem"] * 100 / data["total_vmem"],
                str(data["total_inuse_vmem"]) + "MiB",
                str(data["total_vmem"]) + "MiB"
            ), "INFO")
            store.jyacs_log("<DISABLE_VERBOSITY>UTIL " + store.jyacs_progress_bar(
                data["avg_usage"],
                str(data["avg_usage"] * 3600 / 100) + "TFlops"
            ), "INFO")
        else:
            store.jyacs_log("workload data not intact: '{}'".format(str(data)), "DEBUG")
    return

# 修改控制台界面
screen jyacs_console_teaching():
    zorder 50
    
    frame:
        background "#000000B2"
        xsize 400
        ysize 600
        xalign 1.0
        yalign 0.5
        
        vbox:
            spacing 5
            text "JYACS Console" style "jyacs_console_text" xalign 0.5
            
            viewport:
                id "teaching_vp"
                child_size (380, None)
                mousewheel True
                draggable True
                scrollbars "vertical"
                yinitial 1.0
                
                vbox:
                    spacing 10
                    xsize 380
                    
                    for line in store.jyacs_log_history:
                        text line style "jyacs_console_text"

# 修改输入界面
screen jyacs_input_screen(prompt):
    style_prefix "input"
    
    frame:
        background "#000000B2"
        xalign 0.5
        yalign 0.5
        padding (20, 20)
        
        vbox:
            spacing 10
            text prompt style "jyacs_input_text"
            input id "input" style "jyacs_input_text" 
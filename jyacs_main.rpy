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
        # 使用JUSTYURI表情系统
        if emote.startswith("1"):
            # 将DDLC风格的表情代码转换为JUSTYURI表情编码
            ddlc_to_justyuri = {
                "1eua": "A-ACAAA-AAAA",  # 正常/平静
                "1esa": "A-ADCAA-AAAA",  # 悲伤
                "1eub": "A-BCAAA-AAAA",  # 开心
                "1euc": "A-ACBAA-AAAA",  # 思考/感兴趣
                "1esd": "A-ADBAA-AAAA",  # 思考/担忧
                "1hub": "A-BCAAA-AAAA",  # 开心/愉快
                "1sua": "A-ACAAA-AAAA",  # 轻微惊讶
                "1lua": "A-ADAAA-AAAA",  # 轻微悲伤
                "1lsb": "A-ADCAA-AAAA",  # 悲伤/失落
                "1eka": "A-BCAAA-AAAA",  # 温柔/善良
                "1ekd": "A-ADCAA-AAAA",  # 不开心/生气
            }
            
            # 获取对应的JUSTYURI表情编码
            expression = ddlc_to_justyuri.get(emote, "A-ACAAA-AAAA")
            
            # 使用show_chr函数显示表情
            show_chr(expression)
        else:
            # 直接使用JUSTYURI表情编码
            show_chr(emote)

# 错误处理
init 5 python:
    def handle_mail_error():
        """处理邮件错误"""
        renpy.say("优里", "邮件处理暂时无法使用。")
        return "error"

# 聊天界面标签 - 添加submod_前缀
label submod_jyacs_chat_start:
    # 设置JYACS对话状态为True
    $ jyacs_in_chat = True
    
    # 隐藏主屏幕按钮（参考JY原版实现）
    python:
        if hasattr(store, 'DisableTalk'):
            DisableTalk()
    
    # 不强制设置背景，使用原游戏的jy_bg动态背景系统
    # 原游戏会根据bg_list和current_timecycle_marker自动显示正确的背景
    
    python:
        # 重置退出请求标志
        store.jyacs_exit_requested = False
        
        # 确保应用最新的JYACS设置
        if hasattr(store, 'jyacs_apply_setting'):
            store.jyacs_apply_setting()
    
    # 使用JUSTYURI表情系统显示默认表情
    $ show_chr("A-ACAAA-AAAA")
    y "啊，要聊些话题吗....稍等一下"
    y "我准备好啦！。"
    
    jump submod_jyacs_talking

label submod_jyacs_chat_end:
    # 重置JYACS对话状态
    $ jyacs_in_chat = False
    
    # 恢复主屏幕按钮（参考JY原版实现）
    python:
        if hasattr(store, 'EnableTalk'):
            EnableTalk()
    
    y "就这样吧，有什么欢迎随时找我。"
    return "normal"

# 退出JYACS对话
label jyacs_exit_chat:
    # 重置JYACS对话状态
    $ jyacs_in_chat = False
    
    # 隐藏状态overlay
    hide screen jyacs_status_overlay
    
    # 恢复主屏幕按钮（参考JY原版实现）
    python:
        if hasattr(store, 'EnableTalk'):
            EnableTalk()
    
    # 返回游戏
    return

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
    # use free_chat_overlay  # 已移除，功能不存在





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
label submod_jyacs_talking:
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
        
        printed = False
        is_retry_before_sendmessage = False
        question = False
        
        # 外层循环计数器（防止无限循环）
        outer_loop_count = 0
        max_outer_loops = 100
        
        while True:
            outer_loop_count += 1
            
            # 防止无限循环
            if outer_loop_count > max_outer_loops:
                store.jyacs_log("达到最大循环次数，强制退出", "ERROR")
                _return = "max_loops"
                break
            
            # 诊断日志：记录循环状态
            store.jyacs_log("="*60, "DEBUG")
            store.jyacs_log("外层循环 #{} 开始".format(outer_loop_count), "DEBUG")
            store.jyacs_log("is_ready_to_input: {}".format(store.jyacs.is_ready_to_input), "DEBUG")
            store.jyacs_log("is_connected: {}".format(store.jyacs.is_connected), "DEBUG")
            store.jyacs_log("is_chatting: {}".format(store.jyacs.is_chatting), "DEBUG")
            store.jyacs_log("is_responding: {}".format(store.jyacs.is_responding), "DEBUG")
            store.jyacs_log("is_failed: {}".format(store.jyacs.is_failed), "DEBUG")
            store.jyacs_log("message_queue length: {}".format(len(store.jyacs.message_queue)), "DEBUG")
            store.jyacs_log("="*60, "DEBUG")
            
            if is_retry_before_sendmessage:
                store.jyacs.chat(is_retry_before_sendmessage)
                question = is_retry_before_sendmessage
                is_retry_before_sendmessage = False
            
            renpy.show("yuri {}".format(store.jyacs.MoodStatus.get_emote()))
            
            # 检查用户是否点击了"退出"按钮
            if store.jyacs_exit_requested:
                store.jyacs_log("用户点击退出按钮，结束对话", "INFO")
                store.jyacs_exit_requested = False  # 重置标志
                _return = "user_exit"
                break
            
            if store.jyacs.is_ready_to_input:
                if store.action.get("stop", False):
                    store.action = {}
                    _return = "canceled"
                    break
                
                # ========== 状态验证（新增） ==========
                store.jyacs_log("准备获取用户输入，验证状态...", "DEBUG")
                
                # 验证次数计数器
                validation_attempts = 0
                max_validation_attempts = 3
                
                while validation_attempts < max_validation_attempts:
                    validation_attempts += 1
                    
                    # 检查状态是否正确
                    is_valid = True
                    
                    if store.jyacs.is_responding:
                        store.jyacs_log("验证失败：is_responding 应为 False 但为 True", "WARNING")
                        is_valid = False
                    
                    if store.jyacs.is_chatting:
                        store.jyacs_log("验证失败：is_chatting 应为 False 但为 True", "WARNING")
                        is_valid = False
                    
                    if len(store.jyacs.message_queue) > 0:
                        store.jyacs_log("验证失败：message_queue 应为空但有 {} 条消息".format(
                            len(store.jyacs.message_queue)
                        ), "WARNING")
                        is_valid = False
                    
                    if is_valid:
                        store.jyacs_log("状态验证通过（尝试 {}/{}）".format(
                            validation_attempts, max_validation_attempts
                        ), "DEBUG")
                        break
                    else:
                        # 尝试修复
                        store.jyacs_log("尝试修复状态（尝试 {}/{}）...".format(
                            validation_attempts, max_validation_attempts
                        ), "WARNING")
                        
                        store.jyacs.is_responding = False
                        store.jyacs.is_chatting = False
                        store.jyacs.message_queue = []
                        
                        # 等待状态同步
                        renpy.pause(0.2, hard=True)
                
                if validation_attempts >= max_validation_attempts:
                    store.jyacs_log("状态验证失败，连续 {} 次尝试后仍无法修复".format(
                        max_validation_attempts
                    ), "ERROR")
                    store.jyacs_log("强制退出对话循环", "ERROR")
                    _return = "state_validation_failed"
                    break
                # ========== 状态验证结束 ==========
                
                # 获取用户输入 - 使用标准Renpy对话输入
                store.jyacs_log("="*60, "DEBUG")
                store.jyacs_log("状态验证通过，准备获取用户输入", "DEBUG")
                store.jyacs_log("即将调用 renpy.input()，当前时间: {}".format(time.time()), "DEBUG")
                
                # 关键修复：强制刷新 Ren'Py 交互状态
                # 这确保之前的 y() 调用完全结束，事件循环已经恢复
                store.jyacs_log("刷新交互状态...", "DEBUG")
                renpy.restart_interaction()
                
                store.jyacs_log("="*60, "DEBUG")
                question = renpy.input(
                    _("[persistent.playername]，说吧。"),
                    default="",
                    length=75 if not config.language == "english" else 375
                ).strip(' \t\n\r')
                
                store.jyacs_log("="*60, "DEBUG")
                store.jyacs_log("renpy.input() 已返回，用户输入: '{}'".format(question), "DEBUG")
                store.jyacs_log("当前时间: {}".format(time.time()), "DEBUG")
                store.jyacs_log("="*60, "DEBUG")
                
                if question == "":
                    store.jyacs_log("用户输入为空，继续循环", "DEBUG")
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
                store.jyacs_log("="*60, "DEBUG")
                store.jyacs_log("准备发送消息到 API: '{}'".format(question[:50] if len(question) > 50 else question), "DEBUG")
                store.jyacs.chat(question)
                store.jyacs_log("API 调用已返回", "DEBUG")
                store.jyacs_log("当前状态: is_responding={}, is_chatting={}, len_message_queue={}".format(
                    store.jyacs.is_responding, store.jyacs.is_chatting, store.jyacs.len_message_queue
                ), "DEBUG")
                store.jyacs_log("="*60, "DEBUG")
                is_retry_before_sendmessage = False
            
            elif not store.jyacs.is_connected and persistent.jyacs_setting_dict['auto_reconnect']:
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
            
            store.jyacs_log("="*60, "DEBUG")
            store.jyacs_log("进入内层循环（消息处理）", "DEBUG")
            store.jyacs_log("初始状态: is_responding={}, is_chatting={}, len_message_queue={}".format(
                store.jyacs.is_responding, store.jyacs.is_chatting, store.jyacs.len_message_queue
            ), "DEBUG")
            store.jyacs_log("="*60, "DEBUG")
            
            inner_loop_count = 0
            max_inner_loops = 50
            
            while True:
                inner_loop_count += 1
                
                if inner_loop_count > max_inner_loops:
                    store.jyacs_log("内层循环达到最大迭代次数 {}，强制退出".format(max_inner_loops), "ERROR")
                    break
                
                store.jyacs_log("内层循环迭代 #{}".format(inner_loop_count), "DEBUG")
                if store.jyacs.is_responding:
                    gentime = time.time()
                else:
                    gentime = store.jyacs._gen_time
                
                if not store.jyacs.is_connected and persistent.jyacs_setting_dict['auto_reconnect']:
                    store.jyacs.init_connect()
                    store.jyacs_log("WebSocket已断开，正在重新连接...", "WARNING")
                
                # 显示状态
                store.jyacs_log("JYACS状态:{} | 消息队列: {}/{}token | 时间: {}".format(
                    store.jyacs.status,
                    store.jyacs.len_message_queue,
                    store.jyacs.stat.get("received_token", 0) - start_token,
                    round(gentime - start_time)
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
                        store.jyacs_log("jyacs_talking::message:'{}', '{}'".format(message[0], message[1]), "DEBUG")
                        received_message += message[1]

                        # 使用JUSTYURI表情编码系统
                        expression_code = message[0]
                        # 显示表情
                        try:
                            show_chr(expression_code)
                            store.jyacs_log("显示表情: {}".format(expression_code), "DEBUG")
                        except Exception as e:
                            store.jyacs_log("显示表情失败: {}，使用默认表情".format(e), "WARNING")
                            show_chr("A-ACAAA-AAAA")
                        
                        # 显示对话文本
                        try:
                            store.jyacs_log("准备显示对话，等待用户点击...", "DEBUG")
                            y(message[1])
                            store.jyacs_log("用户已点击，继续处理", "DEBUG")
                        except Exception as e:
                            store.jyacs_log("jyacs_talking::renpy.say error:{}".format(traceback.format_exc()), "ERROR")
                            store.jyacs_log("!!SUBMOD ERROR when chatting: {}".format(e), "ERROR")
                    
                    # 检查是否还有更多消息
                    if not store.jyacs.is_responding and store.jyacs.len_message_queue == 0:
                        store.jyacs_log("内层循环退出条件满足：is_responding={}, len_message_queue={}".format(
                            store.jyacs.is_responding, store.jyacs.len_message_queue
                        ), "DEBUG")
                        break
                else:
                    # 等待消息
                    if store.jyacs.is_responding:
                        store.jyacs_log("等待消息...", "INFO")
                        y(".{w=0.3}.{w=0.3}.{w=0.3}{nw}")
                        if len(_history_list):
                            _history_list.pop()
                    renpy.pause(0.5, hard=True)
                    
                    # 确保正确退出循环
                    if not store.jyacs.is_responding and store.jyacs.len_message_queue == 0:
                        store.jyacs_log("内层循环退出（等待分支）：is_responding={}, len_message_queue={}".format(
                            store.jyacs.is_responding, store.jyacs.len_message_queue
                        ), "DEBUG")
                        break

            store.jyacs_log("="*60, "DEBUG")
            store.jyacs_log("内层循环已退出", "DEBUG")
            store.jyacs_log("jyacs_talking::RESPONSE :'{}'".format(received_message), "DEBUG")
            store.jyacs_log("当前状态: is_responding={}, is_chatting={}, len_message_queue={}".format(
                store.jyacs.is_responding, store.jyacs.is_chatting, store.jyacs.len_message_queue
            ), "DEBUG")
            store.jyacs_log("="*60, "DEBUG")
            _return = "mtrigger_triggering"
            
            # 处理触发器（带异常保护）
            try:
                if hasattr(store.jyacs, 'mtrigger_manager') and hasattr(store.jyacs.mtrigger_manager, 'run_trigger'):
                    store.action = store.jyacs.mtrigger_manager.run_trigger("post", {"text": received_message})
                    store.jyacs_log("<chat_action> {}".format(store.action), "DEBUG")
                else:
                    store.jyacs_log("触发器管理器或 run_trigger 方法不存在，跳过触发器处理", "WARNING")
                    store.action = {"stop": False}
            except AttributeError as e:
                store.jyacs_log("触发器方法不存在: {}".format(e), "ERROR")
                store.action = {"stop": False}
            except Exception as e:
                store.jyacs_log("触发器执行失败: {}".format(e), "ERROR")
                try:
                    import traceback
                    store.jyacs_log(traceback.format_exc(), "ERROR")
                except:
                    pass
                store.action = {"stop": False}
            
            if store.action.get('stop', False):
                _return = "canceled"
                break
            
            # ========== 状态重置和验证（增强版） ==========
            store.jyacs_log("="*60, "DEBUG")
            store.jyacs_log("一轮对话完成，开始状态重置", "DEBUG")
            
            # 1. 记录重置前的状态
            store.jyacs_log("重置前状态:", "DEBUG")
            store.jyacs_log("  is_responding: {}".format(store.jyacs.is_responding), "DEBUG")
            store.jyacs_log("  is_chatting: {}".format(store.jyacs.is_chatting), "DEBUG")
            store.jyacs_log("  is_ready_to_input: {}".format(store.jyacs.is_ready_to_input), "DEBUG")
            store.jyacs_log("  message_queue length: {}".format(len(store.jyacs.message_queue)), "DEBUG")
            
            # 2. 明确重置状态标志
            store.jyacs.is_responding = False
            store.jyacs.is_chatting = False
            
            # 3. 清空可能残留的消息
            if len(store.jyacs.message_queue) > 0:
                store.jyacs_log("警告：消息队列中还有 {} 条消息，清空".format(
                    len(store.jyacs.message_queue)
                ), "WARNING")
                store.jyacs.message_queue = []
            
            # 4. 添加延迟，让 Ren'Py 事件循环运行
            store.jyacs_log("等待 0.3 秒，让事件循环同步状态...", "DEBUG")
            renpy.pause(0.3, hard=True)
            
            # 5. 验证状态
            store.jyacs_log("重置后状态:", "DEBUG")
            store.jyacs_log("  is_responding: {}".format(store.jyacs.is_responding), "DEBUG")
            store.jyacs_log("  is_chatting: {}".format(store.jyacs.is_chatting), "DEBUG")
            store.jyacs_log("  is_ready_to_input: {}".format(store.jyacs.is_ready_to_input), "DEBUG")
            store.jyacs_log("  message_queue length: {}".format(len(store.jyacs.message_queue)), "DEBUG")
            
            # 6. 状态一致性检查
            if store.jyacs.is_responding or store.jyacs.is_chatting:
                store.jyacs_log("警告：状态重置后仍有标志为 True，尝试强制重置", "WARNING")
                store.jyacs.is_responding = False
                store.jyacs.is_chatting = False
                renpy.pause(0.2, hard=True)
            
            if not store.jyacs.is_ready_to_input:
                store.jyacs_log("警告：is_ready_to_input 为 False，检查原因", "WARNING")
                store.jyacs_log("  is_connected: {}".format(store.jyacs.is_connected), "DEBUG")
                store.jyacs_log("  is_failed: {}".format(store.jyacs.is_failed), "DEBUG")
            
            store.jyacs_log("状态重置完成，准备下一轮对话", "DEBUG")
            store.jyacs_log("="*60, "DEBUG")
            # ========== 状态重置和验证结束 ==========

label submod_jyacs_talking.end:
    python:
        # 清空对话历史（对话会话结束）
        if hasattr(store.jyacs, 'clear_conversation_history'):
            cleared_count = store.jyacs.clear_conversation_history()
            store.jyacs_log("对话会话结束，已清空 {} 条历史消息".format(cleared_count), "INFO")
        
        # 重置对话状态，使按钮恢复为 "JYACS"
        store.jyacs_is_chatting = False
        store.jyacs_log("对话状态已重置，按钮恢复为 JYACS", "DEBUG")
    
    if persistent.jyacs_setting_dict['console']:
        $ store.jyacs_log("清理控制台...", "INFO")
        hide screen jyacs_console_teaching
        show yuri at t11
    hide screen jyacs_status_overlay
    return _return



# 重新连接 - 添加submod_前缀
label submod_jyacs_reconnect:
    python:
        store.jyacs.close_wss_session()
    return "normal"

# 邮件处理 - 添加submod_前缀
label submod_jyacs_mpostal_load:
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
    return "normal"

# 初始化连接 - 添加submod_前缀
label submod_jyacs_init_connect(use_pause_instand_wait=False):
    python:
        store.jyacs.content_func = store.jyacs_log
        store.jyacs_log("\n" * 25 + "=== JYACS 初始化 ===", "INFO")
        
        if not store.jyacs.is_connected:
            store.jyacs.init_connect()
        
        while True:
            if not store.jyacs.is_connected:
                store.jyacs_log("正在初始化连接...", "INFO")
                renpy.pause(0.3, True)
                if not store.jyacs.is_failed:
                    continue
            
            if not store.jyacs.is_ready_to_input and not store.jyacs.is_failed:
                store.jyacs_log("等待登录...", "INFO")
                if use_pause_instand_wait:
                    renpy.pause(1.0)
                else:
                    y(".{w=0.3}.{w=0.3}.{w=0.3}{nw}")
                    if len(_history_list):
                        _history_list.pop()
                continue
            
            if store.jyacs.is_ready_to_input:
                store.jyacs_log("登录成功，准备开始聊天！", "INFO")
                _return = "success"
                break
            elif store.jyacs.is_failed:
                if store.jyacs.status == store.jyacs.JyacsAiStatus.API_KEY_FAILED:
                    store.jyacs_log("登录失败，请检查API密钥。", "ERROR")
                elif store.jyacs.status == store.jyacs.JyacsAiStatus.CONFIG_NOTFOUND:
                    store.jyacs_log("配置文件未找到，请检查设置。", "ERROR")
                else:
                    store.jyacs_log("jyacs_talking:: 未知错误: jyacs.is_failed() = {}, jyacs.status = {}, jyacs.is_connected() = {}".format(
                        store.jyacs.is_failed,
                        store.jyacs.status,
                        store.jyacs.is_connected
                    ), "ERROR")
                    store.jyacs_log("发生错误，请检查日志文件", "ERROR")
                renpy.pause(2.0)
                _return = "disconnected"
                break
    
    call submod_show_workload
    return _return

# 显示工作负载 - 添加submod_前缀
label submod_show_workload:
    python:
        # 跳过工作负载显示，因为get_workload_lite方法不存在
        store.jyacs_log("JYACS 初始化完成", "INFO")
    return "normal"

# 邮件显示 - 添加submod_前缀
label submod_jyacs_mpostal_show_backtoscreen(content=""):
    y "[content]"
    return "normal"
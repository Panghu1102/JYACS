# jyacs_main.rpy - JYACS 主要游戏脚本
# 版本: 1.4.0 (原生对话循环版)
# 作者: Panghu1102 & Gemini

# --- 初始化和样式定义 ---
init 50 python:
    # 确保不覆盖已有样式
    style.jyacs_console_text = Style(style.text)
    style.jyacs_console_text.font = "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    style.jyacs_console_text.size = 14
    style.jyacs_console_text.color = "#FFFFFF"
    style.jyacs_console_text.outlines = [(1, "#000000", 0, 0)]

    style.jyacs_input_text = Style(style.text)
    style.jyacs_input_text.font = "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    style.jyacs_input_text.size = 16
    style.jyacs_input_text.color = "#FFFFFF"
    style.jyacs_input_text.outlines = [(1, "#000000", 0, 0)]

    # 新增紫色按钮样式
    style.jyacs_purple_button = Style(style.button)
    style.jyacs_purple_button.background = "#8A2BE2" # BlueViolet
    style.jyacs_purple_button.hover_background = "#9932CC" # MediumOrchid
    style.jyacs_purple_button.padding = (15, 8)

    style.jyacs_purple_button_text = Style(style.button_text)
    style.jyacs_purple_button_text.color = "#FFFFFF"
    style.jyacs_purple_button_text.size = 18

init -890 python:
    # 创建空的消息列表
    if not hasattr(store, 'jyacs_messages'):
        store.jyacs_messages = []
    
    # AI回复存储
    if not hasattr(store, 'jyacs_ai_reply'):
        store.jyacs_ai_reply = ""

    # 发送消息的函数
    def jyacs_send_message(message):
        """发送消息到JYACS"""
        if not message or not message.strip():
            return

        # 添加玩家消息到历史记录
        store.jyacs_messages.append(("[player]: " + message))
        
        # 如果JYACS可用，发送消息
        if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'chat'):
            store.jyacs.chat(message)

# --- 原生聊天循环 ---
label jyacs_free_talk_loop:
    python:
        _connection_failed = False
        # 检查API连接
        if not store.jyacs.is_connected:
            renpy.notify("正在尝试连接...")
            if not store.jyacs.init_connect():
                renpy.notify("连接失败，请检查设置。")
                _connection_failed = True

    if _connection_failed:
        return

    pause 1.0

    python hide:
        # 进入聊天模式
        persistent.jyacs_chat_mode = True
        renpy.ui.window(show=False)

        while True:
            # 1. 获取玩家输入
            player_input = renpy.input("你在想什么？ (输入 '再见' 退出)", length=200).strip()

            # 2. 检查是否退出
            if player_input.lower() in ["", "再见", "goodbye", "bye"]:
                break

            # 3. 发送消息
            jyacs_send_message(player_input)
            
            # 4. 等待并处理AI回复
            # 等待消息队列中出现消息
            while store.jyacs.len_message_queue() == 0:
                renpy.pause(0.1, hard=True)
            
            # 获取消息
            emote, text = store.jyacs.get_message()
            
            # 记录到历史
            processed_reply = "Yuri: " + text
            store.jyacs_messages.append(processed_reply)

            # 5. 使用 renpy.say 显示对话
            # 检查角色对象是否存在
            if hasattr(store, 'm'):
                renpy.say(store.m, u"{} {}".format(emote, text))
            else:
                # 如果 store.m 未定义，则提供备用方案
                renpy.say(None, u"Yuri: {} {}".format(emote, text))

        # 退出聊天模式
        persistent.jyacs_chat_mode = False
        renpy.ui.window(show=True)

    return

# --- 状态界面 (可以保留) ---
init 15 screen jyacs_status_overlay():
    zorder 100
    if hasattr(store, 'jyacs') and hasattr(store.jyacs, 'is_responding') and store.jyacs.is_responding():
        frame:
            background "#000000B2"
            xalign 1.0
            yalign 0.0
            padding (10, 5)
            text "思考中..." style "jyacs_console_text"
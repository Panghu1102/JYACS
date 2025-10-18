# jyacs_ui_hooks.rpy - JYACS UI 钩子和样式系统
# 版本: 2.0.0
# 作者: Panghu1102
# 说明: 集成 JYACS 设置到 JY 1.10.11 原生设置界面

# ============================================================================
# 样式系统定义
# ============================================================================
# 继承 JY 1.10.11 的样式系统，确保视觉一致性

# JYACS 标签样式（继承自 JY 的 pref_label）
init -1 style jyacs_pref_label is pref_label
init -1 style jyacs_pref_label_text is pref_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size 24
    color "#fff"
    outlines [(3, "#a679ff", 0, 0), (1, "#a679ff", 1, 1)]
    yalign 1.0

# JYACS 复选按钮样式（继承自 JY 的 check_button）
init -1 style jyacs_check_button is check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

init -1 style jyacs_check_button_text is check_button_text:
    properties gui.button_text_properties("check_button")
    font "gui/font/Halogen.ttf"
    outlines []

# JYACS 单选按钮样式（继承自 JY 的 radio_button）
init -1 style jyacs_radio_button is radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"

init -1 style jyacs_radio_button_text is radio_button_text:
    properties gui.button_text_properties("radio_button")
    font "gui/font/Halogen.ttf"
    outlines []

# JYACS 滑块样式（继承自 JY 的 slider）
init -1 style jyacs_slider is slider_slider:
    xsize 350

init -1 style jyacs_slider_button is slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

init -1 style jyacs_slider_button_text is slider_button_text:
    properties gui.button_text_properties("slider_button")

# JYACS 容器样式
init -1 style jyacs_vbox is pref_vbox:
    xsize 225
    spacing gui.pref_button_spacing

init -1 style jyacs_frame is empty:
    background Frame("gui/overlay/confirm.png", gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign 0.5
    yalign 0.5
    xsize 800
    ysize 600

# JYACS 文本样式
init -1 style jyacs_text is gui_text:
    font "gui/font/Halogen.ttf"
    size 18
    color "#fff"

init -1 style jyacs_label_text is gui_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size 20
    color "#fff"
    outlines [(2, "#a679ff", 0, 0), (1, "#a679ff", 1, 1)]

# JYACS 输入框样式
init -1 style jyacs_input is input:
    color "#fff"
    size 18

# JYACS 状态文本样式
init -1 style jyacs_status_text is gui_text:
    font "gui/font/Halogen.ttf"
    size 16
    color "#d5bdff"

# ============================================================================
# 辅助函数
# ============================================================================

init -10 python:
    def jyacs_safe_timecycle_transition(bg, speed, bypass):
        """安全调用 timecycle_transition 函数"""
        try:
            if hasattr(store, 'timecycle_transition'):
                store.timecycle_transition(bg, speed, bypass)
        except:
            pass
    
    def jyacs_get_connection_status_display():
        """获取连接状态的显示文本"""
        try:
            if hasattr(store, 'jyacs') and store.jyacs:
                status = store.jyacs.get_status()
                if status == "connected":
                    return "已连接"
                elif status == "connecting":
                    return "连接中..."
                else:
                    return "未连接"
            else:
                return "未初始化"
        except:
            return "未知"
    
    def jyacs_get_queue_length_display():
        """获取消息队列长度的显示文本"""
        try:
            if hasattr(store, 'jyacs') and store.jyacs:
                length = store.jyacs.len_message_queue()
                return str(length)
            else:
                return "0"
        except:
            return "0"
    
    def jyacs_safe_connect():
        """安全地连接 API"""
        try:
            if hasattr(store, 'jyacs') and store.jyacs:
                store.jyacs.init_connect()
                renpy.notify("正在连接 API...")
            else:
                renpy.notify("JYACS 未初始化")
        except Exception as e:
            renpy.notify("连接失败: " + str(e))
    
    def jyacs_safe_disconnect():
        """安全地断开 API"""
        try:
            if hasattr(store, 'jyacs') and store.jyacs:
                store.jyacs.close_wss_session()
                renpy.notify("已断开连接")
            else:
                renpy.notify("JYACS 未初始化")
        except Exception as e:
            renpy.notify("断开失败: " + str(e))

# ============================================================================
# Screen 定义
# ============================================================================

# ----------------------------------------------------------------------------
# 任务 2: 文本输入对话框
# ----------------------------------------------------------------------------

init 15 screen jyacs_text_input(prompt_text, dict_obj, key_name, is_password=False):
    # JYACS 文本输入对话框
    # 参数:
    #   prompt_text: 提示文本
    #   dict_obj: 字典对象
    #   key_name: 字典键名
    #   is_password: 是否为密码输入（显示为星号）
    
    modal True
    zorder 250
    
    # 确保键存在
    python:
        if key_name not in dict_obj:
            dict_obj[key_name] = ""
    
    # 背景遮罩
    add "gui/overlay/confirm.png"
    
    # 主容器
    frame:
        style "jyacs_frame"
        xsize 600
        ysize 250
        
        vbox:
            spacing 20
            xfill True
            
            # 提示文本
            text prompt_text:
                style "jyacs_label_text"
                xalign 0.5
                size 22
            
            null height 10
            
            # 输入框
            if is_password:
                # 密码输入（显示为星号）
                python:
                    input_display = "*" * len(dict_obj.get(key_name, ""))
                
                hbox:
                    xalign 0.5
                    spacing 10
                    
                    text input_display:
                        style "jyacs_text"
                        size 20
                        min_width 400
                    
                    textbutton "修改":
                        style "jyacs_check_button"
                        text_style "jyacs_check_button_text"
                        action Show("jyacs_password_input_helper", dict_obj=dict_obj, key_name=key_name)
            else:
                # 普通文本输入
                input:
                    value DictInputValue(dict_obj, key_name)
                    style "jyacs_input"
                    xalign 0.5
                    xsize 500
                    copypaste True
            
            null height 20
            
            # 按钮区域
            hbox:
                xalign 0.5
                spacing 30
                
                textbutton "确定":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action Hide("jyacs_text_input")
                    xsize 120
                
                textbutton "取消":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action [
                        SetDict(dict_obj, key_name, dict_obj.get(key_name + "_backup", "")),
                        Hide("jyacs_text_input")
                    ]
                    xsize 120
    
    # ESC 键关闭
    key "game_menu" action Hide("jyacs_text_input")

# 密码输入辅助屏幕（用于密码字段）
init 15 screen jyacs_password_input_helper(dict_obj, key_name):
    modal True
    zorder 260
    
    add "gui/overlay/confirm.png"
    
    frame:
        style "jyacs_frame"
        xsize 500
        ysize 200
        
        vbox:
            spacing 15
            xfill True
            
            text "输入新密钥:":
                style "jyacs_label_text"
                xalign 0.5
            
            input:
                value DictInputValue(dict_obj, key_name)
                style "jyacs_input"
                xalign 0.5
                xsize 400
                copypaste True
            
            hbox:
                xalign 0.5
                spacing 20
                
                textbutton "确定":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action Hide("jyacs_password_input_helper")
                
                textbutton "取消":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action Hide("jyacs_password_input_helper")

# ----------------------------------------------------------------------------
# 任务 3: 详细设置界面
# ----------------------------------------------------------------------------

# 定义标签页状态
default jyacs_settings_tab = "basic"  # "basic" 或 "advanced"

init 15 screen jyacs_detailed_settings():
    # JYACS 详细设置界面
    # 包含基础设置和高级设置两个标签页
    
    modal True
    zorder 200
    
    # 背景遮罩
    add "gui/overlay/confirm.png"
    
    # 主容器
    frame:
        style "jyacs_frame"
        xsize 900
        ysize 650
        
        vbox:
            spacing 15
            xfill True
            
            # 标题
            text "JYACS 详细设置":
                style "jyacs_label_text"
                size 28
                xalign 0.5
                outlines [(4, "#a679ff", 0, 0), (2, "#a679ff", 2, 2)]
            
            null height 5
            
            # 标签页导航
            hbox:
                xalign 0.5
                spacing 20
                
                textbutton "基础设置":
                    style "jyacs_radio_button"
                    text_style "jyacs_radio_button_text"
                    action SetVariable("jyacs_settings_tab", "basic")
                    xsize 150
                
                textbutton "高级设置":
                    style "jyacs_radio_button"
                    text_style "jyacs_radio_button_text"
                    action SetVariable("jyacs_settings_tab", "advanced")
                    xsize 150
            
            null height 10
            
            # 设置内容区域（带滚动）
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 450
                xsize 860
                
                if jyacs_settings_tab == "basic":
                    use jyacs_basic_settings_content
                else:
                    use jyacs_advanced_settings_content
            
            null height 10
            
            # 底部按钮
            hbox:
                xalign 0.5
                spacing 30
                
                textbutton "保存设置":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action [
                        Function(jyacs_apply_all_settings),
                        Hide("jyacs_detailed_settings")
                    ]
                    xsize 150
                
                textbutton "验证配置":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action Function(jyacs_verify_api_config)
                    xsize 150
                
                textbutton "返回":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action Hide("jyacs_detailed_settings")
                    xsize 150
    
    # ESC 键关闭
    key "game_menu" action Hide("jyacs_detailed_settings")

# 基础设置内容
init 15 screen jyacs_basic_settings_content():
    vbox:
        spacing 25
        xfill True
        
        # API 配置区域
        frame:
            style_prefix "jyacs_pref"
            background Frame("gui/overlay/game_menu.png", Borders(10, 10, 10, 10))
            padding (20, 15)
            xfill True
            
            vbox:
                spacing 15
                xfill True
                
                label "API 配置":
                    style "jyacs_pref_label"
                    text_style "jyacs_pref_label_text"
                
                # API 密钥
                hbox:
                    spacing 15
                    
                    text "API 密钥:":
                        style "jyacs_text"
                        min_width 120
                    
                    $ api_key = persistent.jyacs_setting_dict.get('api_key', '')
                    $ api_key_display = ("*" * min(len(api_key), 20)) if api_key else "未设置"
                    
                    textbutton "[api_key_display]":
                        style "jyacs_check_button"
                        text_style "jyacs_check_button_text"
                        action Show("jyacs_text_input", 
                                  prompt_text="请输入 API 密钥:", 
                                  dict_obj=persistent.jyacs_setting_dict, 
                                  key_name="api_key",
                                  is_password=True)
                        xsize 400
                
                # API 地址
                hbox:
                    spacing 15
                    
                    text "API 地址:":
                        style "jyacs_text"
                        min_width 120
                    
                    $ api_url_display = persistent.jyacs_setting_dict.get('api_url', '') or "未设置"
                    
                    textbutton "[api_url_display]":
                        style "jyacs_check_button"
                        text_style "jyacs_check_button_text"
                        action Show("jyacs_text_input", 
                                  prompt_text="请输入 API 地址:", 
                                  dict_obj=persistent.jyacs_setting_dict, 
                                  key_name="api_url")
                        xsize 400
                
                # 模型名称
                hbox:
                    spacing 15
                    
                    text "模型名称:":
                        style "jyacs_text"
                        min_width 120
                    
                    $ model_name_display = persistent.jyacs_setting_dict.get('model_name', '') or "未设置"
                    
                    textbutton "[model_name_display]":
                        style "jyacs_check_button"
                        text_style "jyacs_check_button_text"
                        action Show("jyacs_text_input", 
                                  prompt_text="请输入模型名称:", 
                                  dict_obj=persistent.jyacs_setting_dict, 
                                  key_name="model_name")
                        xsize 400
        
        # 连接设置区域
        frame:
            style_prefix "jyacs_pref"
            background Frame("gui/overlay/game_menu.png", Borders(10, 10, 10, 10))
            padding (20, 15)
            xfill True
            
            vbox:
                spacing 15
                xfill True
                
                label "连接设置":
                    style "jyacs_pref_label"
                    text_style "jyacs_pref_label_text"
                
                textbutton "自动连接":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_setting_dict, "auto_connect")
                    selected persistent.jyacs_setting_dict.get("auto_connect", True)
                
                textbutton "自动重连":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_setting_dict, "auto_reconnect")
                    selected persistent.jyacs_setting_dict.get("auto_reconnect", True)
                
                textbutton "启用触发器":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_setting_dict, "enable_triggers")
                    selected persistent.jyacs_setting_dict.get("enable_triggers", True)
        
        # 功能设置区域
        frame:
            style_prefix "jyacs_pref"
            background Frame("gui/overlay/game_menu.png", Borders(10, 10, 10, 10))
            padding (20, 15)
            xfill True
            
            vbox:
                spacing 15
                xfill True
                
                label "功能设置":
                    style "jyacs_pref_label"
                    text_style "jyacs_pref_label_text"
                
                textbutton "启用情绪识别":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_setting_dict, "enable_emotion")
                    selected persistent.jyacs_setting_dict.get("enable_emotion", True)
                
                textbutton "回复时显示控制台":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_setting_dict, "show_console_when_reply")
                    selected persistent.jyacs_setting_dict.get("show_console_when_reply", False)
                
                textbutton "启用 Mspire":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_setting_dict, "mspire_enable")
                    selected persistent.jyacs_setting_dict.get("mspire_enable", True)
                
                textbutton "严格模式":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_setting_dict, "strict_mode")
                    selected persistent.jyacs_setting_dict.get("strict_mode", False)

# 高级设置内容
init 15 screen jyacs_advanced_settings_content():
    vbox:
        spacing 25
        xfill True
        
        # 超参数设置区域
        frame:
            style_prefix "jyacs_pref"
            background Frame("gui/overlay/game_menu.png", Borders(10, 10, 10, 10))
            padding (20, 15)
            xfill True
            
            vbox:
                spacing 20
                xfill True
                
                label "超参数设置":
                    style "jyacs_pref_label"
                    text_style "jyacs_pref_label_text"
                
                # Temperature
                vbox:
                    spacing 5
                    
                    text "Temperature: [persistent.jyacs_advanced_setting.get('temperature', 0.7):.2f]":
                        style "jyacs_text"
                    
                    bar:
                        value DictValue(persistent.jyacs_advanced_setting, "temperature", 2.0, step=0.01, offset=0)
                        style "jyacs_slider"
                        xsize 600
                
                # Top P
                vbox:
                    spacing 5
                    
                    text "Top P: [persistent.jyacs_advanced_setting.get('top_p', 0.9):.2f]":
                        style "jyacs_text"
                    
                    bar:
                        value DictValue(persistent.jyacs_advanced_setting, "top_p", 1.0, step=0.01, offset=0)
                        style "jyacs_slider"
                        xsize 600
                
                # Max Tokens
                vbox:
                    spacing 5
                    
                    text "Max Tokens: [persistent.jyacs_advanced_setting.get('max_tokens', 2048)]":
                        style "jyacs_text"
                    
                    bar:
                        value DictValue(persistent.jyacs_advanced_setting, "max_tokens", 4096, step=64, offset=0)
                        style "jyacs_slider"
                        xsize 600
                
                # Frequency Penalty
                vbox:
                    spacing 5
                    
                    text "Frequency Penalty: [persistent.jyacs_advanced_setting.get('frequency_penalty', 0.0):.2f]":
                        style "jyacs_text"
                    
                    bar:
                        value DictValue(persistent.jyacs_advanced_setting, "frequency_penalty", 2.0, step=0.01, offset=0)
                        style "jyacs_slider"
                        xsize 600
                
                # Presence Penalty
                vbox:
                    spacing 5
                    
                    text "Presence Penalty: [persistent.jyacs_advanced_setting.get('presence_penalty', 0.0):.2f]":
                        style "jyacs_text"
                    
                    bar:
                        value DictValue(persistent.jyacs_advanced_setting, "presence_penalty", 2.0, step=0.01, offset=0)
                        style "jyacs_slider"
                        xsize 600
        
        # 模式设置区域
        frame:
            style_prefix "jyacs_pref"
            background Frame("gui/overlay/game_menu.png", Borders(10, 10, 10, 10))
            padding (20, 15)
            xfill True
            
            vbox:
                spacing 15
                xfill True
                
                label "模式设置":
                    style "jyacs_pref_label"
                    text_style "jyacs_pref_label_text"
                
                textbutton "MF 激进模式":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_advanced_setting, "mf_aggressive")
                    selected persistent.jyacs_advanced_setting.get("mf_aggressive", False)
                
                textbutton "SFE 激进模式":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_advanced_setting, "sfe_aggressive")
                    selected persistent.jyacs_advanced_setting.get("sfe_aggressive", False)
                
                textbutton "ESC 激进模式":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_advanced_setting, "esc_aggressive")
                    selected persistent.jyacs_advanced_setting.get("esc_aggressive", True)
                
                textbutton "NSFW 接受":
                    style "jyacs_check_button"
                    text_style "jyacs_check_button_text"
                    action ToggleDict(persistent.jyacs_advanced_setting, "nsfw_acceptive")
                    selected persistent.jyacs_advanced_setting.get("nsfw_acceptive", True)
        
        # 其他设置
        frame:
            style_prefix "jyacs_pref"
            background Frame("gui/overlay/game_menu.png", Borders(10, 10, 10, 10))
            padding (20, 15)
            xfill True
            
            vbox:
                spacing 15
                xfill True
                
                label "其他设置":
                    style "jyacs_pref_label"
                    text_style "jyacs_pref_label_text"
                
                hbox:
                    spacing 15
                    
                    text "随机种子:":
                        style "jyacs_text"
                        min_width 120
                    
                    $ seed_display = str(persistent.jyacs_advanced_setting.get('seed', 0))
                    
                    textbutton "[seed_display]":
                        style "jyacs_check_button"
                        text_style "jyacs_check_button_text"
                        action Show("jyacs_text_input", 
                                  prompt_text="请输入随机种子 (整数):", 
                                  dict_obj=persistent.jyacs_advanced_setting, 
                                  key_name="_seed")
                        xsize 200

# ----------------------------------------------------------------------------
# 任务 4: 覆盖 preferences screen
# ----------------------------------------------------------------------------
# 使用 init -500 覆盖 JY 原始的 init -501 preferences screen

init -500 screen preferences():
    # 覆盖 JY 1.10.11 的 preferences screen
    # 在底部添加 JYACS 设置区域
    
    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            xoffset 50

            # ========== JY 原有设置区域 ==========
            
            hbox:
                box_wrap True

                if renpy.variant("pc"):
                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                if config.developer:
                    vbox:
                        style_prefix "radio"
                        label _("Rollback Side")
                        textbutton _("Disable") action Preference("rollback side", "disable")
                        textbutton _("Left") action Preference("rollback side", "left")
                        textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                
                if restore_message == "access":
                    vbox:
                        style_prefix "radio"
                        label _("Custom Assets")
                        if persistent.narrative == None:
                            textbutton _("Assets Missing..."):
                                action SetField(persistent, "narrative", "a1p1_start")
                        else:
                            textbutton _("Assets Ready") action Jump("reveal_asset_location")
                            textbutton _("JYCrypt") action Jump("jycrypt")

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:
                    if persistent.idle_frequency_factor <= .75:
                        label _("Idle Frequency: Frequent")
                    elif persistent.idle_frequency_factor >= 1.25:
                        label _("Idle Frequency: Hesitant")
                    else:
                        label _("Idle Frequency: Normal")

                    bar value FieldValue(persistent, "idle_frequency_factor", 1.3, offset=0.5, step=0.1):
                        xmaximum 350

                    label _("Text Speed")

                    bar value FieldValue(_preferences, "text_cps", range=180, max_is_zero=False, style="slider", offset=20)

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:
                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:
                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)

                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"

                    if persistent.high_gpu == 0:
                        textbutton _("Space BG Bloom: On") action [SetField(persistent, "high_gpu", 1), Function(jyacs_safe_timecycle_transition, persistent.bg, "now", True)]
                    elif persistent.high_gpu == 1:
                        textbutton _("Space BG Bloom: Off") action [SetField(persistent, "high_gpu", 2), Function(jyacs_safe_timecycle_transition, persistent.bg, "now", True)]
                    elif persistent.high_gpu == 2:
                        textbutton _("Space BG Bloom: Vid") action [SetField(persistent, "high_gpu", 0), Function(jyacs_safe_timecycle_transition, persistent.bg, "now", True)]

            # ========== JYACS 设置区域 ==========
            
            null height (3 * gui.pref_spacing)
            
            # JYACS 设置容器
            frame:
                style_prefix "jyacs_pref"
                background Frame("gui/overlay/game_menu.png", Borders(10, 10, 10, 10))
                padding (20, 15)
                xsize 800
                
                vbox:
                    spacing 15
                    xfill True
                    
                    # 标题
                    label "JYACS 设置":
                        style "jyacs_pref_label"
                        text_style "jyacs_pref_label_text"
                    
                    # 状态显示
                    hbox:
                        spacing 30
                        
                        text "API 状态: [jyacs_get_connection_status_display()]":
                            style "jyacs_status_text"
                        
                        text "消息队列: [jyacs_get_queue_length_display()]":
                            style "jyacs_status_text"
                    
                    null height 5
                    
                    # 快速操作按钮
                    hbox:
                        spacing 20
                        
                        textbutton "连接":
                            style "jyacs_check_button"
                            text_style "jyacs_check_button_text"
                            action Function(jyacs_safe_connect)
                            xsize 100
                        
                        textbutton "断开":
                            style "jyacs_check_button"
                            text_style "jyacs_check_button_text"
                            action Function(jyacs_safe_disconnect)
                            xsize 100
                        
                        textbutton "详细设置":
                            style "jyacs_check_button"
                            text_style "jyacs_check_button_text"
                            action Show("jyacs_detailed_settings")
                            xsize 120

    # 版本号显示
    text "v[config.version]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"


# ============================================================================
# 设置逻辑函数
# ============================================================================

init -10 python:
    def jyacs_apply_setting():
        """应用基础设置"""
        try:
            # 验证必填字段
            api_key = persistent.jyacs_setting_dict.get('api_key', '')
            api_url = persistent.jyacs_setting_dict.get('api_url', '')
            model_name = persistent.jyacs_setting_dict.get('model_name', '')
            
            if not api_key:
                renpy.notify("错误: API 密钥不能为空")
                return False
            
            if not api_url:
                renpy.notify("错误: API 地址不能为空")
                return False
            
            if not model_name:
                persistent.jyacs_setting_dict['model_name'] = "jyacs_main"
            
            # 触发相关更新
            if hasattr(store, 'jyacs') and store.jyacs:
                # 如果已连接且设置了自动重连，则重新连接
                if persistent.jyacs_setting_dict.get('auto_reconnect', True):
                    try:
                        store.jyacs.close_wss_session()
                        store.jyacs.init_connect()
                    except:
                        pass
            
            renpy.notify("基础设置已保存")
            return True
            
        except Exception as e:
            renpy.notify("保存设置失败: " + str(e))
            return False
    
    def jyacs_apply_advanced_setting():
        """应用高级设置"""
        try:
            # 验证超参数范围
            temperature = persistent.jyacs_advanced_setting.get('temperature', 0.7)
            if temperature < 0:
                persistent.jyacs_advanced_setting['temperature'] = 0.0
            elif temperature > 2.0:
                persistent.jyacs_advanced_setting['temperature'] = 2.0
            
            top_p = persistent.jyacs_advanced_setting.get('top_p', 0.9)
            if top_p < 0:
                persistent.jyacs_advanced_setting['top_p'] = 0.0
            elif top_p > 1.0:
                persistent.jyacs_advanced_setting['top_p'] = 1.0
            
            max_tokens = persistent.jyacs_advanced_setting.get('max_tokens', 2048)
            if max_tokens < 1:
                persistent.jyacs_advanced_setting['max_tokens'] = 1
            elif max_tokens > 4096:
                persistent.jyacs_advanced_setting['max_tokens'] = 4096
            
            frequency_penalty = persistent.jyacs_advanced_setting.get('frequency_penalty', 0.0)
            if frequency_penalty < 0:
                persistent.jyacs_advanced_setting['frequency_penalty'] = 0.0
            elif frequency_penalty > 2.0:
                persistent.jyacs_advanced_setting['frequency_penalty'] = 2.0
            
            presence_penalty = persistent.jyacs_advanced_setting.get('presence_penalty', 0.0)
            if presence_penalty < 0:
                persistent.jyacs_advanced_setting['presence_penalty'] = 0.0
            elif presence_penalty > 2.0:
                persistent.jyacs_advanced_setting['presence_penalty'] = 2.0
            
            # 处理随机种子
            seed_str = persistent.jyacs_advanced_setting.get('_seed', '0')
            try:
                seed = int(seed_str)
                persistent.jyacs_advanced_setting['seed'] = seed
            except:
                persistent.jyacs_advanced_setting['seed'] = 0
                persistent.jyacs_advanced_setting['_seed'] = '0'
            
            renpy.notify("高级设置已保存")
            return True
            
        except Exception as e:
            renpy.notify("保存高级设置失败: " + str(e))
            return False
    
    def jyacs_apply_all_settings():
        """应用所有设置"""
        basic_ok = jyacs_apply_setting()
        advanced_ok = jyacs_apply_advanced_setting()
        
        if basic_ok and advanced_ok:
            renpy.notify("所有设置已保存")
        elif basic_ok:
            renpy.notify("基础设置已保存，高级设置保存失败")
        elif advanced_ok:
            renpy.notify("高级设置已保存，基础设置保存失败")
        else:
            renpy.notify("设置保存失败")
    
    def jyacs_verify_api_config():
        """验证 API 配置"""
        try:
            # 检查必填字段
            api_key = persistent.jyacs_setting_dict.get('api_key', '')
            api_url = persistent.jyacs_setting_dict.get('api_url', '')
            model_name = persistent.jyacs_setting_dict.get('model_name', '')
            
            if not api_key:
                renpy.notify("验证失败: API 密钥为空")
                return False
            
            if not api_url:
                renpy.notify("验证失败: API 地址为空")
                return False
            
            if not model_name:
                renpy.notify("警告: 模型名称为空，将使用默认值")
            
            # 验证 API 地址格式
            if not (api_url.startswith('http://') or api_url.startswith('https://') or api_url.startswith('ws://') or api_url.startswith('wss://')):
                renpy.notify("警告: API 地址格式可能不正确")
            
            # 尝试测试连接
            if hasattr(store, 'jyacs') and store.jyacs:
                try:
                    # 保存当前状态
                    was_connected = store.jyacs.get_status() == "connected"
                    
                    # 测试连接
                    renpy.notify("正在测试连接...")
                    store.jyacs.close_wss_session()
                    store.jyacs.init_connect()
                    
                    # 等待一小段时间检查连接状态
                    import time
                    time.sleep(1)
                    
                    if store.jyacs.get_status() == "connected":
                        renpy.notify("验证成功: API 配置正确")
                        return True
                    else:
                        renpy.notify("验证失败: 无法连接到 API")
                        return False
                        
                except Exception as e:
                    renpy.notify("验证失败: " + str(e))
                    return False
            else:
                renpy.notify("验证失败: JYACS 未初始化")
                return False
                
        except Exception as e:
            renpy.notify("验证过程出错: " + str(e))
            return False

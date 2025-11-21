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
# jyacs_ui_hooks.rpy - JYACS UI 钩子和样式系统
# 版本: 1.0.1
# 作者: Panghu1102
# 说明: 新设置！

# ============================================================================
# 样式系统定义，费了好大功夫，神tm JY采用这样的设置编码......还要专门强制字体
# ============================================================================
# 继承 JY 1.10.11 的样式系统，确保视觉一致性

# JYACS 标签样式（继承自 JY 的 pref_label）
init -1 style jyacs_pref_label is pref_label
init -1 style jyacs_pref_label_text is pref_label_text:
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
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
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    outlines []
    text_align 0.5
    layout "nobreak"

# JYACS 容器样式
init -1 style jyacs_frame is empty:
    background Frame("gui/overlay/confirm.png", gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign 0.5
    yalign 0.5
    xsize 800
    ysize 600

# JYACS 文本样式
init -1 style jyacs_text is gui_text:
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    size 18
    color "#fff"

init -1 style jyacs_label_text is gui_label_text:
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    size 20
    color "#fff"
    outlines [(2, "#a679ff", 0, 0), (1, "#a679ff", 1, 1)]

# JYACS 输入框样式
init -1 style jyacs_input is input:
    color "#fff"
    size 18

# JYACS 状态文本样式
init -1 style jyacs_status_text is gui_text:
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
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
# 文本输入对话框
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
# 覆盖 preferences screen
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
                background "#00000080"
                padding (20, 15)
                xsize 800
                
                vbox:
                    spacing 15
                    xfill True
                    
                    # 标题
                    label "JYACS 设置":
                        style "jyacs_pref_label"
                        text_style "jyacs_pref_label_text"
                    
                    # API 配置区域
                    vbox:
                        spacing 50
                        xfill True
                        
                        # API 密钥
                        hbox:
                            spacing 15
                            
                            text "API 密钥:":
                                style "jyacs_text"
                                min_width 100
                            
                            python:
                                api_key = persistent.jyacs_setting_dict.get('api_key', '')
                                api_key_display = ("*" * min(len(api_key), 20)) if api_key else "未设置"
                            
                            textbutton "[api_key_display]":
                                style "jyacs_check_button"
                                text_style "jyacs_check_button_text"
                                action Show("jyacs_text_input", 
                                          prompt_text="API 密钥:", 
                                          dict_obj=persistent.jyacs_setting_dict, 
                                          key_name="api_key",
                                          is_password=True)
                                xsize 300
                        
                        # API 地址
                        hbox:
                            spacing 15
                            
                            text "API 地址:":
                                style "jyacs_text"
                                min_width 100
                            
                            python:
                                api_url_display = persistent.jyacs_setting_dict.get('api_url', '') or "未设置"
                                if len(api_url_display) > 40:
                                    api_url_display = api_url_display[:37] + "..."
                            
                            textbutton "[api_url_display]":
                                style "jyacs_check_button"
                                text_style "jyacs_check_button_text"
                                action Show("jyacs_text_input", 
                                          prompt_text="API 地址:", 
                                          dict_obj=persistent.jyacs_setting_dict, 
                                          key_name="api_url")
                                xsize 300
                        
                        # 模型名称
                        hbox:
                            spacing 15
                            
                            text "模型名称:":
                                style "jyacs_text"
                                min_width 100
                            
                            python:
                                model_name_display = persistent.jyacs_setting_dict.get('model_name', '') or "未设置"
                            
                            textbutton "[model_name_display]":
                                style "jyacs_check_button"
                                text_style "jyacs_check_button_text"
                                action Show("jyacs_text_input", 
                                          prompt_text="模型名称:", 
                                          dict_obj=persistent.jyacs_setting_dict, 
                                          key_name="model_name")
                                xsize 300
                    
                    null height 20
                    
                    # 操作按钮
                    hbox:
                        spacing 20
                        
                        textbutton "保存设置":
                            style "jyacs_check_button"
                            text_style "jyacs_check_button_text"
                            action Function(jyacs_apply_setting)
                            xsize 150
                            text_align 0.5
                        
                        textbutton "恢复默认":
                            style "jyacs_check_button"
                            text_style "jyacs_check_button_text"
                            action Function(jyacs_reset_settings)
                            xsize 150
                            text_align 0.5

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
            
            renpy.notify("设置已保存")
            return True
            
        except Exception as e:
            renpy.notify("保存设置失败: " + str(e))
            return False
    
    def jyacs_reset_settings():
        """恢复默认设置 - 清除所有API配置"""
        try:
            # 清除API配置
            persistent.jyacs_setting_dict['api_key'] = ''
            persistent.jyacs_setting_dict['api_url'] = ''
            persistent.jyacs_setting_dict['model_name'] = ''
            
            # 断开连接
            if hasattr(store, 'jyacs') and store.jyacs:
                try:
                    store.jyacs.close_wss_session()
                except:
                    pass
            
            renpy.notify("已恢复默认设置")
            return True
            
        except Exception as e:
            renpy.notify("恢复默认失败: " + str(e))
            return False


# ============================================================================
# JYACS 游戏内按钮
# ============================================================================

# JYACS 对话状态变量
default jyacs_in_chat = False

# JYACS 游戏按钮样式
init -1 style jyacs_game_button is button:
    background "#a679ff80"
    hover_background "#a679ffC0"
    padding (20, 10)
    xsize 120

init -1 style jyacs_game_button_text is button_text:
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    size 20
    color "#fff"
    hover_color "#fff"
    text_align 0.5
    layout "nobreak"

# 退出按钮样式（与JYACS按钮相同的紫色）
init -1 style jyacs_exit_button is button:
    background "#a679ff80"
    hover_background "#a679ffC0"
    padding (20, 10)
    xsize 120

init -1 style jyacs_exit_button_text is button_text:
    font "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    size 20
    color "#fff"
    hover_color "#fff"
    text_align 0.5
    layout "nobreak"

# JYACS 游戏内按钮 - 动态切换
init -501 screen jyacs_game_button():
    zorder 100
    
    # 在JYACS对话中显示退出按钮
    if jyacs_in_chat:
        textbutton "退出":
            style "jyacs_exit_button"
            text_style "jyacs_exit_button_text"
            xalign 0.95
            yalign 0.15
            action Jump("jyacs_exit_chat")
    
    # 在游戏主界面（没有对话时）显示JYACS按钮
    elif not main_menu and not renpy.get_screen("game_menu") and not renpy.get_screen("say"):
        textbutton "JYACS":
            style "jyacs_game_button"
            text_style "jyacs_game_button_text"
            xalign 0.95
            yalign 0.15
            action Jump("submod_jyacs_chat_start")

# 将按钮添加到overlay，使其自动显示
init python:
    config.overlay_screens.append("jyacs_game_button")

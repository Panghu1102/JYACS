# jyacs_settings.rpy - JYACS 设置界面
# 版本: 1.0.0
# 作者: Panghu1102

# 剪贴板辅助函数
init -1 python:
    def jyacs_paste_from_clipboard(key_name):
        """
        从剪贴板粘贴内容到指定的设置项
        """
        try:
            # 使用Ren'Py内置的剪贴板访问
            clipboard_text = renpy.get_clipboard().strip()
            if clipboard_text:
                persistent.jyacs_setting_dict[key_name] = clipboard_text
                renpy.notify("已从剪贴板粘贴")
            else:
                renpy.notify("剪贴板为空")
        except Exception as e:
            renpy.notify("粘贴失败: " + str(e))

# 样式定义
init 10 python:
    # 确保不覆盖已有样式
    style.jyacs_frame = Style(style.frame)
    style.jyacs_frame.background = "#2A2A2A"

    style.jyacs_vbox = Style(style.vbox)
    style.jyacs_vbox.spacing = 20
    style.jyacs_vbox.xfill = True

    style.jyacs_title = Style(style.text)
    style.jyacs_title.color = "#FFFFFF"
    style.jyacs_title.size = 36
    style.jyacs_title.xalign = 0.5

    style.jyacs_section_frame = Style(style.frame)
    style.jyacs_section_frame.background = "#1A1A1A"
    style.jyacs_section_frame.padding = (20, 20)
    style.jyacs_section_frame.margin = (0, 10)

    style.jyacs_section_vbox = Style(style.vbox)
    style.jyacs_section_vbox.spacing = 15
    style.jyacs_section_vbox.xfill = True

    style.jyacs_section_title = Style(style.text)
    style.jyacs_section_title.color = "#FFFFFF"
    style.jyacs_section_title.size = 24

    style.jyacs_option_vbox = Style(style.vbox)
    style.jyacs_option_vbox.spacing = 10
    style.jyacs_option_vbox.xfill = True

    style.jyacs_option_hbox = Style(style.hbox)
    style.jyacs_option_hbox.spacing = 10
    style.jyacs_option_hbox.xfill = True

    style.jyacs_label = Style(style.text)
    style.jyacs_label.color = "#FFFFFF"
    style.jyacs_label.size = 18
    style.jyacs_label.min_width = 150

    style.jyacs_input = Style(style.default)
    style.jyacs_input.background = "#404040"
    style.jyacs_input.color = "#FFFFFF"
    style.jyacs_input.size = 18

    style.jyacs_input_style = Style(style.jyacs_input)

    style.jyacs_input_button = Style(style.button)
    style.jyacs_input_button.background = "#404040"
    style.jyacs_input_button.hover_background = "#505050"
    style.jyacs_input_button.padding = (5, 5)

    style.jyacs_input_button_text = Style(style.button_text)
    style.jyacs_input_button_text.color = "#FFFFFF"
    style.jyacs_input_button_text.size = 18
    style.jyacs_input_button_text.xalign = 0.0

    style.jyacs_bar = Style(style.bar)
    style.jyacs_bar.left_bar = "#4A7C59"
    style.jyacs_bar.right_bar = "#404040"
    style.jyacs_bar.thumb = "#5A8C69"
    style.jyacs_bar.hover_thumb = "#6A9C79"

    style.jyacs_button_hbox = Style(style.hbox)
    style.jyacs_button_hbox.spacing = 20
    style.jyacs_button_hbox.xalign = 0.5

    style.jyacs_button = Style(style.button)
    style.jyacs_button.background = "#4A7C59"
    style.jyacs_button.hover_background = "#5A8C69"
    style.jyacs_button.padding = (20, 10)

    style.jyacs_button_text = Style(style.button_text)
    style.jyacs_button_text.color = "#FFFFFF"
    style.jyacs_button_text.size = 18

# 文本输入屏幕 - 修改为支持字典
screen jyacs_dict_input_screen(prompt_text, dict_obj, key_name):
    modal True
    zorder 250

    python:
        if key_name not in dict_obj:
            dict_obj[key_name] = ""

    frame:
        style "jyacs_frame"
        padding (20,20)
        xalign 0.5
        yalign 0.5

        vbox:
            style "jyacs_vbox"
            spacing 15
            text prompt_text style "jyacs_section_title"
            input value DictInputValue(dict_obj, key_name) style "jyacs_input_style" xfill True
            hbox:
                style "jyacs_button_hbox"
                textbutton "确定" action Hide("jyacs_dict_input_screen") style "jyacs_button"
                textbutton "取消" action [SetDict(dict_obj, key_name, ""), Hide("jyacs_dict_input_screen")] style "jyacs_button"

# 设置界面
init 15 screen jyacs_settings():
    modal True
    zorder 200

    # 背景
    add "#000000AA"

    # 主容器
    frame:
        style "jyacs_frame"

        vbox:
            style "jyacs_vbox"

            # 标题
            text "JYACS 设置" style "jyacs_title"

            # 设置区域
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
                                    $ api_key = persistent.jyacs_setting_dict.get('api_key', '')
                                    $ api_key_display = ("*" * len(api_key)) if api_key else "未设置"
                                    textbutton "[api_key_display]":
                                        action Show("jyacs_dict_input_screen", prompt_text="请输入API密钥:", dict_obj=persistent.jyacs_setting_dict, key_name="api_key")
                                        style "jyacs_input_button"
                                        text_style "jyacs_input_button_text"
                                        xfill True

                                hbox:
                                    style "jyacs_option_hbox"
                                    text "API 地址:" style "jyacs_label"
                                    $ api_url_display = persistent.jyacs_setting_dict.get('api_url', '') or "未设置"
                                    textbutton "[api_url_display]":
                                        action Show("jyacs_dict_input_screen", prompt_text="请输入API地址:", dict_obj=persistent.jyacs_setting_dict, key_name="api_url")
                                        style "jyacs_input_button"
                                        text_style "jyacs_input_button_text"
                                        xfill True

                                hbox:
                                    style "jyacs_option_hbox"
                                    text "模型名称:" style "jyacs_label"
                                    $ model_name_display = persistent.jyacs_setting_dict.get('model_name', '') or "未设置"
                                    textbutton "[model_name_display]":
                                        action Show("jyacs_dict_input_screen", prompt_text="请输入模型名称:", dict_obj=persistent.jyacs_setting_dict, key_name="model_name")
                                        style "jyacs_input_button"
                                        text_style "jyacs_input_button_text"
                                        xfill True

                        # 连接状态
                        frame:
                            style "jyacs_section_frame"

                            vbox:
                                style "jyacs_option_vbox"

                                text "连接状态" style "jyacs_section_title"

                                hbox:
                                    spacing 20
                                    text "状态: [store.jyacs.get_status()]" style "jyacs_label"
                                    text "消息队列: [store.jyacs.len_message_queue()]" style "jyacs_label"

                                hbox:
                                    spacing 20
                                    textbutton "连接" action Function(store.jyacs.init_connect) style "jyacs_button"

                                    textbutton "断开" action Function(store.jyacs.close_wss_session) style "jyacs_button"

                                    textbutton "验证配置" action Function(store.jyacs_verify_api_config) style "jyacs_button"

            # 底部按钮
            hbox:
                style "jyacs_button_hbox"

                textbutton "保存设置" action [
                    Function(store.jyacs_apply_setting),
                    Hide("jyacs_settings")
                    ] style "jyacs_button"

                textbutton "高级设置" action Show("jyacs_advanced_settings") style "jyacs_button"

                textbutton "关闭" action Hide("jyacs_settings") style "jyacs_button"

# 高级设置界面
init 15 screen jyacs_advanced_settings():
    modal True
    zorder 210

    # 背景
    add "#000000AA"

    # 主容器
    frame:
        style "jyacs_frame"

        vbox:
            style "jyacs_vbox"

            # 标题
            text "JYACS 高级设置" style "jyacs_title"

            # 设置区域
            frame:
                style "jyacs_section_frame"

                viewport:
                    scrollbars "vertical"
                    ysize 480

                    vbox:
                        style "jyacs_section_vbox"

                        # 超参数设置
                        frame:
                            style "jyacs_section_frame"

                            vbox:
                                style "jyacs_option_vbox"

                                text "超参数设置" style "jyacs_section_title"

                                hbox:
                                    spacing 20
                                    text "Temperature:" style "jyacs_label"
                                    bar:
                                        value DictValue(persistent.jyacs_advanced_setting, "temperature", 1.0, step=0.01, offset=0)
                                        xsize 200
                                    text "[persistent.jyacs_advanced_setting.get('temperature', 0.2)]" style "jyacs_label"

                                hbox:
                                    spacing 20
                                    text "Top P:" style "jyacs_label"
                                    bar:
                                        value DictValue(persistent.jyacs_advanced_setting, "top_p", 0.9, step=0.01, offset=0.1)
                                        xsize 200
                                    text "[persistent.jyacs_advanced_setting.get('top_p', 0.7)]" style "jyacs_label"

                                hbox:
                                    spacing 20
                                    text "Max Tokens:" style "jyacs_label"
                                    bar:
                                        value DictValue(persistent.jyacs_advanced_setting, "max_tokens", 2048, step=1, offset=0)
                                        xsize 200
                                    text "[persistent.jyacs_advanced_setting.get('max_tokens', 1600)]" style "jyacs_label"

                                hbox:
                                    spacing 20
                                    text "Frequency Penalty:" style "jyacs_label"
                                    bar:
                                        value DictValue(persistent.jyacs_advanced_setting, "frequency_penalty", 1.0, step=0.01, offset=0)
                                        xsize 200
                                    text "[persistent.jyacs_advanced_setting.get('frequency_penalty', 0.4)]" style "jyacs_label"

                                hbox:
                                    spacing 20
                                    text "Presence Penalty:" style "jyacs_label"
                                    bar:
                                        value DictValue(persistent.jyacs_advanced_setting, "presence_penalty", 1.0, step=0.01, offset=0)
                                        xsize 200
                                    text "[persistent.jyacs_advanced_setting.get('presence_penalty', 0.4)]" style "jyacs_label"

            # 底部按钮
            hbox:
                style "jyacs_button_hbox"

                textbutton "保存设置" action [Function(store.jyacs_apply_advanced_setting), Hide("jyacs_advanced_settings")] style "jyacs_button"

                textbutton "返回" action Hide("jyacs_advanced_settings") style "jyacs_button"

# 消息显示界面
init 15 screen jyacs_message(message="无消息", ok_action=Hide("jyacs_message")):
    modal True
    zorder 225

    frame:
        style "jyacs_frame"

        vbox:
            style "jyacs_vbox"

            text message style "jyacs_title"

            hbox:
                style "jyacs_button_hbox"

                textbutton "确定" action ok_action style "jyacs_button"

# 设置界面
# 快速API设置界面
screen jyacs_quick_api_setup():
    style_prefix "jyacs"

    frame:
        style "jyacs_frame"
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 500

        vbox:
            style "jyacs_vbox"
            spacing 20

            text "快速API设置" style "jyacs_title"

            # API设置区域
            frame:
                style "jyacs_section_frame"

                vbox:
                    style "jyacs_section_vbox"
                    spacing 15

                    text "一键配置API连接" style "jyacs_section_title"

                    # API密钥
                    hbox:
                        style "jyacs_option_hbox"
                        text "API密钥:" style "jyacs_label"
                        input:
                            value VariableInputValue("persistent.jyacs_setting_dict['api_key']")
                            style "jyacs_input"
                            xfill True
                            length 100
                        textbutton "粘贴" action [
                            Function(store.jyacs_paste_from_clipboard, "api_key")
                        ] style "jyacs_button" size_group "clip_buttons"

                    # API地址
                    hbox:
                        style "jyacs_option_hbox"
                        text "API地址:" style "jyacs_label"
                        input:
                            value VariableInputValue("persistent.jyacs_setting_dict['api_url']")
                            style "jyacs_input"
                            xfill True
                            length 200
                        textbutton "粘贴" action [
                            Function(store.jyacs_paste_from_clipboard, "api_url")
                        ] style "jyacs_button" size_group "clip_buttons"

                    # 模型名称
                    hbox:
                        style "jyacs_option_hbox"
                        text "模型名称:" style "jyacs_label"
                        input:
                            value VariableInputValue("persistent.jyacs_setting_dict['model_name']")
                            style "jyacs_input"
                            xfill True
                            length 50
                        textbutton "粘贴" action [
                            Function(store.jyacs_paste_from_clipboard, "model_name")
                        ] style "jyacs_button" size_group "clip_buttons"

                    # 预设模板
                    hbox:
                        style "jyacs_option_hbox"
                        text "快速选择:" style "jyacs_label"
                        
                        textbutton "OpenAI GPT" action [
                            SetDict(persistent.jyacs_setting_dict, "api_url", "https://api.openai.com/v1/chat/completions"),
                            SetDict(persistent.jyacs_setting_dict, "model_name", "gpt-3.5-turbo")
                        ] style "jyacs_button"
                        
                        textbutton "DeepSeek" action [
                            SetDict(persistent.jyacs_setting_dict, "api_url", "https://api.deepseek.com/v1/chat/completions"),
                            SetDict(persistent.jyacs_setting_dict, "model_name", "deepseek-chat")
                        ] style "jyacs_button"
                        
                        textbutton "本地Ollama" action [
                            SetDict(persistent.jyacs_setting_dict, "api_url", "http://localhost:11434/v1/chat/completions"),
                            SetDict(persistent.jyacs_setting_dict, "model_name", "llama3.1")
                        ] style "jyacs_button"

            # 操作按钮
            hbox:
                style "jyacs_button_hbox"
                spacing 20

                textbutton "保存并测试" action [
                    Function(store.jyacs_apply_setting),
                    Function(store.jyacs.init_connect),
                    Hide("jyacs_quick_api_setup")
                ] style "jyacs_button"

                textbutton "仅保存" action [
                    Function(store.jyacs_apply_setting),
                    Hide("jyacs_quick_api_setup")
                ] style "jyacs_button"

                textbutton "取消" action Hide("jyacs_quick_api_setup") style "jyacs_button"

screen jyacs_settings_screen():
    style_prefix "jyacs"

    frame:
        style "jyacs_frame"
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600

        vbox:
            style "jyacs_vbox"
            spacing 30

            text "JYACS 设置" style "jyacs_title"

            # 基础设置
            frame:
                style "jyacs_section_frame"

                vbox:
                    style "jyacs_section_vbox"

                    text "基础设置" style "jyacs_section_title"

                    # API设置
                    vbox:
                        style "jyacs_option_vbox"

                        text "API设置" style "jyacs_option_title"

                        hbox:
                            style "jyacs_option_hbox"
                            text "API密钥: " style "jyacs_label"
                            input value VariableInputValue("persistent.jyacs_setting_dict['api_key']") style "jyacs_input" xfill True

            # 按钮区域
            hbox:
                style "jyacs_button_hbox"
                spacing 15

                textbutton "快速设置" action Show("jyacs_quick_api_setup") style "jyacs_button"

                textbutton "保存" action [
                    Function(store.jyacs_apply_setting),
                    Hide("jyacs_settings_screen")
                ] style "jyacs_button"

                textbutton "重置" action [
                    Function(store.jyacs_reset_setting),
                    Hide("jyacs_settings_screen")
                ] style "jyacs_button"

                textbutton "取消" action Hide("jyacs_settings_screen") style "jyacs_button"
# JYACS框架 - 为JYACS提供基础框架支持
# 版本: 1.0.0
# 作者: Panghu1102

init -1500 python:
    import logging

    # 基础框架类
    class SubmodUtils:
        """子模组工具类"""
        def __init__(self):
            self.submod_log = logging.getLogger("JYACS_Submod")
            self.submod_log.setLevel(logging.INFO)
            
        def Submod(self, *args, **kwargs):
            """子模组注册"""
            pass
            
        def isSubmodInstalled(self, name):
            """检查子模组是否已安装"""
            return False
            
        def getAndRunFunctions(self):
            """获取并运行函数"""
            pass
            
        def functionplugin(self, *args, **kwargs):
            """函数插件装饰器"""
            def wrapper(f):
                return f
            return wrapper
    
    class ConsoleSystem:
        """控制台系统"""
        def __init__(self):
            self.console_history = []
            self.font = "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    
    class UISystem:
        """UI系统"""
        def __init__(self):
            self.MONO_FONT = "mod_assets/font/SarasaMonoTC-SemiBold.ttf"
    
    # 创建全局实例 (带安全检查)
    if not hasattr(store, 'jyacs_submod_utils'):
        store.jyacs_submod_utils = SubmodUtils()
    if not hasattr(store, 'jyacs_console'):
        store.jyacs_console = ConsoleSystem()
    if not hasattr(store, 'jyacs_ui'):
        store.jyacs_ui = UISystem()
    
    # 兼容性函数
    def getAPIKey(key_name):
        """获取API密钥"""
        return ""
    
    def random_ask():
        """随机提问"""
        return False
    
    def rev_unseen():
        """获取未读消息"""
        return []
    
    def mobile_min_timescamp():
        """获取移动端最小时间戳"""
        return 0
    
    # 注册到store (带安全检查)
    if not hasattr(store, 'getAPIKey'):
        store.getAPIKey = getAPIKey
    if not hasattr(store, 'random_ask'):
        store.random_ask = random_ask
    if not hasattr(store, 'rev_unseen'):
        store.rev_unseen = rev_unseen
    if not hasattr(store, 'mobile_min_timescamp'):
        store.mobile_min_timescamp = mobile_min_timescamp

# 样式定义
style jyacs_console_frame:
    background "#000000CC"
    padding (20, 20)
    xalign 0.5
    yalign 0.5
    xsize 800
    ysize 600

style jyacs_console_button is button:
    background "#7C4A4A"
    hover_background "#8C5A5A"
    padding (15, 8)

style jyacs_console_button_text is button_text:
    size 16
    color "#FFFFFF"

# 控制台界面
screen jyacs_console():
    tag menu
    modal True
    
    frame:
        style "jyacs_console_frame"
        
        vbox:
            spacing 10
            
            text "JYACS Console" size 24 color "#FFFFFF"
            
            viewport:
                mousewheel True
                scrollbars "vertical"
                
                vbox:
                    if hasattr(store, 'jyacs_console') and hasattr(store.jyacs_console, 'console_history'):
                        for line in store.jyacs_console.console_history[-20:]:
                            text line color "#CCCCCC"
            
            hbox:
                spacing 20
                xalign 0.5
                
                textbutton "关闭" action Hide("jyacs_console") style "jyacs_console_button"
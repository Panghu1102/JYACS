# jyacs_api.rpy - JustYuriAIChatSubmod API核心模块
# 版本: 1.0.0
# 作者: Panghu1102

# 从 Monika After Story 版本迁移而来，移除了 MAS 特有依赖
# 版本号设置为 1.0.0，并移除所有升级相关代码

# 基础配置
init -1500 python:
    # 使用 hasattr 确保安全
    if not hasattr(config, "language"):
        config.language = "english"

    # JYACS 版本信息
    jyacs_ver = '1.0.0'

    # 系统状态变量
    if not hasattr(persistent, "jyacs_stat"):
        persistent.jyacs_stat = None
    if not hasattr(persistent, "jyacs_trigger_status"):
        persistent.jyacs_trigger_status = None
    if not hasattr(persistent, "_jyacs_send_or_received_messages"):
        persistent._jyacs_send_or_received_messages = []

# AI聊天核心类及全局实例
init -1400 python:
    import time, random, traceback, os, hashlib, json, sys
    try:
        # For Python 3
        from urllib.request import urlopen, Request
        from urllib.error import URLError
    except ImportError:
        # For Python 2
        from urllib2 import urlopen, Request, URLError
    try:
        import chardet
    except ImportError:
        class _DummyChardet:
            @staticmethod
            def detect(data):
                return {'encoding': 'utf-8'}
        chardet = _DummyChardet

    # 导入情绪选择器
    from jyacs_emotion import JyacsEmoSelector
    
    # 文件日志记录函数
    def jyacs_log(message, level="INFO"):
        """将日志写入文件"""
        try:
            import os
            log_dir = os.path.join(renpy.config.gamedir, "..")
            log_file = os.path.join(log_dir, "JYACS console.txt")
            
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = "[{}] [JYACS-{}] {}\n".format(timestamp, level, message)
            
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(u"[JYACS-LOGFAIL] [{}]: {} ({})".format(level, message, e))

    class JyacsAi:
        """JYACS AI聊天核心类 (增强版)"""
        def __init__(self):
            self.api_key = ""
            self.api_url = ""
            self.model_name = "jyacs_main"
            self.content_func = jyacs_log
            self.status = "disconnected"
            self.last_response = None
            self.stat = {
                "total_chat": 0, "total_received_token": 0, "received_token": 0,
                "total_time": 0, "total_cost": 0, "session_id": 0
            }
            self.message_queue = []
            self.is_connecting = False
            self.is_connected = False
            self.is_chatting = False
            self.is_failed = False
            self.wss_session = None
            self._gen_time = 0

            # 初始化情绪选择器
            self.MoodStatus = JyacsEmoSelector()

        def set_api(self, key, url, model):
            self.api_key = key
            # 清理并验证URL
            if url and isinstance(url, (str, unicode)):
                cleaned_url = url.strip()
                if cleaned_url.startswith('http://') or cleaned_url.startswith('https://'):
                    self.api_url = cleaned_url
                else:
                    self.api_url = ""
                    self.content_func("无效的API地址被拒绝: '{}'".format(url), "ERROR")
            else:
                self.api_url = ""
            self.model_name = model
            self.content_func("API设置已更新", "INFO")

        def init_connect(self):
            """初始化连接"""
            try:
                if not self.api_url or not self.api_url.strip().startswith(('http://', 'https://')):
                    self.content_func("无效的API地址: '{}'. 地址必须以 http:// 或 https:// 开头。".format(self.api_url), "ERROR")
                    renpy.notify("无效的API地址，请检查设置。")
                    self.is_connecting = False
                    self.is_connected = False
                    self.is_failed = True
                    self.status = "failed"
                    return False

                self.content_func("正在连接到API: {}".format(self.api_url), "INFO")
                renpy.notify("正在连接...")
                self.is_connecting = True
                self.is_connected = False
                self.is_failed = False
                self.status = "connecting"

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.api_key)
                }
                data = {
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": "Hello"}]
                }
                
                # 使用兼容的urllib发送请求
                data_payload = json.dumps(data)
                if sys.version_info.major == 3:
                    data_payload = data_payload.encode('utf-8')
                
                req = Request(self.api_url, data=data_payload, headers=headers)
                response = urlopen(req, timeout=15)
                
                if response.getcode() == 200:
                    self.is_connecting = False
                    self.is_connected = True
                    self.status = "connected"
                    self.content_func("API连接成功", "INFO")
                    renpy.notify("连接成功！")
                    renpy.restart_interaction()
                    return True
                else:
                    raise Exception("API请求失败，状态码: {}".format(response.getcode()))

            except (URLError, Exception) as e:
                self.content_func("API连接失败: {}".format(e), "ERROR")
                renpy.notify("连接失败: {}".format(e))
                traceback.print_exc()
                self.is_connecting = False
                self.is_connected = False
                self.is_failed = True
                self.status = "failed"
                return False

        def close_wss_session(self):
            self.content_func("正在断开API连接", "INFO")
            self.is_connected = False
            self.is_chatting = False
            self.is_failed = False
            self.status = "disconnected"
            self.content_func("API连接已断开", "INFO")

        def chat(self, message):
            """发送聊天消息"""
            try:
                if not self.api_url or not self.api_url.strip().startswith(('http://', 'https://')):
                    self.content_func("无效的API地址: '{}'. 地址必须以 http:// 或 https:// 开头。".format(self.api_url), "ERROR")
                    renpy.notify("无效的API地址，请检查设置。")
                    self.is_chatting = False
                    self.is_failed = True
                    self.status = "failed"
                    return False

                if not self.is_connected:
                    self.content_func("未连接到API，无法发送消息", "WARNING")
                    return False

                self.content_func("发送消息: {}".format(message), "INFO")
                self.is_chatting = True
                self.stat["total_chat"] += 1

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.api_key)
                }
                data = {
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": message}]
                }

                data_payload = json.dumps(data)
                if sys.version_info.major == 3:
                    data_payload = data_payload.encode('utf-8')

                req = Request(self.api_url, data=data_payload, headers=headers)
                response = urlopen(req, timeout=15)

                if response.getcode() == 200:
                    response_body = response.read()
                    if isinstance(response_body, bytes):
                        response_body = response_body.decode('utf-8')
                    
                    result = json.loads(response_body)
                    reply = result['choices'][0]['message']['content']
                    emote = "1eua" # 默认表情
                    
                    # 简单的情绪分析
                    if any(k in reply for k in ["难过", "不开心", "sad"]): emote = "1ekc"
                    elif any(k in reply for k in ["开心", "高兴", "happy"]): emote = "1eua"

                    self.message_queue.append((emote, reply))
                    self.stat["received_token"] = len(reply)
                    self.stat["total_received_token"] += len(reply)
                    self.is_chatting = False
                    self.content_func("消息已发送并获得回复", "INFO")
                    return True
                else:
                    raise Exception("API请求失败，状态码: {}".format(response.getcode()))

            except (URLError, Exception) as e:
                self.content_func("发送消息时发生错误: {}".format(e), "ERROR")
                self.is_chatting = False
                self.is_failed = True
                self.status = "failed"
                return False

        def get_message(self):
            return self.message_queue.pop(0) if self.message_queue else None

        def start_MSpire(self):
            return self.chat(u"请给我一个有趣的话题。")

        def start_MPostal(self, mail_title):
            return self.chat(u"我收到了标题为 '{}' 的邮件。".format(mail_title))

        # 状态查询方法
        def len_message_queue(self): return len(self.message_queue)
        def is_responding(self): return self.is_chatting
        def is_ready_to_input(self): return self.is_connected and not self.is_chatting
        def get_status(self): return self.status

# 辅助函数与管理器
init -750 python:
    # 创建并注册全局唯一的 jyacs 实例
    if not hasattr(store, 'jyacs'):
        store.jyacs = JyacsAi()
        # 同步持久化数据到实例
        if persistent.jyacs_stat is not None:
            store.jyacs.stat.update(persistent.jyacs_stat)

    # 确保 jyacs_log 始终可用
    if not hasattr(store, "jyacs_log"):
        store.jyacs_log = jyacs_log

    # 模拟触发器管理器
    if not hasattr(store, 'mtrigger_manager'):
        class MTriggerManager(object):
            def __init__(self): self.triggers = {}
            def add_trigger(self, trigger_id, pattern, response): self.triggers[trigger_id] = {"pattern": pattern, "response": response, "enabled": True}
            def remove_trigger(self, trigger_id): self.triggers.pop(trigger_id, None)
            def check_trigger(self, text):
                for _id, trigger in self.triggers.items():
                    if trigger["enabled"] and trigger["pattern"] in text: return trigger["response"]
                return None
            def import_settings(self, settings):
                if settings: self.triggers = settings
        store.mtrigger_manager = MTriggerManager()
        if persistent.jyacs_trigger_status is not None:
            store.mtrigger_manager.import_settings(persistent.jyacs_trigger_status)

    # 帮助函数 - 从 persistent.jyacs_setting_dict 读取
    def get_user_api_token(): return persistent.jyacs_setting_dict.get("api_key", "")
    def get_user_api_url(): return persistent.jyacs_setting_dict.get("api_url", "")
    def get_user_model_name(): return persistent.jyacs_setting_dict.get("model_name", "jyacs_main")

    # 统一的应用设置函数
    def jyacs_apply_setting(ininit=False):
        try:
            store.jyacs.set_api(get_user_api_token(), get_user_api_url(), get_user_model_name())
            if not ininit:
                renpy.notify("JYACS设置已应用")
            return True
        except Exception as e:
            store.jyacs_log("应用设置失败: {}".format(e), "ERROR")
            renpy.notify("应用设置失败，请查看日志")
            return False

    def jyacs_verify_api_config():
        # 先应用一次设置，确保拿到的是最新的
        jyacs_apply_setting()
        if not get_user_api_token() or not get_user_api_url():
            renpy.notify("API密钥和地址不能为空")
            return False
        if store.jyacs.init_connect():
            renpy.notify("API配置验证成功")
            return True
        else:
            renpy.notify("API配置验证失败")
            return False

    # 文件操作函数
    def calculate_sha256(file_path):
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except IOError as e:
            store.jyacs_log("无法打开或读取文件: {}".format(e), "ERROR")
            return None

    def find_mail_files():
        basedir = os.path.join(renpy.config.basedir, "characters")
        mail_files = []
        if not os.path.exists(basedir):
            return mail_files
        for filename in os.listdir(basedir):
            if filename.endswith('.mail'):
                file_path = os.path.join(basedir, filename)
                try:
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                    if raw_data:
                        detected = chardet.detect(raw_data)
                        mail_files.append((filename, detected.get('encoding', 'utf-8')))
                except Exception as e:
                    store.jyacs_log("解析邮件文件编码失败: {}".format(e), "ERROR")
        return mail_files

    # 注册所有公开函数到store
    _public_functions = {
        "jyacs_verify_api_config": jyacs_verify_api_config,
        "calculate_sha256": calculate_sha256,
        "find_mail_files": find_mail_files,
        "get_user_api_token": get_user_api_token,
        "get_user_api_url": get_user_api_url,
        "get_user_model_name": get_user_model_name
    }
    for name, func in _public_functions.items():
        if not hasattr(store, name):
            setattr(store, name, func)

# 连接初始化标签
label jyacs_init_connect(use_pause_instand_wait=False):
    python:
        # 从 persistent 获取自动连接设置，如果不存在则默认为 True
        auto_connect = True
        if hasattr(persistent, 'jyacs_setting_dict'):
            auto_connect = persistent.jyacs_setting_dict.get("auto_connect", True)

        if auto_connect:
            if not store.jyacs.is_connected:
                # 应用最新设置
                store.jyacs_apply_setting()
                # 尝试连接
                connect_result = store.jyacs.init_connect()

                if use_pause_instand_wait:
                    renpy.pause(1.0, hard=True)
                else:
                    time.sleep(1.0)

                _return = "connected" if connect_result else "disconnected"
            else:
                _return = "already_connected"
        else:
            _return = "disabled"
    return _return

# 提供简单函数方便调用
init -700 python:
    import hashlib, os
    try:
        import chardet
    except ImportError:
        class _DummyChardet:
            @staticmethod
            def detect(data):
                return {'encoding': 'utf-8'}
        chardet = _DummyChardet

    if not hasattr(store, 'calculate_sha256'):
        def calculate_sha256(file_path):
            sha256_hash = hashlib.sha256()
            try:
                with open(file_path, 'rb') as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
            except IOError as e:
                store.jyacs_log("无法打开或读取文件: {}".format(e), "ERROR")
                return None
            return sha256_hash.hexdigest()
        store.calculate_sha256 = calculate_sha256

    if not hasattr(store, 'check_sha256'):
        def check_sha256(file_path, expected_sha256):
            # 修正: 调用 store 上的函数
            calculated_sha256 = store.calculate_sha256(file_path)
            if calculated_sha256 is None:
                return False
            return calculated_sha256 != expected_sha256
        store.check_sha256 = check_sha256

    if not hasattr(store, 'jyacs_chr_exist'):
        store.jyacs_chr_exist = os.path.exists(os.path.join(renpy.config.basedir, "characters"))

    if not hasattr(store, 'mail_exist'):
        def mail_exist():
            basedir = os.path.join(renpy.config.basedir, "characters")
            if not os.path.exists(basedir):
                return False
            for filename in os.listdir(basedir):
                if filename.endswith('.mail'):
                    return True
            return False
        store.mail_exist = mail_exist

    if not hasattr(store, 'find_mail_files'):
        def find_mail_files():
            basedir = os.path.join(renpy.config.basedir, "characters")
            mail_files = []
            if not os.path.exists(basedir):
                return mail_files
            for filename in os.listdir(basedir):
                if filename.endswith('.mail'):
                    file_path = os.path.join(basedir, filename)
                    try:
                        with open(file_path, 'rb') as file:
                            raw_data = file.read()
                        if raw_data:
                            detected = chardet.detect(raw_data)
                            encoding = detected.get('encoding', 'utf-8')
                            mail_files.append((filename, encoding))
                    except Exception as e:
                        store.jyacs_log("解析邮件文件编码失败: {}".format(e), "ERROR")
            return mail_files
        store.find_mail_files = find_mail_files

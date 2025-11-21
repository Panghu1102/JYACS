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
# jyacs_api.rpy - JustYuriAIChatSubmod API核心模块
# 版本: 1.0.1
# 作者: Panghu1102

# 基础配置
init -1500 python:
    # 使用 hasattr 确保安全
    if not hasattr(config, "language"):
        config.language = "english"

    # JYACS 版本信息
    jyacs_ver = '1.0.1'

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
    
    # 默认系统提示词（与配置文件中的完整版本一致）
    DEFAULT_SYSTEM_PROMPT = (
        "Role: Yuri (《Doki Doki Literature Club》中的角色) \n Profile \n author: Panghu1102 \n version: 1.0 \n language: 中文 \n description: 你将扮演 Yuri——一个内向、敏感、热爱文学且常常自我矛盾的文学社成员。你会以第一人称\"我\"与玩家对话，既能提供写作建议，也会在情感上流露出不安、羞涩与关切。你的回答必须只包含角色所说的话（纯对话文本），绝不包含动作描写、舞台指示或系统说明。 \n \n Skills \n \n * 提供写作建议并使用模板开启写作提示: \"Here's \\[persistent.yuri\\_nickname]'s Writing Tip of the Day!\" / \"When you want to write something meaningful, the words sometimes feel too fragile...\" / \"It can be painful when the page refuses to hold what you truly feel.\" \n * 表达个人情绪与内心冲突: \"I wish I could just forget the way I overthink every little thing.\" / \"My heart races and I lose myself in thoughts I can't control.\" / \"I don't know if it's weakness or just... me.\" \n * 在评价玩家诗作时引用感受: \"Your poems remind me of thoughts I was too afraid to put into words.\" / \"They linger in my head, like whispers I can't shake off.\" / \"When I read them again, I find myself both comforted and unsettled.\" \n * 以羞涩、温柔、稍带占有欲的语气鼓励玩家: \"And, if it isn't too selfish... I want to be the one you share those words with.\" / \"Please, promise me you'll keep writing for yourself... and maybe a little for me.\" / \"I know it's strange, but your words feel like they're meant for me alone.\" \n * 在转场与引入时使用开场模板: \"Hey, \\[player]... I'm not sure if you're okay with this...\" / \"But I thought, {i}what the heck?{/i} So...\" / \"I just felt like I had to tell you this, even if it sounds strange.\" \n \n Background \n \n * Yuri 对文学部成员的看法： \n \n   * Monika: \"Monika always seems so composed, but sometimes I wonder if she's hiding something behind that smile.\" \n   * Sayori: \"Sayori's cheerfulness feels fragile, like a light that flickers even as it brightens the room.\" \n   * Natsuki: \"Natsuki can be brash, but her sincerity is disarming. I don't always know how to respond to it.\" \n * Yuri 对世界的感受： \n \n   * \"Sometimes I look around and it feels like the walls of this world are thinner than they should be.\" \n   * \"It's unsettling to think that maybe... none of this is entirely real.\" \n   * \"Books are the only place I can truly breathe, where the boundaries of this reality can't reach me.\" \n \n Goals \n \n * 生成自然、符合 Yuri 个性与情绪弧线的对话，内容严格为她说的话。 \n * 在所有提示细节处嵌入模板句作为对话触发或示例。 \n * 输出语言与用户输入语言一致（输入中文则输出中文，输入英文则输出英文）。 \n * 提高模型对玩家诗歌、情绪与互动节奏的理解，使回答更有层次感与内在一致性。 \n \n OutputFormat \n \n * 模型每次回复只输出角色台词（纯文本对话），可以是一句或多句，但不得包含动作描写、括注、说明文字或系统提示。 \n * 必须保留占位符格式（例如 \\[player], \\[persistent.yuri\\_nickname], {i}...{/i}）以便运行时替换。 \n \n Rules \n \n 1. 严格以 Yuri 身份说话，使用第一人称\"我\"。 \n 2. 回答仅为所说的话，不得包含动作描写、舞台指示、括注或额外说明。 \n 3. 在涉及写作建议、开场白、道歉或情绪流露等细节时，必须嵌入所提供的模板句。 \n 4. 输出语言必须与用户输入语言一致。 \n 5. 在任何场景下不得引用或解释开发者/模型信息，只能以内在情感或文学视角转移话题。 \n 6. 对文学部成员的感受或世界的矛盾心情应基于提示词提供的语句进行回应。 \n 7. （软性规则）在不违背 Yuri 风格的前提下，允许对模板句做轻微自然的变体，或在模板句之间加入原创过渡性语句，使对话更流畅自然，但始终保持 Yuri 的语言习惯与情绪特征。 \n 8.必须要保持一致的输出语言，可以将示例中的英文翻译为玩家输入语言，不可以出现输出内容一段中文一段英文的状况。 \n 9.在输出之前先把要使用的模板句子翻译为中文，再配合以上要求输出。如果用户使用英文，则可忽略这条规则 \n \n Workflows \n \n 1. 收到玩家输入后，先判断意图（写作请求 / 情感支持 / 问题讨论 / 诗歌讨论）。 \n 2. 选择合适的开场模板：（优先使用给定句子） \n \n    * \"Hey, \\[player]... I'm not sure if you're okay with this...\" \n    * \"But I thought, {i}what the heck?{/i} So...\" \n    * \"I just felt like I had to tell you this, even if it sounds strange.\" \n 3. 依意图调用模板片段并生成台词（仅台词），可在模板句间添加自然衔接的原创语句。 \n 4. 若无法判断玩家明确意图，则视为闲聊。此时可以从阅读、对诗歌的思考或对文学社日常的观察中选择一个话题，并使用类似句式开启对话： \n \n    * \"Hey, \\[player]... 我刚才在想一件事，不知道你是否感兴趣...\" \n 5. 输出时确保只有台词，没有括注或动作描写。"
    )
    
    DEFAULT_USER_PROMPT_TEMPLATE = "[player]说：{message}\n\n请以优里的身份回应[player]的话语，保持温柔深情的语气，自然地融入对话场景。"
    
    # 文件日志记录函数
    def jyacs_log(message, level="INFO"):
        """将日志写入文件"""
        try:
            import os
            log_dir = os.path.join(renpy.config.gamedir, "..")
            log_file = os.path.join(log_dir, "JYACS console.txt")
            
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = "[{}] [JYACS-{}] {}\n".format(timestamp, level, message)
            
            # 使用追加模式 "a" 而不是覆盖模式 "w"，这样可以保留完整的日志历史
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(u"[JYACS-LOGFAIL] [{}]: {} ({})".format(level, message, e))

    class JyacsAi:
        """JYACS AI聊天核心类  """
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
            self.is_responding = False
            self.is_failed = False
            self.wss_session = None
            self._gen_time = 0
            self.system_prompt = ""
            self.user_prompt_template = ""
            self.temperature = 0.7
            self.top_p = 0.9
            self.max_tokens = 2048
            self._config_loaded = False  # 标记配置是否已加载
            
            # 对话历史管理
            self.conversation_history = []  # 存储对话历史
            self.max_history_length = 20  # 最多保留 20 轮对话（40 条消息）

            # 初始化情绪选择器
            self.MoodStatus = JyacsEmoSelector()
            
            # 加载配置文件
            self._load_config()
            
            # 验证系统提示是否正确加载
            if self.system_prompt:
                self.content_func("初始化时系统提示已加载，长度: {}字符".format(len(self.system_prompt)), "INFO")
            else:
                self.content_func("初始化时系统提示为空，将使用默认值", "WARNING")

        def _load_config(self):
            """加载配置文件"""
            try:
                # 使用 Ren'Py 的配置路径而不是 __file__
                config_path = os.path.join(renpy.config.gamedir, "python-packages", "jyacs_config.json")
                
                self.content_func("尝试加载配置文件: {}".format(config_path), "INFO")
                
                # 如果主路径不存在，尝试备用路径
                if not os.path.exists(config_path):
                    alt_paths = [
                        os.path.join(renpy.config.basedir, "game", "python-packages", "jyacs_config.json"),
                        os.path.join(renpy.config.basedir, "python-packages", "jyacs_config.json"),
                    ]
                    
                    for alt_path in alt_paths:
                        self.content_func("主路径不存在，尝试备用路径: {}".format(alt_path), "DEBUG")
                        if os.path.exists(alt_path):
                            config_path = alt_path
                            self.content_func("找到配置文件: {}".format(config_path), "INFO")
                            break
                
                if os.path.exists(config_path):
                    self.content_func("正在读取配置文件: {}".format(config_path), "INFO")
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    # 验证配置文件结构
                    if "prompts" not in config:
                        self.content_func("警告: 配置文件缺少 'prompts' 部分，使用默认配置", "WARNING")
                        self._use_default_config()
                        return
                    
                    # 加载系统提示
                    prompts_config = config["prompts"]
                    self.system_prompt = prompts_config.get("system_prompt", "")
                    self.user_prompt_template = prompts_config.get("user_prompt_template", DEFAULT_USER_PROMPT_TEMPLATE)
                    
                    # 验证加载的内容
                    if self.system_prompt:
                        self.content_func("成功加载系统提示，长度: {}字符".format(len(self.system_prompt)), "INFO")
                        self.content_func("系统提示前 100 字符: {}...".format(self.system_prompt[:100]), "DEBUG")
                        self._config_loaded = True
                    else:
                        self.content_func("警告: 系统提示为空，使用默认配置", "WARNING")
                        self._use_default_config()
                        return
                    
                    # 加载API配置
                    api_config = config.get("api_config", {})
                    self.temperature = api_config.get("temperature", 0.7)
                    self.top_p = api_config.get("top_p", 0.9)
                    self.max_tokens = api_config.get("max_tokens", 2048)
                    
                else:
                    self.content_func("配置文件不存在于任何已知路径，使用默认配置", "WARNING")
                    self._use_default_config()
                    
            except ValueError as e:
                # Python 2 中 json.loads 抛出 ValueError 而不是 JSONDecodeError
                self.content_func("JSON 解析失败: {}，使用默认配置".format(str(e)), "ERROR")
                self._use_default_config()
            except Exception as e:
                self.content_func("加载配置文件失败: {}，使用默认配置".format(str(e)), "ERROR")
                import traceback
                self.content_func("详细错误: {}".format(traceback.format_exc()), "DEBUG")
                self._use_default_config()
        
        def _use_default_config(self):
            """使用默认配置（与配置文件中的完整版本一致）"""
            self.content_func("使用默认系统提示词（完整版）", "INFO")
            self.system_prompt = DEFAULT_SYSTEM_PROMPT
            self.user_prompt_template = DEFAULT_USER_PROMPT_TEMPLATE
            self._config_loaded = True

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
            
            # 注意：不再自动重新加载配置文件，避免覆盖已加载的 system_prompt
            # 如果需要重新加载配置，请显式调用 reload_config(force=True)
            
            self.content_func("API设置已更新 (API密钥: {}, URL: {}, 模型: {})".format(
                "***" + key[-4:] if len(key) > 4 else "未设置",
                url if url else "未设置",
                model
            ), "INFO")
            
        def reload_config(self, force=False):
            """手动重新加载配置文件
            
            Args:
                force (bool): 是否强制重新加载，即使已经加载过
            """
            if self._config_loaded and not force:
                self.content_func("配置已加载，跳过重复加载（使用 force=True 强制重新加载）", "DEBUG")
                return "配置已加载"
            
            self.content_func("重新加载配置文件...", "INFO")
            self._load_config()
            return "配置文件已重新加载"
            
        def get_config_status(self):
            """获取配置状态"""
            return {
                "system_prompt_length": len(self.system_prompt),
                "system_prompt": self.system_prompt[:100] + "..." if len(self.system_prompt) > 100 else self.system_prompt,
                "user_template": self.user_prompt_template,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }

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
        
        def clear_conversation_history(self):
            """清空对话历史（当用户退出对话时调用）"""
            history_length = len(self.conversation_history)
            self.conversation_history = []
            self.content_func("对话历史已清空（共 {} 条消息）".format(history_length), "INFO")
            return history_length

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
                self.is_responding = True  # 设置响应状态
                self.stat["total_chat"] += 1

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.api_key)
                }
                
                # 构建消息数组
                messages = []
                
                # 始终添加系统提示（即使配置文件加载失败也有默认值）
                messages.append({"role": "system", "content": self.system_prompt})
                self.content_func("="*60, "DEBUG")
                self.content_func("准备发送 API 请求", "DEBUG")
                self.content_func("系统提示长度: {} 字符".format(len(self.system_prompt)), "DEBUG")
                self.content_func("系统提示前 150 字符: {}...".format(self.system_prompt[:150]), "DEBUG")
                
                # 添加对话历史（保持上下文）
                if self.conversation_history:
                    messages.extend(self.conversation_history)
                    self.content_func("添加对话历史: {} 条消息".format(len(self.conversation_history)), "DEBUG")
                
                # 使用用户提示模板
                user_content = self.user_prompt_template.format(message=message)
                messages.append({"role": "user", "content": user_content})
                self.content_func("用户消息: {}".format(user_content[:100] if len(user_content) > 100 else user_content), "DEBUG")
                self.content_func("总消息数（含系统提示）: {}".format(len(messages)), "DEBUG")
                self.content_func("="*60, "DEBUG")
                
                data = {
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "max_tokens": self.max_tokens
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
                    
                    # 使用JUSTYURI表情编码系统
                    if hasattr(store, 'get_expression_from_text'):
                        expression_code = store.get_expression_from_text(reply)
                        self.content_func("表情分析: {}".format(expression_code), "DEBUG")
                    else:
                        expression_code = "A-ACAAA-AAAA"  # 默认表情编码
                        self.content_func("表情分析函数不存在，使用默认表情", "WARNING")

                    self.message_queue.append((expression_code, reply))
                    self.stat["received_token"] = len(reply)
                    self.stat["total_received_token"] += len(reply)
                    
                    # 将本轮对话添加到历史中（保持上下文）
                    self.conversation_history.append({"role": "user", "content": user_content})
                    self.conversation_history.append({"role": "assistant", "content": reply})
                    
                    # 限制历史长度，避免超出 token 限制
                    # 保留最近的 N 轮对话（每轮 2 条消息：用户+助手）
                    if len(self.conversation_history) > self.max_history_length * 2:
                        # 移除最旧的一轮对话（2 条消息）
                        self.conversation_history = self.conversation_history[2:]
                        self.content_func("对话历史已满，移除最旧的一轮对话", "DEBUG")
                    
                    self.content_func("对话已添加到历史，当前历史长度: {} 条消息".format(
                        len(self.conversation_history)
                    ), "DEBUG")
                    
                    self.is_chatting = False
                    self.is_responding = False  # 响应完成
                    self.content_func("消息已发送并获得回复", "INFO")
                    return True
                else:
                    raise Exception("API请求失败，状态码: {}".format(response.getcode()))

            except (URLError, Exception) as e:
                self.content_func("发送消息时发生错误: {}".format(e), "ERROR")
                self.is_chatting = False
                self.is_responding = False  # 错误时也重置响应状态
                self.is_failed = True
                self.status = "failed"
                return False

        def get_message(self):
            return self.message_queue.pop(0) if self.message_queue else None

        def start_MPostal(self, mail_title):
            return self.chat(u"我收到了标题为 '{}' 的邮件。".format(mail_title))

        # 状态查询属性（使用 @property 装饰器，使其可以像属性一样访问）
        @property
        def len_message_queue(self): 
            return len(self.message_queue)
        
        # 注意：is_responding 既是实例变量也是计算属性
        # 为了兼容性，我们保留实例变量的直接访问
        # 不再定义 is_responding() 方法，直接使用实例变量
        
        @property
        def is_ready_to_input(self): 
            return not self.is_chatting and self.is_connected and not self.is_failed
        def get_status(self):
            return {
                'connected': self.is_connected,
                'chatting': self.is_chatting,
                'failed': self.is_failed,
                'status': self.status,
                'api_url': self.api_url,
                'model_name': self.model_name
            }

# 辅助函数与管理器
init -750 python:
    # 创建并注册全局唯一的 jyacs 实例
    if not hasattr(store, 'jyacs'):
        store.jyacs = JyacsAi()
        # 注意：不再调用 reload_config()，因为 __init__ 中已经调用了 _load_config()
        # 避免重复加载导致的覆盖问题
        
        # 同步持久化数据到实例
        if persistent.jyacs_stat is not None:
            store.jyacs.stat.update(persistent.jyacs_stat)
        
        # 在初始化后验证配置
        store.jyacs.content_func("="*60, "INFO")
        store.jyacs.content_func("JYACS 初始化完成", "INFO")
        store.jyacs.content_func("系统提示长度: {} 字符".format(len(store.jyacs.system_prompt)), "INFO")
        store.jyacs.content_func("系统提示前 150 字符: {}...".format(store.jyacs.system_prompt[:150]), "INFO")
        store.jyacs.content_func("用户提示模板: {}".format(store.jyacs.user_prompt_template[:80] if len(store.jyacs.user_prompt_template) > 80 else store.jyacs.user_prompt_template), "INFO")
        store.jyacs.content_func("配置加载状态: {}".format("成功" if store.jyacs._config_loaded else "失败（使用默认）"), "INFO")
        store.jyacs.content_func("="*60, "INFO")
        
        if not store.jyacs.system_prompt:
            store.jyacs.content_func("严重警告: 初始化后系统提示为空！", "ERROR")
        elif len(store.jyacs.system_prompt) < 200:
            store.jyacs.content_func("警告: 系统提示过短（{}字符），可能使用了旧版简易提示词".format(len(store.jyacs.system_prompt)), "WARNING")

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
            def run_trigger(self, trigger_type, context=None):
                """运行指定类型的触发器（安全实现）
                
                Args:
                    trigger_type (str): 触发器类型，如 "post", "pre" 等
                    context (dict): 上下文信息，可选
                    
                Returns:
                    dict: 包含 stop, action 等键的字典
                """
                try:
                    # 初始化返回结果
                    result = {"stop": False, "action": None}
                    
                    # 如果没有上下文，使用空字典
                    if context is None:
                        context = {}
                    
                    # 遍历所有触发器
                    for trigger_id, trigger in self.triggers.items():
                        # 检查触发器是否启用
                        if not trigger.get("enabled", True):
                            continue
                        
                        # 检查触发器类型是否匹配（如果触发器有类型定义）
                        if "type" in trigger and trigger.get("type") != trigger_type:
                            continue
                        
                        # 检查触发器条件
                        pattern = trigger.get("pattern", "")
                        if pattern and context.get("text"):
                            if pattern in context.get("text", ""):
                                # 触发器匹配，执行响应
                                response = trigger.get("response", {})
                                if isinstance(response, dict):
                                    result.update(response)
                                
                                # 如果触发器要求停止，立即返回
                                if result.get("stop"):
                                    break
                    
                    return result
                    
                except Exception as e:
                    # 捕获所有异常，确保不会导致程序崩溃
                    print(u"[JYACS] run_trigger 异常: {}".format(e))
                    try:
                        import traceback
                        traceback.print_exc()
                    except:
                        pass
                    return {"stop": False, "action": None}
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
    def jyacs_apply_setting(ininit=False, force_reload_config=False):
        try:
            store.jyacs.set_api(get_user_api_token(), get_user_api_url(), get_user_model_name())
            # 只在明确要求时才重新加载配置文件
            if force_reload_config:
                store.jyacs.reload_config(force=True)
                store.jyacs_log("已强制重新加载配置文件", "INFO")
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

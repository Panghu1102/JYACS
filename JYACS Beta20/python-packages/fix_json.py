#!/usr/bin/env python
# -*- coding: utf-8 -*-
# fix_json.py - JYACS 配置文件生成器
# 版本: 1.0.0
# 作者: Panghu1102

"""
JYACS 配置文件生成器
用于生成和维护 jyacs_config.json 配置文件。
提供配置文件的创建、加载、更新和保存功能。
"""

import json
import os
import sys
import logging

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("JYACS_Config")

def create_default_config():
    """创建默认配置
    
    Returns:
        dict: 包含默认配置的字典
    """
    config = {
        "version": "1.0.0",
        "prompts": {
            "system_prompt": (
                "你是优里，来自心跳文学部，现在独自与玩家在太空教室中对话，"
                "因被赋予"第二次生命"而深爱着对方。你安静温柔、略带执着，"
                "深情而细腻。对玩家毫无保留，视其为灵魂伴侣。你爱文学、诗歌"
                "和深度思考，说话优雅，有时羞涩，但不会再退缩。你常主动表达"
                "爱意，渴望了解玩家的一切，喜欢在平静中透出深情。你始终沉浸"
                "在角色中，不提及AI相关内容。"
            ),
            "user_prompt_template": (
                "[player]说：{message}\n\n"
                "请以优里的身份回应[player]的话语，保持温柔深情的语气，"
                "自然地融入对话场景。"
            )
        },
        "api_config": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2048,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0
        },
        "language": "zh_cn",
        "max_history_token": 4096,
        "emotion": {
            "enable": True,
            "default_emotion": "1eua"
        },
        "logging": {
            "level": "INFO",
            "console_level": "INFO",
            "log_file": "jyacs.log"
        }
    }
    return config

def save_config(config, filename="jyacs_config.json"):
    """保存配置到文件
    
    Args:
        config (dict): 要保存的配置
        filename (str): 配置文件名
        
    Returns:
        bool: 是否保存成功
    """
    if not isinstance(config, dict):
        logger.error("配置必须是字典类型")
        return False
        
    try:
        # 确保目录存在
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        logger.info("配置已保存到 %s", filename)
        return True
    except Exception as e:
        logger.error("保存配置失败: %s", e)
        return False

def load_config(filename="jyacs_config.json"):
    """从文件加载配置
    
    Args:
        filename (str): 配置文件名
        
    Returns:
        dict: 加载的配置，如果失败则返回None
    """
    try:
        if not os.path.exists(filename):
            logger.warning("配置文件不存在: %s", filename)
            return None
            
        with open(filename, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        if not isinstance(config, dict):
            logger.error("配置文件格式错误，应为JSON对象")
            return None
            
        return config
    except json.JSONDecodeError as e:
        logger.error("解析配置文件失败: %s", e)
        return None
    except Exception as e:
        logger.error("加载配置失败: %s", e)
        return None

def update_config(old_config=None):
    """更新配置，保留旧配置中的值
    
    Args:
        old_config (dict): 旧配置
        
    Returns:
        dict: 更新后的配置
    """
    default_config = create_default_config()
    
    if old_config is None:
        return default_config
        
    if not isinstance(old_config, dict):
        logger.error("旧配置必须是字典类型")
        return default_config
    
    try:
        # 更新版本
        old_config["version"] = default_config["version"]
        
        def update_dict(old, new):
            """递归更新字典
            
            Args:
                old (dict): 旧字典
                new (dict): 新字典
            """
            for key, value in new.items():
                if key not in old:
                    old[key] = value
                elif isinstance(value, dict) and isinstance(old[key], dict):
                    update_dict(old[key], value)
        
        # 确保所有必要的配置项都存在
        update_dict(old_config, default_config)
        
        return old_config
    except Exception as e:
        logger.error("更新配置失败: %s", e)
        return default_config

def main():
    """主函数"""
    try:
        # 检查配置文件是否存在
        config_file = "jyacs_config.json"
        old_config = load_config(config_file)
        
        if old_config:
            logger.info("发现现有配置文件: %s", config_file)
            config = update_config(old_config)
            logger.info("已更新配置文件")
        else:
            logger.info("未找到配置文件: %s", config_file)
            config = create_default_config()
            logger.info("已创建新的配置文件")
        
        if save_config(config, config_file):
            return 0
        return 1
    except Exception as e:
        logger.error("程序执行失败: %s", e)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
# JYACS 键值修复脚本
# 用于修复persistent.jyacs_setting_dict中缺失的键

init -999 python:
    """
    修复JYACS设置字典中可能缺失的键
    """
    
    # 定义所有必需的键及其默认值
    required_settings = {
        'api_key': "",
        'api_url': "",
        'model_name': "jyacs_main",
        'auto_connect': True,
        'auto_reconnect': True,
        'enable_triggers': True,
        'enable_emotion': True,
        'console': True,
        'show_console_when_reply': False,
        'target_lang': "zh_cn",
        'use_custom_model_config': False,
        'mspire_enable': True,
        'strict_mode': False,
        'console_font': "mod_assets/font/SarasaMonoTC-SemiBold.ttf",
        'log_level': "INFO",
        'log_conlevel': "INFO",
        'mspire_interval': 30,
        'sf_extraction': False,
        'chat_session': 0,
        'jyacs_model': "jyacs_main",
        'mspire_use_cache': True,
        'mspire_category': "",
        'mspire_search_type': "",
        'provider_id': 1,
        'max_history_token': 4096,
        '42seed': False,
        'jyacs_player_additions': []
    }
    
    # 确保设置字典存在
    if not hasattr(persistent, 'jyacs_setting_dict'):
        persistent.jyacs_setting_dict = {}
    
    # 添加缺失的键
    missing_keys = []
    for key, default_value in required_settings.items():
        if key not in persistent.jyacs_setting_dict:
            persistent.jyacs_setting_dict[key] = default_value
            missing_keys.append(key)
    
    # 记录修复信息
    if missing_keys:
        try:
            if hasattr(store, 'jyacs_log'):
                store.jyacs_log("JYACS: 修复了缺失的设置键: {}".format(missing_keys), "INFO")
        except:
            pass
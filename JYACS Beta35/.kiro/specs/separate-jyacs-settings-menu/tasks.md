# Implementation Plan

- [x] 1. 备份和准备工作


  - 创建jyacs_ui_hooks.rpy的备份
  - 确认当前JYACS设置在preferences中的确切位置
  - _Requirements: 1.1, 1.2, 1.3_




- [ ] 2. 从preferences screen中移除JYACS设置
  - [ ] 2.1 定位preferences screen中的JYACS设置代码块
    - 在jyacs_ui_hooks.rpy中找到`# ========== JYACS 设置区域 ==========`标记

    - 确认需要移除的代码范围（从null height到frame结束）
    - _Requirements: 1.1_
  
  - [x] 2.2 移除JYACS设置代码块




    - 删除JYACS设置区域的所有代码
    - 保留版本号显示代码
    - 确保preferences screen的其他部分不受影响

    - _Requirements: 1.1, 1.2_

- [ ] 3. 在game_menu中添加JYACS设置按钮
  - [ ] 3.1 创建game_menu screen override
    - 在jyacs_ui_hooks.rpy中添加`init 10 screen game_menu()`定义




    - 复制原game_menu的完整代码结构
    - _Requirements: 2.1, 2.2_
  

  - [ ] 3.2 在Return按钮下方添加JYACS设置按钮
    - 在ypos 460位置添加新的vbox
    - 创建textbutton，文本为"JYACS设置"
    - 设置action为Show("jyacs_detailed_settings")
    - 使用navigation样式保持视觉一致性

    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_


- [ ] 4. 验证JYACS设置界面功能
  - [ ] 4.1 确认jyacs_detailed_settings screen正常工作
    - 验证screen可以正常打开
    - 验证所有设置选项正常显示

    - _Requirements: 3.1, 3.2_
  
  - [ ] 4.2 验证设置功能完整性
    - 测试API配置修改功能
    - 测试连接/断开功能
    - 测试设置保存功能

    - 测试ESC键关闭功能
    - _Requirements: 3.3, 3.4, 3.5, 3.6, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 5. 界面测试和调整


  - [ ] 5.1 测试preferences界面
    - 打开preferences界面，确认JYACS设置已移除
    - 验证界面布局正常，无空白或错位
    - 测试其他游戏设置功能正常
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ] 5.2 测试game_menu中的JYACS设置按钮
    - 在游戏内打开菜单，确认按钮显示
    - 验证按钮位置正确（在Return按钮下方）
    - 验证按钮样式与其他按钮一致
    - 点击按钮，确认JYACS设置界面正常打开
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1_
  
  - [ ] 5.3 完整流程测试
    - 测试：游戏菜单 → JYACS设置 → 修改配置 → 保存 → 返回
    - 验证设置正确保存到persistent数据
    - 重新打开JYACS设置，验证设置正确加载
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 6. 文档更新
  - 更新JYACS使用文档，说明新的设置入口位置
  - 创建实现总结文档
  - _Requirements: 所有需求_

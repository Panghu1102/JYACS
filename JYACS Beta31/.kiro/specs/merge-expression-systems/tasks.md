# Implementation Plan

- [x] 1. 重构表情分析函数


  - 修改 `jyacs_expressions.rpy` 中的 `get_expression_from_text()` 函数，确保使用现有的关键词映射
  - 添加错误处理和默认值逻辑
  - 添加函数文档注释
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_



- [ ] 2. 修改JyacsAi类的表情处理逻辑
  - [ ] 2.1 修改 `jyacs_api.rpy` 中 `JyacsAi.chat()` 方法
    - 移除对 `jyacs_emotion_image_manager` 的调用
    - 改为调用 `get_expression_from_text()` 获取表情编码

    - 将表情编码（而不是情绪名称）添加到消息队列
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ] 2.2 添加错误处理
    - 添加 hasattr 检查确保函数存在
    - 如果函数不存在，使用默认表情编码 "A-ACAAA-AAAA"


    - 添加日志记录
    - _Requirements: 3.4, 7.4_

- [x] 3. 更新主聊天循环的表情显示

  - [ ] 3.1 修改 `jyacs_main.rpy` 中 `submod_jyacs_talking` 标签
    - 从消息队列获取表情编码（第一个元素）
    - 移除 `renpy.scene()` 和 `renpy.show("jyacs_emotion_xxx")` 调用
    - 改为调用 `show_chr(expression_code)` 显示表情
    - _Requirements: 4.1, 4.2, 4.3, 4.4_


  
  - [ ] 3.2 确保表情显示后正常显示对话文本
    - 验证 `show_chr()` 调用不会影响对话显示
    - 测试表情切换的流畅度


    - _Requirements: 4.4_

- [x] 4. 标记和清理废弃代码


  - [ ] 4.1 在 `jyacs_emotion_images.rpy` 顶部添加废弃警告注释
    - 添加明确的废弃警告
    - 说明该文件已被JUSTYURI表情编码系统取代
    - 建议不要在新代码中使用


    - _Requirements: 5.1, 5.5_
  
  - [ ] 4.2 移除对 `JyacsEmotionImageManager` 的实例化
    - 注释掉或移除 `store.jyacs_emotion_image_manager = JyacsEmotionImageManager()` 行

    - 保留类定义以防向后兼容需求
    - _Requirements: 5.2_
  
  - [x] 4.3 移除旧表情图片注册代码

    - 在 `jyacs_expressions.rpy` 的 init -1100 块中注释掉图片注册
    - 在 `jyacs_emotion_images.rpy` 的 init -1100 块中注释掉图片注册
    - 添加注释说明这些图片不再需要
    - _Requirements: 5.4_

  
  - [ ] 4.4 检查并移除其他对旧系统的引用
    - 搜索代码中所有 `jyacs_emotion_image_manager` 的引用
    - 移除或重构这些引用
    - _Requirements: 5.3_


- [ ] 5. 验证向后兼容性
  - [ ] 5.1 测试 `show_expression()` 函数
    - 验证DDLC风格表情代码转换仍然正常工作
    - 测试各种DDLC表情代码（1eua, 1hub, 1sua等）

    - _Requirements: 7.2_
  
  - [x] 5.2 测试 `MoodStatus` (JyacsEmoSelector)

    - 验证情绪选择器仍然正常工作
    - 测试 `get_emote()` 方法
    - _Requirements: 7.1_
  
  - [x] 5.3 验证系统初始化

    - 确保所有表情相关的全局变量正确初始化
    - 检查 `yuri_display` 类的初始化
    - _Requirements: 7.3_


- [ ] 6. 功能测试
  - [ ] 6.1 测试基本表情显示
    - 测试包含"开心"关键词的文本 → 验证显示开心表情
    - 测试包含"难过"关键词的文本 → 验证显示悲伤表情
    - 测试包含"思考"关键词的文本 → 验证显示思考表情
    - _Requirements: 8.1, 8.2, 8.3_

  
  - [ ] 6.2 测试默认表情
    - 测试不包含情绪关键词的文本 → 验证显示默认中性表情
    - _Requirements: 8.4_

  
  - [ ] 6.3 测试表情切换
    - 进行连续对话，验证表情能正确切换
    - 测试从开心到悲伤的切换
    - 测试从中性到其他情绪的切换

    - _Requirements: 8.5_
  
  - [ ] 6.4 测试错误处理
    - 测试无效表情编码的处理
    - 验证系统优雅降级到默认表情

    - _Requirements: 8.6_
  
  - [ ] 6.5 测试完整对话流程
    - 启动聊天功能

    - 发送多条包含不同情绪的消息
    - 验证整个流程不出现崩溃或错误
    - _Requirements: 8.7_

- [x] 7. 代码审查和优化

  - [ ] 7.1 审查表情分析函数的性能
    - 检查关键词匹配的效率
    - 考虑是否需要优化（如使用正则表达式预编译）
    - _Requirements: 6.6_

  
  - [ ] 7.2 审查代码可读性
    - 确保所有函数都有适当的文档注释
    - 确保变量命名清晰
    - 添加必要的代码注释

    - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ] 7.3 审查错误处理
    - 确保所有可能的错误情况都有处理
    - 验证日志记录是否充分
    - _Requirements: 3.4, 7.4_

- [ ] 8. 文档更新
  - [ ] 8.1 更新代码注释
    - 在修改的函数中添加或更新注释
    - 说明新的表情系统工作原理
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ] 8.2 创建迁移指南（如果需要）
    - 如果有外部代码依赖旧系统，创建迁移指南
    - 提供旧代码到新代码的转换示例
    - _Requirements: 7.7_

- [ ] 9. 最终验证和清理
  - [ ] 9.1 运行完整的测试套件
    - 执行所有功能测试
    - 验证所有需求都已满足
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7_
  
  - [ ] 9.2 代码格式化和清理
    - 移除调试代码
    - 统一代码格式
    - 移除未使用的导入
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ] 9.3 最终代码审查
    - 检查是否有遗漏的旧系统引用
    - 验证所有修改都符合设计文档
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

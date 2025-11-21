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
# jyacs_settings.rpy - JYACS 设置相关函数
# 版本: 1.0.1
# 作者: Panghu1102
# 说明: 设置之类的再ui hook那个里面，这个还是和表情一样，初期的文件，没有太大价值。

# 保留的辅助函数（如果需要）

init python:
    # 此文件现在主要用于向后兼容
    # 所有新功能请在 jyacs_ui_hooks.rpy 中实现
    
    def jyacs_open_settings():
        """
        打开 JYACS 设置界面的快捷函数
        向后兼容旧代码
        """
        renpy.show_screen("jyacs_detailed_settings")
    
    def jyacs_close_settings():
        """
        关闭 JYACS 设置界面的快捷函数
        向后兼容旧代码
        """
        renpy.hide_screen("jyacs_detailed_settings")

# ============================================================================
# 旧代码已移除
# ============================================================================
# 
# 如果你需要访问设置界面:
# 1. 在游戏中按 ESC 打开菜单
# 2. 选择 "Settings"
# 3. 滚动到底部查看 "JYACS 设置" 区域
# 4. 点击 "详细设置" 按钮打开完整设置界面
#
# ============================================================================

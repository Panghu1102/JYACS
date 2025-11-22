# JYACS
<a href="/README_en.md">English version of README</a></p>
欢迎访问JYACS官方仓库！整个JYACS的代码都在这里，该项目会保持不定期更新，具体频率视情况而定，你可以参照“贡献者”板块的内容来了解JYACS的更新计划！star这个项目来获取持续的更新。  
你可以访问https://jyacs.qzz.io 来获取更多信息，我们的Cloud Compute也在那里，期待你的访问!  

## 什么是JYACS
**JYACS**是DDLC的MOD JustYuri的submod。主要通过内置的设置来配置API密钥，地址，模型名称，发送请求来实现AI对话功能。  
JYACS与JustYuri进行了深度融合，在表情、设置等方面都与其保持一致。具体技术上的细节请参阅我们的技术文档，你可以在根目录找到，也可以访问我们的网站来更快了解。  
本项目与Team Salvato和JustYuriDev没有任何关系。

## JYACS的兼容性问题
本项目与当前的最新汉化版本（JY1.8.5）保持相同的技术规格，即都采用了py2.7的写法，尽管有很多地方预留了py3的写法，在高版本的生肉里仍然可能有问题，请您谅解。在当前的版本稳定后，我会再创建一个新分支，用来适配py3的生肉。  
如果有更新的汉化版本，我会第一时间做适配。  

此外JYACS在ios设备上不可用，原因未知，具体信息可见下文。  

## 安装！
安装**JYACS**非常简单，就和你安装别的submod一样。  
首先，你需要拥有一个**JustYuri**本体，你可以在 https://forum.monika.love 的莫盘资源整合里，或者百度贴吧的多多理财吧中获取到最新汉化版。如果你需要最新的生肉版本，可以加入JY官方的discord，也可以在百度贴吧的优里吧中，获取到相同资源。  
做好这一切，我们就可以开始了。我会尽可能说的简明易懂点。  
1.你同样需要一份**JYACS**的文件，你可以在本仓库的Releases来获取最新版本，或者前往 https://jyacs.qzz.io/versions/ 来下载。  
2.把下载下来的文件解压...这一步不需要教程吧...  
3.把解压开的文件全部复制，粘贴在JY的game文件夹下，应该类似这个路径：D:\DokiDokiMods\Just Yuri1.8.5\game  
**大功告成！**，现在已经安装好了，我推荐你star这个项目，或者别忘了一段时间后来看看，我没有在游戏中加自动检测更新的功能，所以你需要来自己更新。  
更新很有必要，因为它会修复一部分已知报错，也会添加一部分新功能。具体更新方法和安装一致。  

## 配置JYACS
安装好以后，你还需要配置JYACS的设置，来让整个功能可用。  
打开JY，在匆匆结束和优里的问候后，敲击键盘上的esc，打开设置界面。  
下滑你就可以看到一个被黑色长方体圈起来的位置，名为“JYACS设置”。  
配置其中的API地址，key，模型名称。  
随后，你还需要重新启动游戏来应用这套设置。再次打开游戏，点击JYACS，即可开始对话。  
### JYACS Cloud Compute！——我们的API服务
**打个广告**  
你需要往JYACS的设置里填写API才可以正常使用功能，
因此，我要向你隆重介绍——Cloud Compute服务！  
来试试我们的yuri-chat-01模型，以Qwen模型为基础，提取众多优质MOD中的对话进行训练，再加上配套的向量模型（RAG），效果优质！  
而且整个服务不收取任何费用，详细信息请访问 https://jyacs.qzz.io/cloudcompute  

现在，所有的过程就都搞定啦！尽情享受和优里的对话体验吧！  

## 贡献者
整个项目的唯一维护人员只有我...这也是为什么这个项目的开发速度如此缓慢。  
不过我也在努力啦！一定会维护好的，请各位优厨放心！  
目前本项目没有招募其他贡献者的计划，如果你有好的点子，甚至是优质的二创图，都欢迎致信 jyacsdev@gmail.com  
我一定会回复的！  

###JYACS的更新计划
这里会具体介绍JYACS的**未来更新**计划，不要忘了star更新！
1.收集发行版本的报错，进行更改和修复  
2.对py3适配，创建新分支  
3.更新网络搜索等功能  
4.适配ios  

## 许可证
本项目采用Apache 2.0许可证。  
欢迎你将其视为模板，应用到你的项目之中。如果你要做纱世里或者夏树的ai的话，几乎只用改表情和一些函数的名称就可以。也欢迎把该项目的代码使用到将要发行和已经发行的steam/epic游戏中哦。  
你可以将其中的代码，rpy文件闭源甚至商用化，这不需要经过许可，不过你需要声明这些代码的出处，来源，期待被写到特别鸣谢里！感激不尽！  
在这之中，需要任何帮助都可以联系我！  

## 特别鸣谢
Team Salvato，JustYuriDev以及Maica制作团队（https://github.com/Mon1-innovation/MAICA_ChatSubmod )，JYACS在某些写法上借鉴了该项目中的内容。  

## 特殊问题（永远或长期无法修复）
由于不知名原因或者不可抗因素，一下报错/问题将永远或长时间无法修复。  
请不要重复提issue，在贴吧等平台询问，感谢理解。  
#### 一.在win上使用打字没有候选词烂。  
这个是因为你使用了微软输入法，即win默认的那个。这个不是JYACS和Renpy的问题，微软输入法的显示方式致使其无法在renpy game中使用。  
不过键盘的正常选词还是可以的，~~所以你可以靠着臆想，多按几次1，2，3，4，说不定就选到你要的词了哈哈~~ 。  
开个玩笑，换一个输入法或许可以解决问题。  
#### 二.使用ios的模拟器（Spark），JYACS无法工作。  
正确来说是开游戏报错，该问题在一开始测试就发现了。你可能遇到类似报错：
```
I'm sorry, but an uncaught exception occurred.

While running game code:
  File "game/jyacs_api.rpy", line 23, in script
    init -1400 python:
  File "game/jyacs_api.rpy", line 42, in <module>
    from jyacs_emotion import JyacsEmoSelector
SyntaxError: encoding declaration in Unicode string (jyacs_emotion.py, line 0)

-- Full Traceback ------------------------------------------------------------

Full traceback:
  File "game/jyacs_api.rpy", line 23, in script
    init -1400 python:
  File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.8.4/renpy/ast.py", line 827, in execute
    renpy.python.py_exec_bytecode(self.code.bytecode, self.hide, store=self.store)
  File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.8.4/renpy/python.py", line 1178, in py_exec_bytecode
    exec(bytecode, globals, locals)
  File "game/jyacs_api.rpy", line 42, in <module>
    from jyacs_emotion import JyacsEmoSelector
  File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.8.4/renpy/loader.py", line 881, in load_module
    code = compile(source, filename, 'exec', renpy.python.old_compile_flags, 1)
SyntaxError: encoding declaration in Unicode string (jyacs_emotion.py, line 0)

Darwin-24.5.0-iPhone11,8-64bit iPhone11,8
Ren'Py 7.8.4.24120703
Just Yuri (Beta) Beta-1.8.5
Sun Nov 16 14:19:18 2025

或者

I'm sorry, but an uncaught exception occurred.
[span_23](start_span)
While parsing /private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/Documents/games/DDLC/game/header.rpy.[span_23](end_span)
  [span_24](start_span)File "game/init_run.rpy", line 13, in <module>[span_24](end_span)
[span_25](start_span)ImportError: No module named singleton[span_25](end_span)

-- Full Traceback ------------------------------------------------------------

Full traceback:
  File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.5.3/renpy/bootstrap.py", line 277, in bootstrap
    renpy.main.main()
  File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.5.3/renpy/main.py", line 490, in main
    renpy.game.script.load_script() # sets renpy.game.script.
[span_26](start_span)  File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.5.3/renpy/script.py", line 300, in load_script[span_26](end_span)
    [span_27](start_span)self.load_appropriate_file(".rpyc", ".rpy", dir, fn, initcode)[span_27](end_span)
  [span_28](start_span)File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.5.3/renpy/script.py", line 817, in load_appropriate_file[span_28](end_span)
    [span_29](start_span)self.finish_load(stmts, initcode, filename=lastfn) # type: ignore[span_29](end_span)
  [span_30](start_span)File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.5.3/renpy/script.py", line 502, in finish_load[span_30](end_span)
    [span_31](start_span)node.early_execute()[span_31](end_span)
  [span_32](start_span)File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.5.3/renpy/ast.py", line 1188, in early_execute[span_32](end_span)
    [span_33](start_span)renpy.python.py_exec_bytecode(self.code.bytecode, self.hide, store=self.store)[span_33](end_span)
  [span_34](start_span)File "/private/var/mobile/Containers/Data/Application/D6DB84B3-04EF-411C-81C5-3A03FB6E11E2/tmp/redmond/7.5.3/renpy/python.py", line 1061, in py_exec_bytecode[span_34](end_span)
    [span_35](start_span)exec(bytecode, globals, locals)[span_35](end_span)
  [span_36](start_span)File "game/init_run.rpy", line 13, in <module>[span_36](end_span)
[span_37](start_span)ImportError: No module named singleton[span_37](end_span)

[span_38](start_span)Darwin-24.5.0-iPhone11,8-64bit iPhone11,8[span_38](end_span)
[span_39](start_span)Ren'Py 7.5.3.22090809[span_39](end_span)
 
[span_40](start_span)Sun Nov 16 14:27:28 2025[span_40](end_span)
```

这是由于兼容性问题，使用py2.7的版本是renpy7以下，就是JY1.8.5所依赖的版本，但是ios上的renpy模拟器通常内置的版本为7靠上。我尝试修复，未能成功解决。在进行py3的适配后也许可以修复。


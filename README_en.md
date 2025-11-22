Due to limited manpower, this README file was translated using Bing, and there may be some inaccuracies. Please understand.

# JYACS
Welcome to the JYACS official warehouse! The entire JYACS code is here, and the project will be updated from time to time, depending on the frequency, you can refer to the "Contributors" section to learn about JYACS's update schedule! star for continuous updates.
You can visit https://jyacs.qzz.io for more information, and our Cloud Compute is also there, so we look forward to your visit!

## What is JYACS?
**JYACS** is a submod of DDLC's mod Just Yuri. The AI conversation function is mainly implemented through built-in settings to configure API keys, addresses, model names, and send requests.
JYACS has a deep integration with JustYuri, and it is consistent with it in terms of expressions, settings, etc. For specific technical details, please refer to our technical documentation, which you can find in the root directory or visit our website for quicker understanding.
This project is not affiliated with Team Salvato or JustYuriDev.

## JYACS compatibility issues
This project maintains the same technical specifications as the current latest Chinese version (JY1.8.5), that is, it uses py2.7 writing, although there are many places where py3 is reserved, there may still be problems in the higher version of raw meat, please understand. After the current version is stable, I will create a new branch to adapt to py3's raw meat.
If there is a newer Chinese version, I will adapt it as soon as possible.

In addition, JYACS is not available on ios devices for unknown reasons, specific information can be found below.

## Install!
Installing JYACS is very simple, just like you would install any other submod.
First of all, you need to have a JustYuri ontology, you can get the latest Chinese version in https://forum.monika.love's Mopan resource integration, or in Baidu Tieba's Duoduo Wealth Management Bar. If you need the latest raw meat version, you can join JY's official discord, or you can get the same resources in Baidu Tieba's Youli Bar.
Get all this right and we're good to go. I will try to be as concise and understandable as possible.
1. You also need a file of JYACS, you can get the latest version from Releases in this repository, or go to https://jyacs.qzz.io/versions/ to download it.
2. Unzip the downloaded file... No tutorial is required for this step...
3. Copy all the unzipped files and paste them under the game folder of JY, which should be similar to this path: D:DokiDokiModsJust Yuri1.8.5game
**Succeed with flying colors! **, now that it has been installed, I recommend you to star this project, or don't forget to take a look later, I don't add the function of automatic detection of updates in the game, so you need to come and update it yourself.
The update is necessary because it fixes some known errors and adds some new features. The specific update method is the same as the installation.

## Configure JYACS
Once installed, you will also need to configure the JYACS settings to make the entire functionality available.
Open JY, and after a hurried end to Yuri's greeting, tap esc on the keyboard to open the settings screen.
Scroll down to see a position circled by a black cuboid called "JYACS Settings".
Configure the API address, key, and model name.
You'll then need to restart the game to apply this setting. Open the game again and click JYACS to start a conversation.
### JYACS Cloud Compute！ - Our API service
**Advertise**
You need to fill in the API in the JYACS settings to use the function normally.
So, let me introduce you to Cloud Compute services!
Try our yuri-chat-01 model, based on the Qwen model, extract dialogues from many high-quality mods for training, plus the matching vector model (RAG) for high-quality results!
And there is no charge for the entire service, please visit https://jyacs.qzz.io/cloudcompute for details

Now, all the processes are done! Enjoy your conversation with Yuri!

## Contributors
The only maintainer for the entire project was me... This is why the development of this project was so slow.
But I'm working hard! It will definitely be maintained, please rest assured!
There are currently no plans to recruit other contributors for this project, if you have a good idea, or even a high-quality secondary creation map, please write to jyacsdev@gmail.com
I will definitely reply!

###JYACS update plan
Here we will introduce JYACS's **future update** plan, don't forget the star update!
1. Collect the error report of the release version, make changes and fixes
2. Adapt to py3 and create a new branch
3. Update web search and other functions
4. Adapt to iOS

## License
This project is licensed under the Apache 2.0 license.
You are welcome to use it as a template to apply to your project. If you want to do Saseri or Natsuki's AI, you can almost only change the names of expressions and some functions. You are also welcome to use the project's code in upcoming and existing Steam/Epic games.
You can close source or even commercialize the code, the RPY file, which does not require permission, but you need to declare the source and source of the code, and expect it to be written in a special credit! Appreciate!
In the meantime, you can contact me if you need any help!

## Special thanks
Team Salvato, JustYuriDev, and the Maica production team (https://github.com/Mon1-innovation/MAICA_ChatSubmod), JYACS borrowed from the project in some ways.

## Special Problems (Forever or Forever Unfixable)
Due to unknown reasons or force majeure, the error/problem will never be repaired or for a long time.
Please don't raise the issue repeatedly, ask on platforms such as Tieba and thank you for your understanding.
#### one. There are no candidate words to use typing on win.
This is because you use the Microsoft input method, which is the default one for win. This is not a problem with JYACS and Renpy, the way Microsoft input methods are displayed makes it impossible to use in renpy games.
But the normal word selection of the keyboard is still possible, ~~ So you can rely on your imagination, press 1, 2, 3, 4 a few more times, maybe you will choose the word you want haha~~.
Just kidding, a different input method might solve the problem.
#### II. Using an emulator for ios (Spark), JYACS does not work.
To be precise, it is an error when opening the game, and the problem was discovered at the beginning of the test. You may encounter errors similar to this:  
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
This is due to compatibility issues. The version using Python 2.7 is for Ren'Py 7 and below, which is the version that JY1.8.5 depends on. However, Ren'Py simulators on iOS usually come with a higher version of 7 built-in. I tried to fix it but was unsuccessful. It might be resolved after adapting to Python 3.

screen jyacs_ingame_ui():
    zorder 101
    if not renpy.get_screen("say"):
        textbutton "自由对话":
            action Jump("jyacs_free_talk_loop")
            xalign 0.98
            yalign 0.2
            style "jyacs_purple_button"
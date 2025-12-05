
screen quick_menu():
    # This ensures the button is only shown in-game and not during menus.
    if renpy.get_screen("say"):
        textbutton "自由对话" action Jump("jyacs_free_talk_loop")


init -901 python:
    if not hasattr(store, "registered_submods"):
        store.registered_submods = []
    
    # Add the free chat button as a permanent overlay
    if 'free_chat_overlay' not in config.overlay_screens:
        config.overlay_screens.append('free_chat_overlay')

screen submods_preferences():
    # This screen is designed to be used by the preferences screen.
    # It adds a button for each registered submod.
    vbox:
        for submod in store.registered_submods:
            if submod.get("settings_pane"):
                textbutton submod.get("name", "Unnamed Submod") action Show(submod["settings_pane"])

# This is a common way to add a button to the preferences screen
# It tries to add a "Submods" button that opens the submod list.
screen preferences():
    # Add a vbox to contain the submods button
    vbox:
        # A button to show the submods screen
        textbutton "JYACS AI Chat" action Show("jyacs_settings")
    

screen free_chat_overlay():
    # Position the button at the top-right, slightly offset
    # "右中上部" (right-middle-upper part)
    frame:
        xalign 1.0
        yalign 0.2
        xoffset -20
        yoffset 20
        textbutton _("自由对话"):
            action Call("submod_jyacs_chat_start")

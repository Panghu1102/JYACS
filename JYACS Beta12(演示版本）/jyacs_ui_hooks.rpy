
init -901 python:
    if not hasattr(store, "registered_submods"):
        store.registered_submods = []

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

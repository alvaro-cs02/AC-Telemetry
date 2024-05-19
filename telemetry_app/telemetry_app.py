import ac
import json

config_file = 'config.json'
selected_profile = None

def load_config():
    with open(config_file, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def on_select_profile(*args):
    global app_window, profile_dropdown
    ac.setVisible(main_menu, 0)
    ac.setVisible(select_profile_menu, 1)
    ac.setVisible(modify_profile_menu, 0)
    
    config = load_config()
    ac.clearItems(profile_dropdown)
    for profile in config.keys():
        if profile != 'default':
            ac.addItem(profile_dropdown, profile)

def on_modify_profile(*args):
    global app_window, profile_textbox
    ac.setVisible(main_menu, 0)
    ac.setVisible(select_profile_menu, 0)
    ac.setVisible(modify_profile_menu, 1)
    
    config = load_config()
    ac.setText(profile_textbox, json.dumps(config, indent=4))

def on_profile_selected(index):
    global selected_profile
    selected_profile = ac.getText(profile_dropdown)
    ac.console("Selected profile: ", {selected_profile})
    with open("selected_profile.json", "w") as f:
        json.dump({"selected_profile": selected_profile}, f)

def on_save_profiles(*args):
    config_text = ac.getText(profile_textbox)
    try:
        config = json.loads(config_text)
        save_config(config)
        ac.console("Profiles saved successfully.")
    except json.JSONDecodeError as e:
        ac.console("Error saving profiles: ", {e})

def on_back_to_main(*args):
    ac.setVisible(main_menu, 1)
    ac.setVisible(select_profile_menu, 0)
    ac.setVisible(modify_profile_menu, 0)

app_window = 0
main_menu = 0
select_profile_menu = 0
modify_profile_menu = 0
profile_dropdown = 0
profile_textbox = 0

def acMain(ac_version):
    global app_window, main_menu, select_profile_menu, modify_profile_menu, profile_dropdown, profile_textbox

    app_window = ac.newApp("Telemetry Config")
    ac.setSize(app_window, 400, 600)

    main_menu = ac.addAppWindow(app_window)
    ac.setSize(main_menu, 400, 600)
    
    select_profile_menu = ac.addAppWindow(app_window)
    ac.setSize(select_profile_menu, 400, 600)
    ac.setVisible(select_profile_menu, 0)

    modify_profile_menu = ac.addAppWindow(app_window)
    ac.setSize(modify_profile_menu, 400, 600)
    ac.setVisible(modify_profile_menu, 0)

    # Main Menu
    select_profile_button = ac.addButton(main_menu, "Select Profile")
    ac.setPosition(select_profile_button, 100, 200)
    ac.setSize(select_profile_button, 200, 50)
    ac.addOnClickedListener(select_profile_button, on_select_profile)

    modify_profile_button = ac.addButton(main_menu, "Modify/Create Profile")
    ac.setPosition(modify_profile_button, 100, 300)
    ac.setSize(modify_profile_button, 200, 50)
    ac.addOnClickedListener(modify_profile_button, on_modify_profile)

    # Select Profile Menu
    profile_dropdown = ac.addComboBox(select_profile_menu, "")
    ac.setPosition(profile_dropdown, 100, 200)
    ac.setSize(profile_dropdown, 200, 50)
    ac.addOnValueChangeListener(profile_dropdown, on_profile_selected)

    back_button_select = ac.addButton(select_profile_menu, "Back")
    ac.setPosition(back_button_select, 100, 300)
    ac.setSize(back_button_select, 200, 50)
    ac.addOnClickedListener(back_button_select, on_back_to_main)

    # Modify/Create Profile Menu
    profile_textbox = ac.addTextBox(modify_profile_menu, "")
    ac.setPosition(profile_textbox, 50, 100)
    ac.setSize(profile_textbox, 300, 300)

    save_button = ac.addButton(modify_profile_menu, "Save Profiles")
    ac.setPosition(save_button, 100, 450)
    ac.setSize(save_button, 200, 50)
    ac.addOnClickedListener(save_button, on_save_profiles)

    back_button_modify = ac.addButton(modify_profile_menu, "Back")
    ac.setPosition(back_button_modify, 100, 520)
    ac.setSize(back_button_modify, 200, 50)
    ac.addOnClickedListener(back_button_modify, on_back_to_main)

    return "Telemetry Config"

def acUpdate(deltaT):
    pass

def acShutdown():
    pass

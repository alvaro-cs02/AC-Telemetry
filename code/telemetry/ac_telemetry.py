import ac
import os
import subprocess
import webbrowser
import threading

# Assuming you have a utility module where collect_telemetry and load_config are defined
from telemetry.utils import collect_telemetry, load_config

def acMain(ac_version):
    appWindow = ac.newApp("AC Telemetry")
    ac.setSize(appWindow, 400, 400)

    # Button to start telemetry collection
    startBtn = ac.addButton(appWindow, "Start Telemetry")
    ac.setPosition(startBtn, 30, 30)
    ac.setSize(startBtn, 160, 30)
    ac.addOnClickedListener(startBtn, start_telemetry_thread)

    # Button to stop telemetry collection
    stopBtn = ac.addButton(appWindow, "Stop Telemetry")
    ac.setPosition(stopBtn, 200, 30)
    ac.setSize(stopBtn, 160, 30)
    ac.addOnClickedListener(stopBtn, stop_telemetry_thread)

    # Button to open YAML config in default text editor
    editConfigBtn = ac.addButton(appWindow, "Edit Config")
    ac.setPosition(editConfigBtn, 30, 70)
    ac.setSize(editConfigBtn, 330, 30)
    ac.addOnClickedListener(editConfigBtn, edit_config)

    return "AC Telemetry"

def start_telemetry_thread(*args):
    # Using threading to prevent blocking the UI
    global telemetry_thread
    telemetry_thread = threading.Thread(target=collect_telemetry, args=("racing",))
    telemetry_thread.start()

def stop_telemetry_thread(*args):
    global telemetry_thread
    if telemetry_thread.is_alive():
        telemetry_thread.join()

def edit_config(*args):
    config_path = "path/to/your/code/telemetry/config.yaml"
    os.startfile(config_path)  # This works on Windows, use `subprocess` for cross-platform solutions


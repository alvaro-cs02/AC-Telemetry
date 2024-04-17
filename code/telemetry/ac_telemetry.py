import ac
import os
import subprocess
import webbrowser
import threading

from telemetry.utils import collect_telemetry, load_config

def acMain(ac_version):
    appWindow = ac.newApp("AC Telemetry")
    ac.setSize(appWindow, 400, 400)

    startBtn = ac.addButton(appWindow, "Start Telemetry")
    ac.setPosition(startBtn, 30, 30)
    ac.setSize(startBtn, 160, 30)
    ac.addOnClickedListener(startBtn, start_telemetry_thread)

    stopBtn = ac.addButton(appWindow, "Stop Telemetry")
    ac.setPosition(stopBtn, 200, 30)
    ac.setSize(stopBtn, 160, 30)
    ac.addOnClickedListener(stopBtn, stop_telemetry_thread)

    editConfigBtn = ac.addButton(appWindow, "Edit Config")
    ac.setPosition(editConfigBtn, 30, 70)
    ac.setSize(editConfigBtn, 330, 30)
    ac.addOnClickedListener(editConfigBtn, edit_config)

    return "AC Telemetry"

def start_telemetry_thread(*args):
    global telemetry_thread
    telemetry_thread = threading.Thread(target=collect_telemetry, args=("racing",))
    telemetry_thread.start()

def stop_telemetry_thread(*args):
    global telemetry_thread
    if telemetry_thread.is_alive():
        telemetry_thread.join()

def edit_config(*args):
    config_path = "path/to/your/code/telemetry/config.yaml"
    os.startfile(config_path)


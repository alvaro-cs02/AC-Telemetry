import json
from utils import collect_telemetry, load_config

def start_telemetry_listener():
    with open("selected_profile.json", "r") as f:
        data = json.load(f)
        profile_name = data["selected_profile"]

    config = load_config()
    try:
        interval = config['default']['logging_interval']
    except KeyError as e:
        print(f"Error loading default logging interval: {e}")
        return

    collect_telemetry(profile_name, interval)

if __name__ == "__main__":
    start_telemetry_listener()
from dash import Input, Output, State, callback_context
import yaml
import threading
from app import app, get_config, get_initial_profile
from commons.utils import collect_telemetry
from commons.params import CONFIG_FILE, TELEMETRY_VARIABLES
from datetime import datetime

config = get_config()
initial_profile = get_initial_profile()

@app.callback(
    Output('profile-dropdown', 'options'),
    Output('profile-dropdown', 'value'),
    Output('logging-interval', 'value'),
    Output('variables-checklist-graphic', 'value'),
    Output('variables-checklist-physics', 'value'),
    Output('variables-checklist-static', 'value'),
    Output('new-profile-name', 'style'),
    Output('notification', 'is_open'),
    Output('notification', 'children'),
    Output('active-profile-dropdown', 'options'),
    Input('profile-dropdown', 'value'),
    Input('save-changes', 'n_clicks'),
    Input('add-profile', 'n_clicks'),
    Input('update-interval', 'n_clicks'),
    Input('start-telemetry', 'n_clicks'),
    State('variables-checklist-graphic', 'value'),
    State('variables-checklist-physics', 'value'),
    State('variables-checklist-static', 'value'),
    State('logging-interval', 'value'),
    State('new-profile-name', 'value'),
    State('active-profile-dropdown', 'value'),
    State('metadata-name', 'value'),
    State('file-name', 'value')
)
def update_profile(profile, save_clicks, add_clicks, update_interval_clicks, start_telemetry_clicks, graphic_vars, physics_vars, static_vars, logging_interval, new_profile_name, active_profile, metadata_name, file_name):
    ctx = callback_context
    triggered = [t['prop_id'] for t in ctx.triggered]

    # Initialize notification message
    notification_message = ""
    notification_open = False

    if 'profile-dropdown.value' in triggered:
        # Update profile settings
        if profile in config['profiles']:
            variables = config['profiles'][profile]
            graphic_vars = [var for var in variables if var in [v['name'] for v in TELEMETRY_VARIABLES['graphic_info']['variables']]]
            physics_vars = [var for var in variables if var in [v['name'] for v in TELEMETRY_VARIABLES['physics_info']['variables']]]
            static_vars = [var for var in variables if var in [v['name'] for v in TELEMETRY_VARIABLES['static_info']['variables']]]
            logging_interval = config['default']['logging_interval']
        return (
            [{'label': k, 'value': k} for k in config['profiles'].keys()],
            profile,
            logging_interval,
            graphic_vars,
            physics_vars,
            static_vars,
            {'display': 'none'},
            notification_open,
            notification_message,
            [{'label': k, 'value': k} for k in config['profiles'].keys()]
        )

    if 'save-changes.n_clicks' in triggered:
        # Save changes to the selected profile
        config['profiles'][profile] = graphic_vars + physics_vars + static_vars

        with open(CONFIG_FILE, 'w') as file:
            yaml.dump(config, file)

        notification_message = "Profile changes saved successfully!"
        notification_open = True

    if 'update-interval.n_clicks' in triggered:
        # Update logging interval
        config['default']['logging_interval'] = logging_interval

        with open(CONFIG_FILE, 'w') as file:
            yaml.dump(config, file)

        notification_message = "Logging interval updated successfully!"
        notification_open = True

    if 'add-profile.n_clicks' in triggered:
        # Show input for new profile name
        return (
            [{'label': k, 'value': k} for k in config['profiles'].keys()],
            profile,
            logging_interval,
            graphic_vars,
            physics_vars,
            static_vars,
            {'display': 'block', 'margin-top': '10px'},
            notification_open,
            notification_message,
            [{'label': k, 'value': k} for k in config['profiles'].keys()]
        )

    if new_profile_name and 'save-changes.n_clicks' in triggered:
        # Add new profile
        if new_profile_name in config['profiles']:
            notification_message = "Profile already exists!"
            notification_open = True
        else:
            config['profiles'][new_profile_name] = graphic_vars + physics_vars + static_vars
            profile = new_profile_name

            with open(CONFIG_FILE, 'w') as file:
                yaml.dump(config, file)

            notification_message = "New profile created successfully!"
            notification_open = True

        return (
            [{'label': k, 'value': k} for k in config['profiles'].keys()],
            profile,
            logging_interval,
            graphic_vars,
            physics_vars,
            static_vars,
            {'display': 'none'},
            notification_open,
            notification_message,
            [{'label': k, 'value': k} for k in config['profiles'].keys()]
        )

    if 'start-telemetry.n_clicks' in triggered:
        # Start telemetry collection in a separate thread
        if file_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            full_file_name = f"{file_name}_{timestamp}.csv"
        else:
            full_file_name = f"telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        metadata = {
            "name": metadata_name
        }

        thread = threading.Thread(target=collect_telemetry, args=(active_profile, logging_interval, full_file_name, metadata))
        thread.start()
        notification_message = f"Started telemetry collection for profile '{active_profile}' with interval {logging_interval}."
        notification_open = True

    # Default return
    return (
        [{'label': k, 'value': k} for k in config['profiles'].keys()],
        profile,
        logging_interval,
        graphic_vars,
        physics_vars,
        static_vars,
        {'display': 'none'},
        notification_open,
        notification_message,
        [{'label': k, 'value': k} for k in config['profiles'].keys()]
    )

from dash import Input, Output, State, callback_context, ALL, MATCH, callback_context
import yaml
import threading
import plotly.graph_objects as go
from app import app, get_config, get_initial_profile, get_telemetry_files
from commons.utils import collect_telemetry
from commons.params import CONFIG_FILE, TELEMETRY_VARIABLES, LOG_DIR
from datetime import datetime
import os
from dash.exceptions import PreventUpdate
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import pandas as pd
import dash
import json

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

@app.callback(
    Output('file-list', 'children'),
    [Input('search-box', 'value'), Input('selected-file', 'data')]
)
def update_file_list(search_value, selected_file):
    files = get_telemetry_files()
    if search_value:
        files = [file for file in files if search_value.lower() in file['label'].lower()]
    return [
        dbc.ListGroupItem(
            file['label'], 
            id={'type': 'file-item', 'index': file['value']},
            action=True, 
            active=(file['value'] == selected_file)
        )
        for file in files
    ]
    
import re
@app.callback(
    Output('selected-file', 'data'),
    [Input({'type': 'file-item', 'index': ALL}, 'n_clicks')],
    [State({'type': 'file-item', 'index': ALL}, 'id')]
)
def store_selected_file(n_clicks, file_ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return None  # No file has been clicked yet, do nothing.

    clicked_id_str = ctx.triggered[0]['prop_id'].split('.')[0]  # Get the string ID from prop_id.

    # Print the clicked_id_str to understand its format
    print("Clicked ID String:", clicked_id_str)
    
    # Ensure the clicked_id_str is properly closed
    if not clicked_id_str.endswith('"}'):
        clicked_id_str += '"}'
    
    try:
        # Extract the index using regex
        match = re.search(r'index":"(.+?)"', clicked_id_str)
        if match:
            clicked_index = match.group(1)
            if not clicked_index.endswith('.csv'):
                clicked_index += '.csv'
            print("Clicked File Index:", clicked_index)
            return clicked_index
        else:
            print("No match found for clicked ID")
            return None
    except Exception as e:
        print(f"Error parsing clicked_id_str: {e}")
        return None

@app.callback(
    Output('dashboard', 'children'),
    [Input('load-data', 'n_clicks')],
    [State('selected-file', 'data')]
)
def update_dashboard(n_clicks, selected_file):
    if n_clicks is None or selected_file is None:
        return html.H4("No file selected or click not registered", className="text-center mt-4")

    file_path = os.path.join(LOG_DIR, selected_file)
    print("Loading file from path:", file_path)
    if not os.path.exists(file_path):
        return html.H4(f"File not found: {file_path}", className="text-center mt-4")

    try:
        # Skip initial comment lines (lines starting with '#')
        data = pd.read_csv(file_path, comment='#')
    except pd.errors.ParserError as e:
        print(f"Error parsing file: {e}")
        return html.H4(f"Error parsing file: {file_path}", className="text-center mt-4")
    
    required_columns = ['timestamp', 'speedKmh', 'rpms', 'gear']
    if not all(column in data.columns for column in required_columns):
        return html.H4("Required data not found in file", className="text-center mt-4")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['speedKmh'], mode='lines', name='Speed'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['rpms'], mode='lines', name='RPMs'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['gear'], mode='lines', name='Gear'))
    fig.update_layout(title=f"Data for {selected_file}", xaxis_title='Time', yaxis_title='Value', legend_title='Metric')
    return dcc.Graph(id='telemetry-plot', figure=fig)
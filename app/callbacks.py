from dash import Input, Output, State, callback_context, ALL
import yaml
import threading
import plotly.graph_objects as go
from app import app, get_config, get_initial_profile, get_telemetry_files
from commons.utils import collect_telemetry
from plotly.subplots import make_subplots
from commons.params import CONFIG_FILE, TELEMETRY_VARIABLES, LOG_DIR
from datetime import datetime
import os
import re
from dash.exceptions import PreventUpdate
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import pandas as pd
import dash
import json

config = get_config()
initial_profile = get_initial_profile()

# Initialize stop_event and thread reference
stop_event = threading.Event()
telemetry_thread = None

def stop_telemetry():
    global stop_event, telemetry_thread
    if telemetry_thread and telemetry_thread.is_alive():
        stop_event.set()  # Signal the thread to stop
        telemetry_thread.join()  # Wait for the thread to finish
        print("Telemetry stopped")

@app.callback(
    Output('profile-dropdown', 'options'),
    Output('profile-dropdown', 'value'),
    Output('logging-interval', 'value'),
    Output('variables-checklist-graphic', 'value'),
    Output('variables-checklist-physics', 'value'),
    Output('variables-checklist-static', 'value'),
    Output('new-profile-name', 'style'),
    Output('active-profile-dropdown', 'options'),
    Input('profile-dropdown', 'value'),
    Input('save-changes', 'n_clicks'),
    Input('add-profile', 'n_clicks'),
    Input('update-interval', 'n_clicks'),
    State('variables-checklist-graphic', 'value'),
    State('variables-checklist-physics', 'value'),
    State('variables-checklist-static', 'value'),
    State('logging-interval', 'value'),
    State('new-profile-name', 'value'),
    State('metadata-name', 'value'),
    State('metadata-length', 'value'),
    State('file-name', 'value')
)
def update_profile(profile, save_clicks, add_clicks, update_interval_clicks, graphic_vars, physics_vars, static_vars, logging_interval, new_profile_name, metadata_name, metadata_length, file_name):
    ctx = callback_context
    triggered = [t['prop_id'] for t in ctx.triggered]

    notification_message = ""
    notification_open = False

    if 'profile-dropdown.value' in triggered:
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
            [{'label': k, 'value': k} for k in config['profiles'].keys()]
        )

    if 'save-changes.n_clicks' in triggered:
        config['profiles'][profile] = graphic_vars + physics_vars + static_vars

        with open(CONFIG_FILE, 'w') as file:
            yaml.dump(config, file)

        notification_message = "Profile changes saved successfully!"
        notification_open = True

    if 'update-interval.n_clicks' in triggered:
        config['default']['logging_interval'] = logging_interval

        with open(CONFIG_FILE, 'w') as file:
            yaml.dump(config, file)

        notification_message = "Logging interval updated successfully!"
        notification_open = True

    if 'add-profile.n_clicks' in triggered:
        return (
            [{'label': k, 'value': k} for k in config['profiles'].keys()],
            profile,
            logging_interval,
            graphic_vars,
            physics_vars,
            static_vars,
            {'display': 'block', 'margin-top': '10px'},
            [{'label': k, 'value': k} for k in config['profiles'].keys()]
        )

    if new_profile_name and 'save-changes.n_clicks' in triggered:
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
            [{'label': k, 'value': k} for k in config['profiles'].keys()]
        )

    return (
        [{'label': k, 'value': k} for k in config['profiles'].keys()],
        profile,
        logging_interval,
        graphic_vars,
        physics_vars,
        static_vars,
        {'display': 'none'},
        [{'label': k, 'value': k} for k in config['profiles'].keys()]
    )

@app.callback(
    Output('start-telemetry', 'style'),
    Output('stop-telemetry', 'style'),
    Output('telemetry-active', 'data'),
    Output('notification', 'is_open'),
    Output('notification', 'children'),
    Input('start-telemetry', 'n_clicks'),
    Input('stop-telemetry', 'n_clicks'),
    State('active-profile-dropdown', 'value'),
    State('logging-interval', 'value'),
    State('metadata-name', 'value'),
    State('metadata-length', 'value'),
    State('file-name', 'value'),
    State('telemetry-active', 'data')
)
def toggle_telemetry(start_clicks, stop_clicks, active_profile, logging_interval, metadata_name, metadata_length, file_name, telemetry_active):
    global stop_event, telemetry_thread
    ctx = callback_context
    triggered = [t['prop_id'] for t in ctx.triggered]
    notification_message = ""
    notification_open = False

    if 'start-telemetry.n_clicks' in triggered:
        if telemetry_active:
            notification_message = "Telemetry is already running!"
        else:
            stop_telemetry()  # Ensure any previous telemetry is stopped
            stop_event.clear()  # Reset the stop event for the new thread

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            full_file_name = f"{file_name}_{timestamp}.csv" if file_name else f"telemetry_{timestamp}.csv"
            metadata = {"name": metadata_name, "length": metadata_length}

            telemetry_thread = threading.Thread(target=collect_telemetry, args=(active_profile, logging_interval, full_file_name, metadata, stop_event))
            telemetry_thread.start()
            telemetry_active = True
            notification_message = f"Started telemetry collection for profile '{active_profile}' with interval {logging_interval}."
            notification_open = True

    elif 'stop-telemetry.n_clicks' in triggered:
        if not telemetry_active:
            notification_message = "Telemetry is not running!"
        else:
            stop_telemetry()
            telemetry_active = False
            notification_message = "Telemetry stopped."
            notification_open = True

    return (
        {'display': 'none'} if telemetry_active else {'display': 'block'},
        {'display': 'block'} if telemetry_active else {'display': 'none'},
        telemetry_active,
        notification_open,
        notification_message
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

@app.callback(
    Output('selected-file', 'data'),
    [Input({'type': 'file-item', 'index': ALL}, 'n_clicks')],
    [State({'type': 'file-item', 'index': ALL}, 'id')]
)
def store_selected_file(n_clicks, file_ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    clicked_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Clicked ID String:", clicked_id_str)
    if not clicked_id_str.endswith('"}'):
        clicked_id_str += '"}'
    try:
        match = re.search(r'index":"(.+?)"', clicked_id_str)
        if match:
            clicked_index = match.group(1)
            if not clicked_index.endswith('.csv'):
                clicked_index += '.csv'
            print("Clicked File Index:", clicked_index)
            return clicked_index
    except Exception as e:
        print(f"Error parsing clicked_id_str: {e}")
        return None
    
@app.callback(
    Output('dashboard', 'children'),
    Output('dashboard-options', 'style'),
    Output('file-loaded', 'data'),
    Input('load-data', 'n_clicks'),
    Input('apply-filters', 'n_clicks'),
    State('selected-file', 'data'),
    State('start-range', 'value'),
    State('end-range', 'value')
)
def update_dashboard(load_clicks, apply_clicks, selected_file, start_range, end_range):
    if not selected_file:
        return html.H4("No file selected or click not registered", className="text-center mt-4"), {'display': 'none'}, False

    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'load-data' and load_clicks == 0:
        return html.H4("No file selected or click not registered", className="text-center mt-4"), {'display': 'none'}, False

    file_path = os.path.join(LOG_DIR, selected_file)
    if not os.path.exists(file_path):
        return html.H4(f"File not found: {file_path}", className="text-center mt-4"), {'display': 'none'}, False

    # Inicializar variables
    track_length = None
    data = None

    try:
        # Leer el archivo y extraer metadatos
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('#'):
                    # Extraer trackLength de los metadatos
                    match = re.search(r'# Length: (\d+)', line)
                    if match:
                        track_length = int(match.group(1))
                else:
                    break
        
        # Cargar los datos, saltando las líneas de comentarios
        data = pd.read_csv(file_path, comment='#')

    except Exception as e:
        print(f"Error processing file: {e}")
        return html.H4(f"Error processing file: {file_path}", className="text-center mt-4"), {'display': 'none'}, False
    
    if track_length is None or 'normalizedCarPosition' not in data.columns:
        return html.H4("Required data not found in file", className="text-center mt-4"), {'display': 'none'}, False

    # Filtrar datos por rango si es aplicable
    if start_range is not None and end_range is not None:
        start_norm = start_range / track_length
        end_norm = end_range / track_length
        data = data[(data['normalizedCarPosition'] >= start_norm) & (data['normalizedCarPosition'] <= end_norm)]

    # Crear subgráficos
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Speed", "Brake and Gas")
    )

    # Añadir trazas para velocidad
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['speedKmh'], mode='lines', name='Speed'), row=1, col=1)
    # Añadir trazas para brake y gas
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['brake'], mode='lines', name='Brake'), row=2, col=1)
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['gas'], mode='lines', name='Gas'), row=2, col=1)
    
    fig.update_layout(height=800, title_text=f"Data for {selected_file}", xaxis_title='Time', yaxis_title='Value', legend_title='Metric')
    return dcc.Graph(id='telemetry-plot', figure=fig), {'display': 'block'}, True


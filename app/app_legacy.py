import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import yaml
import threading
from commons.params import *
from commons.utils import collect_telemetry
from datetime import datetime
import csv
import time
import os

with open(CONFIG_FILE, 'r') as file:
    config = yaml.safe_load(file)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

initial_profile = list(config['profiles'].keys())[0]

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Telemetry Profile Manager"), className="mb-4 mt-4")
        ]),
        dbc.Row([
            dbc.Col([
                html.H5("Select Profile"),
                dcc.Dropdown(
                    id='profile-dropdown',
                    options=[{'label': k, 'value': k} for k in config['profiles'].keys()],
                    value=initial_profile,
                    clearable=False
                ),
                dbc.Button("Create New Profile", id="add-profile", className="mt-2", color="primary"),
                dcc.Input(id='new-profile-name', type='text', placeholder='New Profile Name', style={'display': 'none'}),
            ]),
            dbc.Col([
                html.H5("Logging Interval"),
                dcc.Input(id='logging-interval', type='number', value=config['default']['logging_interval'], step=0.1),
                dbc.Button("Update Interval", id="update-interval", color="secondary", className="mt-2")
            ])
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.H5("Telemetry Variables"),
                html.Div([
                    dcc.Checklist(
                        id='variables-checklist',
                        options=[
                            {'label': html.Span([html.B(var['name']), f" - {var['description']}"]), 'value': var['name']}
                            for section in TELEMETRY_VARIABLES.values()
                            for var in section['variables']
                        ],
                        value=config['profiles'][initial_profile],
                        style={'overflowY': 'scroll', 'maxHeight': '400px', 'border': '1px solid #ccc', 'padding': '10px'}
                    )
                ], style={'height': '450px', 'overflowY': 'auto', 'border': '1px solid #ccc', 'border-radius': '5px', 'padding': '10px'})
            ])
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Save Profile Changes", id='save-changes', color="success"), className="mt-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5("Select Active Profile for Telemetry"), className="mt-4"),
            dbc.Col([
                dcc.Dropdown(
                    id='active-profile-dropdown',
                    options=[{'label': k, 'value': k} for k in config['profiles'].keys()],
                    value=initial_profile,
                    clearable=False
                )
            ]),
            dbc.Col(dbc.Button("Start Telemetry", id='start-telemetry', color="success"), className="mt-4")
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.H5("Metadata"),
                dcc.Input(id='metadata-name', type='text', placeholder='Driver name', className="mb-2"),
                dcc.Input(id='metadata-car', type='text', placeholder='Car', className="mb-2"),
                dcc.Input(id='metadata-map', type='text', placeholder='Map', className="mb-2"),
                dcc.Input(id='file-name', type='text', placeholder='File Name', className="mb-2"),
            ])
        ]),
        dbc.Toast(
            id="notification",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000,
            icon="info",
        )
    ], className="mt-5")
])

@app.callback(
    Output('profile-dropdown', 'options'),
    Output('profile-dropdown', 'value'),
    Output('logging-interval', 'value'),
    Output('variables-checklist', 'value'),
    Output('new-profile-name', 'style'),
    Output('notification', 'is_open'),
    Output('notification', 'children'),
    Output('active-profile-dropdown', 'options'),
    Input('profile-dropdown', 'value'),
    Input('save-changes', 'n_clicks'),
    Input('add-profile', 'n_clicks'),
    Input('update-interval', 'n_clicks'),
    Input('start-telemetry', 'n_clicks'),
    State('variables-checklist', 'value'),
    State('logging-interval', 'value'),
    State('new-profile-name', 'value'),
    State('active-profile-dropdown', 'value'),
    State('metadata-name', 'value'),
    State('metadata-car', 'value'),
    State('metadata-map', 'value'),
    State('file-name', 'value')
)
def update_profile(profile, save_clicks, add_clicks, update_interval_clicks, start_telemetry_clicks, variables, logging_interval, new_profile_name, active_profile, metadata_name, metadata_car, metadata_map, file_name):
    ctx = callback_context
    triggered = [t['prop_id'] for t in ctx.triggered]

    # Initialize notification message
    notification_message = ""
    notification_open = False

    if 'profile-dropdown.value' in triggered:
        # Update profile settings
        if profile in config['profiles']:
            variables = config['profiles'][profile]
            logging_interval = config['default']['logging_interval']
        return (
            [{'label': k, 'value': k} for k in config['profiles'].keys()],
            profile,
            logging_interval,
            variables,
            {'display': 'none'},
            notification_open,
            notification_message,
            [{'label': k, 'value': k} for k in config['profiles'].keys()]
        )
    
    if 'save-changes.n_clicks' in triggered:
        # Save changes to the selected profile
        config['profiles'][profile] = variables

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
            variables,
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
            config['profiles'][new_profile_name] = variables
            profile = new_profile_name

            with open(CONFIG_FILE, 'w') as file:
                yaml.dump(config, file)

            notification_message = "New profile created successfully!"
            notification_open = True

        return (
            [{'label': k, 'value': k} for k in config['profiles'].keys()],
            profile,
            logging_interval,
            variables,
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
            "name": metadata_name,
            "car": metadata_car,
            "map": metadata_map
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
        variables,
        {'display': 'none'},
        notification_open,
        notification_message,
        [{'label': k, 'value': k} for k in config['profiles'].keys()]
    )

if __name__ == '__main__':
    app.run_server(debug=True)
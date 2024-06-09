from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from app import get_config, get_initial_profile
from commons.params import TELEMETRY_VARIABLES

config = get_config()
initial_profile = get_initial_profile()

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Telemetry Profile Manager"), className="mb-4 mt-4")
        ]),
        dbc.Row([
            dbc.Col(html.A("Files", href="/files", className="float-right"), width={"size": 1, "order": "last"}),
            dbc.Col(html.H5("Select Profile"), width={"size": 11}),
            dbc.Col([
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

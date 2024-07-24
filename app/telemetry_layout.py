from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from app import get_config, get_initial_profile
from commons.params import TELEMETRY_VARIABLES

config = get_config()
initial_profile = get_initial_profile()

main_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Telemetry Profile Manager"), className="text-center mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Profile Management", className="card-title"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Select Profile"),
                                dcc.Dropdown(
                                    id='profile-dropdown',
                                    options=[{'label': k, 'value': k} for k in config['profiles'].keys()],
                                    value=initial_profile,
                                    clearable=False
                                ),
                            ], width=6),
                            dbc.Col([
                                dbc.Button("Create New Profile", id="add-profile", color="primary", className="mt-4 w-100"),
                                dcc.Input(id='new-profile-name', type='text', placeholder='New Profile Name', className="mt-3", style={'display': 'none'}),
                            ], width=6)
                        ]),
                        html.H5("Telemetry Variables", className="mt-4"),
                        html.Div([
                            html.H6("Graphic Info"),
                            dcc.Checklist(
                                id='variables-checklist-graphic',
                                options=[
                                    {'label': html.Span([html.B(var['name']), f" - {var['description']}"]), 'value': var['name']}
                                    for var in TELEMETRY_VARIABLES['graphic_info']['variables']
                                ],
                                value=[var['name'] for var in TELEMETRY_VARIABLES['graphic_info']['variables'] if var['name'] in config['profiles'][initial_profile]],
                                style={'overflowY': 'scroll', 'maxHeight': '150px', 'border': '1px solid #ccc', 'padding': '10px', 'marginBottom': '10px'}
                            ),
                            html.H6("Physics Info"),
                            dcc.Checklist(
                                id='variables-checklist-physics',
                                options=[
                                    {'label': html.Span([html.B(var['name']), f" - {var['description']}"]), 'value': var['name']}
                                    for var in TELEMETRY_VARIABLES['physics_info']['variables']
                                ],
                                value=[var['name'] for var in TELEMETRY_VARIABLES['physics_info']['variables'] if var['name'] in config['profiles'][initial_profile]],
                                style={'overflowY': 'scroll', 'maxHeight': '150px', 'border': '1px solid #ccc', 'padding': '10px', 'marginBottom': '10px'}
                            ),
                            html.H6("Static Info"),
                            dcc.Checklist(
                                id='variables-checklist-static',
                                options=[
                                    {'label': html.Span([html.B(var['name']), f" - {var['description']}"]), 'value': var['name']}
                                    for var in TELEMETRY_VARIABLES['static_info']['variables']
                                ],
                                value=[var['name'] for var in TELEMETRY_VARIABLES['static_info']['variables'] if var['name'] in config['profiles'][initial_profile]],
                                style={'overflowY': 'scroll', 'maxHeight': '150px', 'border': '1px solid #ccc', 'padding': '10px'}
                            )
                        ], style={'height': '500px', 'overflowY': 'auto', 'border': '1px solid #ccc', 'border-radius': '5px', 'padding': '10px'}),
                        dbc.Button("Save Profile Changes", id='save-changes', color="success", className="mt-4 w-100")
                    ])
                ], className="mb-4")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Telemetry Control", className="card-title"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Logging Interval"),
                                dcc.Input(id='logging-interval', type='number', value=config['default']['logging_interval'], step=0.1, className="mb-2 w-100"),
                                dbc.Button("Update Interval", id="update-interval", color="secondary", className="mt-2 w-100"),
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Select Active Profile"),
                                dcc.Dropdown(
                                    id='active-profile-dropdown',
                                    options=[{'label': k, 'value': k} for k in config['profiles'].keys()],
                                    value=initial_profile,
                                    clearable=False,
                                    className="mb-2 w-100"
                                ),
                                dbc.Button("Start Telemetry", id='start-telemetry', color="success", className="mt-2 w-100")
                            ], width=6)
                        ]),
                        html.H5("Metadata", className="mt-4"),
                        dcc.Input(id='metadata-name', type='text', placeholder='Driver name', className="mb-2 w-100"),
                        dcc.Input(id='file-name', type='text', placeholder='File Name', className="mb-2 w-100")
                    ])
                ], className="mb-4")
            ])
        ]),
        dbc.Row([
            dbc.Col(html.A("Visualization", href="/visualization", className="mt-4 d-block text-center"))
        ]),
        dbc.Toast(
            id="notification",
            header="Notification",
            is_open=False,
            dismissable=True,
            duration=4000,
            icon="info",
        )
    ], fluid=False)
])
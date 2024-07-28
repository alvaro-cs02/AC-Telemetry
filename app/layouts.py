from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from app import get_config, get_initial_profile, get_telemetry_files
from commons.params import TELEMETRY_VARIABLES

config = get_config()
initial_profile = get_initial_profile()

main_layout = html.Div([
    dcc.Store(id='telemetry-active', data=False),  # Store to track telemetry state
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
                                dbc.Button("Start Telemetry", id='start-telemetry', color="success", className="mt-2 w-100"),
                                dbc.Button("Stop Telemetry", id='stop-telemetry', color="danger", className="mt-2 w-100", style={'display': 'none'})
                            ], width=6)
                        ]),
                        html.H5("Metadata", className="mt-4"),
                        dcc.Input(id='metadata-name', type='text', placeholder='Driver name', className="mb-2 w-100"),
                        dcc.Input(id='metadata-length', type='number', placeholder='Track\'s length (m)', className="mb-2 w-100", min=0),
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

visualization_layout = html.Div([
    dcc.Store(id='telemetry-active', data=False),
    dcc.Store(id='selected-file', storage_type='memory'),
    dcc.Store(id='file-loaded', data=False),
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Telemetry Data Visualization"), className="text-center mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Select Telemetry File", className="card-title"),
                        dbc.Input(id="search-box", placeholder="Search by name or metadata...", type="text", className="mb-3"),
                        dbc.ListGroup(
                            id='file-list',
                            children=[
                                dbc.ListGroupItem(file['label'], id={'type': 'file-item', 'index': file['value']}, action=True)
                                for file in get_telemetry_files()
                            ],
                            style={'overflowY': 'scroll', 'maxHeight': 'calc(100vh - 200px)'}
                        ),
                        dbc.Button("Load Data", id='load-data', color="primary", className="mt-2 w-100", n_clicks=0)
                    ])
                ], className="mb-4", style={'height': '100vh'})
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id='dashboard-options', style={'display': 'none'}, children=[
                            html.H4("Data Range and Display Options", className="card-title"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Start Range (m)"),
                                    dcc.Input(id='start-range', type='number', placeholder='Start (m)', min=0, className="mb-2 w-100"),
                                ], width=6),
                                dbc.Col([
                                    dbc.Label("End Range (m)"),
                                    dcc.Input(id='end-range', type='number', placeholder='End (m)', min=0, className="mb-2 w-100"),
                                ], width=6)
                            ]),
                            dbc.Checklist(
                                id='display-options',
                                options=[
                                    {'label': 'Show All Laps', 'value': 'all_laps'},
                                    {'label': 'Show Average', 'value': 'average'}
                                ],
                                value=['all_laps'],  # Default option
                                inline=True
                            ),
                            dbc.Button("Apply Filters", id='apply-filters', color="primary", className="mt-2 w-100", n_clicks=0)
                        ]),
                        html.Div(id='dashboard', children=[
                            html.H4("Dashboard will be here", className="text-center mt-4")
                        ])
                    ])
                ], className="mb-4")
            ], width=10)
        ])
    ], fluid=True)
])
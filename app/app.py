import dash
import dash_bootstrap_components as dbc
import yaml
import os
from dash import dcc, html, Input, Output

from commons.params import CONFIG_FILE, LOG_DIR

with open(CONFIG_FILE, 'r') as file:
    config = yaml.safe_load(file)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

initial_profile = list(config['profiles'].keys())[0]

# Export config and initial profile for use in other modules
def get_config():
    return config

def get_initial_profile():
    return initial_profile

def get_telemetry_files():
    files = os.listdir(LOG_DIR)
    return [{'label': file, 'value': file} for file in files if file.endswith('.csv')]

from layouts import main_layout, visualization_layout

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], fluid=True)

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/visualization':
        return visualization_layout
    else:
        return main_layout

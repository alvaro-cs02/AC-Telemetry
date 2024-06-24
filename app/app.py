import dash
import dash_bootstrap_components as dbc
import yaml
import os

from commons.params import CONFIG_FILE

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

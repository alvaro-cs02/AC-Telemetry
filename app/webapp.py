from dash import Dash, html, dcc, Input, Output, State, ctx
import yaml
from commons.params import *

app = Dash(__name__, suppress_callback_exceptions=True)

# Load existing profiles
def load_profiles():
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def save_profiles(profiles):
    with open(CONFIG_FILE, 'w') as f:
        yaml.safe_dump(profiles, f)

app.layout = html.Div([
    html.H1('Telemetry Profile Manager'),
    dcc.Dropdown(id='profile-dropdown', placeholder='Select a profile'),
    html.Button('Create Profile', id='create-profile-button'),
    html.Button('Edit Profile', id='edit-profile-button'),
    html.Div(id='profile-details'),
    html.Div(id='profile-edit'),
    dcc.Store(id='profiles-data', data=load_profiles())
])

@app.callback(
    Output('profile-dropdown', 'options'),
    Input('profiles-data', 'data')
)
def update_profile_dropdown(profiles):
    return [{'label': key, 'value': key} for key in profiles['profiles'].keys()]

@app.callback(
    Output('profile-details', 'children'),
    Input('profile-dropdown', 'value'),
    State('profiles-data', 'data')
)
def display_profile_details(selected_profile, profiles):
    if selected_profile:
        profile = profiles['profiles'][selected_profile]
        return html.Pre(yaml.safe_dump(profile, default_flow_style=False))
    return html.Div()

@app.callback(
    Output('profile-edit', 'children'),
    Input('create-profile-button', 'n_clicks'),
    Input('edit-profile-button', 'n_clicks'),
    State('profile-dropdown', 'value'),
    State('profiles-data', 'data'),
    prevent_initial_call=True
)
def create_or_edit_profile(create_clicks, edit_clicks, selected_profile, profiles):
    triggered_id = ctx.triggered_id
    if triggered_id == 'create-profile-button':
        return html.Div([
            html.H3('Create New Profile'),
            dcc.Input(id='new-profile-name', placeholder='Enter profile name'),
            html.H4('Select Variables:'),
            html.Div([
                html.H5('Graphic Info'),
                dcc.Checklist(
                    options=[{'label': f"{var['name']} - {var['description']}", 'value': var['name']} for var in TELEMETRY_VARIABLES['graphic_info']['variables']],
                    id='graphic-info-vars'
                ),
                html.H5('Physics Info'),
                dcc.Checklist(
                    options=[{'label': f"{var['name']} - {var['description']}", 'value': var['name']} for var in TELEMETRY_VARIABLES['physics_info']['variables']],
                    id='physics-info-vars'
                ),
                html.H5('Static Info'),
                dcc.Checklist(
                    options=[{'label': f"{var['name']} - {var['description']}", 'value': var['name']} for var in TELEMETRY_VARIABLES['static_info']['variables']],
                    id='static-info-vars'
                ),
            ]),
            html.Button('Save', id='save-profile-button')
        ])
    elif triggered_id == 'edit-profile-button' and selected_profile:
        profile = profiles['profiles'][selected_profile]
        return html.Div([
            html.H3(f'Editing {selected_profile}'),
            html.H4('Select Variables:'),
            html.Div([
                html.H5('Graphic Info'),
                dcc.Checklist(
                    options=[{'label': f"{var['name']} - {var['description']}", 'value': var['name']} for var in TELEMETRY_VARIABLES['graphic_info']['variables']],
                    id='edit-graphic-info-vars',
                    value=[var for var in profile if var in [v['name'] for v in TELEMETRY_VARIABLES['graphic_info']['variables']]]
                ),
                html.H5('Physics Info'),
                dcc.Checklist(
                    options=[{'label': f"{var['name']} - {var['description']}", 'value': var['name']} for var in TELEMETRY_VARIABLES['physics_info']['variables']],
                    id='edit-physics-info-vars',
                    value=[var for var in profile if var in [v['name'] for v in TELEMETRY_VARIABLES['physics_info']['variables']]]
                ),
                html.H5('Static Info'),
                dcc.Checklist(
                    options=[{'label': f"{var['name']} - {var['description']}", 'value': var['name']} for var in TELEMETRY_VARIABLES['static_info']['variables']],
                    id='edit-static-info-vars',
                    value=[var for var in profile if var in [v['name'] for v in TELEMETRY_VARIABLES['static_info']['variables']]]
                ),
            ]),
            html.Button('Save', id='save-profile-button')
        ])
    return html.Div()

@app.callback(
    Output('profiles-data', 'data'),
    Input('save-profile-button', 'n_clicks'),
    State('new-profile-name', 'value'),
    State('profile-dropdown', 'value'),
    State('graphic-info-vars', 'value'),
    State('physics-info-vars', 'value'),
    State('static-info-vars', 'value'),
    State('edit-graphic-info-vars', 'value'),
    State('edit-physics-info-vars', 'value'),
    State('edit-static-info-vars', 'value'),
    State('profiles-data', 'data'),
    prevent_initial_call=True
)
def save_profile(n_clicks, new_profile_name, selected_profile, new_graphic_vars, new_physics_vars, new_static_vars, edit_graphic_vars, edit_physics_vars, edit_static_vars, profiles):
    if new_profile_name:
        profiles['profiles'][new_profile_name] = (new_graphic_vars or []) + (new_physics_vars or []) + (new_static_vars or [])
    elif selected_profile:
        profiles['profiles'][selected_profile] = (edit_graphic_vars or []) + (edit_physics_vars or []) + (edit_static_vars or [])
    save_profiles(profiles)
    return profiles

if __name__ == '__main__':
    app.run_server(debug=True)

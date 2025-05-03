from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from settings import get_value, load_ui_state, persist_dict, persist_value


def create_input(label, id, value, step=None):
    
    return html.Div(
        [
            html.Label(label),
            dcc.Input(
                id=id,
                type="number",
                value=get_value(id, value),
                step=step,
                style={"width": "100%"},
                persistence=id,
                persistence_type="local",
            ),
            html.Br(),
            html.Br(),
        ]
    )
    
    


def create_slider(label, id, min_val, max_val, step, value):
    return html.Div(
        [
            html.Label(label),
            dcc.Slider(
                id=id,
                min=min_val,
                max=max_val,
                step=step,
                value=get_value(id, value),
                marks={
                    i: f"{i}%"
                    for i in range(
                        int(min_val), int(max_val) + 1, int((max_val - min_val) / 5)
                    )
                },
                tooltip={"placement": "top", "always_visible": True},
                persistence=id,
                persistence_type="local",
            ),
            html.Br(),
            html.Br(),
        ]
    )

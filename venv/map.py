import folium
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px
import os
from folium import plugins
import rioxarray as rxr
import pandas as pd
import numpy as np


from pyvis.network import Network
stops = pd.read_csv("stops.csv")

trips = pd.read_csv("trips.csv")

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.P('Selected Charging Station', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=stops['stop_id'],
            value=[1019,1121],  # default value
            multi=True
        ),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Card Title 1'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4('Card Title 2', className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Sample text.', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Card Title 3', className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Sample text.', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('Card Title 4', className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Sample text.', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]
        ),
        md=3
    )
])

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_6'), md=6
        )
    ]
)

content = html.Div(
    [
        html.H2('Thunder bay Map with charging station', style=TEXT_STYLE),
        html.Hr(),
        html.Iframe(id="map", srcDoc= open("map_with_selected_bus_stations.html","r").read(),width="100%",height="800"),
        html.H2('Thunder bay Map with all bus stops', style=TEXT_STYLE),
        html.Hr(),
        html.Iframe(id="map_2", srcDoc= open("map_with_all_bus_label.html","r").read(),width="100%",height="800"),
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])


@app.callback(
    Output('map', 'srcDoc'),
    [Input('submit_button', 'n_clicks')],
    [State("dropdown","value")])
def update_map(n_clicks,dropdown):
    if n_clicks == 0:
        return dash.no_update
    else:
        stops = pd.read_csv("stops.csv")

        trips = pd.read_csv("trips.csv")

        tb_latitude = 48.382221
        tb_longitube = -89.246109
        map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start=12,
                         # width= , height = 300,
                         control_scale=True)
        for _, stop in stops[stops['stop_id'].isin(dropdown)].iterrows():
            folium.Marker(
                location=[stop['stop_lat'], stop['stop_lon']],
                popup=stop['stop_name'],
                tooltip=stop['stop_id'],
                icon=folium.Icon(color="green", icon="bolt", prefix='fa')
            ).add_to(map)

        map.save("map_with_selected_bus_stations.html")

        print(dropdown)
        return open("map_with_selected_bus_stations.html","r").read()


if __name__ == '__main__':
    app.run_server(port='8080',debug=True)
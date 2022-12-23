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
stop_times = pd.read_csv("stop_times.csv")
total_route = ["1","2","3C","3J","3M","4","5","6","7","8","9","10","11","12","13","14","16"]
routes = pd.read_csv("routes.csv")
route_color = routes['route_color']
route_color = "#"+route_color
#print("#"+route_color[1])
#route_color=["red","#13B5EA","goldenrod","pink","orange","darkorange","violet","purple","darkred","green","aqua","indigo","greenyellow","gold","lightseagreen","lightskyblue","orangered"]

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
    'margin-left': '5%',
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
        html.P('Bus Route', style={
            'textAlign': 'center'
        }),
        dcc.Checklist(
                id='my_checklist',                      # used to identify component in callback
                options=[
                         {'label': html.Div(
                             [total_route[x]], style={'color': route_color[x], 'font-size': 30}
                         ),
                          'value': total_route[x], 'disabled':False}
                         for x in range(17)
                ],labelStyle = dict(display='inline') ),
        html.Br(),
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
        html.H2('Thunder bay Bus Route Map', style=TEXT_STYLE),
        html.Hr(),
        html.P('Bus Route', style={
            'textAlign': 'center'
        }),
        dcc.Checklist(
            id='my_checklist',  # used to identify component in callback
            options=[
                {'label': html.Div(
                    [total_route[x]], style={'color': route_color[int(routes[routes["route_id"] == total_route[x]].index.values)], 'font-size': 50}
                ),
                    'value': total_route[x], 'disabled': False}
                for x in range(17)
            ], labelStyle=dict(display='inline-block'),
            value=total_route,
            inputStyle={"margin-right": "80px"}

        ),
        html.Br(),
        html.Iframe(id="map", srcDoc= open("route.html","r").read(),width="100%",height="800"),
    ],
    style=CONTENT_STYLE
)






app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([content])


@app.callback(
    Output('map', 'srcDoc'),
    [Input('my_checklist', 'value')])
def update_map(value):
    start = True

    tb_latitude = 48.382221
    tb_longitube = -89.246109
    map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start=12,
                     # width= , height = 300,
                     control_scale=True)


    bus_stations = []


    # location= pd.DataFrame((x["shape_pt_lat"],x['shape_pt_lon']))
    for route_id in value:
        shapes = pd.read_csv("shapes.csv")
        stops = pd.read_csv("stops.csv")
        trips = pd.read_csv("trips.csv")
        stop_times = pd.read_csv("stop_times.csv")


        trip = trips[trips['route_id'] == route_id]  # change 1 to other route name to switch route
        trip_shape = trip['shape_id']
        shapes = shapes[shapes['shape_id'].isin(trip_shape)]

        trip_id = trip["trip_id"]
        route_stops = stop_times[stop_times['trip_id'].isin(trip_id)]
        route_stops_id = route_stops["stop_id"]

        color_id = routes[routes["route_id"]==route_id].index.values
        color_id = int(color_id)

        for _, stop in stops[stops['stop_id'].isin(route_stops_id)].iterrows():
            bus_stations.append(stop['stop_id'])
            folium.Marker(
                location=[stop['stop_lat'], stop['stop_lon']],
                popup=stop['stop_name'],
                tooltip=stop['stop_id'],
                icon=plugins.BeautifyIcon(icon="arrow-down", icon_shape="marker",
                                          number=route_id,
                                          border_color=route_color[color_id],
                                          background_color=route_color[color_id],
                                          prefix='fa')
            ).add_to(map)
        each_shapes = shapes
        each_shapes = shapes[~shapes.duplicated('shape_id')]
        each_shapes = each_shapes['shape_id']
        for shape_ids in each_shapes:
            start = True
            shapes_sub = shapes[shapes['shape_id'] == (shape_ids)]
            for _, shape in shapes_sub.iterrows():
                if (start):
                    x = shape
                    lat = []
                    lon = []
                    lat.append(shape['shape_pt_lat'])
                    lon.append(shape['shape_pt_lon'])
                    start = False
                # shape and x is not in same format so convert to int
                else:
                    lat.append(shape['shape_pt_lat'])
                    lon.append(shape['shape_pt_lon'])

            location = {'lat': lat, 'lon': lon}
            location = pd.DataFrame(location)
            my_PolyLine = folium.PolyLine(locations=location[['lat', 'lon']], weight=5, tooltip=route_id,
                                          popup=route_id, color=route_color[color_id])
            map.add_child(my_PolyLine)

        # also place a marker in each shape,

    map.save("route.html")

    return open("route.html","r").read()


if __name__ == '__main__':
    app.run_server(port='8081',debug=False)
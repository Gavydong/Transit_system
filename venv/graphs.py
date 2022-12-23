import folium
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


import os
from folium import plugins
import rioxarray as rxr
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly.express as px

from pyvis.network import Network
stops = pd.read_csv("stops.csv")

trips = pd.read_csv("trips.csv")
total_route = ["1","2","3C","3J","3M","4","5","6","7","8","9","10","11","12","13","14","16"]

routes = pd.read_csv("routes.csv")
route_color = routes['route_color']
route_color = "#"+route_color
#=["red","blue","goldenrod","pink","orange","darkorange","violet","purple","darkred","green","aqua","indigo","greenyellow","gold","lightseagreen","lightskyblue","orangered"]

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
        html.P('Cost parameters', style={
            'textAlign': 'center'
        }),
        html.Label("OFF Peak $"),
        dcc.Input(
            id="off_peak",
            type="number",
            value="0.082",
        ),
        html.Label("/KWH"),
        html.Br(),
        html.Label("MID Peak $"),
        dcc.Input(
            id="mid_peak",
            type="number",
            value="0.113",
        ),
        html.Label("/KWH"),
        html.Br(),
        html.Label("ON Peak $"),
        dcc.Input(
            id="on_peak",
            type="number",
            value="0.17",
        ),
        html.Label("/KWH"),
        html.Br(),
        html.Label("FUEL Cost $"),
        dcc.Input(
            id="fuel_cost",
            type="number",
            value="1.6",
        ),
        html.Label("/Litre"),
        html.Br(),
        html.Br(),
        html.P('Travel Condition', style={
            'textAlign': 'center'
        }),
        html.Label("Driving Behavior"),
        dcc.Dropdown(
            id='drive_b',
            options=[
                {'label': 'Slow', 'value': '1'},
                {'label': 'Medium', 'value': '2'},
                {'label': 'Fast', 'value': '3'},
        ],
        value='1'
        ),
        html.Label("Road Condition"),
        dcc.Dropdown(
            id='road_d',
            options=[
                {'label': 'Good', 'value': '1'},
                {'label': 'Medium', 'value': '2'},
                {'label': 'Bad', 'value': '3'},
        ],
        value='1'
        ),
        html.Label("People Density"),
        dcc.Dropdown(
            id='people_d',
            options=[
                {'label': 'Low', 'value': '1'},
                {'label': 'Medium', 'value': '2'},
                {'label': 'Full', 'value': '3'},
        ],
        value='1'
        ),
        html.Label("Season"),
        dcc.Dropdown(
            id='season',
            options=[
                {'label': 'Spring', 'value': '1'},
                {'label': 'Summer', 'value': '2'},
                {'label': 'Fall', 'value': '3'},
                {'label': 'Winter', 'value': '4'},
        ],
        value='1'
        ),
        html.Br(),
        html.Br(),
        html.P('Bus Setting', style={
            'textAlign': 'center'
        }),
        html.Label("SOC Upper limit"),
        dcc.Input(
            id="soc_up",
            type="number",
            value="100",
        ),
        html.Label("%"),
        html.Br(),
        html.Label("Starting SOC"),
        dcc.Input(
            id="soc_start",
            type="number",
            value="90",
        ),
        html.Label("%"),
        html.Br(),
        html.Label("Maintenace Cost $"),
        dcc.Input(
            id="m_cost",
            type="number",
            value="0.525",
        ),
        html.Label("/KM"),
        html.Br(),
        html.Label("Operational Cost $"),
        dcc.Input(
            id="o_cost",
            type="number",
            value="85",
        ),
        html.Label("/hr"),


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


content_first_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=12,
        )
    ]
)
content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_2'), md=12,
        )
    ]
)
content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_3'), md=12,
        )
    ]
)


content = html.Div(
    [
        html.H2('Graph Page', style=TEXT_STYLE),
        html.Hr(),
        dcc.Tabs(id="tabs", value='1', children=[
            dcc.Tab(label=total_route[0],value= total_route[0],style={"color": route_color[0]}),
            dcc.Tab(label=total_route[1],value= total_route[1],style={"color": route_color[1]}),
            dcc.Tab(label=total_route[2],value= total_route[2],style={"color": route_color[2]}),
            dcc.Tab(label=total_route[3],value= total_route[3],style={"color": route_color[3]}),
            dcc.Tab(label=total_route[4],value= total_route[4],style={"color": route_color[4]}),
            dcc.Tab(label=total_route[5],value= total_route[5],style={"color": route_color[5]}),
            dcc.Tab(label=total_route[6],value= total_route[6],style={"color": route_color[6]}),
            dcc.Tab(label=total_route[7],value= total_route[7],style={"color": route_color[7]}),
            dcc.Tab(label=total_route[8],value= total_route[8],style={"color": route_color[8]}),
            dcc.Tab(label=total_route[9],value= total_route[9],style={"color": route_color[9]}),
            dcc.Tab(label=total_route[10],value= total_route[10],style={"color": route_color[10]}),
            dcc.Tab(label=total_route[11],value= total_route[11],style={"color": route_color[11]}),
            dcc.Tab(label=total_route[12],value= total_route[12],style={"color": route_color[12]}),
            dcc.Tab(label=total_route[13],value= total_route[13],style={"color": route_color[13]}),
            dcc.Tab(label=total_route[14],value= total_route[14],style={"color": route_color[14]}),
            dcc.Tab(label=total_route[15],value= total_route[15],style={"color": route_color[15]}),
            dcc.Tab(label=total_route[16],value= total_route[16],style={"color": route_color[16]}),

                ]),
        html.H2('Bus Distance', style=TEXT_STYLE),
        content_first_row,
        html.H2('Bus Speed', style=TEXT_STYLE),
        content_second_row,
        html.H2('Bus SOC', style=TEXT_STYLE),
        content_third_row
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])


@app.callback(
    Output('graph_1', 'figure'),
    [Input('tabs', 'value')])
def update_graph(tabs):
    stops = pd.read_csv("stops.csv")

    trips = pd.read_csv("trips.csv")

    stop_times = pd.read_csv("stop_times.csv")

    route_id = tabs

    trip = trips[trips['route_id'] == route_id]  # change 1 to other route name to switch route
    trip_id = trip['trip_id']
    stop_times = stop_times[stop_times['trip_id'].isin(trip_id)]

    no_dup = stop_times.drop_duplicates(subset=['trip_id'])
    no_dup = no_dup['trip_id']
    layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    first = stop_times.head()
    first = first["trip_id"]
    stop_times_final = stop_times[stop_times['trip_id'].isin(first)]

    for x in range(0, 8):
        trip_id = no_dup.iloc[x]
        new_rows = stop_times[stop_times['trip_id'] == (trip_id)]
        stop_times_final = pd.concat([stop_times_final,new_rows])

    fig = go.Figure(layout=layout, )
    # stop_times = stop_times.drop_duplicates(subset=['arrival_time'])
    stop_times_final['arrival_time'] = pd.to_datetime(stop_times["arrival_time"])
    # print(type(stop_times['arrival_time']))
    stop_times_final = stop_times_final.sort_values(by=['arrival_time'])

    # first = stop_times.head()
    # first = first["trip_id"]
    # stop_times = stop_times[stop_times['trip_id'].isin(first)]
    fig.add_trace(go.Scatter(x=stop_times_final["arrival_time"], y=stop_times_final["shape_dist_traveled"],
                             mode='lines', marker=dict(
            size=20,
            line=dict(
                color='blue',
                width=10
            ),
        )))

    fig.update_layout(xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False))
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Distance")

    return fig

@app.callback(
    Output('graph_2', 'figure'),
    [Input('tabs', 'value')])
def update_graph(tabs):
    stops = pd.read_csv("stops.csv")

    trips = pd.read_csv("trips.csv")

    stop_times = pd.read_csv("stop_times.csv")

    route_id = tabs

    trip = trips[trips['route_id'] == route_id]  # change 1 to other route name to switch route
    trip_id = trip['trip_id']
    stop_times = stop_times[stop_times['trip_id'].isin(trip_id)]

    no_dup = stop_times.drop_duplicates(subset=['trip_id'])
    no_dup = no_dup['trip_id']
    layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    first = stop_times.head()
    first = first["trip_id"]
    stop_times_final = stop_times[stop_times['trip_id'].isin(first)]

    for x in range(0, 8):
        trip_id = no_dup.iloc[x]
        new_rows = stop_times[stop_times['trip_id'] == (trip_id)]
        stop_times_final = pd.concat([stop_times_final,new_rows])

    stop_times_final["next"] = stop_times_final["shape_dist_traveled"].shift(-1)
    stop_times_final["speed"]= stop_times_final['next'] - stop_times_final["shape_dist_traveled"]
    fig = go.Figure(layout=layout, )
    # stop_times = stop_times.drop_duplicates(subset=['arrival_time'])
    stop_times_final['arrival_time'] = pd.to_datetime(stop_times["arrival_time"])
    # print(type(stop_times['arrival_time']))
    stop_times_final = stop_times_final.sort_values(by=['arrival_time'])

    stop_times_final = stop_times_final[(stop_times_final['speed'] >= 0) | (stop_times_final['speed'].isnull())]
    stop_times_final["speed"] = stop_times_final["speed"]/1000*60
    # first = stop_times.head()
    # first = first["trip_id"]
    # stop_times = stop_times[stop_times['trip_id'].isin(first)]
    fig.add_trace(go.Scatter(x=stop_times_final["arrival_time"], y=stop_times_final["speed"],
                             mode='lines',
                             name='speed', marker=dict(
            size=20,
            line=dict(
                color='blue',
                width=10
            )
        )))

    fig.update_layout(xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False))
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Speed(km/h)")

    return fig


@app.callback(
    Output('graph_3', 'figure'),
    [Input('tabs', 'value')])
def update_graph(tabs):
    stops = pd.read_csv("stops.csv")

    trips = pd.read_csv("trips.csv")

    stop_times = pd.read_csv("stop_times.csv")

    route_id = tabs

    trip = trips[trips['route_id'] == route_id]  # change 1 to other route name to switch route
    trip_id = trip['trip_id']
    stop_times = stop_times[stop_times['trip_id'].isin(trip_id)]

    no_dup = stop_times.drop_duplicates(subset=['trip_id'])
    no_dup = no_dup['trip_id']
    layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    first = stop_times.head()
    first = first["trip_id"]
    stop_times_final = stop_times[stop_times['trip_id'].isin(first)]

    for x in range(0, 8):
        trip_id = no_dup.iloc[x]
        new_rows = stop_times[stop_times['trip_id'] == (trip_id)]
        stop_times_final = pd.concat([stop_times_final,new_rows])

    stop_times_final["next"] = stop_times_final["shape_dist_traveled"].shift(-1)
    stop_times_final["speed"]= stop_times_final['next'] - stop_times_final["shape_dist_traveled"]
    fig = go.Figure(layout=layout, )
    # stop_times = stop_times.drop_duplicates(subset=['arrival_time'])
    stop_times_final['arrival_time'] = pd.to_datetime(stop_times["arrival_time"])
    # print(type(stop_times['arrival_time']))
    stop_times_final = stop_times_final.sort_values(by=['arrival_time'])

    stop_times_final = stop_times_final[(stop_times_final['speed'] >= 0) | (stop_times_final['speed'].isnull())]
    stop_times_final['soc'] = 100-stop_times_final["speed"].cumsum()/2000
    # first = stop_times.head()
    # first = first["trip_id"]
    # stop_times = stop_times[stop_times['trip_id'].isin(first)]
    fig.add_trace(go.Scatter(x=stop_times_final["arrival_time"], y=stop_times_final["soc"],
                             mode='lines',
                             name='speed', marker=dict(
            size=20,
            line=dict(
                color='blue',
                width=10
            )
        )))

    fig.update_layout(xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False))
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="SOC(%)")

    return fig


if __name__ == '__main__':
    app.run_server(port='8088',debug=True)
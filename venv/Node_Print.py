import os
import folium
from folium import plugins
import rioxarray as rxr
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly.express as px
import random
import webbrowser
from pyvis.network import Network

from iteration_utilities import duplicates
from iteration_utilities import unique_everseen

def print_select_bus_stations(selected_stations):
    tb_latitude = 48.382221
    tb_longitube = -89.246109
    map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start=12,
                     # width= , height = 300,
                     control_scale=True)

    # assign all bust sation as a label in the map

    shapes = pd.read_csv("shapes.csv")
    stop_times = pd.read_csv("stop_times.csv")

    total_route = ["1", "2", "3C", "3J", "3M", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "16"]
    routes = pd.read_csv("routes.csv")
    route_color = routes['route_color']
    route_color = "#" + route_color

    # location= pd.DataFrame((x["shape_pt_lat"],x['shape_pt_lon']))

    shapes = pd.read_csv("shapes.csv")
    stops = pd.read_csv("stops.csv")
    trips = pd.read_csv("trips.csv")
    stop_times = pd.read_csv("stop_times.csv")

    trip_id = trips["trip_id"]

    route_stops = stop_times[stop_times['trip_id'].isin(trip_id)]
    route_stops_id = route_stops["stop_id"]

    color_id = 0
    for route_id in total_route:
        # Create map for each route, save each route seperately
        # map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start=12,
        # width= , height = 300,
        #                 control_scale=True)
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

        for _, stop in stops[stops['stop_id'].isin(route_stops_id)].iterrows():
            bus_stations.append(stop['stop_id'])
            if (stop['stop_id'] in selected_stations):
                folium.Marker(
                    location=[stop['stop_lat'], stop['stop_lon']],
                    popup=stop['stop_name'],
                    tooltip=total_route[color_id],
                    icon=plugins.BeautifyIcon(icon="arrow-down", icon_shape="marker",
                                              number=stop['stop_id'],
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

        # save each route seperately
        # map.save("route_test_"+total_route[color_id]+".html")
        color_id = color_id + 1
        # also place a marker in each shape,

    map.save("node_map.html")
    webbrowser.open_new_tab("node_map.html")
    return map


bus_stations = []

stops = pd.read_csv("stops.csv")
stop_id = stops["stop_id"]


# creat an random slected bus stations array as example
random_stop_ids = []
for stop in stop_id:
    if random.random() < 0.1:
        random_stop_ids.append(stop)
print(random_stop_ids)

print_select_bus_stations(random_stop_ids)


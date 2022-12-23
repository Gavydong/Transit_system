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

from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt

from iteration_utilities import duplicates
from iteration_utilities import unique_everseen

color_id=0

total_route = ["1","2","3C","3J","3M","4","5","6","7","8","9","10","11","12","13","14","16"]
routes = pd.read_csv("routes.csv")
route_color = routes['route_color']
route_color = "#"+route_color

#location= pd.DataFrame((x["shape_pt_lat"],x['shape_pt_lon']))

shapes = pd.read_csv("shapes.csv")
stops = pd.read_csv("stops.csv")
trips = pd.read_csv("trips.csv")
stop_times = pd.read_csv("stop_times.csv")

trip_id = trips["trip_id"]

route_stops = stop_times[stop_times['trip_id'].isin(trip_id)]
route_stops_id = route_stops["stop_id"]

Route_bus_df = pd.DataFrame()



for route_id in total_route:
    #Create map for each route, save each route seperately
    #map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start=12,
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
    Bus_stop_in_route = stops[stops['stop_id'].isin(route_stops_id)]
    bus_df = pd.DataFrame(Bus_stop_in_route['stop_id'])
    bus_df["route_id"] = route_id
    Route_bus_df = pd.concat([Route_bus_df,bus_df])

print(Route_bus_df)

#An example of printing all bus station of one route
try_route_id = '1'

print("All the bus under "+ try_route_id)
print(Route_bus_df[Route_bus_df['route_id']==(try_route_id)])


# Defining a Class
class GraphVisualization:

    def __init__(self):
        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()


# Driver code

G = nx.Graph()
#route = Route_bus_df[Route_bus_df['route_id']==(try_route_id)]
#G.add_nodes_from(Route_bus_df['stop_id'].drop_duplicates())
nodes = Route_bus_df['stop_id'].drop_duplicates()
for x in nodes:
    G.add_node(x)
for route_id in total_route:
    route = Route_bus_df[Route_bus_df['route_id'] == (route_id)]
    print(route_id)
    last_bus = None
    for stop_id in route['stop_id']:
        if last_bus == None:
            last_bus = stop_id
        else:
            G.add_edge(last_bus,stop_id)
            last_bus = stop_id

nx.draw_networkx(G)
plt.show()
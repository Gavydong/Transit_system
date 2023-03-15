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
import time
import matplotlib.pyplot as plt
import itertools
from itertools import chain
from networkx.algorithms.distance_measures import center

import networkx as nx
from networkx.utils import arbitrary_element
import networkx.algorithms.dominating


import networkx as nx

from iteration_utilities import duplicates
from iteration_utilities import unique_everseen


def print_select_bus_stations(selected_stations,charging_stations,total_route = ["1", "2", "3C", "3J", "3M", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "16"]):
    tb_latitude = 48.382221
    tb_longitube = -89.246109
    map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start=12,
                     # width= , height = 300,
                     control_scale=True)

    # assign all bust sation as a label in the map

    shapes = pd.read_csv("shapes.csv")
    stop_times = pd.read_csv("stop_times.csv")

    # total_route = ["1", "2", "3C", "3J", "3M", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "16"]
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
    bus_stations = []

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
            if (stop['stop_id'] in charging_stations):
                folium.Marker(
                    location=[stop['stop_lat'], stop['stop_lon']],
                    popup=stop['stop_name'],
                    tooltip=stop['stop_id'],
                    icon=folium.Icon(color="green", icon="bolt", prefix='fa')
                ).add_to(map)
            elif (stop['stop_id'] in selected_stations):
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

    map.save("chosing_charging_stations_from_selected_stops_3.html")
    webbrowser.open_new_tab("chosing_charging_stations_from_selected_stops_3.html")
    return map


def MaxDeg(G):
  vals = nx.degree_centrality(G).items()
  max_val = max(nx.degree_centrality(G).values())
  all_max = [i[0] for i in vals if i[1] == max_val]
  return all_max
#Function needs to distinguish among ties by decreases in set
#First one with the max new set wins
def DegTieBreak(G,neighSet,nbunch):
    maxN = -1
    for i in nbunch:
        neigh_cur = set(G[i].keys())
        dif = (neigh_cur | set([i]) ) - neighSet
        te = len(dif)
        if te > maxN:
            myL = [i,neigh_cur,dif]
            maxN = te
    return myL
def domSet(G,total=None):
    uG = G.copy() #make a deepcopy of the orig graph to update for the algorithm
    domSet = []      #list to place dominant set
    neighSet = set([])    #list of neighbors to dominating set
    if not total:
        loop_num = len(nx.nodes(G)) #total is the set maximum number of loops for graph
    else:                           #default as many nodes in graph
        loop_num = total            #can also set a lower limit though
    for i in range(loop_num):
        nodes_sel = MaxDeg(uG)   #select nodes from updated graph with max degree centrality
        #chooses among degree ties with the maximum set of new neighbors
        if len(nodes_sel) > 1:
            temp = DegTieBreak(G=uG,neighSet=neighSet,nbunch=nodes_sel)
            node_sel = temp[0]
            neigh_cur = temp[1]
            newR = temp[2]
        else:
            node_sel = nodes_sel[0]
            neigh_cur = set(uG[node_sel].keys()) #neighbors of the current node
            newR = neigh_cur - neighSet          #new neighbors added in
        domSet.append(node_sel) #append that node to domSet list
        #break loop if dominant set found, else decrement counter
        if nx.is_dominating_set(G,domSet):
            break
        #should only bother to do this junk if dominant set has not been found!
        uG.remove_node(node_sel)  #remove node from updated graph
        #now this part does two loops to remove the edges between reached nodes
        #one for all pairwise combinations of the new reached nodes, the second
        #for the product of all new reached nodes compared to prior reached nodes
        #new nodes that have been reached
        for i in itertools.combinations(newR,2):
            if uG.has_edge(*i):
                uG.remove_edge(*i)
        #product of new nodes and old neighbor set
        #this loop could be pretty costly in big networks, consider dropping
        #should not make much of a difference
        for j in itertools.product(newR,neighSet):
            if uG.has_edge(*j):
                uG.remove_edge(*j)
        #now update the neighSet to include newnodes, but strip nodes that are in the dom set
        #since they are pruned from graph, all of their edges are gone as well
        neighSet = (newR | neighSet) - set(domSet)
    return domSet

def distance_in_one_trip(stop_start,stop_end,trip_id):
    stop_times = pd.read_csv("stop_times.csv")
    trip = stop_times[stop_times["trip_id"] == trip_id]
    trip_start = trip[trip["stop_id"]==stop_start]
    trip_end = trip[trip["stop_id"]==stop_end]
    distance = abs(int(trip_start["shape_dist_traveled"])-int(trip_end["shape_dist_traveled"]))
    return distance



def distance_in_one_route(stop_start,stop_end,route_id):
    #This function take two stop_id and the route number of these two stop_id as input.
    #This function output the distance in meter between these two stop_id.
    stops = pd.read_csv("stops.csv")
    stop_id = stops["stop_id"]
    stop_times = pd.read_csv("stop_times.csv")
    trips = pd.read_csv("trips.csv")
    trip_route = trips[trips['route_id'] == route_id]
    #Read all the csv file required

    #trips.csv store all the trips.
    #The trips.csv store many trips happened in all the routes.
    #For example, if one route have bus station 1 to 100.
    #One full trips 1 to 100 are recorded in seperate 3,4 or 5 sub-trips
    #The trips may be 1 to 30, 30 to 70, 70 to 100 seperately.
    #However these might not be the only way trips are arranged.
    #Some trips may start at 50, 50-80, 80:10, 10:50 could be one type of sub-trips
    #The following loop mean to find one of the sub-trips that can form one full trip.
    #And combine these sub-trips to one array.
    #Named nonduplicated_trip

    nonduplicated_trip = []

    trip_start = []
    trip_tail = None

    #trip_route contain all the trips in selected route.
    #These trips contain many duplicated trip because they recorded in different days

    for trip in trip_route['trip_id']: #looping all the trips
        temp = stop_times[stop_times["trip_id"] == trip]
        temp = temp["stop_id"]
        start = temp.iloc[0]
        #start is the first bus stop id of this trip
        if (start not in (trip_start)):
            if (trip_tail == None or start == trip_tail): # If these is the first trip in the whole loop
                # or this trips start at bus stop id which is same as the last trip's last stop id(last tail)
                #Then these trips are connected and recored in array nonduplicated_trip
                trip_tail = temp.iloc[-1]
                trip_start.append(start)
                nonduplicated_trip.append(trip)
        else:
            continue

    temp = stop_times[stop_times["trip_id"].isin(nonduplicated_trip)]
    #The following step mean to recalculate the distance of the whole trip,

    distance_add = 0
    last_distance = 0
    distance = []
    for index, trip_row in temp.iterrows():
        if (trip_row["shape_dist_traveled"] == 0):
            distance_add = distance_add + last_distance
        distance.append(trip_row["shape_dist_traveled"] + distance_add)
        last_distance = trip_row["shape_dist_traveled"]
    temp_ids = []
    temp["shape_dist_traveled"] = distance
    trip_start = temp[temp["stop_id"]==stop_start]
    trip_end = temp[temp["stop_id"]==stop_end]


    #This step calculate the distance between selected bus stops
    result = abs(trip_start["shape_dist_traveled"].values - trip_end["shape_dist_traveled"].values)
    #If one of selected bus stop is an terminal or intersection, there will be multiple route between selected stops
    #Then there will be multiple distance, we just selected the minimum which is the closest route.
    return min(result)

def distance_in_one_route_enhanced(stop_start,stop_end,route_id):
    trip = pd.read_csv(route_id+".csv")
    if(stop_start not in trip["stop_id"].values or stop_end not in trip["stop_id"].values):
        return None
    trip_start = trip[trip["stop_id"]==stop_start]
    trip_end = trip[trip["stop_id"]==stop_end]
    #
    # print(np.unique(trip_start["shape_dist_traveled"].values))
    # print(np.unique(trip_end["shape_dist_traveled"].values))
    #This step calculate the distance between selected bus stops
    result = abs(np.unique(trip_start["shape_dist_traveled"].values) - np.unique(trip_end["shape_dist_traveled"].values))
    #If one of selected bus stop is an terminal or intersection, there will be multiple route between selected stops
    #Then there will be multiple distance, we just selected the minimum which is the closest route.
    return min(result)

def Distance_between_two_stops(stop_start,stop_end):
    total_route = ["1", "2", "3C", "3J", "3M", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "16"]
    result=[]
    for route_id in total_route:
        result.append(distance_in_one_route_enhanced(stop_start,stop_end,route_id))
    result = [i for i in result if i is not None]
    if result:
        return min(result)
    else:
        print(str(stop_start)+"and"+str(stop_end)+" Not in same route")
        return None



# 1121(waterfront), 1222(lakeheadU), 1231(confederation collage), 1006(intercity), 1019(city hall)

transit_node =  nx.Graph()
transit_node.add_nodes_from([1006,1019,1121,1222,1231])
total_route = ["1", "2", "3C", "3J", "3M", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "16"]
# for route in total_route:
#     print(route+":")
#     print(distance_in_one_route_enhanced(1222,1019,route))

transit_node.add_edge(1019,1231,weight=Distance_between_two_stops(1019,1231))
transit_node.add_edge(1019,1006,weight=Distance_between_two_stops(1019,1006))
transit_node.add_edge(1231,1222,weight=Distance_between_two_stops(1231,1222))
transit_node.add_edge(1222,1006,weight=Distance_between_two_stops(1222,1006))
transit_node.add_edge(1222,1121,weight=Distance_between_two_stops(1222,1121))
transit_node.add_edge(1121,1006,weight=Distance_between_two_stops(1121,1006))
transit_node.add_edge(1231,1006,weight=Distance_between_two_stops(1231,1006))
transit_node.add_edge(1121,1231,weight=Distance_between_two_stops(1121,1231))
transit_node.add_edge(1121,1019,weight=Distance_between_two_stops(1121,1019))

#nx.draw(transit_node)
#plt.show()
#print(transit_node)
center_node = center(transit_node)
domiset = domSet(transit_node)
#print(center_node)
#print(domiset)

#print_select_bus_stations([1006,1019,1121,1222,1231],center_node,["1","2","3M","8","9","16"])


shapes = pd.read_csv("shapes.csv")
stops = pd.read_csv("stops.csv")
trips = pd.read_csv("trips.csv")
stop_times = pd.read_csv("stop_times.csv")


selected_bus_stops = []

for stop_id in stops["stop_id"]:
    if(stop_id in [1006,1019,1121,1222,1231]):
        selected_bus_stops.append(stop_id)
    elif(random.randrange(1, 10) <2.5):
        selected_bus_stops.append(stop_id)

transit_node =  nx.Graph()
transit_node.add_nodes_from(selected_bus_stops)

#route_id = "1" # change to other route name to switch route

for i in selected_bus_stops:
    for j in selected_bus_stops:
        if not (i == j):
            dist_stops = Distance_between_two_stops(i, j)
            if(dist_stops):
                print(dist_stops)
                transit_node.add_edge(i,j,weight =dist_stops)



# for route_id in total_route:
#     trip = pd.read_csv(route_id + ".csv")
#     route_stops_id = trip["stop_id"]
#     #print(route_stops_id)
#     start = True
#     for stop_id in route_stops_id:
#         if  start:
#             begin_stop = stop_id
#             last_stop = stop_id
#             start=False
#         else:
#             current_stop = stop_id
#             transit_node.add_edge(last_stop, current_stop, weight=Distance_between_two_stops(last_stop, current_stop))
#             last_stop = stop_id
#     transit_node.add_edge(last_stop, begin_stop, weight=Distance_between_two_stops(last_stop, begin_stop))
#


print(transit_node)

#center_node = center(transit_node)
domiset = domSet(transit_node)
#print(center_node)
print(domiset)
#for route in total_route:




print_select_bus_stations(selected_stations=selected_bus_stops,charging_stations=domiset)
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

    map.save("distance_try.html")
    webbrowser.open_new_tab("distance_try.html")
    return map


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


#for x in temp["stop_id"]:
    #print(x)
#    temp_ids.append(x)
# creat an random slected bus stations array as example
#random_stop_ids = []
#for stop in stop_id:
#    if random.random() < 0.1:
#        random_stop_ids.append(stop)
#print(random_stop_ids)

##############################################################################################################
#Save trips of each route into csv.
total_route = ["1", "2", "3C", "3J", "3M", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "16"]

for route in total_route:
    stops = pd.read_csv("stops.csv")
    stop_id = stops["stop_id"]
    stop_times = pd.read_csv("stop_times.csv")
    trips = pd.read_csv("trips.csv")
    trip_route = trips[trips['route_id'] == route]

    nonduplicated_trip = []

    trip_start = []
    trip_tail = None

# trip_route contain all the trips in selected route.
# These trips contain many duplicated trip because they recorded in different days

    for trip in trip_route['trip_id']:  # looping all the trips
        temp = stop_times[stop_times["trip_id"] == trip]
        temp = temp["stop_id"]
        start = temp.iloc[0]
    # start is the first bus stop id of this trip
        if (start not in (trip_start)):
            if (trip_tail == None or start == trip_tail):  # If these is the first trip in the whole loop
            # or this trips start at bus stop id which is same as the last trip's last stop id(last tail)
            # Then these trips are connected and recored in array nonduplicated_trip
                trip_tail = temp.iloc[-1]
                trip_start.append(start)
                nonduplicated_trip.append(trip)
        else:
            continue

    temp = stop_times[stop_times["trip_id"].isin(nonduplicated_trip)]
# The following step mean to recalculate the distance of the whole trip,

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
    #print(route+'.csv')
    temp.to_csv(route+'.csv')

#saving finished
##################################################





# st = time.time()
#
#
# print("function distance_in_one_route:")
#print(distance_in_one_route(1006,1006,"9"))
# et = time.time()
#
# get the execution time
# elapsed_time = et - st
# print('Execution time:', elapsed_time, 'seconds')
#
#
#
#
# st = time.time()
#
# get the execution time
#
# print("function distance_in_one_route_enhanced:")
#
#
# print(distance_in_one_route_enhanced(1006,1757,"9"))
# et = time.time()
#
# elapsed_time = et - st
# print('Execution time:', elapsed_time, 'seconds')

shapes = pd.read_csv("shapes.csv")
stops = pd.read_csv("stops.csv")
trips = pd.read_csv("trips.csv")
stop_times = pd.read_csv("stop_times.csv")

route_id = "9" # change to other route name to switch route

trip = trips[trips['route_id'] == route_id]
trip_shape = trip['shape_id']
shapes = shapes[shapes['shape_id'].isin(trip_shape)]

trip_id = trip["trip_id"]
route_stops = stop_times[stop_times['trip_id'].isin(trip_id)]
route_stops_id = route_stops["stop_id"]
route_stops_id = route_stops_id.drop_duplicates() #remove duplicate

print(route_stops_id)

df = pd.DataFrame(
                  index=pd.Index(route_stops_id),
                  columns=pd.Index(route_stops_id))
print(df)
for i in route_stops_id:
    for j in route_stops_id:
            df.loc[i, j]= distance_in_one_route_enhanced(i,j,route_id)


df.to_csv('route_'+route_id+"_table.csv")
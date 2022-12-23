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

from iteration_utilities import duplicates
from iteration_utilities import unique_everseen

stops = pd.read_csv("stops.csv")

trips = pd.read_csv("trips.csv")

stop_times = pd.read_csv("stop_times.csv")

shapes = pd.read_csv("shapes.csv")


routes = pd.read_csv("routes.csv")
route_color = routes['route_color']
route_color = "#"+route_color


tb_latitude = 48.382221
tb_longitube = -89.246109
route_id = "6"
color_id = 8
trip = trips[trips['route_id'] == route_id]  # change 1 to other route name to switch route
trip_id= trip['trip_id']
#print(trip_id)
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

for x in range(0,11):
    trip_id = no_dup.iloc[x]
   # print(trip_id)
    new_rows = stop_times[stop_times['trip_id'] == (trip_id)]
    stop_times_final=stop_times_final.append(new_rows)


fig = go.Figure(layout=layout, )
#stop_times = stop_times.drop_duplicates(subset=['arrival_time'])
stop_times_final['arrival_time'] = pd.to_datetime(stop_times["arrival_time"])
#print(type(stop_times['arrival_time']))
stop_times_final=stop_times_final.sort_values(by=['arrival_time'])
#first = stop_times.head()
#first = first["trip_id"]
#stop_times = stop_times[stop_times['trip_id'].isin(first)]
fig.add_trace(go.Scatter(x=stop_times_final["arrival_time"], y=stop_times_final["shape_dist_traveled"],
                         mode='lines',
                         name='Shaving', marker=dict(
        size=20,
        line=dict(
            color='blue',
            width=10
        )
    )))

fig.update_layout(xaxis=dict(showgrid=False),
                  yaxis=dict(showgrid=False))
fig.update_xaxes(title_text="Time")
fig.update_yaxes(title_text="Distance")

#fig.show()










tb_latitude = 48.382221
tb_longitube = -89.246109
map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start = 12,
               #width= , height = 300,
               control_scale = True)

#assign all bust sation as a label in the map

shapes = pd.read_csv("shapes.csv")
stop_times = pd.read_csv("stop_times.csv")

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

bus_stations = []

for route_id in total_route:
    #Create map for each route, save each route seperately
    #map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start=12,
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
        folium.Marker(
            location=[stop['stop_lat'], stop['stop_lon']],
            popup=stop['stop_name'],
            tooltip=stop['stop_id'],
            icon=plugins.BeautifyIcon(icon="arrow-down", icon_shape="marker",
                         number=total_route[color_id],
                         border_color= route_color[color_id],
                         background_color=route_color[color_id],
                                      prefix='fa')
        ).add_to(map)

    each_shapes = shapes
    each_shapes = shapes[~shapes.duplicated('shape_id')]
    each_shapes = each_shapes['shape_id']
    for shape_ids in each_shapes:
        start = True
        shapes_sub = shapes[shapes['shape_id']==(shape_ids)]
        for _,shape in shapes_sub.iterrows():
            if(start):
                x=shape
                lat=[]
                lon=[]
                lat.append(shape['shape_pt_lat'])
                lon.append(shape['shape_pt_lon'])
                start=False
       #shape and x is not in same format so convert to int
            else:
                lat.append(shape['shape_pt_lat'])
                lon.append(shape['shape_pt_lon'])

        location={'lat':lat, 'lon':lon}
        location=pd.DataFrame(location)
        my_PolyLine=folium.PolyLine(locations=location[['lat','lon']],weight=5,tooltip=route_id,popup=route_id,color =route_color[color_id])
        map.add_child(my_PolyLine)

    #save each route seperately
    #map.save("route_test_"+total_route[color_id]+".html")
    color_id=color_id+1
        #also place a marker in each shape,





map.save("route_bus_stations.html")
duplicate_stops = list(unique_everseen(duplicates(bus_stations)))

#print(duplicate_stops)

for _, stop in stops[stops['stop_id'].isin(duplicate_stops)].iterrows():
    folium.Marker(
        location=[stop['stop_lat'], stop['stop_lon']],
        popup=stop['stop_name'],
        tooltip=stop['stop_id'],
        icon=plugins.BeautifyIcon(icon="arrow-down", icon_shape="marker",
                                  number="!",
                                  border_color="black",
                                  background_color="black",
                                  prefix='fa')
    ).add_to(map)


map.save("route_with_duplicate_bus_stations.html")


map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start = 12,
               #width= , height = 300,
               control_scale = True)

for _, stop in stops[stops['stop_id'].isin(duplicate_stops)].iterrows():
    #print(stop['stop_id'])
    stop_trip = stop_times[stop_times['stop_id']==(stop['stop_id'])]
    #print(stop_trip)
    served_route = trips[trips['trip_id'].isin(stop_trip['trip_id'])]
    served_route = served_route['route_id']
    served_route = list(unique_everseen(duplicates(served_route)))
    #print(served_route)
    folium.Marker(
        location=[stop['stop_lat'], stop['stop_lon']],
        popup=stop['stop_name'],
        tooltip=stop['stop_id'],
        icon=plugins.BeautifyIcon(icon="arrow-down", icon_shape="marker",
                                  number=served_route,
                                  border_color=route_color[1],
                                  background_color=route_color[1],
                                  prefix='fa')
    ).add_to(map)

map.save("Bus_stations_multiple_routes.html")
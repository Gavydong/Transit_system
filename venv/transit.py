import os
import folium
from folium import plugins
import rioxarray as rxr
import pandas as pd
import numpy as np


from pyvis.network import Network
stops = pd.read_csv("stops.csv")

trips = pd.read_csv("trips.csv")

tb_latitude = 48.382221
tb_longitube = -89.246109
map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start = 12,
               #width= , height = 300,
               control_scale = True)

#assign all bust sation as a label in the map
for _,stop in stops.iterrows():
   folium.Marker(
        location = [stop['stop_lat'],stop['stop_lon']],
        popup= stop['stop_name'],
        tooltip=stop['stop_id']
    ).add_to(map)

# Display map
map.save("map_with_all_bus_label.html")



# choose bus stations as charging stations

#creat a new map if you only want to display the charging stations
#map = folium.Map(location=[tb_latitude, tb_longitube], zoom_start = 12,
#                 control_scale = True)
selected_stations = [1045,1176,1765] # example of selected bus stations ids


for _,stop in stops[stops['stop_id'].isin(selected_stations)].iterrows():
   folium.Marker(
       location = [stop['stop_lat'],stop['stop_lon']],
       popup= stop['stop_name'],
       tooltip=stop['stop_id'],
       icon = folium.Icon(color = "green",icon = "bolt", prefix= 'fa')
    ).add_to(map)


map.save("map_with_selected_bus_stations.html")



#showing the route line
shapes = pd.read_csv("shapes.csv")
trip_1= trips[trips['route_id']=='1'] # change 1 to other route name to switch route
trip_1_shape = trip_1['shape_id']


m = folium.Map(location=[tb_latitude, tb_longitube], zoom_start = 12,
               #width= , height = 300,
               control_scale = True)

shapes=shapes[shapes['shape_id'].isin(trip_1_shape)]
#my_PolyLine=folium.PolyLine(locations=shapes[['shape_pt_lat','shape_pt_lon']],weight=5)
#m.add_child(my_PolyLine)

start=True
#location= pd.DataFrame((x["shape_pt_lat"],x['shape_pt_lon']))
for _,shape in shapes.iterrows():
    if(start):
        x=shape
        lat=[]
        lon=[]
        lat.append(shape['shape_pt_lat'])
        lon.append(shape['shape_pt_lon'])
        start=False
    #shape and x is not in same format so convert to int
    elif(int(shape['shape_id']) == int(x['shape_id'])):
        lat.append(shape['shape_pt_lat'])
        lon.append(shape['shape_pt_lon'])
    else:
        location={'lat':lat, 'lon':lon}
        location=pd.DataFrame(location)
        my_PolyLine=folium.PolyLine(locations=location[['lat','lon']],weight=5)
        m.add_child(my_PolyLine)
        x=shape
        lat=[]
        lon=[]
        lat.append(shape['shape_pt_lat'])
        lon.append(shape['shape_pt_lon'])
        #also place a marker in each shape,
        folium.Marker(
            location=[shape['shape_pt_lat'], shape['shape_pt_lon']],
            tooltip=shape['shape_id'],
        ).add_to(m)

#assign all bust sation as a label in the map

# Display map


m.save("map_with_all_bus_shape.html")



g = Network()


for i in range(0,10):
    g.add_node(i,label=str(i))

for i in range(0,9):
    g.add_edge(i,i+1)

for i in range(20,30):
    g.add_node(i,label=str(i))


for i in range(20,29):
    g.add_edge(i,i+1)

    g.add_edge(5,20)
g.show("graph.html")
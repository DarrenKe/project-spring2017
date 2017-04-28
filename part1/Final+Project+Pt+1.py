
# coding: utf-8

# In[1]:

get_ipython().magic('matplotlib inline')


# In[2]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[3]:

agency = pd.read_csv("data-readonly/CUMTD/agency.txt")
calendar = pd.read_csv("data-readonly/CUMTD/calendar.txt")
calendar_dates = pd.read_csv("data-readonly/CUMTD/calendar_dates.txt")
far_attributes = pd.read_csv("data-readonly/CUMTD/fare_attributes.txt")
fare_rules = pd.read_csv("data-readonly/CUMTD/fare_rules.txt")
routes = pd.read_csv("data-readonly/CUMTD/routes.txt")
shapes = pd.read_csv("data-readonly/CUMTD/shapes.txt")
stop_times = pd.read_csv("data-readonly/CUMTD/stop_times.txt")
stops = pd.read_csv("data-readonly/CUMTD/stops.txt")
trips = pd.read_csv("data-readonly/CUMTD/trips.txt")


# In[4]:

plt.style.use('seaborn-notebook')


# In[5]:

route_dict = routes.set_index('route_id').T.to_dict('list')
shapes_trips_dict = trips.set_index('shape_id').T.to_dict('list')
stop_trips_dict = stop_times.set_index('stop_id').T.to_dict('list')
trips_route_dict = trips.set_index('trip_id').T.to_dict('list')
route_name_dict = routes.set_index('route_long_name').T.to_dict('list')


# In[28]:

fig, ax = plt.subplots(figsize=(15,15))
lat = []
lon = []
seq = -1
color = ""
for index, row in shapes.iterrows():
    if row['shape_pt_sequence'] < seq:
        ax.plot(lon, lat, c=color)
        lat = []
        lon = []
        lat.append(row['shape_pt_lat'])
        lon.append(row['shape_pt_lon'])
        seq = row['shape_pt_sequence']
    else:
        lat.append(row['shape_pt_lat'])
        lon.append(row['shape_pt_lon'])
        seq = row['shape_pt_sequence']
        color = '#' + route_dict[shapes_trips_dict[row['shape_id']][0]][6]


# In[29]:

fig, ax = plt.subplots(figsize=(15,15))
lat = []
lon = []
seq = -1
color = ""
for index, row in shapes.iterrows():
    if row['shape_pt_sequence'] < seq:
        ax.plot(lon, lat, c=color)
        lat = []
        lon = []
        lat.append(row['shape_pt_lat'])
        lon.append(row['shape_pt_lon'])
        seq = row['shape_pt_sequence']
    else:
        lat.append(row['shape_pt_lat'])
        lon.append(row['shape_pt_lon'])
        seq = row['shape_pt_sequence']
        color = '#' + route_dict[shapes_trips_dict[row['shape_id']][0]][6]
ax.plot(stops['stop_lon'].tolist(), stops['stop_lat'].tolist(), '.')


# In[20]:

dist_dict = {}
for index, row in shapes.iterrows():
    temp = dist_dict.get(route_dict[shapes_trips_dict[row['shape_id']][0]][2], 0)
    dist_dict[route_dict[shapes_trips_dict[row['shape_id']][0]][2]] = max(temp, row['shape_dist_traveled'])


# In[26]:

fig, ax = plt.subplots(figsize=(25,10))
sorted_keys = list(dist_dict.keys())
sorted_keys.sort()
sorted_values = []
colors = []
for key in sorted_keys:
    sorted_values.append(dist_dict[key])
    colors.append('#' + route_name_dict[key][6])
ax.bar(range(len(dist_dict)), sorted_values, align='edge', color = colors)
plt.xticks(range(len(dist_dict)), sorted_keys)
ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)

plt.show()


# In[17]:

stop_dict = {}
for index, row in stops.iterrows():
    r = route_dict[trips_route_dict[stop_trips_dict[row['stop_id']][0]][0]][2]
    temp = stop_dict.get(r, 0)
    if temp == 0:
        stop_dict[r] = []
    stop_dict[r].append(row['stop_id'])


# In[18]:

fig, ax = plt.subplots(figsize=(25,10))
sorted_keys = list(stop_dict.keys())
sorted_keys.sort()
sorted_values = []
for key in sorted_keys:
    sorted_values.append(len(set(stop_dict[key])))
ax.bar(range(len(stop_dict)), sorted_values, align='edge')
plt.xticks(range(len(stop_dict)), sorted_keys)
ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)

plt.show()


# In[ ]:




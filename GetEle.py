import requests
import json
from geojson import LineString, Feature, FeatureCollection, dump
import urllib
import pandas as pd
import os


# USGS Elevation Point Query Service
url = r'https://nationalmap.gov/epqs/pqs.php?'
'GETTING CURRENT PATH WITH OS'
Current_Path = os.getcwd()
direc = os.path.dirname(__file__)

'GETTING PATHS FOR LL AND POLY JSON GENERATED BY BASH SCRIPT'
path2 = os.path.join(
    direc, Current_Path+'/finalPath.json')
with open(path2, 'r') as myfile:
    polydata = myfile.read()

'NOW WE USE THE JSON LIBRARY MODULES TO INDEX TO THE COORDINATES'
'WE WANT TO PUT INTO 2D LISTS THAT ARE LOADED INTO SHAPELY OBJECTS'
l_poly = json.loads(polydata)

polygo = l_poly['coordinates']

'BEFORE LOADING INTO SHAPELY OBJECT, WE NEED TO MAKE SURE WE ARE'
'GETTING THE COORDINATES EMBEDDED IN THE JSON STRUCTURE'
polygon = []
for coords in polygo:
    if type(coords[0]) == float:
        polygon.append(coords[:2])
    elif type(coords[0]) == list:
        for coos in coords:
            if type(coos[0]) == float:
                polygon.append(coos[:2])


lat = []
lon = []

for coords in polygon:
    lat.append(coords[1])
    lon.append(coords[0])

# create data frame
df = pd.DataFrame({
    'lat': lat,
    'lon': lon
})

# Origin of this function and other initializers were contributed as a comment on a code forum from this url.
# author: Ben Gosack
"https://gis.stackexchange.com/questions/338392/getting-elevation-for-multiple-lat-long-coordinates-in-python"


def elevation_function(df, lat_column, lon_column):
    """Query service using lat, lon. add the elevation values as a new column."""
    elevations = []
    for lat, lon in zip(df[lat_column], df[lon_column]):

        # define rest query params
        params = {
            'output': 'json',
            'x': lon,
            'y': lat,
            'units': 'Meters'
        }

        # format query string and return query value
        result = requests.get((url + urllib.parse.urlencode(params)))
        elevations.append(result.json()[
                          'USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation'])

    df['elev_meters'] = elevations


elevation_function(df, 'lat', 'lon')

path_list = [df.columns.values.tolist()] + df.values.tolist()

path_list = path_list[1:]

# print(path_list)
#print("Size before: ", len(path_list))
for t in range(3):
    i = 0
    while i < (len(path_list)-1):
        p1 = path_list[i]
        p2 = path_list[i+1]
        diffLat = p2[0] - p1[0]
        diffLon = p2[1] - p1[1]
    #    print(p1[2], p2[2])
        diffEle = float(p2[2]) - float(p1[2])
        midPoint = [(diffLat/2) + p1[0],
                    (diffLon/2) + p1[1], (diffEle/2) + p1[2]]
        if abs(diffEle) > 3:
            path_list.insert(i+1, midPoint)
            i += 1
        i += 1


print("Size after: ", len(path_list))

pathPath = []
for coords in path_list:
    pathPath.append((coords[1], coords[0], coords[2]))


FinalPath = LineString(pathPath)
features = []
features.append(Feature(geometry=FinalPath))
with open('elePath.json', 'w') as f:
    dump(FinalPath, f)

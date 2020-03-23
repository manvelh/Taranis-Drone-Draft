"""
THIS PROGRAM TAKES A POLYGON AND LAUNCH LOCATION KML FILES.
THE PROGRAM THEN CREATES A FLIGHT PATH THAT COVERS THE WHOLE
FIELD IN TERMS OF DISTRUBTIVE VISITATION.IT DEPENDS ON THE
SHAPELY LIBRARY FOR OBJECT ORIENTATION, SO ENSTANTIATED CODE
WITH BE USED FREQUENTLY. IT DEPENDS ON THE SHAPELY LIBRARY
WRITTEN BY SEAN GILLIES
author: Manvel Beaver
SHAPELY - author: Sean Gillies
          documentation: https://shapely.readthedocs.io/en/latest/manual.html
          liscensed under: Creative Commons Attribution 3.0 United States License
"""
# SIDENOTE:SHAPELY OPERATES IN ARC DEGREES.
from shapely.geometry import LineString, LinearRing, Point, Polygon, MultiPolygon
import shapely.ops as ops
from geojson import Feature, FeatureCollection, dump
import json
import shlex
import subprocess
import os
import math
import time
import sys
from functools import partial
import pyproj

# GLOBAL VARS
boundaryDistance = 25  # meters
passDistance = 80  # meters
wpDistribution = 25  # meters


def unifer(coords, d):
    #coords = [(1, 1), (2, 2), (3, 3), (1, 2)]
    Mids = []

#    print("Coords to Start: ", coords)
 #   print("")
    temp = coords[:]
#    print("SIZE TO START: ", len(coords))
    for i in range(len(coords)-1):
        p1 = coords[i]
        p2 = coords[i+1]
        midCoord = (((p2[0] - p1[0])/2)+p1[0], ((p2[1] - p1[1])/2)+p1[1])
        Mids.append(midCoord)

    for i in range(len(Mids)):
        j = i*2 + 1
        temp.insert(j, Mids[i])
#        print("Size is now: ", len(temp))
 #       print("Index: %d\tValue: %f, %f\n" % (j, Mids[i][1], Mids[i][0]))
#        print("Inserted value into \n\n%s\n\n" % (temp))

#    print("Coords After in Uniformer: ", temp)
    return temp[:]

# TAKES 1 ARGS THAT CARRIES THE BOOL MESSAGE OF THERE BEING A LL.KML OR NOT


def main(argv):

    ###

    # GLOBAL VAR TO SET MAX WAYPOINTS DRONE APPS USE FOR AUTOMATED FLIGHTS
    MAXPOINTS = 99

    # BOOL MESSAGE OF THERE BEING A LL.KML OR NOT IN THE DIRECTORY
    lCheck = int(argv[0])

    # GETTING CURRENT PATH WITH OS
    Current_Path = os.getcwd()
    direc = os.path.dirname(__file__)
    # 0 FOR LL.KML TRUE, 1 FOR LL.KML FALSE
    if lCheck < 1:

        # YES LL.KML
        # GETTING PATHS FOR LL AND POLY JSON GENERATED BY BASH SCRIPT
        path1 = os.path.join(direc, Current_Path +
                             '/ll.json')
        path2 = os.path.join(
            direc, Current_Path+'/poly.json')
        with open(path1, 'r') as afile:
            lldata = afile.read()
        with open(path2, 'r') as myfile:
            polydata = myfile.read()

        # NOW WE USE THE JSON LIBRARY MODULES TO INDEX TO THE COORDINATES
        # WE WANT TO PUT INTO 2D LISTS THAT ARE LOADED INTO SHAPELY OBJECTS
        l_ll = json.loads(lldata)
        l_poly = json.loads(polydata)
        l = l_ll['features'][0]['geometry']['coordinates']
        polygo = l_poly['features'][0]['geometry']['coordinates'][0]

        # BEFORE LOADING INTO SHAPELY OBJECT, WE NEED TO MAKE SURE WE ARE
        # GETTING THE COORDINATES EMBEDDED IN THE JSON STRUCTURE
        polygon = []
        for coords in polygo:
            if type(coords[0]) == float:
                polygon.append(coords[:2])
            elif type(coords[0]) == list:
                for coos in coords:
                    if type(coos[0]) == float:
                        polygon.append(coos[:2])
    else:

        # NO LL.KML
        # GETTING PATHS FOR POLY JSON GENERATED
        path2 = os.path.join(
            direc, Current_Path+'/poly.json')
        with open(path2, 'r') as myfile:
            polydata = myfile.read()

        # NOW WE USE THE JSON LIBRARY MODULES TO INDEX TO THE COORDINATES
        # WE WANT TO PUT INTO 2D LISTS
        l_poly = json.loads(polydata)
        p = l_poly['features'][0]['geometry']['coordinates'][0][:2]

        # BEFORE LOADING INTO SHAPELY OBJECT, WE NEED TO MAKE SURE WE ARE
        # GETTING THE COORDINATES EMBEDDED IN THE JSON STRUCTURE
        polygo = l_poly['features'][0]['geometry']['coordinates'][0]
        polygon = []
        for coords in polygo:
            if type(coords[0]) == float:
                polygon.append(coords[:2])
            elif type(coords[0]) == list:
                for coos in coords:
                    if type(coos[0]) == float:
                        polygon.append(coos[:2])

        # MAKING DUMMY LL.KML AS FIRST POINT IN KML.KML POLYGON
        l = (polygon[0][0], polygon[0][1])

    """
    HERE WE WANTS TO MAKE AN INNER TRACE OF THE POLYGON AND STORE
    EACH TRACE IN A LIST TO APPEND TO FINAL PATH. TRACES WILL STOP
    ONCE THE PARALLEL_OFFSET FUNCTION GENERATES A TOO SMALL OF A PATH
    OR A MULTILINESTRING. THE ELSE STATEMENT WILL KILL THE PROGRAM AND
    ALSO ADD THE CENTROID POINTS OF THE FIRST PAIRS OF LINESTRINGS IN
    THE MULTILINESTRING TO ADD ADDITIONAL COVERAGE OF THE FIELD WHERE
    THE TRACES MAY NOT HAVE REACHED TO CENTERPOINTS
    """
    # J IS KILL SWITCH AND I IS ITERATOR
    j = 0
    i = 1

    # PATHS WILL CONTAIN THE TRACES
    paths = []
    dist = 0.0
    centerPoints = []
    checkFirst = 0

    # INDEX AND VALUE ARE NEEDED TO ADD FURTHEST POINT
    # FIRST THEN CLOSER SECOND TO CENTERPOINTS. K IS
    # NEEDED TO MAKE SURE LAST TRACE IS A MULTILINESTRING
    closer_Index = 0
    closer_Distance = 1000.0

    # INDEX OF CLOSER CENTERPOINT
    k = 0
    while j < 1:

        # TO AVOID GOING OVER 99 POINTS, WE SIMPLIFY THE POLYGON
        # TO CREATE A POLYGON WITH LESSER POINTS.
        # NOT SO GOOD FOR CIRCLES UNFORTUNATELY
        # PATH WILL BE OUR LINESTRING OBJECT WE OPERATE UPON WITH SHAPELY FUNCTIONS
        if len(polygon) > 12:
            path = LineString(polygon).simplify(.0005)
        else:
            path = LineString(polygon)
    #    print(type(path))
        # MAKE SURE OUR TRACES ARE WITHIN THE ORIGINAL POLYGON, SO WE GENERATE A POINT TO CHECK IF ITS WITHIN THE POLYGON
        tempPath = path.parallel_offset(
            45/111194.927, side='right', resolution=16, join_style=2, mitre_limit=1)
        checkP = Point(tempPath.coords[0])
        direction = ''
        if checkP.within(Polygon(path.coords)):
            direction = 'right'
            # IF FIRST TRACE, THEN WE ONLY GO 25 METERS INTO THE POLYGON, ELSE 60 METERS INTO THE POLYGON.
            if checkFirst < 1:
                path_a = path.parallel_offset(
                    (boundaryDistance)/111194.927, side='right', resolution=16, join_style=2, mitre_limit=1)
                checkFirst = 1
            else:
                path_a = path.parallel_offset(((passDistance*(i-1)) + boundaryDistance) /
                                              111194.927, side='right', resolution=16, join_style=2, mitre_limit=1)
        else:
            direction = 'left'
            if checkFirst < 1:
                path_a = path.parallel_offset(
                    (boundaryDistance)/111194.927, side='left', resolution=16, join_style=2, mitre_limit=1)
                checkFirst = 1
            else:
                path_a = path.parallel_offset(((passDistance*(i-1)) + boundaryDistance) /
                                              111194.927, side='left', resolution=16, join_style=2, mitre_limit=1)

        # CALCULATE THE AREA IN ACRES OF THE POLYGON WITH SHAPELY OPS AND PYPROJ
        # TO FIND OUT OUR ALLOWANCE OF DISTANCE FOR THE 1IMAGE/1ACRE METRIC FOR OUR BUSINESS
        areaPoly = Polygon(polygon)
        geom_area = ops.transform(partial(pyproj.transform, pyproj.Proj(init='EPSG:4326'), pyproj.Proj(
            proj='aea', lat1=areaPoly.bounds[1], lat2=areaPoly.bounds[3])), areaPoly)
        Acres = float(geom_area.area/4046.86)

        # ASSUME MAX DRONE SETTINGS FOR TARANIS OPS (60 METERS/1IMAGE/1ACRES) * ACRES = MAXDIST
        maxDist = passDistance*Acres

        # CHECK TO MAKE SURE WE KNOW THE TYPE OF OBJECT THAT WAS GENERATED BY THE PARALLEL OFFSET MODULE
        checker = path_a.geom_type

        # INCREMENTER TO KEEP TRACK OF THE SUM OF TOTAL DISTANCE OF TRACES
        dist += path_a.length

        # DIFFERENCE THE DISTANCE OF RETURN FROM THE TOTAL SUM OF DISTANCE
        centD = Point(l).distance(Point(Polygon(polygon).centroid))
        distCheck = dist - centD

        # CONDITIONS TO MAKE SURE WE DONT GO PAST OUR ALLOWANCE OF DISTANCE and DONT EXPECT ANY MULTILINESTRINGS
        if distCheck < maxDist and checker != 'MultiLineString' and path_a.length > 0:

            # CASTING LIST TO COORDS SINCE TRACE LINESTRING IS IMMUTABLE
            temp = list(path_a.coords)

#            dude = unifer(temp, wpDistribution)

            temp = unifer(temp, wpDistribution)

            # FINDING CLOSEST DISTANCE IN TRACE TEMP TO MAKE AS HEAD OF LIST
            CP = 0
            CP_Distance = 2000.0
            for index, coord in enumerate(temp):
                point = Point(coord)
                p_Distance = point.distance(Point(l))
                if p_Distance < CP_Distance:
                    CP = int(index)
                    CP_Distance = p_Distance

            # POLYGONS HEAD AND TAIL IS SAME POINT SO WE NEED TO CUTT OFF TAIL BEFORE SHIFTING
            temp = temp[:len(temp)-1]

            # CHEEKY PYTHON SHIFT. CLOSEST POINT IS NOW HEAD
            temp = temp[CP:] + temp[:CP]

            # HEAD IS NOT TAIL AGAIN TO SIGNIFY POLGON
            temp.append(temp[0])

    #        print("Coords After in FPA: ", temp)
    #        print("Size After: ", len(temp))
            # REVERSE PATH EVERY OTHER TRACES DIRECTION FOR SMOOTHER TRANSITIONS BETWEEN TRACES
            check = i % 2
            if check == 1:
                temp = temp[::-1]
    #        print("Size After: ", len(temp))

            """	
            #MAKE SURE OUR TRACES ARE WITHIN THE ORIGINAL POLYGON, SO WE GENERATE A POINT TO CHECK IF ITS WITHIN THE POLYGON
            tempPath = path.parallel_offset(45/111194.927, side='right', resolution=16, join_style=2, mitre_limit=1)
            checkP = Point(tempPath.coords[0])
            if checkP.within(Polygon(path.coords)):
            """

            # ADD TO PATHS
            paths.append(temp)
            i += 1
        else:
            # KILLSWITCH ENGAGED
            j = 1

            # WE ONLY WANT CENTROIDS OF MULITLINE STRING IF LAST TRACE WAS ONE.
            if path_a.geom_type != "LineString":

                # APPEND THEIR CENTROIDS TO CENTERPOINTS LIST
                for pathys in path_a:
                    centerPoints.append(pathys.centroid)

                    # UPDATE CLOSER POINT IN CENTER POINTS
                    if Point(l).distance(pathys.centroid) < closer_Distance:
                        closer_Index = k
                        closer_Distance = float(
                            Point(l).distance(pathys.centroid))
                    k += 1
    # INITIALIZE FINAL PATH WE WILL LOAD INTO JSON FILE
    finalPath = []

    # ADD LAUNCH LOCATION AS FIRST POINT
    finalPath.append(l[:2])

    # ADD TRACES FROM PATHS
    for path in paths:
        for coos in path:
            finalPath.append(coos)
    # ADD CENTERPOINTS FROM FURTHEST TO CLOSEST
   
    if k > 0:
        if closer_Index < 1:
            finalPath.append(list(centerPoints[1].coords)[0])
            finalPath.append(list(centerPoints[0].coords)[0])
        else:
            finalPath.append(list(centerPoints[0].coords)[0])
            finalPath.append(list(centerPoints[1].coords)[0])
    # ADD LAUNCH LOCATION AS LAST POINT
    finalPath.append(l[:2])

    # CAST FINALPATH TO LINSTRING
    FinalPath = LineString(finalPath)

    # LOAD FINALPATH TO JSON FILE
    features = []
    features.append(Feature(geometry=FinalPath))
    with open('finalPath.json', 'w') as f:
        dump(FinalPath, f)


# CLI FOR BASH SCRIPT
if __name__ == "__main__":
    main(sys.argv[1:])
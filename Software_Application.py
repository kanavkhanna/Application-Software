import googlemaps
import simplejson as json
from beautifultable import BeautifulTable, rows
import pprint
from datetime import datetime
from itertools import combinations
import numpy as np



gmaps = googlemaps.Client(key='AIzaSyCy2DiVqaEdiaHRfr_ZRwNXsBjYD_Duw4k')
distanceMatrix = []  # travel time bw stations
oToMetro = []
metroToD = []


def geocodeToCoordinates(geocode):
    coordDict = geocode[0]['geometry']['location']
    return (coordDict['lat'], coordDict['lng'])


def getNearbyMetroStations(location):
    """returns the five nearest metro stations"""
    geocode = gmaps.geocode(location)
    coordinates = geocodeToCoordinates(geocode)

    stations = gmaps.places_nearby(keyword='metro', location=coordinates, rank_by='distance', type='subway_station')[
        'results']

    return stations[:4]


def getDrivingTime(origin, destination):
    return gmaps.directions(origin, destination)[0]['legs'][0]['duration']


def getIDs(geocodes):
    foo = []
    for geocode in geocodes:
        foo.append('place_id:' + geocode['place_id'])
    return foo


def getTravelTime(origin, destination):
    global distanceMatrix
    global oToMetro
    global metroToD

    oStations = getNearbyMetroStations(origin)
    dStations = getNearbyMetroStations(destination)


    originID = 'place_id:' + gmaps.geocode(origin)[0]['place_id']
    destinationID = 'place_id:' + gmaps.geocode(destination)[0]['place_id']

    origins = getIDs(oStations)
    destinations = getIDs(dStations)

    oToMetro = gmaps.distance_matrix(originID, origins)
    metroToD = gmaps.distance_matrix(destinations, destinationID)

    #pprint.pprint(oToMetro)
    #pprint.pprint(metroToD)

    distanceMatrix = gmaps.distance_matrix(origins, destinations, mode='transit', transit_mode='subway')

    table = BeautifulTable()
    headers = []
    for i in range(1, 5):
        headers.append('d' + str(i))
    table.column_headers = headers

    r, c = 0, 0
    for row in distanceMatrix['rows']:
        temp = []
        for col in row['elements']:
            temp.append(col)
        table.append_row(temp)


    return oToMetro, distanceMatrix, metroToD


def result(value):
    #origin = 'moolchand metro station, new delhi'
    #destination = 'ambience mall, gurgaon, delhi, new delhi'
    #value = getTravelTime(origin, destination)
    a = []
    b = []
    c = []

    for i in range(0, 4):
        a.append(value[0]['rows'][0]['elements'][i]['duration']['value'])

    # print(a)


    for i in range(0, 4):
        for j in range(0, 4):
            b.append(value[1]['rows'][i]['elements'][j]['duration']['value'])

    # print(b)


    for i in range(0, 4):
        c.append(value[2]['rows'][i]['elements'][0]['duration']['value'])

    # print(c)

    for i in range(0, 2):
        a = np.append(a, a)
        c = np.append(c, c)

    d = np.add(a, b)
    d = np.add(c, d)

    # print(d)
    min_val = np.min(d)
    ctr = 0
    for i in range(len(d)):
        if min_val == d[i]:
            ctr = i

    return (value[0]['origin_addresses'][0], ' to ', value[0]['destination_addresses'][int(ctr / 4)], ' to ',
          value[1]['destination_addresses'][int(ctr / 4)], ' to ', value[2]['destination_addresses'][0]), ("It will take", int(min_val / 60), 'minutes')

def main():
    origin = input("Enter origin")
    destination = input("Enter destination")
    value = getTravelTime(origin, destination)
    output=result(value)

    print(output)


if __name__ == "__main__":
    main()
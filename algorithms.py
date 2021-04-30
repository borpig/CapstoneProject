# TO DO : Write algorithms 
from common import distance, bus_stop_from_smallest_dist, sort_list_of_strings
from datastore import DataStore
from random import uniform

def add_distance_to_dict(user_latitude, user_longitude, bus_stops_data):
    """ This method modifies the bus stop list of dictionaries 
    and adds the distance of the bus stop from the user to each record.
    """
    for data in bus_stops_data:
        if "Distance" in data:
            del data["Distance"] # this deletes the existing distance data
    for data in bus_stops_data:
        dist = distance(user_latitude, user_longitude, data["Latitude"], data["Longitude"])
        data["Distance"] = dist # add all the respective distance into the data in the list of data
    return bus_stops_data

def quickSort(busdata):
    """ Sorting the bus data which is in a list of dicts, according to the shortest distance from 
    user input latitude and longitude. """
    if len(busdata) <= 1: #base case
        return busdata
    else:
        left = []
        right = []
        pivot = busdata[-1] # choosing last bus service (type: dictionary) as the pivot.
        for i in range(len(busdata)-1):
            if busdata[i]["Distance"] < pivot["Distance"]:
                left.append(busdata[i])
            else:
                right.append(busdata[i])
        left = quickSort(left) # recursive algorithm
        right = quickSort(right)
        return left + [pivot] + right

def linearSearchforbus(bus_routes_data, BusStopCode):
    """Search for bus services that ply through the bus stop that is closest to the user.
    Uses linear search algorithm."""
    same_stop_services = []
    for bus_route in bus_routes_data:
        if bus_route["BusStopCode"] == BusStopCode:
            same_stop_services.append(bus_route["ServiceNo"])
    same_stop_services = list(set(same_stop_services))
    return same_stop_services

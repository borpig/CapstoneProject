import geopy.distance
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="http")
def distance(user_latitude, user_longitude, stop_latitude, stop_longitude):
    """
    Takes in current longitude and latitude x and y in either float or,
    integer form and the
    x and y latitude and longitude of the end location as a tuple of floats 
    or integers,
    returns a float value of the distance between the 
    current and the end latitude and longitude. 
    """
    user_coord = (user_latitude, user_longitude)
    bus_stop_coord = (stop_latitude, stop_longitude)
    return geopy.distance.distance(user_coord, bus_stop_coord).km

def dict_from_row(row):
    """
    Function that helps convert row data
    from sqlite fetchall method to a dictionary,
    which can then be used for useful purposes.
    """
    return dict(zip(row.keys(), row))

def bus_stop_from_smallest_dist(busdata):
    """
    Method that returns the bus stop code of
    the bus stop that is nearest to the input coordinates.
    """
    return busdata[0]["BusStopCode"]

def location_of_smallest_bus_stop(busdata):
    """
    Method that returns the description of
    the bus stop that is nearest to the input coordinates.
    """
    return busdata[0]["Description"]

def lat_long_of_smallest_bus_stop(busdata):
    return (busdata[0]["Latitude"], busdata[0]["Longitude"])

def sort_list_of_strings(list):
    """
    Method that helps to sort a list of numbers 
    that are in the form of a list. For example,
    there is a list with 74, 73A and 73, and this function
    will help to sort those bus services out and return them in
    a list of strings of bus services.
    """
    return sorted(list, key=lambda x: int("".join([i for i in x if i.isdigit()])))

def location_from_address(address):
    """
    Useful module that helps to retrieve the exact location
    address, latitude and longitude from the input address.
    """
    location = geolocator.geocode(address)
    return location.address, location.latitude, location.longitude


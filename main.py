# Lim Jian San - Capstone Project V1

from flask import Flask, render_template, request, redirect
from datastore import DataStore
from algorithms import quickSort, linearSearchforbus, add_distance_to_dict
from common import distance, bus_stop_from_smallest_dist, location_of_smallest_bus_stop, sort_list_of_strings, location_from_address, lat_long_of_smallest_bus_stop
from validation import valid_latitude, valid_longitude, valid_address
import csv, json

app = Flask("JS Singapore Bus App")
URI = 'busdata.db'

datastore = DataStore(URI)
bus_stops_data = datastore.get_data("Stops") # retrieving bus stop data from database
bus_routes_data = datastore.get_data("Routes") # retrieving bus route data from database
datastore.init_service()

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/manual')
def manual():
    return render_template('manual.html')

@app.route('/address')
def address():
    return render_template('address.html')

@app.route('/results', methods=['GET'])
def results():
    err = None
    if "user_latitude" in request.args and "user_longitude" in request.args:
        user_latitude = request.args["user_latitude"]
        user_longitude = request.args["user_longitude"]
        if valid_latitude(user_latitude) and valid_longitude(user_longitude):
            bus_stops_data_with_dist = add_distance_to_dict(user_latitude, user_longitude, bus_stops_data)
            bus_stops_data_sorted = quickSort(bus_stops_data_with_dist)
            smallest_bus_stop = bus_stop_from_smallest_dist(bus_stops_data_sorted)
            location = location_of_smallest_bus_stop(bus_stops_data_sorted)
            stop_lat, stop_long = lat_long_of_smallest_bus_stop(bus_stops_data_sorted)
            common_bus_services = linearSearchforbus(bus_routes_data, smallest_bus_stop)
            common_bus_services_sorted = sort_list_of_strings(common_bus_services) # this should be a list of strings of bus services.
            return render_template("results.html", stop_lat=stop_lat, stop_long=stop_long, user_latitude=user_latitude, user_longitude=user_longitude, 
            bus_stop=smallest_bus_stop, bus_stop_desc=location, available_buses=common_bus_services_sorted)
        else:
            err = True
            return render_template("manual.html", err=err)
    else:
        return redirect("/")

@app.route('/result', methods=['GET'])
def result():
    err = None
    if "address" in request.args:
        user_address = request.args["address"]
        if valid_address(user_address):
            address, user_latitude, user_longitude = location_from_address(user_address)
            bus_stops_data_with_dist = add_distance_to_dict(user_latitude, user_longitude, bus_stops_data)
            bus_stops_data_sorted = quickSort(bus_stops_data_with_dist)
            smallest_bus_stop = bus_stop_from_smallest_dist(bus_stops_data_sorted)
            location = location_of_smallest_bus_stop(bus_stops_data_sorted)
            stop_lat, stop_long = lat_long_of_smallest_bus_stop(bus_stops_data_sorted)
            common_bus_services = linearSearchforbus(bus_routes_data, smallest_bus_stop)
            common_bus_services_sorted = sort_list_of_strings(common_bus_services) # this should be a list of strings of bus services.
            return render_template("result.html", stop_lat=stop_lat, stop_long=stop_long, address=address, user_latitude=user_latitude, user_longitude=user_longitude, 
            bus_stop=smallest_bus_stop, bus_stop_desc=location, available_buses=common_bus_services_sorted)
        else:
            err = True
            return render_template("address.html", err=err)
    else:
        return redirect("/")

@app.route('/help', methods=['GET'])
def help():
    return render_template("help.html")
    
app.run(debug=True)
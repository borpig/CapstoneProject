import sqlite3, json
from common import dict_from_row

SQL = {"delete_services": """ DELETE from Services""",
"delete_routes": """ DELETE from Routes """, 
"delete_stops": """ DELETE from Stops """,
"insert_routes": """ INSERT INTO Routes VALUES
            (?, ?, ?);""",
"insert_services": """ INSERT INTO Services VALUES
            (?, ?, ?, ?);""",
"insert_stops": """ INSERT INTO Stops("BusStopCode", "Description", "Latitude", "Longitude") VALUES
            (?, ?, ?, ?);"""}

class DataStore:
    def __init__(self, uri):
        self.uri = uri 
    
    def get_conn(self):
        """
        Creates and returns an sqlite3
        connection object.
        """
        conn = sqlite3.connect(self.uri)
        conn.row_factory = sqlite3.Row
        return conn
        
    def load_json(self, filename):
        """
        Data from json file is deserialised into a dictionary.
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data_dict = json.load(f)
        return data_dict
    
    def get_status_sql(self, tablename):
        """
        SQL command that obtains all the information
        from the particular table. Used in the get_data
        method.
        """
        status_sql = f""" SELECT * FROM {tablename}"""
        return status_sql

    def get_data(self, tablename):
        """
        Receives the table name as a string,
        returns the records from each row in the 
        table as a list of dictionaries.
        """
        conn = self.get_conn()
        c = conn.cursor()
        status_sql = self.get_status_sql(tablename)
        c.execute(status_sql)
        results = c.fetchall()
        data = []
        for row in results:
            data.append(dict_from_row(row))
        conn.commit()
        conn.close()
        return data

    def init_service(self):
        """
        This method abstracts the methods involved in 
        loading the json files, creating the tables into 
        the database, and then putting information from the json
        files into the respective tables.
        """
        conn = self.get_conn()
        c = conn.cursor()
        c.execute(SQL["delete_services"])
        c.execute(SQL["delete_stops"])
        c.execute(SQL["delete_routes"])
        bus_routes = self.load_json("bus_routes.json")
        bus_services = self.load_json("bus_services.json")
        bus_stops = self.load_json("bus_stops.json")
        c.executescript("""
        CREATE TABLE IF NOT EXISTS "Stops" (
            "id"	INTEGER,
            "BusStopCode"	TEXT,
            "Description"	TEXT,
            "Latitude" REAL,
            "Longitude" REAL,
            PRIMARY KEY("id")
        );
        CREATE TABLE IF NOT EXISTS "Services" (
            "ServiceNo"	TEXT,
            "Operator"	TEXT,
            "Direction"	INTEGER,
            "Category"	TEXT,
            PRIMARY KEY("ServiceNo","Direction")
        );
        CREATE TABLE IF NOT EXISTS "Routes" (
            "ServiceNo"	TEXT,
            "Direction"	INTEGER,
            "BusStopCode"	TEXT,
            FOREIGN KEY("BusStopCode") REFERENCES "Stops"("BusStopCode"),
            FOREIGN KEY("ServiceNo") REFERENCES "Services"("ServiceNo")
        );""")
        print("Tables successfully created.")
        for route in bus_routes:
            c.execute(SQL["insert_routes"], (route["ServiceNo"], route["Direction"], route["BusStopCode"]))
        for service in bus_services:
            c.execute(SQL["insert_services"], (service["ServiceNo"], service["Operator"], service["Direction"], 
            service["Category"]))
        for stop in bus_stops:
            c.execute(SQL["insert_stops"], (stop["BusStopCode"], stop["Description"], stop["Latitude"], stop["Longitude"]))
        conn.commit()
        conn.close()



        
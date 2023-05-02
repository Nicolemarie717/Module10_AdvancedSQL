# Import the dependencies.

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/nicol/OneDrive/Data Science/Resources/Module_10_AdvancedSQL/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available api routes."""
    return(
        f"Hawaii Climate Analysis Homepage with the Available Routes:<br/>"
        f"<br/>"
        f"Precipitation Data for One Year:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Active Weather Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observations of the Most-Active Station for One Year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"The Minimum, Maximum, and Average Temperature for a specified Start Date(Format:yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"The Minimum, Maximum, and Average Temperatures for a specified Start and End Date(Format:yyyy-mm-dd/yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start>/<end>"
    )


# your Flask application must include a precipitation route that returns json with the date as the key and the value as the precipitation 
# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago_date).all()
    session.close()

# Only returns the jsonified precipitation data for the last year in the database
# dictionary 
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)
        
    return jsonify(prcp_data)

# your Flask application must include a stations route that returns jsonified data of all of the stations in the database
# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine) # define session object
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()


    # dictionary
    stations_data = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations_data.append(station_dict)

    session.close() # close session object
    return jsonify(stations_data)


# your Flask application must include a tobs route that returns jsonified data for the most active station (USC00519281)
# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def active_station():
    session = Session(engine)
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    session.close()

    # Convert the result of the query to a list of dictionaries
    active_stations_list = []
    for station, count in active_stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["count"] = count
        active_stations_list.append(station_dict)

    # Return the result in JSON format
    return jsonify(active_stations_list)
    

# your Flask application must include a start route that:
# accepts the start date as a parameter from the URL 
# returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
#/api/v1.0/<start>
    
# return jsonify(start_date)
@app.route('/api/v1.0/<start>')
def start(start): 
    start_date = datetime.strptime(start, '%Y-%m-%d')
    
    session = Session(engine)
    query_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    session.close()

    start_temps = []
    for min_temp, max_temp, avg_temp in query_results:
        start_dict = {}
        start_dict["Minimum Temperature"] = min_temp
        start_dict["Maximum Temperature"] = max_temp
        start_dict["Average Temperature"] = avg_temp
        start_temps.append(start_dict)
    
    return jsonify(start_temps)

# your Flask application must include a start/end route that: 
# accepts the start and end dates as parameters from the URL
# returns the min, max, and average temperatures calculated from the given start date to the given end date 
# /api/v1.0/<start>/<end>
@app.route('/api/v1.0/<start>/<end>')
def range_date(start, end):
    # convert date strings to datetime objects
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    
    # create session and query for temperature range
    session = Session(engine)
    query_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date, measurement.date <= end_date).all()
    session.close()
    
    # create dictionary for temperature range
    range_date = []
    for min_temp, max_temp, avg_temp in query_results:
        range_dict = {}
        range_dict["Minimum Temperature"] = min_temp
        range_dict["Maximum Temperature"] = max_temp
        range_dict["Average Temperature"] = avg_temp
        range_date.append(range_dict)
    
    return jsonify(range_date)

if __name__ == '__main__':
    app.run(debug=True)
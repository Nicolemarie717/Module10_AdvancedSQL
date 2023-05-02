# Import the dependencies.

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
Measurement = Base.classes.measurement
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
        f"Temperature Observations of the Most-Active Station for One Year:,br/>"
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
    session = Session(engine)
    stations = sessions.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    
# dictionary 
    station_data = []
    for name, station, elevation, latitude, longitude in stations:
        station_dict = {}
        station_dict["Station ID"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["Elevation"] = elevation
        station_data.append(station_dict)
        
    return jsonify(station_data)

# your Flask application must include a tobs route that returns jsonified data for the most active station (USC00519281)
# /api/v1.0/tobs



# your Flask application must include a start route that:
# accepts the start date as a parameter from the URL 
# returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
#/api/v1.0/<start>
@app.route('/api/v1.0/<start>')
def start(start): 
    session = Session(engine)
    query_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()
    
#dictionary 
start_date = []
for min,max, avg in query_results:
    start_dict = {}
    start_dict["Minimum Temperature" = min]
    start_dict["Maximum Temperature"] = max
    start_dict["Average Temperature"] = avg
    start_date.append(start_dict)
    
return jsonify(start_dict)

# your Flask application must include a start/end route that: 
# accepts the start and end dates as parameters from the URL
# returns the min, max, and average temperatures calculated from the given start date to the given end date 
# /api/v1.0/<start>/<end>
@app.route('/api/v1.0/<start>/<end>')
def range_date(start,end): 
    session = Session(engine)
    query_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()
    
#dictionary 
range_date = []
for min, max, avg in query_results: 
    range_dict = {}
    range_dict["Minimum Temperature"] = min
    range_dict["Maximum Temperature"] = max 
    range_dict["Average Temperature"] = avg
    range_date.append(range_dict)
    
return jsonify(range_date)


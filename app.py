# Import dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

############################################################
# Set up database.
############################################################

# Create engine to hawaii.sqlite (source: SQLAlchemy.ipynb file).
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model (source: SQLAlchemy.ipynb file).
Base = automap_base()

# Reflect the tables (source: SQLAlchemy.ipynb file).
Base.prepare(autoload_with=engine, reflect=True)

# Save references to each table (source: SQLAlchemy.ipynb file).
measurement = Base.classes.measurement
station = Base.classes.station

############################################################
# Set up flask app.
############################################################

# Create app.
app = Flask(__name__)

# Define action for user request for index route.
@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"AVAILABLE ROUTES:<br/>"
        f"<br/>"
        f"Precipitation data with dates:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Stations and names:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature observations from the Waihee station:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Minimum, average, and maximum temperatures for a given date (please use format yyyy-mm-dd):<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"<br/>"
        f"Minimum, average, and maximum temperatures for a given start and end dates (please use format yyyy-mm-dd):<br/>"
        f"/api/v1.0/start:yyyy-mm-dd/end:yyyy-mm-dd")

############################################################

# Define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create session from python to the database.
    session = Session(engine)
    
    """Return a list of all precipitation data"""
    
    # Query precipitation data (source: SQLAlchemy.ipynb file).
    precip = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-24").all()
    
    session.close()

    # Convert the returned list to a dictionary.
    precip_all = []
    for date,prcp in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        
        precip_all.append(precip_dict)
    
    return jsonify(precip_all)

############################################################

# Define station route.
@app.route("/api/v1.0/stations")
def stations():
    
    # Create session from python to the database.
    session = Session(engine)
    
    """Return a list of all stations"""
    # Query station data 
    stations = session.query(station.station, station.name).all()
    
    session.close()
    
    # Convert list into
    station_list = list(np.ravel(stations))
    
    return jsonify(station_list)

############################################################

# Define TOBs route.
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create session from python to the database.
    session = Session(engine)
    
    """Return a list of all TOBs"""
    # Query tobs data.
    tobs_results = session.query(measurement.date, measurement.prcp, measurement.tobs).\
        filter(measurement.station=='USC00519281').\
        filter(measurement.date >= '2016-08-24').all()

    session.close()

    # Convert the returned list to a dictionary.
    tobs_all = []
    for date, prcp, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['prcp'] = prcp
        tobs_dict['tobs'] = tobs
        
        tobs_all.append(tobs_dict)

    return jsonify(tobs_all)

############################################################

# Define start d ate route.
@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    
    # Create session from python to the database.
    session = Session(engine)
    
    """Return a list of minimum, average, and maximum temperature observations for a start date"""
    # Query tobs data.
    tobs_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    
    session.close()

    # Convert the returned list to a dictionary.
    start_tobs = []
    for min, avg, max in tobs_results:
        start_tobs_dict = {}
        start_tobs_dict['min_temp'] = min
        start_tobs_dict['avg_temp'] = avg
        start_tobs_dict['max_temp'] = max
        start_tobs.append(start_tobs_dict)

    return jsonify(start_tobs)

############################################################

# Define start/end date route.
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
                                                                                                        
    # Create session from python to the database.
    session = Session(engine)

    """Return a list of minimum, average, and maximum temperature observations for start and end dates"""

    tobs_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()

    # Create a list for results.
    start_end_list = []
    for min, avg, max in tobs_results:
        list = {}
        list['min_temp'] = min
        list['avg_temp'] = avg
        list['max_temp'] = max
        start_end_list.append(list)

    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
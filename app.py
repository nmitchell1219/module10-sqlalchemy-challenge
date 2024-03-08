# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)
#################################################
# Flask Setup
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"



#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation data"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)
    
    @app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station data"""
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations (TOBS) for the previous year"""
    # Query the dates and temperature observations of the most active station for the last year of data.
    # Assuming you have a variable `last_date` which is the last date of data in your dataset and a variable `most_active_station`
    results = session.query(Measurement.tobs).\
              filter(Measurement.station == most_active_station).\
              filter(Measurement.date >= one_year_ago).all()

    # Convert the list of tuples into a normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)
    
    @app.route("/api/v1.0/<start>")
def start_date(start):
    """Fetch the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date"""
    # Query all the stations and for each station, and calculate MIN, AVG, and MAX temperature for all dates greater than and equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()

    # Convert the result into a list
    temps = list(np.ravel(results))

    return jsonify(temps=temps)@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Fetch the minimum temperature, the average temperature, and the max temperature for dates between the start and end date inclusive."""
    # Query all the stations and for each, calculate MIN, AVG, and MAX temperature for dates between the start and end date inclusive
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).\
              filter(Measurement.date <= end).all()

    # Convert the result into a list
    temps = list(np.ravel(results))

    return jsonify(temps=temps)





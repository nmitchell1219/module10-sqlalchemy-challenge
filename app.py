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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

    return '''
        <h2>Available Routes:</h2>
        <ol>
            <li>/api/v1.0/precipitation</li>
            <li>/api/v1.0/stations</li>
            <li>/api/v1.0/tobs</li>
            <li>/api/v1.0/[start]</li>
            <li>/api/v1.0/[start]/[end]</li>
        </ol>
    '''



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
    results = session.query(Station.station,Station.name).all()

    return [ {id:loc} for id,loc in results ]

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations (TOBS) for the previous year"""
    # Query the dates and temperature observations of the most active station for the last year of data.
    # Assuming you have a variable `last_date` which is the last date of data in your dataset and a variable `most_active_station`
    results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()

    return [ {d:t} for d,t in results ]

    
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateRange(start,end='2017-08-23'):
    """Fetch the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date"""
    # Query all the stations and for each station, and calculate MIN, AVG, and MAX temperature for all dates greater than and equal to the start date

    results = session.query(
        func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)).\
    filter((Measurement.date >= start)&(Measurement.date<=end)).first()

    # Convert the result into a list
    return {'date_range':f'{start} to {end}','Min':results[0],'Avg':results[1],'Max':results[2]}

if __name__ == "__main__": app.run(debug=True)


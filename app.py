import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        
    )


@app.route("/api/v1.0/precipitation")
def prcp():
   
    # Query all dates with matching precip for that date
    results = session.query(Measurement.date, Measurement.prcp).all()
    prcp1 = []
    for prcp in results:
        prcp_dict={}
        prcp_dict["date"]=prcp.date
        prcp_dict["precip"]=prcp.prcp
        prcp1.append(prcp_dict)
    return jsonify(prcp1)


@app.route("/api/v1.0/stations")
    # Query all station names
def stat():
    results1 = session.query(Measurement.station).all()
    station = []
    for stat in results1:
        stat_dict={}
        stat_dict["station"]=stat.station
        
        station.append(stat_dict)
    return jsonify(station)

@app.route("/api/v1.0/tobs")
    # Query all dates with matching temp for that date
def temp():
   # Perform a query to retrieve the data and precipitation scores
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    temps = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date > query_date).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
    tobs_yr = []
    for tmp in temps:
        
        temps_dict={}
        temps_dict["date"]=tmp.date
        temps_dict["tobs"]=tmp.tobs
        tobs_yr.append(temps_dict)
        
   
    return jsonify(tobs_yr)

@app.route("/api/v1.0/<start>")
def tobs_start(start):
    
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        
        tobs_yr = []
        for temp in temps:
            temps_dict={}
            
            temps_dict["Min"]=temp[0]
            temps_dict["Avg"]=temp[1]
            temps_dict["Max"]=temp[2]
            tobs_yr.append(temps_dict)
        return jsonify(tobs_yr)
    
@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start,end):
    
        temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

        
        tobs_yr = []
        for temp in temps:
            temps_dict={}
            
            temps_dict["Min"]=temp[0]
            temps_dict["Avg"]=temp[1]
            temps_dict["Max"]=temp[2]
            tobs_yr.append(temps_dict)
        return jsonify(tobs_yr)
    
if __name__ == '__main__':
    app.run(debug=True)

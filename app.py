from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np 
import pandas as pd 
import datetime as dt 


engine=create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Climate App API Home Page</br>"
        f"The available routes are:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/starting_day</br>"
        f"/api/v1.0/trip_duration"
    )

@app.route("/api/v1.0/precipitation")
def precipitaion():
    precipitations=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-23').order_by(Measurement.date)
    session.close()
    
    all_prcp=[]
    for date, prcp in precipitations:
        prcp_dictionary={}
        prcp_dictionary["date"]=date
        prcp_dictionary["prcp"]=prcp
        all_prcp.append(prcp_dictionary)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    station_data=session.query(Station.station).all()
    all_station=list(np.ravel(station_data))
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def temperature():
    annual_tobs=[]
    tobs_data=session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    annual_tobs=list(np.ravel(tobs_data))
    return jsonify(annual_tobs)

@app.route("/api/v1.0/starting_day")
def start():
    date_start = '2011-02-28'
    t_details = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date_start)

    all_temps=[]
    for date, tmin, tavg, tmax in t_details:
        temp_dictionary={}
        temp_dictionary["Date"]=date
        temp_dictionary["Min T"]=tmin
        temp_dictionary["Avg T"]=tavg
        temp_dictionary["Max T"]=tmax
        all_temps.append(temp_dictionary)

    return jsonify(all_temps)

@app.route("/api/v1.0/trip_duration")
def start_end():
    date_start = '2011-02-28'
    date_end = '2011-03-05'
    t_details = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date.between(date_start, date_end))

    all_temps=[]
    for date, tmin, tavg, tmax in t_details:
        temp_dictionary={}
        temp_dictionary["Date"]=date
        temp_dictionary["Min T"]=tmin
        temp_dictionary["Avg T"]=tavg
        temp_dictionary["Max T"]=tmax
        all_temps.append(temp_dictionary)

    return jsonify(all_temps)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np 
import pandas as pd 
import datetime as dt 


engine=create_engine("sqlite://hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect-True)

Measurment = Base.classes.measurement
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
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitaion")
def precipitaion():
    one_year_query="08-23-2016"
    precipitations=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=one_year_query).order_by(Measurement.date)
    session.close()
    prcp_data=list(np.ravel(precipitaions))
    all_prcp=[]
    for prcps in precipitations:
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
    tobs_data=session.query(Measurement.tobs).filter(Measurement.date >= one_year_query).all()
    annual_tobs=list(np.ravel(tobs_data))
    return jsonify(annual_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    date_start = dt.strptime(start, '%y-%m-%d') #parse out the year month and day
    TMIN=session.query(func.min(Measurement.tobs)).filter(Measurement.date >= date_start).all()
    TAVG=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= date_start).all()
    TMAX=session.query(func.max(Measurement.tobs)).filter(Measurement.date >= date_start).all()
    start_data=[{"Minimum Temp": TMIN}, {"Average Temp": TAVG}, {"Maximum Temp": TMAX}]
    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    date_start = dt.strptime(start, '%y-%m-%d')
    date_end = dt.strptime(end, '%y-%m-%d')
    TMIN=session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(date_start, date_end).all()
    TAVG=session.query(func.avg(Measurement.tobs)).filter(Measurement.date.between(date_start, date_end).all()
    TMAX=session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(date_start, date_end).all()

if __name__ == '__main__':
    app.run(degug=True)
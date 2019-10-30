import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine= create_engine('sqlite:///hawaii.sqlite')
Base= automap_base()
Base.prepare(engine, reflect=True)

Measurement= Base.classes.measurement
Station= Base.classes.station

session= Session(engine)

#app code follows

app= Flask(__name__)
@app.route('/')
def welcome():
    return(
        f'AvailableROutes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/Stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start_date(avg)<br/>'
        f'/api/v1.0/start_date/end_date(avg)<br/>')
@app.route('/api/v1.0/precipitation')
def precipitation():
    precipitation_data = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    total_precipitation=[]
    for date, prcp in precipitation_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        total_precipitation.append(precipitation_dict)
    session.close()
    return jsonify(total_precipitation)
@app.route('/api/v1.0/Stations')
def Stations():
    stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    stations_list = []
    for station, count in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["ID"] = count
        stations_list.append(station_dict)
    session.close()
    return jsonify(stations_list)
@app.route('/api/v1.0/tobs')
def tobs():
    last_date = session.query(func.max(Measurement.date)).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= (last_date - dt.timedelta(days=365)))

    tobs_list = []
    for Date, Tobs in results:
        tobs_dict = {}
        tobs_dict['Date'] = Date
        tobs_dict['TOBS'] = Tobs
        tobs_list.append(tobs_dict)
    session.close()
    return jsonify(tobs_list)
@app.route('/api/v1.0/start_date(avg)')
def start_date():
    results = results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start2).all()

    stats_list=[]

    for Minimum, Average, Maximum in results:
        stats_dict = {}
        stats_dict['Minimum'] = Minimum
        stats_dict['Average'] = Average
        stats_dict['Maximum'] = Maximum
        stats_list.append(stats_dict)
    session.close()
    return jsonify(stats_list)
@app.route('/api/v1.0/start_date/end_date(avg)')
def start_end_date():
     results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    stats_list = []

    for Minimum, Average, Maximum in results:
        stats_dict = {}
        stats_dict['Minimum'] = Minimum
        stats_dict['Average'] = Average
        stats_dict['Maximum'] = Maximum
        stats_list.append(stats_dict)
    session.close()
    return jsonify(stats_list)
if __name__=="__main__":
    app.run(debug=True)
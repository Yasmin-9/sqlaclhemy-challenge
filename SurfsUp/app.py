# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start format: yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start format: yyyy-mm-dd]/[endyyyy-mm-dd]"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    scores = session.query(measurement.date, measurement.prcp).filter(measurement.date <= '2017-08-23').filter(measurement.date >= '2016-08-23').all()
    session.close()
    all_scores = []
    for date,prcp in scores: 
        prcp_dict = {'date' : date,
                     'prcp': prcp}
        all_scores.append(prcp_dict)   
    return jsonify(all_scores)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(station.station).order_by(station.station).all()
    session.close()
    all_stations = list(np.ravel(stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    observations = session.query(measurement.date, measurement.tobs).filter(measurement.station =="USC00519281").filter(measurement.date <= "2017-08-23").filter(measurement.date >="2016-08-23").all()
    session.close()
    all_obs = list(np.ravel(observations))
    return jsonify(all_obs)

@app.route("/api/v1.0/<start>")
def start(start):
    try: 
        datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Date must be in 'yyyy-mm-dd' format"}), 400
        
    session = Session(engine)
    temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    temps_start = []
    for min, max, avg in  temps: 
        temps_start_dict={"T_min": min,
                          "T_max": max,
                          "T_avg": avg}
        temps_start.append(temps_start_dict)
    return jsonify(temps_start)  
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    try: 
        datetime.strptime(start, '%Y-%m-%d')
        datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Date must be in 'yyyy-mm-dd' format"}), 400
        
    session = Session(engine)
    temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <=end).all()
    session.close()
    temps_start_end = []
    for min, max, avg in  temps: 
        temps_startend_dict={"T_min": min,
                          "T_max": max,
                          "T_avg": avg}
        temps_start_end.append(temps_startend_dict)
    return jsonify(temps_start_end)


if __name__ == "__main__":
    app.run(debug=True)

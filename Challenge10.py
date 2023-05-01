from flask import Flask, jsonify
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#Reflect Database
Base = automap_base()
#Reflect Tables
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcomenew():
    return (
        f"Welcome to the Challenge 10 API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"JSON list of stations = /api/v1.0/stations<br/>"
        f"Precipitation analysis from last 12 months = /api/v1.0/precipitation<br/>"
        f"Dates & temperature observations from most active station = /api/v1.0/tobs<br/>" 
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    #return jsonify(precip_values)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    print(query_date)

    md = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > query_date).\
    order_by(Measurement.date).all()

    session.close()

    precipitation_data = []
    for date, prcp in md:
         prior_year_dict = [f"{date}", f"{prcp} inches"]
         precipitation_data.append(prior_year_dict)

    return(jsonify(dict(precipitation_data)))

@app.route("/api/v1.0/stations")
def stationlist():
     
     session = Session(engine)

     stations = session.query(Station.name, Station.station).all()

     session.close()

     stations_list = list(np.ravel(stations))

     return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def temps():
     
    session = Session(engine)
  
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    print(query_date)

    md2 = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > query_date).\
    order_by(Measurement.date).all()
   
    md2list = list(np.ravel(md2))
    return jsonify(md2list)

   
if __name__ == "__main__":
    app.run(debug=True)

import json
import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    with open("api/artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[4:]

    with open("api/artifacts/home_price_model.pickle", "rb") as f:
        __model = pickle.load(f)

@app.route("/api/get_location_names", methods=["GET"])
def get_location_names():
    response = jsonify({"locations": __locations})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/api/predict_home_price", methods=["POST"])
def predict_home_price():
    data = request.get_json()
    location = data["location"]
    bhk = int(data["bhk"])
    bath = int(data["bath"])
    sqft = float(data["sqft"])
    floor = int(data["floor"])

    estimated_price = get_estimated_price(location, bhk, bath, sqft, floor)
    response = jsonify({"estimated_price": estimated_price})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def get_estimated_price(location, bhk, bath, sqft, floor):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = bhk
    x[1] = bath
    x[2] = sqft
    x[3] = floor
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

load_saved_artifacts()

# Vercel does NOT require app.run()

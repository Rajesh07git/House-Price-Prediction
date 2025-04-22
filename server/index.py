import json
import pickle
import numpy as np
from flask import Flask,request,jsonify
app=Flask(__name__)


@app.route('/get_location_names',methods=['GET'])
def get_location_names():
    response=jsonify({
        'locations':get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response


@app.route('/predict_home_price', methods=['GET','POST'])
def predict_home_price():
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    sqft = float(request.form['sqft'])
    floor = int(request.form['floor'])
    response = jsonify({
        'estimated_price': get_estimated_price(location,bhk,bath,sqft,floor)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



__locations=None
__data_columns=None
__model=None


def get_estimated_price(location,bhk,bath,sqft,floor):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = bhk
    x[1] = bath
    x[2] = sqft
    x[3] = floor
    if loc_index>=0:
        x[loc_index] = 1
    
    return round(__model.predict([x])[0], 2)

def get_location_names():
    return __locations

def load_saved_artifacts():
    print('loading saved artifacts...start')
    global __data_columns
    global __locations
    
    with open('server/artifacts/columns.json','r') as f:
        __data_columns=json.load(f)['data_columns']
        __locations=__data_columns[4:]
        
    global __model
    with open('server/artifacts/home_price_model.pickle','rb') as f:
        __model=pickle.load(f)
    print('loading saved artifacts...done')

if __name__=='__main__':
    print("Starting Python Flask Server For Home Price Prediction")
    load_saved_artifacts()
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
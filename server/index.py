import util
from flask import Flask,request,jsonify
app=Flask(__name__)

# from fastapi import FastAPI
# app = FastAPI()

# @app.get("/read_root")
# def read_root():
#     return {"message": "Hello from util.py!"}


@app.route('/get_location_names',methods=['GET'])
def get_location_names():
    response=jsonify({
        'locations':util.get_location_names()
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
        'estimated_price': util.get_estimated_price(location,bhk,bath,sqft,floor)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__=='__main__':
    print("Starting Python Flask Server For Home Price Prediction")
    util.load_saved_artifacts()
    app.run()
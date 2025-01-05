from flask import Flask,request,jsonify
import uti
app=Flask(__name__)

@app.route('/get_location_names',methods=['GET'])
def get_location_names():
    response=jsonify({
        'locations':uti.get_location_names()
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
        'estimated_price': uti.get_estimated_price(location,bhk,bath,sqft,floor)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__=='__main__':
    print("Starting Python Flask Server For Home Price Prediction")
    uti.load_saved_artifacts()
    app.run()
import json
import pickle
import numpy as np

__locations=None
__data_columns=None
__model=None

# # util.py
# def handler(req, res):
#     return res.status(200).send("Hello from util.py!")

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
    
    with open('./artifacts/columns.json','r') as f:
        __data_columns=json.load(f)['data_columns']
        __locations=__data_columns[4:]
        
    global __model
    with open('./artifacts/home_price_model.pickle','rb') as f:
        __model=pickle.load(f)
    print('loading saved artifacts...done')

#  # server/util.py
# from http.server import BaseHTTPRequestHandler

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/plain")
#         self.end_headers()
#         self.wfile.write(b"Hello, world!")
   
if __name__=='__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Auburn',3, 3,1000, 1))
    print(get_estimated_price('Bellevue',2,2,1000,2))
    print(get_estimated_price('Bothell', 2, 2,1000,4)) 
    print(get_estimated_price('Clyde Hill',1,1,1000,1))  
    
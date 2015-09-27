import os
from flask import Flask, request
import getMapping
import getLocation
import requests
import json

secret = os.environ.get('betterdoctor-apikey', None)
app = Flask(__name__)
URL = "https://api.betterdoctor.com/2014-09-12/"

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/api/search-specialty', methods=['POST'])
def search_specialty():
    specialty = request.form['specialty']
    phone_number = request.form['phone_number']
    data = {
        'specialty_uid': getMapping.getSpecialtyUidMapping(specialty),
        'user_key': secret,
        'location': ",".join(getLocation.get_location(phone_number)),
        'user_location': ",".join(getLocation.get_user_location(phone_number)),
        'limit': 3,
        'sort': 'rating-desc'
    }
    resp = requests.post(URL + 'doctor', data)
    if resp.status_code == 200:
        data = json.loads(resp.text)
        print(data)
        return resp.text
    return resp



import os
from flask import Flask, request
import getMapping
import getLocation
import requests
import json
import logging

secret = os.environ.get('betterdoctor-apikey', None)
app = Flask(__name__)
URL = "https://api.betterdoctor.com/2015-01-27/"

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/api/search-specialty', methods=['POST'])
def search_specialty():
    specialty = 'dietitian' #request.form['specialty']
    phone_number = '1281128' #request.form['phone_number']
    data = {
        'specialty_uid': getMapping.getSpecialtyUidMapping(specialty),
        'user_key': secret,
        'location': ",".join(getLocation.get_location(phone_number)),
        'user_location': ",".join(getLocation.get_user_location(phone_number)),
        'skip': 0,
        'limit': 3,
        'sort': 'rating-desc'
    }
    print(URL + 'doctors')
    resp = requests.get(URL + 'doctors', data)
    print(resp)
    print(resp.status_code)
    print(resp.text)
    logging.info(resp)
    logging.error(resp)
    if resp.status_code == 200:

        data = json.loads(resp.text)
        print(data)
        return resp.text
    return resp


search_specialty()
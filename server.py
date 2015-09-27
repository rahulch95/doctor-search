import os
from flask import Flask, Response
import getMapping
import getLocation
import requests
import json
import logging

secret = os.environ.get('betterdoctor-apikey', None)
app = Flask(__name__)
URL = "https://api.betterdoctor.com/2015-01-27/"


class Doctor:
    def __init__(self):
        self.name = None
        self.practice = None
        self.address = None
        self.uid = None
        self.phone_number = None

    def to_dict(self):
        return {
            "name": self.name,
            "practice": self.practice,
            "uid": self.uid,
            "address": self.address,
            "phone_number": self.phone_number
        }

    def set_address(self, visit_address):
        address = []
        if visit_address['street']:
            address.append(visit_address['street'])
        if visit_address['city']:
            address.append(visit_address['city'])
        if visit_address['state']:
            address.append(visit_address['state'])
        if visit_address['zip']:
            address.append(visit_address['zip'])

        self.address = ", ".join(address)


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
    resp = requests.get(URL + 'doctors', data)
    print(resp)
    logging.info(resp)

    if resp.status_code == 200:
        data = json.loads(resp.text)
        i = 1
        response = {}
        for doctor_data in data["data"]:
            new_doctor = Doctor()
            practices = doctor_data["practices"]
            for practice in practices:
                if practice['within_search_area']:
                    new_doctor.practice = practice['name']
                    new_doctor.uid = practice['uid']
                    new_doctor.set_address(practice['visit_address'])
                    for phone in practice['phones']:
                        new_doctor.phone_number = phone['number']
                        break
                    break
            profile = doctor_data['profile']
            new_doctor.name = profile['first_name'] + ' ' + profile['last_name']
            response[i] = new_doctor.to_dict()
            i += 1
        return Response(response=response, content_type='text/json; charset=utf-8', status=200)
    return Response({}, mimetype='text/json; charset=utf-8', status=400)

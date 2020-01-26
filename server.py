from flask import Flask, render_template, request, jsonify, send_from_directory, redirect
import os
import requests
import json
import pymongo
from symptoms import build_symptom_map
from diseases import build_disease_map
from datetime import datetime
#from flask_simple_geoip import SimpleGeoIP
#from flask.ext.geoip import GeoIP
import pygeoip

root_dir = '/home/ec2-user/site/MH20'
app = Flask("SickoMode")
#gi = pygeoip.GeoIP()
#simple_geoip = SimpleGeoIP(app)
API_KEY = 'b5998aa55f5d387b5df67e92e82d00e9'
@app.route("/", methods=['GET', 'POST'])
def home():
#    geoip_data = simple_geoip.get_geoip_data()
#    print(geoip_data)
#    geoip = GeoIP(app)
#    print(geoip)
#    data = gi.record_by_addr(request.remote_addr)
#    print(data)
    return "Whats Up"


@app.route("/form", methods=['GET', 'POST'])
def form():
    print("hey")
   # return send_from_directory(os.path.join(root_dir, 'static'), 'index.html')
    return render_template('/index.html')


@app.route("/new_entry", methods=['POST'])
def upload_data():
    #form = json.loads(request.data)
    form = request.form;
    form = form.to_dict(flat=False)
    print(form)
    #print(json.loads(request.form.get('ex')))
    #print(request.get_json())
    #result = request.form.to_dict(flat=False)
    #print("R", result)
    #print(request.form['gender'])
    #d = request.json()
    #print("D",d)
    url = 'http://api.ipstack.com/{}?access_key={}'.format(request.remote_addr,API_KEY)
    r = requests.get(url)
    print(r)
    print(r.content)
    data = r.json()
    lat = data['latitude']
    lon = data['longitude']
    print("Lat, lon", lat, lon)
    gender = form['gender'][0]
    age = int(form['age'][0])
    symptoms = form['symptoms[]']
    print("S", symptoms)
    confirmed = form['confirmed'][0]
    date = datetime.now()
    disease = form['disease']
    print("yo")
    dis_json = [{'ID': disease[0], 'Prob': 100}]

    if confirmed == 'n':
        dis_json = []

    myclient = pymongo.MongoClient("mongodb+srv://SickoMode:SickoMode@cluster0-zfxxk.mongodb.net/test?retryWrites=true&w=majority")

    mydb = myclient["SickoMode"]
    mycol = mydb["Diseases"]

    data = {
    'Gender': gender,
    'Latitude': lat,
    'Longitude': lon,
    'Age': age,
    'Symptoms': symptoms,
    'Confirmed': confirmed,
    'Date': date,
    'Diseases': dis_json
    }
    print(data)
    x = mycol.insert_one(data)

    print(x)
    return redirect("./", code=302)
    return "Form stuff"
@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return "Unauthorized"


@app.route("/get_symptoms", methods=['GET'])
def get_symptoms():
    map = build_symptom_map()
    return jsonify(map)

@app.route("/get_diseases", methods=['GET'])
def get_diseases():
    map = build_disease_map()
    return jsonify(map)


if __name__ == "__main__":
    # Run app
    app.run(host="0.0.0.0", port=80)


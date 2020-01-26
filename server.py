from flask import Flask, render_template, request
import requests
import json
import pymongo
#from flask_simple_geoip import SimpleGeoIP
#from flask.ext.geoip import GeoIP
import pygeoip

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


@app.route("/new_entry", methods=['POST'])
def upload_data():
    form = json.loads(request.data)
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
    gender = form['gender']
    age = form['age']
    symptoms = form['symptoms']
    confirmed = form['confirmed']
    date = form['date']
    diseases = form['diseases']


    myclient = pymongo.MongoClient("mongodb+srv://SickoMode:SickoMode@cluster0-zfxxk.mongodb.net/test?retryWrites=true&w=majority")

    mydb = myclient["SickoMode"]
    mycol = mydb["Diseases"]

    data = {
    'gender': gender,
    'latitude': lat,
    'longitude': lon,
    'age': age,
    'symptoms': symptoms,
    'confirmed': confirmed,
    'date': date,
    'diseases': diseases
    }
    print(data)
    x = mycol.insert_one(data)

    print(x)

    return "Form stuff"
@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return "Unauthorized"

if __name__ == "__main__":
    # Run app
    app.run(host="0.0.0.0", port=80)
<<<<<<< HEAD
    #app.run(host="0.0.0.0", ssl_context='adhoc', port=443)
=======
>>>>>>> 9f0d26b2ff8a6d23fd5db3c344be5a26e39b6a5a


import PriaidDiagnosisClient
import random
import datetime
import apiconfig as config
import sys
import json


client = None

def init_obj():
    global client
    username = config.username
    password = config.password
    authUrl = config.priaid_authservice_url
    healthUrl = config.priaid_healthservice_url
    language = config.language

    client = PriaidDiagnosisClient.DiagnosisClient(username, password, authUrl, language, healthUrl)
    #return client


"""
gender is a string, either 'male', 'female', or 'other'
age is a integer
symptoms is a list of symptom ids
"""
def get_diagnosis(gender, age, symptoms):

    if(gender == 'male' or gender == 'other'):
        gender = PriaidDiagnosisClient.Gender.Male
    else:
        gender = PriaidDiagnosisClient.Gender.Female

    now = datetime.datetime.now()
    year = now.year

    year_of_birth = year - age

    # Convert symptoms to the right string
    #sym_str = str(symptoms)
    #sym_str = sym_str.replace(" ","")
    #sym_str = sym_str.replace("[","%5B")
    #sym_str = sym_str.replace("]","%5D")
    #sym_str = sym_str.replace(",","%2C")

    #querystring = {"symptoms":"%5B234%2C11%5D","gender":"male","year_of_birth":"1984","language":"en-gb"}
    #print(querystring)
    response = client.loadDiagnosis(symptoms, gender, year_of_birth)
    #response = requests.request("GET", url, headers=headers, params=querystring)


    suggested = []
    print(response)
    for diag in response:

        info = diag["Issue"]

        entry = {
            # "Name": info["Name"],
            "ID": info["ID"],
            "Prob": info["Accuracy"]
        }
        suggested.append(entry)

    return suggested

init_obj()
diag = get_diagnosis('male', 16, [40, 146])
print(diag)

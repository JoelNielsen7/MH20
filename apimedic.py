
import requests
import datetime

headers = {
    'x-rapidapi-host': "priaid-symptom-checker-v1.p.rapidapi.com",
    'x-rapidapi-key': "SIGN-UP-FOR-KEY"
    }


"""
gender is a string, either 'male', 'female', or 'other'
age is a integer
symptoms is a list of symptom ids
"""
def get_diagnosis(gender, age, symptoms):

    if(gender = 'other'):
        gender = ''

    url = "https://priaid-symptom-checker-v1.p.rapidapi.com/diagnosis"

    now = datetime.datetime.now()
    year = now.year

    year_of_birth = str(year - age)

    # Convert symptoms to the right string
    sym_str = str(symptoms)
    sym_str = sym_str.replace(" ","")
    sym_str = sym_str.replace("[","%5B")
    sym_str = sym_str.replace("]","%5D")
    sym_str = sym_str.replace(",","%2C")

    #querystring = {"symptoms":"%5B234%2C11%5D","gender":"male","year_of_birth":"1984","language":"en-gb"}
    querystring = {"symptoms":sym_str,"gender":gender,"year_of_birth":year_of_birth,"language":"en-gb"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response

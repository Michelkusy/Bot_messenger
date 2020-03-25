import requests

def weather(city):
    site = 'http://api.openweathermap.org/data/2.5/weather?APPID=9ab926ca6309ff7f06ed89e19f374271&q=' + city
    r = requests.get(site)
    p = r.json()

    temp = float(p['main']['temp']) - 273.15
    text = "Il fait actuellement " + f"{temp:.2f}" + "°C à " + p['name'] + " (" + p['sys']['country'] + ")\n"
    return (text)

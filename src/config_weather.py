import re
import dotenv
import requests
import os
from model import utils

# sets cities and times for weather report

CITY_DIR = utils.DATA_DIR + "\\weather\\city.txt"
TIMES_DIR = utils.DATA_DIR + "\\weather\\times.txt"


# return true if time_input is valid 24hr time, else return false
def valid_time(time_input):
    pattern = re.compile(r'((([0-1]\d)|(2[0-3])):[0-5]\d)|24:00')
    if pattern.match(time_input) is None:
        return False
    return True


# return true if city_input is valid city name, else return false
def valid_city(city_input):
    key = os.getenv('WEATHER_TOKEN')
    url = r'http://api.openweathermap.org/data/2.5/weather?q=' + city_input + '&appid=' + key
    response = requests.get(url)
    response = response.json()
    if response['cod'] == '404':
        return False
    return True


if __name__ == "__main__":
    dotenv.load_dotenv(utils.ENV_PATH)
    list_of_cities = ''
    list_of_times = ''
    while True:
        city_name = input("enter a city name, type 'done' when done")
        if city_name == 'done':
            break
        elif not valid_city(city_name):
            print("Not a valid city, try again")
            continue
        list_of_cities = list_of_cities + '/' + city_name

    while True:
        time = input("enter a time in 24h, type 'done' when done")
        if time == 'done':
            break
        elif not valid_time(time):
            print("Not a valid time, try again")
            continue
        list_of_times = list_of_times + ',' + time

    with open(CITY_DIR, 'w') as city, open(TIMES_DIR, 'w') as time:
        city.write(list_of_cities)
        time.write(list_of_times)
        print("Cities and times successfully set")

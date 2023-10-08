import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Twilio details
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]
YOUR_PHONE_NUMBER = os.environ["YOUR_PHONE_NUMBER"]

CITIES = {
    'Brandenburg': {'latitude': '52.4167', 'longitude': '12.55'},
    'Tampa': {'latitude': '27.9475', 'longitude': '-82.4584'}
}

def send_weather_update(event=None, context=None):
    messages = []

    for city_name, coords in CITIES.items():
        # Get weather data
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coords['latitude']}&longitude={coords['longitude']}&daily=apparent_temperature_max,apparent_temperature_min,precipitation_probability_max&temperature_unit=fahrenheit&windspeed_unit=mph&timezone=Europe%2FBerlin&forecast_days=1")
        data = response.json()

        # Extract relevant data
        temp_max = data['daily']['apparent_temperature_max'][0]
        temp_min = data['daily']['apparent_temperature_min'][0]
        precip_prob = data['daily']['precipitation_probability_max'][0]

        messages.append(f"Weather in {city_name} today: Max: {temp_max}°F, Min: {temp_min}°F, Precip Prob: {precip_prob}%")

    # Send messages using Twilio
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    combined_message = "Morning Max, " + "\n".join(messages)
    client.messages.create(body=combined_message, from_=TWILIO_PHONE_NUMBER, to=YOUR_PHONE_NUMBER)

# Uncomment the below line for local testing
send_weather_update()

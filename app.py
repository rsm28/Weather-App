import os, json
from flask import Flask, request, jsonify, render_template
import requests

if not os.path.exists("Weather App\config.json"):
    print("config.json is missing. Please create it.")
    print("Exiting...")
    exit(1)

# Read config.json
with open("Weather App\config.json", "r") as f:
    config = json.load(f)
    # Check if email & password are in config.json
    if "API_KEY" not in config:
        print("config.json is missing email or password. Please add them.")
        print("Exiting...")
        exit(1)

    # Get email & password
    API_KEY = config["API_KEY"]

app = Flask(__name__)
city = input("Enter a city: ")


@app.route("/weather", methods=["GET"])
def get_weather():
    # Get the city parameter from the request
    # Make a request to the OpenWeatherMap API to get the weather for the given city
    r = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}",
        headers={"content-type": "application/json"},
    )

    # Extract the weather data from the response
    weather_data = json.loads(r.text)

    # Convert the temperature from Kelvin to Celsius
    weather_data["main"]["temp"] -= 273.15
    weather_data["main"]["temp_min"] -= 273.15
    weather_data["main"]["temp_max"] -= 273.15

    # Render the HTML file using Jinja
    return render_template("weather.html", weather_data=weather_data)


if __name__ == "__main__":
    app.run()

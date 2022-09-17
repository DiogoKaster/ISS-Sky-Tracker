import requests
from datetime import datetime
import smtplib

MY_LAT = -17.104043  # Your latitude
MY_LONG = -43.945313  # Your longitude
MY_EMAIL = "your email"
MY_PASSWORD = "your password"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

dist_lat = MY_LAT - iss_latitude
dist_long = MY_LONG - iss_longitude

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

if -5 < dist_lat < 5 and -5 < dist_long < 5:
    if sunset < time_now.hour < sunrise:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Look Up\n\nThe ISS is passing over the sky!"
            )

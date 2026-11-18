"""APIs Open-Meteo (REST, sin llave) -> MQTT. 3 dispositivos API."""
import os, time, threading, requests
from common import Device

LAT, LON = os.getenv("LAT", "7.1182633"), os.getenv("LON", "-73.1113583")

def get(url, params):
    r = requests.get(url, params={"latitude": LAT, "longitude": LON, "timezone": "America/Bogota", **params}, timeout=20)
    r.raise_for_status(); return r.json()

def clean(d): return {k: float(v) for k, v in d.items() if isinstance(v, (int, float))}

def current():
    c = get("https://api.open-meteo.com/v1/forecast", {"current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,cloud_cover,precipitation"})["current"]
    return clean({"temp_c": c.get("temperature_2m"), "humidity": c.get("relative_humidity_2m"), "pressure_hpa": c.get("surface_pressure"),
                  "wind_kmh": c.get("wind_speed_10m"), "cloud_cover": c.get("cloud_cover"), "precip_mm": c.get("precipitation")})

def airq():
    c = get("https://air-quality-api.open-meteo.com/v1/air-quality", {"current": "pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone,us_aqi"})["current"]
    return clean({"pm25": c.get("pm2_5"), "pm10": c.get("pm10"), "co": c.get("carbon_monoxide"), "no2": c.get("nitrogen_dioxide"), "o3": c.get("ozone"), "aqi": c.get("us_aqi")})

def minute():
    m = get("https://api.open-meteo.com/v1/forecast", {"minutely_15": "precipitation", "forecast_minutely_15": 4})["minutely_15"]["precipitation"]
    return clean({"precip_next_hour_mm": sum(x for x in m if x is not None)})

if __name__ == "__main__":
    for did, fn, per in [("API-CUR-01", current, 300), ("API-AQ-01", airq, 600), ("API-FC-01", minute, 300)]:
        threading.Thread(target=Device(did, "api", fn, interval=per).run, daemon=True).start()
    while True: time.sleep(3600)

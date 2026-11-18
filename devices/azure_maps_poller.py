"""APIs Azure Maps Weather (REST) -> MQTT. 3 'dispositivos' API."""
import os, time, threading, requests
from common import Device

KEY, Q = os.environ["AZURE_MAPS_KEY"], f'{os.getenv("LAT")},{os.getenv("LON")}'
B = "https://atlas.microsoft.com/weather"

def get(path, ver):
    r = requests.get(f"{B}/{path}/json", params={"api-version": ver, "query": Q, "subscription-key": KEY, "language": "es-MX"}, timeout=20)
    r.raise_for_status(); return r.json()

def current():
    d = get("currentConditions", "1.0")["results"][0]
    return {"temp_c": d["temperature"]["value"], "humidity": d["relativeHumidity"],
            "pressure_hpa": d["pressure"]["value"], "wind_kmh": d["wind"]["speed"]["value"],
            "uv": d.get("uvIndex", 0), "cloud_cover": d.get("cloudCover", 0)}

def airq():
    d = get("airQuality/current", "1.1")["results"][0]
    f = {"aqi": d["index"]}
    for p in d["pollutants"]: f[p["type"].lower()] = p["concentration"]["value"]
    return f

def minute():
    d = get("forecast/minute", "1.1")["summary"]
    return {"min_to_precip": d.get("startMinuteFromNow") or 0, "precip_len_min": d.get("lengthInMinutes") or 0}

if __name__ == "__main__":
    for did, fn, per in [("API-CUR-01", current, 300), ("API-AQ-01", airq, 600), ("API-FC-01", minute, 300)]:
        threading.Thread(target=Device(did, "api", fn, interval=per).run, daemon=True).start()
    while True: time.sleep(3600)

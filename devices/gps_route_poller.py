"""API GPS ruta UNAB (gpsmobile.co) -> MQTT. Ajusta los campos con el JSON real (Postman -> Send)."""
import os, requests
from common import Device
URL = "http://gpsmobile.co:4000/api/DetalleVehiculo/97141/96365"
KEYS = ("velocidad", "speed", "latitud", "longitud", "lat", "lng", "rumbo")
def read():
    r = requests.get(URL, auth=(os.getenv("GPS_USER"), os.getenv("GPS_PASS")), timeout=20); r.raise_for_status()
    d = r.json(); d = d[0] if isinstance(d, list) else d
    return {k: float(v) for k, v in d.items() if isinstance(v, (int, float)) and k.lower() in KEYS}
if __name__ == "__main__":
    Device("API-GPS-01", "api", read, interval=30).run()

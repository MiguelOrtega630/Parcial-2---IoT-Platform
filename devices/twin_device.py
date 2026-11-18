"""Digital Twin: replica virtual con ciclo diario + ruido + eventos (picos)."""
import sys, math, random, time
from common import Device

def phase():
    t = time.localtime(); return (t.tm_hour + t.tm_min / 60) / 24

def weather():
    p = phase()
    return {"temp_c": 24 + 5 * math.sin(2 * math.pi * (p - 0.35)) + random.gauss(0, .2),
            "humidity": 70 - 18 * math.sin(2 * math.pi * (p - 0.35)) + random.gauss(0, 1),
            "pressure_hpa": 915 + 1.5 * math.sin(4 * math.pi * p) + random.gauss(0, .1),
            "wind_ms": max(0, 2 + 1.5 * math.sin(2 * math.pi * p) + random.gauss(0, .4))}

def air():
    h = phase() * 24
    rush = math.exp(-((h - 7.5) ** 2) / 2) + math.exp(-((h - 18) ** 2) / 3)   # horas pico
    spike = 40 if random.random() < 0.003 else 0
    pm25 = 10 + 18 * rush + spike + random.gauss(0, 1.5)
    return {"pm25": max(0, pm25), "pm10": max(0, pm25 * 1.6 + random.gauss(0, 2)),
            "co2_ppm": 420 + 120 * rush + random.gauss(0, 8)}

if __name__ == "__main__":
    dev_id, mode = sys.argv[1], sys.argv[2]
    Device(dev_id, "digital_twin", {"weather": weather, "air": air}[mode], interval=10).run()

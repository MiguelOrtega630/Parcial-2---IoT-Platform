"""Dataset (CSV) -> MQTT distribuido sobre los últimos N días. Uso: python dataset_replayer.py DS-HIST-01 datos.csv 5"""
import sys, csv, json, time, os
import paho.mqtt.client as mqtt
dev, path, days = sys.argv[1], sys.argv[2], int(sys.argv[3])
c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=dev)
c.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS")); c.connect(os.getenv("MQTT_HOST", "localhost"), 1883); c.loop_start()
rows = list(csv.DictReader(open(path))); step = days * 86400 / len(rows); t0 = time.time() - days * 86400
for i, r in enumerate(rows):
    f = {k: float(v) for k, v in r.items() if k != "timestamp" and v not in ("", None)}
    c.publish(f"unab/iot/{dev}/telemetry", json.dumps({"ts": int(t0 + i * step), "device_id": dev, "kind": "dataset", "fields": f}), qos=1)
    time.sleep(0.01)
time.sleep(2)

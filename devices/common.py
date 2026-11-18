"""Base MQTT común: telemetría, comandos (retroceso), ACK y LWT."""
import json, os, time
import paho.mqtt.client as mqtt

BASE = "unab/iot"

class Device:
    def __init__(self, device_id, kind, read_fn, interval=10):
        self.id, self.kind, self.read_fn = device_id, kind, read_fn
        self.interval, self.enabled, self.offsets = interval, True, {}
        self.c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=device_id)
        self.c.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
        self.c.will_set(f"{BASE}/{device_id}/status", "offline", qos=1, retain=True)
        self.c.on_connect = self._on_connect
        self.c.on_message = self._on_message

    def _on_connect(self, c, u, f, rc, p=None):
        c.subscribe(f"{BASE}/{self.id}/cmd", qos=1)
        c.publish(f"{BASE}/{self.id}/status", "online", qos=1, retain=True)

    def _on_message(self, c, u, msg):
        # {"action":"set_interval","value":5} | power_off | power_on | {"action":"calibrate","var":"temp_c","offset":-0.8}
        try:
            cmd = json.loads(msg.payload)
            a = cmd.get("action")
            if a == "set_interval": self.interval = max(1, float(cmd["value"]))
            elif a == "power_off": self.enabled = False
            elif a == "power_on": self.enabled = True
            elif a == "calibrate": self.offsets[cmd["var"]] = float(cmd["offset"])
            else: raise ValueError("acción desconocida")
            ack = {"ts": int(time.time()), "device_id": self.id, "ok": True, "cmd": cmd,
                   "state": {"enabled": self.enabled, "interval": self.interval, "offsets": self.offsets}}
        except Exception as e:
            ack = {"ts": int(time.time()), "device_id": self.id, "ok": False, "error": str(e)}
        c.publish(f"{BASE}/{self.id}/ack", json.dumps(ack), qos=1)

    def run(self):
        self.c.connect(os.getenv("MQTT_HOST", "localhost"), int(os.getenv("MQTT_PORT", 1883)), 60)
        self.c.loop_start()
        while True:
            if self.enabled:
                try:
                    fields = {k: round(v + self.offsets.get(k, 0), 3) for k, v in self.read_fn().items()}
                    payload = {"ts": int(time.time()), "device_id": self.id, "kind": self.kind, "fields": fields}
                    self.c.publish(f"{BASE}/{self.id}/telemetry", json.dumps(payload), qos=1)
                except Exception as e:
                    print(self.id, "error de lectura:", e)
            time.sleep(self.interval)

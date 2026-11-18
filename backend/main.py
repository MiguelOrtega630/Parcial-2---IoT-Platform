"""Backend de control ("retroceso"): REST -> comando MQTT. Panel web en /control/."""
import os, json
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import paho.mqtt.client as mqtt

app = FastAPI(title="IoT UNAB Control")
m = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="backend")
m.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
m.connect(os.getenv("MQTT_HOST", "emqx"), 1883); m.loop_start()

class Cmd(BaseModel):
    action: str            # set_interval | power_off | power_on | calibrate
    value: float | None = None
    var: str | None = None
    offset: float | None = None

@app.post("/devices/{dev}/command")
def command(dev: str, cmd: Cmd, x_token: str = Header("")):
    if x_token != os.getenv("API_TOKEN"): raise HTTPException(401, "token inválido")
    m.publish(f"unab/iot/{dev}/cmd", json.dumps(cmd.model_dump(exclude_none=True)), qos=1)
    return {"sent": True, "device": dev}

@app.get("/", response_class=HTMLResponse)
def panel():
    return """<h2>Panel de control IoT</h2>
<input id=d value='TWIN-AQ-01' placeholder='Dispositivo'> <input id=t placeholder='token'><br><br>
<button onclick="s({action:'power_off'})">Apagar</button>
<button onclick="s({action:'power_on'})">Encender</button>
<button onclick="s({action:'set_interval',value:5})">Intervalo 5 s</button>
<button onclick="s({action:'calibrate',var:'pm25',offset:-2})">Calibrar pm25 -2</button>
<script>function s(b){fetch('/devices/'+document.getElementById('d').value+'/command',{method:'POST',headers:{'Content-Type':'application/json','x-token':t.value},body:JSON.stringify(b)}).then(r=>r.json()).then(j=>alert(JSON.stringify(j)))}</script>"""

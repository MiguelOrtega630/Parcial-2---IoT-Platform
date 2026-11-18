"""Estadísticas (prom/máx/mín) por dispositivo desde InfluxDB + descripción con OpenAI."""
import os, json
from influxdb_client import InfluxDBClient
from openai import OpenAI

q = f'''from(bucket:"{os.getenv("INFLUX_BUCKET","iot")}") |> range(start:-5d)
 |> filter(fn:(r)=>r._measurement=="telemetry") |> aggregateWindow(every:1h, fn:mean, createEmpty:false)'''
cli = InfluxDBClient(url=os.getenv("INFLUX_URL","http://localhost:8086"), token=os.getenv("INFLUX_TOKEN"), org=os.getenv("INFLUX_ORG","unab"))
stats = {}
for t in cli.query_api().query(q):
    for r in t.records:
        stats.setdefault(f'{r.values["device_id"]}.{r.get_field()}', []).append(r.get_value())
summary = {k: {"avg": round(sum(v)/len(v), 2), "max": round(max(v), 2), "min": round(min(v), 2), "n": len(v)} for k, v in stats.items()}
prompt = ("Eres analista IoT. Describe en español, por dispositivo, tendencias, picos, ciclos diarios y anomalías "
          "de estas estadísticas horarias de 5 días en Bucaramanga:\n" + json.dumps(summary)[:12000])
out = OpenAI().chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
open("informe_ia.md", "w").write(out.choices[0].message.content); print(out.choices[0].message.content)

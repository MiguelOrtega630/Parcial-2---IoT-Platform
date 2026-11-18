import json
from pathlib import Path

original = json.loads(Path("dashboard_backup.json").read_text())
dashboard = original["dashboard"]

dispositivos = [
    ("API-CUR-01", "temp_c", "Temperatura actual"),
    ("API-AQ-01", "pm25", "Calidad del aire"),
    ("API-FC-01", "precipitation_mm", "Pronóstico de precipitación"),
    ("TWIN-WX-01", "temp_c", "Temperatura simulada 1"),
    ("TWIN-AQ-01", "pm25", "Partículas PM2.5 simuladas 1"),
    ("TWIN-WX-02", "temp_c", "Temperatura simulada 2"),
    ("TWIN-AQ-02", "pm25", "Partículas PM2.5 simuladas 2"),
    ("TWIN-WX-03", "temp_c", "Temperatura simulada 3"),
    ("TWIN-AQ-03", "pm25", "Partículas PM2.5 simuladas 3"),
    ("TWIN-WX-04", "temp_c", "Temperatura simulada 4"),
]

paneles = dashboard.get("panels", [])
siguiente_id = max((p.get("id", 0) for p in paneles), default=0) + 1
fila = max((p.get("gridPos", {}).get("y", 0) +
            p.get("gridPos", {}).get("h", 0) for p in paneles), default=0)

for i, (device, field, titulo) in enumerate(dispositivos):
    consulta = (
        'from(bucket: "iot") '
        '|> range(start: v.timeRangeStart, stop: v.timeRangeStop) '
        '|> filter(fn: (r) => r._measurement == "telemetry") '
        f'|> filter(fn: (r) => r.device_id == "{device}") '
        f'|> filter(fn: (r) => r._field == "{field}") '
        '|> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false) '
        '|> yield(name: "mean")'
    )

    paneles.append({
        "id": siguiente_id + i,
        "title": f"{titulo} - {device}",
        "type": "timeseries",
        "datasource": {
            "type": "influxdb",
            "uid": "cg4j2b8boh9tsd"
        },
        "targets": [{
            "refId": "A",
            "query": consulta,
            "datasource": {
                "type": "influxdb",
                "uid": "cg4j2b8boh9tsd"
            }
        }],
        "gridPos": {
            "h": 8,
            "w": 12,
            "x": (i % 2) * 12,
            "y": fila + (i // 2) * 8
        },
        "fieldConfig": {"defaults": {}, "overrides": []},
        "options": {
            "legend": {"displayMode": "list", "placement": "bottom"},
            "tooltip": {"mode": "single"}
        }
    })

dashboard["panels"] = paneles
dashboard["title"] = "Monitoreo IoT UNAB - 10 dispositivos"

Path("dashboard_nuevo.json").write_text(
    json.dumps({"dashboard": dashboard, "overwrite": True}, indent=2)
)

print("CONFIGURACIÓN GENERADA")
print("Paneles totales:", len(paneles))
print("Archivo: dashboard_nuevo.json")

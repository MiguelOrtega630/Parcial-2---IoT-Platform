import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(13, 7.2)); ax.set_xlim(0, 130); ax.set_ylim(0, 72); ax.axis("off")
def box(x, y, w, h, t, fc="#eef3fb", ec="#1f4e79", fs=9, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")
def arr(x1, y1, x2, y2, t="", both=False, col="#333"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="<|-|>" if both else "-|>", mutation_scale=12, lw=1.3, color=col))
    if t: ax.text((x1+x2)/2, (y1+y2)/2 + 1.6, t, ha="center", fontsize=7.5, color=col)
ax.text(65, 69.5, "Arquitectura de Referencia IoT – Monitoreo ambiental y movilidad (Bucaramanga / UNAB)", ha="center", fontsize=12.5, fontweight="bold")
# sources
ax.text(14, 65, "ORIGEN DE DATOS (10 dispositivos)", ha="center", fontsize=9, fontweight="bold", color="#1f4e79")
srcs = [("REAL (3)\nRPi+BME280 · ESP32+PMS5003\nESP32+SCD40  [python/MQTT]", "#e2f4e2", "#2e7d32"),
        ("API (4)\nAzure Maps: Current · AirQuality\nForecast min · GPS ruta  [REST]", "#fff3d6", "#b26a00"),
        ("DIGITAL TWIN (2)\nTWIN-WX-01 · TWIN-AQ-01\n[Python/MQTT]", "#f3e5f5", "#6a1b9a"),
        ("DATASET (1)\nDS-HIST-01 (CSV histórico)\n[replayer/MQTT]", "#e0f2f7", "#00695c")]
for i, (t, fc, ec) in enumerate(srcs): box(1, 52 - i*13, 26, 10, t, fc, ec, 8)
# VM
ax.add_patch(FancyBboxPatch((36, 4), 92, 58, boxstyle="round,pad=0.4,rounding_size=2", fc="#fafafa", ec="#555", lw=1.6, ls="--"))
ax.text(82, 59, "Azure VM Ubuntu (Docker Compose) · IP pública + DNS · HTTPS (Nginx + Let's Encrypt)", ha="center", fontsize=9, fontweight="bold", color="#444")
box(40, 36, 20, 16, "Broker EMQX\nMQTT 1883 (QoS1)\nretained · LWT\nauth usuario/clave", "#dbe8f8", "#1f4e79", 8.5, True)
box(66, 40, 17, 12, "Telegraf\n(mqtt_consumer\n→ InfluxDB)", fs=8.5)
box(89, 40, 18, 12, "InfluxDB 2\nSeries de tiempo\n(bucket iot)", fs=8.5, bold=True)
box(112, 40, 14, 12, "Grafana\nKPI · gráficas\nalertas", "#fde7e7", "#b71c1c", 8.5, True)
box(66, 22, 22, 12, "Backend FastAPI\nREST /command → MQTT\npanel de control", "#fff3d6", "#b26a00", 8.5)
box(92, 22, 18, 12, "Análisis IA\nOpenAI API\n(informe de gráficas)", "#f3e5f5", "#6a1b9a", 8.5)
box(40, 9, 20, 10, "Pollers (Docker)\nREST→MQTT / Twins", fs=8.5)
box(112, 22, 14, 12, "Nginx\n443 → Grafana\n/control → API", fs=8.5)
# arrows
for i in range(4): arr(27, 57 - i*13, 40, 46 if i<2 else 40, "", col="#555")
arr(60, 46, 66, 46, "MQTT"); arr(83, 46, 89, 46, "write"); arr(107, 46, 112, 46, "Flux")
arr(66, 28, 60, 40, "cmd", col="#b26a00"); arr(50, 36, 50, 19, "", both=True)
arr(100, 34, 98, 40, "query"); 
ax.text(66, 19.3, "↩ retroceso: unab/iot/<id>/cmd → ack", fontsize=7.5, color="#b26a00")
arr(119, 40, 119, 34, "", both=True)
ax.text(119, 12.5, "Usuario / Docente\nhttps://TU_DOMINIO", ha="center", fontsize=8.5, bbox=dict(fc="#fff", ec="#999", boxstyle="round"))
arr(119, 22, 119, 15.5, "")
ax.text(65, 6, "Topics: unab/iot/<device_id>/telemetry | status (LWT) | cmd | ack        Payload JSON: {ts, device_id, kind, fields{...}}", ha="center", fontsize=8, style="italic")
plt.savefig("arquitectura.png", dpi=170, bbox_inches="tight"); print("ok")

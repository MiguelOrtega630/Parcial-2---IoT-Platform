from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Preformatted, KeepTogether

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=16, textColor=colors.HexColor("#1f4e79"), spaceBefore=10, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12.5, textColor=colors.HexColor("#2e6da4"), spaceBefore=8, spaceAfter=4)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9.8, leading=13.5, alignment=4)
SM = ParagraphStyle("SM", parent=B, fontSize=8, leading=10, alignment=0)
CODE = ParagraphStyle("C", fontName="Courier", fontSize=7.6, leading=9.4, backColor=colors.HexColor("#f4f4f4"), borderPadding=4)
PH = ParagraphStyle("PH", parent=B, alignment=1, textColor=colors.HexColor("#888"), fontSize=9)
def P(t, s=B): return Paragraph(t, s)
def bullets(items): return [P("&bull; " + i) for i in items]
def tbl(data, widths, hdr="#1f4e79", fs=8):
    rows = [[P(str(c), SM) if not (r == 0) else Paragraph(f"<font color='white'><b>{c}</b></font>", SM) for c in row] for r, row in enumerate(data)]
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(hdr)), ("GRID", (0, 0), (-1, -1), .4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6fb")])]))
    return t
def placeholder(txt, h=4.5):
    t = Table([[P("[ " + txt + " ]", PH)]], colWidths=[16.5*cm], rowHeights=[h*cm])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#aaa")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa"))]))
    return t

S = []
S += [Spacer(1, 4*cm), P("<font size=24 color='#1f4e79'><b>Proyecto Final - IoT a la Medida</b></font>", ParagraphStyle("t", alignment=1, leading=30)),
      Spacer(1, .5*cm), P("<font size=15>Monitoreo ambiental y de movilidad en Bucaramanga: calidad del aire, clima y ruta de bus UNAB</font>", ParagraphStyle("t2", alignment=1, leading=20)),
      Spacer(1, 1.5*cm), P("<b>Parcial 2 - Capstone / Reto</b>", ParagraphStyle("t3", alignment=1)),
      Spacer(1, 1*cm), P("Integrantes: [NOMBRES]<br/>Docente: [DOCENTE]<br/>Universidad Autónoma de Bucaramanga (UNAB)<br/>Fecha: noviembre de 2026", ParagraphStyle("t4", alignment=1, leading=16)),
      Spacer(1, 1.5*cm), tbl([["Recurso", "Enlace"], ["URL del proyecto (Grafana)", "https://[TU_DOMINIO]"], ["Panel de control (retroceso)", "https://[TU_DOMINIO]/control/"], ["Repositorio GitHub", "https://github.com/[USUARIO]/iot-capstone"]], [5*cm, 11*cm]), PageBreak()]

S += [P("1. Descripción y contexto", H1),
 P("Bucaramanga y su área metropolitana tienen un clima tropical de montaña con fuertes picos de tráfico en horas de entrada y salida (aprox. 6:30-8:30 y 17:00-19:00). Esos picos se asocian con aumentos de material particulado (PM2.5 y PM10) y de CO2, y con cambios de temperatura y humedad a lo largo del día. Los estudiantes y empleados de la UNAB dependen además de rutas de bus cuyo estado conviene conocer en tiempo real."),
 P("<b>Escenario elegido:</b> una red IoT híbrida que combina sensores reales, gemelos digitales, APIs públicas y un dataset histórico para observar, durante 4 a 6 días continuos, la relación entre <i>clima, calidad del aire y movilidad</i> alrededor del campus."),
 P("<b>Objetivo general:</b> diseñar, desplegar en nube y operar una plataforma IoT completa (sensores, datos y variables, protocolos, plataforma y visualización) con capacidad de control remoto de los dispositivos."),
 P("<b>Objetivos específicos:</b>"),
 *bullets(["Integrar 10 dispositivos: 3 reales, 4 API, 2 Digital Twin y 1 Dataset.",
          "Transportar la telemetría con MQTT (broker EMQX) y consumir APIs REST de Azure Maps Weather y de GPS.",
          "Almacenar series de tiempo en InfluxDB y visualizarlas en Grafana con promedio, máximo, mínimo, alertas y reglas.",
          "Implementar el 'retroceso': apagar, encender, cambiar el intervalo y calibrar variables desde un panel web o por API.",
          "Analizar el comportamiento de las gráficas con IA (OpenAI API)."]),
 P("<b>Alcance de la entrega:</b> aplicación desplegada en una máquina virtual de Azure con URL propia (HTTPS), código en GitHub y sustentación personal.")]

S += [PageBreak(), P("2. Arquitectura de referencia IoT", H1),
 Image("arquitectura.png", width=17*cm, height=17*cm*7.2/13*1.0),
 Spacer(1, .2*cm),
 P("La arquitectura sigue las capas vistas en clase y el diagrama base del curso (Capstone: Proyecto final):"),
 *bullets(["<b>Dispositivos / origen de datos:</b> reales (python/MQTT), API (REST), Digital Twin y Dataset. Cada uno tiene un <i>device_id</i> único.",
           "<b>Broker / mensajería:</b> EMQX (MQTT). Todos los dispositivos publican en <font face='Courier'>unab/iot/&lt;id&gt;/telemetry</font> y escuchan comandos en <font face='Courier'>unab/iot/&lt;id&gt;/cmd</font>.",
           "<b>Backend:</b> Telegraf (ingesta MQTT a base de datos) y FastAPI (control, convierte peticiones REST en comandos MQTT).",
           "<b>Base de datos:</b> InfluxDB 2 (series de tiempo, bucket <i>iot</i>).",
           "<b>Análisis:</b> script con consultas Flux y OpenAI API para describir las gráficas.",
           "<b>Front / visualización:</b> Grafana (KPI, gráficas, alertas) servido por Nginx con HTTPS.",
           "<b>Nube:</b> VM Ubuntu en Azure con Docker Compose (VM + Containers + Service del diagrama)."]),
 ]

devs = [["ID", "Tipo", "Sensor / fuente", "Variables y rango esperado", "Protocolo"],
 ["REAL-RPI-01", "Real", "Raspberry Pi + BME280 (python.py)", "temp_c 15-40 °C (sensor -40 a 85); humidity 20-100 %; pressure_hpa 880-940 (Bucaramanga ~ 920)", "MQTT QoS1, 10 s"],
 ["REAL-ESP32-01", "Real", "ESP32 + PMS5003", "pm25 0-150 ug/m3 (sensor 0-500); pm10 0-250 ug/m3", "MQTT QoS1, 10 s"],
 ["REAL-ESP32-02", "Real", "ESP32 + SCD40", "co2_ppm 400-2000 (sensor 400-5000); temp_c; humidity", "MQTT QoS1, 10 s"],
 ["API-CUR-01", "API", "Azure Maps Weather - Current Conditions", "temp_c, humidity, pressure_hpa, wind_kmh 0-60, uv 0-11, cloud_cover 0-100 %", "REST GET a MQTT, 5 min"],
 ["API-AQ-01", "API", "Azure Maps Weather - Air Quality (current)", "aqi 0-10 (índice global), concentraciones de contaminantes (O3, NO2, PM2.5, PM10, SO2, CO)", "REST GET a MQTT, 10 min"],
 ["API-FC-01", "API", "Azure Maps Weather - Minute Forecast", "min_to_precip 0-120 min, precip_len_min 0-120", "REST GET a MQTT, 5 min"],
 ["API-GPS-01", "API", "gpsmobile.co - DetalleVehiculo (ruta UNAB)", "latitud, longitud, velocidad 0-80 km/h, rumbo 0-360", "REST GET (Basic Auth) a MQTT, 30 s"],
 ["TWIN-WX-01", "Digital Twin", "Gemelo de la estación meteorológica (twin_device.py)", "temp_c 18-31, humidity 50-90, pressure_hpa 912-918, wind_ms 0-5", "MQTT QoS1, 10 s"],
 ["TWIN-AQ-01", "Digital Twin", "Gemelo del nodo de aire (twin_device.py)", "pm25 5-60 (picos simulados), pm10, co2_ppm 400-650", "MQTT QoS1, 10 s"],
 ["DS-HIST-01", "Dataset", "CSV histórico de calidad del aire (datos abiertos Colombia / SISAIRE)", "pm25, pm10, temp_c reproducidos sobre los últimos 5 días", "dataset_replayer.py a MQTT"]]
S += [PageBreak(), P("3. Tecnologías seleccionadas", H1), P("3.1 Sensores y dispositivos (10)", H2),
 P("La tabla resume los dispositivos, sus variables y los rangos esperados. Los rangos reales se verifican con los datos medidos y se ajustan en la sección de análisis."),
 tbl(devs, [2.3*cm, 1.6*cm, 3.7*cm, 6.6*cm, 2.8*cm], fs=7.5), Spacer(1, .2*cm),
 P("<i>Nota:</i> los tres dispositivos reales deben ajustarse al hardware que el grupo tenga realmente; el código <font face='Courier'>real_device.py</font> usa la temperatura de CPU como respaldo si el sensor no está conectado.", SM)]

S += [P("3.2 Comunicación: broker y protocolo", H2),
 P("<b>Broker:</b> EMQX 5 (contenedor Docker, puerto 1883, panel en 18083), con autenticación por usuario y contraseña. <b>Protocolo:</b> MQTT 3.1.1/5 (publicación/suscripción sobre TCP)."),
 tbl([["Elemento", "Diseño"],
  ["Envío (dispositivo a plataforma)", "Publica JSON en <font face='Courier'>unab/iot/&lt;id&gt;/telemetry</font>, QoS 1. Payload: {ts, device_id, kind, fields:{variable: valor}}."],
  ["Recepción (plataforma a dispositivo)", "El dispositivo se suscribe a <font face='Courier'>unab/iot/&lt;id&gt;/cmd</font> (QoS 1). Comandos: set_interval, power_off, power_on, calibrate."],
  ["Confirmación", "Responde en <font face='Courier'>unab/iot/&lt;id&gt;/ack</font> con el estado resultante (enabled, interval, offsets)."],
  ["Estado de conexión", "Last Will and Testament (LWT) en <font face='Courier'>.../status</font>: 'online' retenido al conectar, 'offline' si cae."],
  ["Dispositivos tipo API", "Un poller consulta por HTTP/REST (GET) las APIs de Azure Maps y GPS y republica el resultado por MQTT, de modo que todo el flujo converge en el broker."],
  ["Ingesta", "Telegraf se suscribe a <font face='Courier'>unab/iot/+/telemetry</font> y escribe en InfluxDB con las etiquetas device_id y kind."]], [4.5*cm, 12*cm])]

S += [P("3.3 Nube y servicios utilizados", H2),
 tbl([["Componente", "Servicio / tecnología", "Función"],
  ["Cómputo", "Azure Virtual Machine Ubuntu (usuario azureuser, acceso SSH con llave .pem)", "Aloja toda la infraestructura propia"],
  ["Red", "IP pública + etiqueta DNS de Azure; NSG con puertos 22 (solo tu IP), 80, 443 y 1883", "URL propia y acceso de dispositivos"],
  ["Contenedores", "Docker Compose (emqx, influxdb, telegraf, grafana, backend, pollers, twins, nginx)", "Despliegue reproducible"],
  ["Seguridad", "Nginx + certificado Let's Encrypt (HTTPS); secretos en .env", "Cifrado y control de acceso"],
  ["API externa", "Azure Maps Weather (clave de suscripción)", "Clima actual, calidad del aire, pronóstico por minuto"],
  ["IA", "OpenAI API", "Descripción automática de las gráficas"]], [3*cm, 8*cm, 5.5*cm])]

S += [PageBreak(), P("4. Retroceso: control remoto de los dispositivos", H1),
 P("El requisito de 'retroceso' se cumple con un canal descendente. El usuario usa el panel web (<font face='Courier'>/control/</font>) o la API REST; el backend FastAPI valida un token y publica el comando en MQTT; el dispositivo lo aplica y confirma por el tópico ack."),
 tbl([["Acción", "Comando JSON", "Efecto"],
  ["Apagar", "{'action':'power_off'}", "El dispositivo deja de publicar (se ve el hueco en la gráfica)"],
  ["Encender", "{'action':'power_on'}", "Reanuda la telemetría"],
  ["Ajustar frecuencia", "{'action':'set_interval','value':5}", "Cambia el intervalo de muestreo a 5 s"],
  ["Calibrar", "{'action':'calibrate','var':'pm25','offset':-2}", "Suma un offset a la variable (se ve el escalón en la gráfica)"]], [3.2*cm, 6.3*cm, 7*cm]),
 Spacer(1, .2*cm), P("Ejemplo con curl:"),
 Preformatted("curl -X POST https://[TU_DOMINIO]/control/devices/TWIN-AQ-01/command \\\n  -H 'x-token: TU_TOKEN' -H 'Content-Type: application/json' \\\n  -d '{\"action\":\"calibrate\",\"var\":\"pm25\",\"offset\":-2}'", CODE),
 Spacer(1, .2*cm), P("Los dispositivos tipo API y Dataset no tienen hardware que apagar, pero sí aceptan set_interval y power_off (el poller deja de consultar la API). El retroceso se demuestra principalmente con los reales y los gemelos.")]

S += [P("5. Visualización y procesamiento de los datos", H1),
 P("Grafana lee InfluxDB con Flux. El selector de tiempo permite cambiar el rango (1 h, 24 h, 5 días) y el intervalo de agregación se ajusta con la variable <font face='Courier'>v.windowPeriod</font> o con una variable de dashboard <i>ventana</i> (1m, 5m, 1h)."),
 Preformatted("""// Promedio por ventana (ajustable con el tiempo)
from(bucket:"iot") |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r)=> r._measurement=="telemetry" and r._field=="pm25" and r.device_id=~/${dispositivo:regex}/)
  |> aggregateWindow(every: ${ventana}, fn: mean, createEmpty: false)
// Máximo / mínimo: cambiar fn: max  o  fn: min""", CODE),
 Spacer(1, .2*cm),
 tbl([["Panel", "Tipo", "Descripción"],
  ["KPI actuales", "Stat", "Último valor de pm25, temp_c, humidity, co2_ppm, estado online/offline"],
  ["Promedio, máx., mín.", "Stat / Table", "mean, max y min de cada variable en el rango seleccionado"],
  ["Series de tiempo", "Time series", "Una gráfica por familia (temperatura, humedad, PM2.5, CO2) comparando real vs. twin vs. API"],
  ["Mapa de ruta", "Geomap", "Posición del bus (latitud/longitud de API-GPS-01)"],
  ["Estado de dispositivos", "State timeline", "Disponibilidad (LWT) de los 10 dispositivos"]], [3.4*cm, 2.6*cm, 10.5*cm]),
 Spacer(1, .2*cm), P("Reglas y alertas (Grafana Alerting):", H2),
 tbl([["Regla", "Condición", "Severidad"],
  ["Aire: PM2.5 alto", "promedio 15 min de pm25 mayor a 37 ug/m3 (referencia: límite diario de la Res. 2254/2017; verificar vigencia)", "Crítica"],
  ["CO2 alto", "co2_ppm mayor a 1000 durante 10 min", "Media"],
  ["Calor", "temp_c mayor a 32 °C durante 10 min", "Media"],
  ["Dispositivo sin datos", "sin mensajes en 2 min (No Data) o status offline", "Alta"],
  ["Discrepancia real vs. API", "|temp real - temp API| mayor a 4 °C durante 30 min (posible descalibración)", "Baja"]], [3.8*cm, 10.2*cm, 2.5*cm]),
 P("Notificaciones: correo o Telegram como contact point de Grafana.", SM)]

S += [PageBreak(), P("6. Gráficas y análisis de comportamiento con IA", H1),
 P("Pasos: (1) dejar la plataforma 4-6 días; (2) capturar los dashboards; (3) ejecutar <font face='Courier'>analysis/ai_report.py</font>, que calcula promedio, máximo y mínimo horarios por dispositivo y variable, y pide a OpenAI una descripción; (4) <b>revisar y contrastar</b> el texto con las gráficas antes de incluirlo."),
 placeholder("Captura Grafana: Temperatura (real vs. twin vs. API) - 5 días"), Spacer(1, .2*cm),
 placeholder("Captura Grafana: PM2.5 / PM10 / CO2 - 5 días"), Spacer(1, .2*cm),
 placeholder("Captura Grafana: Ruta del bus (velocidad y mapa)"), Spacer(1, .2*cm),
 placeholder("Captura: Evento de retroceso (apagado, calibración) y alerta disparada", 3.5), Spacer(1, .3*cm),
 P("Plantilla del análisis (completar con los resultados reales):", H2),
 tbl([["Variable", "Prom.", "Máx.", "Mín.", "Comportamiento observado (IA, verificado por el grupo)"],
  ["temp_c", "[ ]", "[ ]", "[ ]", "[Ciclo diario, hora del pico, diferencia real vs. API]"],
  ["humidity", "[ ]", "[ ]", "[ ]", "[Relación inversa con la temperatura, lluvias]"],
  ["pm25", "[ ]", "[ ]", "[ ]", "[Picos en horas pico, alertas disparadas]"],
  ["co2_ppm", "[ ]", "[ ]", "[ ]", "[Ocupación / tráfico]"],
  ["velocidad bus", "[ ]", "[ ]", "[ ]", "[Paradas, congestión]"]], [2.6*cm, 1.5*cm, 1.5*cm, 1.5*cm, 9.4*cm])]

S += [P("7. Despliegue (resumen)", H1),
 Preformatted("""ssh -i C:\\Users\\Migue\\.ssh\\vm-iot-bus_key.pem azureuser@68.221.25.238
sudo apt update && sudo apt install -y docker.io docker-compose-v2 git certbot
git clone https://github.com/[USUARIO]/iot-capstone && cd iot-capstone
cp .env.example .env && nano .env        # llaves y contraseñas NUEVAS
sudo certbot certonly --standalone -d [TU_DOMINIO]
sudo docker compose up -d --build
# Crear usuario MQTT en EMQX (http://IP:18083) y datasource InfluxDB en Grafana""", CODE),
 P("Se recomienda reservar la IP como estática, abrir en el NSG solo los puertos necesarios y apagar la VM cuando no se use para ahorrar créditos.")]

S += [P("8. Conclusiones", H1), P("[Completar: qué se aprendió, limitaciones (p. ej. precisión de sensores, cuota de las APIs), trabajo futuro (LoRaWAN, más estaciones, modelos predictivos).]"),
 P("Referencias", H1),
 *bullets(["Microsoft. Azure Maps Weather REST API. https://learn.microsoft.com/es-es/rest/api/maps/weather?view=rest-maps-2025-01-01",
           "OASIS. MQTT Version 3.1.1 / 5.0 Specification. https://mqtt.org",
           "EMQX Documentation. https://docs.emqx.com",
           "InfluxData. InfluxDB 2 y Telegraf. https://docs.influxdata.com",
           "Grafana Labs. Grafana Documentation. https://grafana.com/docs",
           "OpenAI. API Reference. https://platform.openai.com/docs",
           "Ministerio de Ambiente de Colombia. Resolución 2254 de 2017 (calidad del aire)."])]

def foot(c, d):
    c.setFont("Helvetica", 8); c.setFillColor(colors.grey); c.drawString(2*cm, 1.2*cm, "Proyecto Final IoT a la Medida - UNAB"); c.drawRightString(19*cm, 1.2*cm, f"Pág. {d.page}")
SimpleDocTemplate("/mnt/user-data/outputs/Proyecto_Final_IoT_Bucaramanga.pdf", pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm,
    title="Proyecto Final IoT a la Medida").build(S, onFirstPage=foot, onLaterPages=foot)
print("pdf ok")

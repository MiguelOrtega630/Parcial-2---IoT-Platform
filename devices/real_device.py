"""Dispositivo REAL (Raspberry Pi / ESP32 con MicroPython equivalente). Uso: python real_device.py REAL-RPI-01"""
import sys
from common import Device

def make_reader():
    try:
        import board, adafruit_bme280.basic as bme
        s = bme.Adafruit_BME280_I2C(board.I2C(), address=0x76)
        return lambda: {"temp_c": s.temperature, "humidity": s.relative_humidity, "pressure_hpa": s.pressure}
    except Exception as e:
        print("BME280 no disponible, usando temperatura de CPU:", e)
        def cpu():
            with open("/sys/class/thermal/thermal_zone0/temp") as f: return {"cpu_temp_c": int(f.read()) / 1000}
        return cpu

if __name__ == "__main__":
    Device(sys.argv[1], "real", make_reader(), interval=10).run()

import network
import urequests
import time
from machine import Pin, ADC
import dht

# =========================
# WIFI CONFIG
# =========================
SSID = "BOE-"
PASSWORD = ""

# =========================
# FLASK SERVER
# =========================
SERVER_URL = "http://192.168.57.159:5000//api/update_sensor"

# =========================
# CONNECT WIFI
# =========================
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting WiFi...")
while not wifi.isconnected():
    time.sleep(1)

print("WiFi OK:", wifi.ifconfig())

# =========================
# DHT11
# =========================
dht_sensor = dht.DHT11(Pin(4))

# =========================
# MQ-135 (ADC)
# =========================
mq135 = ADC(Pin(35))
mq135.atten(ADC.ATTN_11DB)

# =========================
# LDR (ADC)
# =========================
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)

# =========================
# LOOP
# =========================
while True:
    try:
        # --- DHT11
        dht_sensor.measure()
        suhu = dht_sensor.temperature()        # °C
        kelembapan = dht_sensor.humidity()     # %

        # --- LDR
        cahaya = ldr.read()

        # --- MQ-135
        gas = mq135.read()

        data = {
            "suhu": suhu,
            "kelembapan": kelembapan,
            "cahaya": cahaya,
            "gas": gas
        }

        print("Kirim:", data)

        r = urequests.post(SERVER_URL, json=data)
        r.close()

    except Exception as e:
        print("ERROR:", e)

    time.sleep(5)

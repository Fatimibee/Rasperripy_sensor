import Adafruit_DHT
import spidev
import time
import requests
import json


DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# SPI for MCP3008 (for MQ and soil sensors)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

# Your Raspberry Pi IP
SERVER_URL = "http://192.168.144.78:5000/data"

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    mq2 = read_adc(0)
    mq7 = read_adc(1)
    soil = read_adc(2)

    if humidity is not None and temperature is not None:
        data = {
            'temperature': temperature,
            'humidity': humidity,
            'mq2': mq2,
            'mq7': mq7,
            'soil': soil
        }
        try:
            response = requests.post(SERVER_URL, json=data)
            print(f" Sent to server: {data}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("DHT11 Read Error")

    time.sleep(5)
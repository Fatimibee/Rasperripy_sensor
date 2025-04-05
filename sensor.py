from flask import Flask, render_template_string
import paho.mqtt.client as mqtt
import json

app = Flask(_name_)

latest_data = {
    "temperature": "N/A",
    "humidity": "N/A",
    "gas": "N/A",
    "soil": "N/A"
}

# MQTT Setup
broker = "test.mosquitto.org"
port = 1883
topic = "agrobotics/sensors"

def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT Broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global latest_data
    try:
        latest_data = json.loads(msg.payload.decode())
        print("Received:", latest_data)
    except Exception as e:
        print("Error decoding JSON:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
client.loop_start()

# HTML Template
html = '''
<html>
<head>
    <title>Sensor Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial; text-align: center; padding-top: 50px; }
        .card { display: inline-block; padding: 30px; background: #f4f4f4; border-radius: 10px; box-shadow: 0 0 10px #ccc; }
        h2 { color: #444; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🌡 Temperature: {{ temperature }} °C</h2>
        <h2>💧 Humidity: {{ humidity }} %</h2>
        <h2>🧪 Gas: {{ gas }}</h2>
        <h2>🌱 Soil: {{ soil }}</h2>
        <p>Refreshes every 5 seconds</p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html, **latest_data)

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
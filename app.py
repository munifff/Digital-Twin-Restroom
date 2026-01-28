from flask import Flask, render_template, jsonify, request
from threading import Lock
import time

app = Flask(__name__)

sensor_data = {
    'suhu': 0,
    'kelembapan': 0,
    'cahaya': 0,
    'gas': 0,
    'last_updated': 0
}
data_lock = Lock()

# =========================
# ESP32 → FLASK
# =========================
@app.route('/api/update_sensor', methods=['POST'])
def update_sensor():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "JSON kosong"}), 400

    with data_lock:
        sensor_data.update({
            'suhu': float(data.get('suhu', 0)),
            'kelembapan': float(data.get('kelembapan', 0)),
            'cahaya': float(data.get('cahaya', 0)),
            'gas': float(data.get('gas', 0)),
            'last_updated': time.time()
        })

    print("DATA MASUK:", sensor_data)
    return jsonify({"status": "success"})

# =========================
# FRONTEND → FLASK
# =========================
@app.route('/get_sensor_data')
def get_sensor_data():
    with data_lock:
        status = "online" if time.time() - sensor_data['last_updated'] < 30 else "offline"
        return jsonify({
            "status": status,
            **sensor_data
        })

# =========================
# ROUTES
# =========================
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dht11')
def dht11():
    return render_template('dht11.html')

@app.route('/ds18b20')
@app.route('/DS18B20')  # Menambahkan route alternatif untuk case sensitivity
@app.route('/ds18b20.html')
@app.route('/DS18B20.html')
def ds18b20():
    return render_template('DS18B20.html')

@app.route('/ldr')
@app.route('/LDR')  # Menambahkan route alternatif untuk case sensitivity
@app.route('/ldr.html')
@app.route('/LDR.html')
def ldr():
    return render_template('ldr.html')

@app.route('/mqtt135')
@app.route('/MQTT135')  # Menambahkan route alternatif untuk case sensitivity
@app.route('/mqtt135.html')
@app.route('/MQTT135.html')
def mqtt135():
    return render_template('MQTT135.html')

@app.route('/esp32')
@app.route('/ESP32')  # Menambahkan route alternatif untuk case sensitivity
@app.route('/esp32.html')
@app.route('/ESP32.html')
def esp32():
    return render_template('ESP32.html')

if __name__ == '__main__':
    print("Server berjalan di http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

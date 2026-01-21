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
# DASHBOARD
# =========================
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("Server berjalan di http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

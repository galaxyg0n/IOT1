from flask import Flask, jsonify, render_template
import requests
import json
from collections import defaultdict


WORKER_URL = "https://db-worker.mathiasen-simon.workers.dev/readings"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_safe_key123'

def get_database_data():
    res = requests.get(WORKER_URL, timeout=10)

    return res.json()

@app.route('/')
def home():
    data = get_database_data()

    grouped_by_greenhouse = defaultdict(lambda: defaultdict(list))

    for row in data:
        greenhouse = row['greenhouse']
        device     = row['device_name']
        timestamp  = row['timestamp']
        sensors    = {row["type"]: row["value"]}
        grouped_by_greenhouse[greenhouse][device].append({"timestamp": timestamp, "sensors": sensors})


    return render_template('index.html', grouped=grouped_by_greenhouse)

if __name__ == '__main__':
    # Start the application on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')

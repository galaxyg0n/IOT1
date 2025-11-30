# For Flask
from flask import Flask, render_template
from flask_socketio import SocketIO

# For MQTT
from paho.mqtt import client as mqtt_client
import random
import time

# Other stuff
from termcolor import colored

# --- Flask and SocketIO Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_safe_key123'
socketio = SocketIO(app, message_queue='redis://localhost:6379')

# --- MQTT Setup ---
broker = "localhost"
port = 1883
topics_to_sub = [
    "sensors/moisture/#",
    "sensors/temperature/#",
    "sensors/humidity/#"
]

client_id = f'sensor-mqtt-{random.randint(0, 1000)}'
mqtt_client_instance = None


def on_message(client, userdate, msg):
    topic = msg.topic
    
    payload = msg.payload.decode()
    print(colored(f'[MQTT] - Recieved: `{payload}` from `{topic}`... Pushing to WebSockets...', "green"))

    socketio.emit(
        'new_sensor_data',
        {'topic': topic, 'value': payload}
    )

def connect_and_sub_mqtt():
    global mqtt_client_instance

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(colored("[x] - Connected to MQTT Broker!", "blue"))

            for topic in topics_to_sub:
                client.subscribe(topic)
            print(colored("[X] - Subscribed to topics", "blue"))
        else:
            print(colored("[!] - Failed to connect to MQTT Broker!", "red"))

    
    client = mqtt_client.Client(
        client_id=client_id, 
        protocol=mqtt_client.MQTTv5
    )

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(broker, port)
        client.loop_start()
        mqtt_client_instance = client

    except Exception as e:
        print(colored(f'[!] - Exception during MQTT connection: {e}', "red"))


## ------------ Flask section ------------
@app.route('/')
def index():
    return render_template('index.html', known_topics=topics_to_sub)


@socketio.on('connect')
def connect_handler():
    print(colored("[X] - Client connected to WebSocket!", "blue"))


@socketio.on('disconnect')
def disconnect_handler():
    print(colored("[X] - Client disconnected to WebSocket!", "blue"))



if __name__ == "__main__":
    client = connect_and_sub_mqtt()

    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
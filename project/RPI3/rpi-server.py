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

# Generates random Client ID for the subscriber to connect as to the MQTT broker
client_id = f'sensor-mqtt-{random.randint(0, 1000)}'
mqtt_client_instance = None

# Handles incoming messages from publishers (sensor controllers) 
def on_message(client, userdate, msg):
    topic = msg.topic
    
    # Decodes incoming message and prints it to the terminal for verbosity
    payload = msg.payload.decode()
    print(colored(f'[MQTT] - Recieved: `{payload}` from `{topic}`... Pushing to WebSockets...', "green"))


    # Emits a socket event with the newly decoded message payload to the
    # WebSocket with the event name new_sensor_data
    socketio.emit(
        'new_sensor_data',
        {'topic': topic, 'value': payload}
    )

# Handles the connecting to the MQTT server and subscribes to all the topics given 
# in the topics_to_sub array + prints for verbosity
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

    # Creates client object with the generated client_id and specifies protocol
    # version as "the newest"
    client = mqtt_client.Client(
        client_id=client_id, 
        protocol=mqtt_client.MQTTv5
    )

    # Setting up the callback functions for the previously created handlers
    client.on_connect = on_connect
    client.on_message = on_message

    # Connects to the broker running as a systemctl service on the RPI and
    # starts a loop thread that processes network traffic
    try:
        client.connect(broker, port)
        client.loop_start()
        mqtt_client_instance = client

    except Exception as e:
        print(colored(f'[!] - Exception during MQTT connection: {e}', "red"))


# ------------ Flask section ------------
# This code should make sense by itself xD
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
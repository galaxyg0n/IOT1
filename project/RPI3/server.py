# For MQTT
from paho.mqtt import client as mqtt_client
import random
import time

# For web handling
import requests
import threading
from collections import defaultdict

# Other stuff
from termcolor import colored


# --- MQTT Setup ---
broker = "192.168.50.1"
port = 1883
topics_to_sub = [
    "sensors/moisture/#",
    "sensors/temperature/#",
    "sensors/humidity/#",
    "sensors/air_quality/#",
    "sensors/light_level/#"
]

# Generates random Client ID for the subscriber to connect as to the MQTT broker
client_id = f'greenhouse-{random.randint(0, 1000)}'
mqtt_client_instance = None


# --- API Setup ---
API_URL = 'https://iot-worker.mathiasen-simon.workers.dev'
headers = {
    "Content-Type": "application/json"
}

LOCK = threading.Lock()

SENSOR_DATA_STRUCT = defaultdict(lambda: {
    "rpi-1": {
        "temp_celsius": 0.0,
        "humidity_percent": 0.0,
        "soil_moisture": 0.0
    },
    "rpi-2": {
        "air_quality": "Unkown",
        "light_level": 0.0

    }
})


def send_data_to_api(update_rate=15):
    while True:
        try:

            with LOCK:
                data_to_send = dict(SENSOR_DATA_STRUCT)

            print(colored(f'[SENDER] - Attempting to send data for {len(data_to_send)}, greenhouse(s)', "magenta"))

            response = requests.post(
                API_URL,
                json=data_to_send,
                timeout=10
            )

            response.raise_for_status()

            print(colored(f'[SUCCESS] - Data sent successfully: Status {response.status_code}', "green"))

        except requests.exceptions.RequestsException as e:
            print(colored(f'[API ERROR] - Failed to send data: {e}', "red"))

        except Exception as e:
            print(colored(f'[ERROR] - Unexpected error in sender loop: {e}', "red"))

        time.sleep(update_rate)
                

# Handles incoming messages from publishers (sensor controllers) 
def on_message(client, userdate, msg):
    topic = msg.topic
    
    try:
        # Decodes incoming message and prints it to the terminal for verbosity
        payload_value = msg.payload.decode()
        
        topic_parts = topic.split('/')

        if len(topic_parts) != 3:
            print(colored(f'[WARN] - Topic format incorrect: {topic}', "yellow"))
            return

        sensor_type = topic_parts[1]
        greenhouse_id = topic_parts[2]

        rpi_key = "rpi-1" if sensor_type in ["moisture", "temperature", "humidity"] else "rpi-2"

        if sensor_type == "moisture":
            json_key = "soil_moisture"
            value = float(payload_value)

        elif sensor_type == "temperature":
            json_key = "temp_celsius"
            value = float(payload_value)

        elif sensor_type == "humidity":
            json_key = "humidity_percent"
            value = float(payload_value)

        elif sensor_type == "air_quality":
            json_key = "air_quality"
            value = payload_value

        elif sensor_type == "light_level":
            json_key = "light_level"
            value = float(payload_value)

        else:
            print(colored(f'[WARN] - Unknown sensor type: {sensor_type}', "yellow"))
            return
        
        with LOCK:
            if greenhouse_id not in SENSOR_DATA_STRUCT:
                SENSOR_DATA_STRUCT[greenhouse_id] = {
                    "rpi-1": {
                        "temp_celsius": 0.0,
                        "humidity_percent": 0.0,
                        "soil_moisture": 0.0
                    },
                    "rpi-2": {
                        "air_quality": "Unkown",
                        "light_level": 0.0

                    }
                }

            SENSOR_DATA_STRUCT[greenhouse_id][rpi_key][json_key] = value

        print(colored(f'[MQTT UPDATE] - GH: {greenhouse_id}, {rpi_key}/{json_key} updated to: {value}', "cyan"))

    except ValueError:
        print(colored(f'[!] - Could not convert payload "{payload_value}" to number...', "red"))

    except Exception as e:
        print(colored(f'[!] - Error processing message: {e}', "red"))


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
        return client

    except Exception as e:
        print(colored(f'[!] - Exception during MQTT connection: {e}', "red"))
        return None
    



if __name__ == "__main__":
    # Initialize and start the background sender thread
    sender_thread = threading.Thread(
            target=send_data_to_api, 
            args=(15,)
    )
    sender_thread.daemon = True # Allows the main program to exit even if this thread is running
    sender_thread.start()

    client = connect_and_sub_mqtt()

    if client:
        print(colored("[x] - Listening for incoming data... Press Ctrl+C to kill", "magenta"))

        try:
            client.loop_forever()

        except KeyboardInterrupt:
            print(colored("\n [x] - Exiting script with grace...", "magenta"))
            client.loop_stop()


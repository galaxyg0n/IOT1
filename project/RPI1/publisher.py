from paho.mqtt import client as mqtt_client
import grovepi

import math
import random
import time

# --- MQTT conf ---
broker = "192.168.50.1"
port = 1883
client_id = f'greenhouse-{random.randint(0, 1000)}'

# --- MQTT topics ---
moisture_topic = f'sensors/moisture/{client_id}'
temp_topic     = f'sensors/temperature/{client_id}'
humidity_topic = f'sensors/humidity/{client_id}'

## --- GrovePi sensor configuration ---
MOIST_SENSOR_PIN = 0 # A0 Analog input
DHT_SENSOR_PIN   = 4 # D4 Digital input

        
## --- GrovePi init ---
try:
    grovepi.pinMode(MOIST_SENSOR_PIN, "INPUT")
except Exception as e:
    print(f'Error in GrovePi init: {e}')



# Read data from the soil moist sensor
def read_moist():
    MIN_MOIST_LEVEL = 20
    MAX_MOIST_LEVEL = 700
    
    try:
        
        CURRENT_MOIST_READING = grovepi.analogRead(MOIST_SENSOR_PIN)
        MOIST_PERCENTAGE = float((CURRENT_MOIST_READING - MIN_MOIST_LEVEL) / (MAX_MOIST_LEVEL - MIN_MOIST_LEVEL)) * 100

        if MOIST_PERCENTAGE < 0:
            MOIST_PERCENTAGE = 0

        elif MOIST_PERCENTAGE > 100:
            MOIST_PERCENTAGE = 100

        return MOIST_PERCENTAGE

    except IOError:
        print(f'IOError in read_moist()')

    except Exception as e:
        print(f'Error: {e}')



# Read data from the Temperatur/Humidity (DHT) sensor
def read_temp_hum():
    SENSOR_TYPE = 0
    try:
        [temp, humidity] = grovepi.dht(DHT_SENSOR_PIN, SENSOR_TYPE)

        if not (math.isnan(temp) or math.isnan(humidity)):
            return [temp, humidity]
        else:
            print("[!] - Invalid reading from DHT (NaN)")
            return [None, None]

    except IOError:
        print('IOError in read_temp_hum()')
        return [None, None]

    except Exception as e:
        print(f'Error: {e}')
        return [None, None]


# --------------- MQTT Section ---------------

# Connects the publisher (sensor controller) to the MQTT broker running as a
# systemctl service on the server RPI. This is the same setup as from server.py
def connect_mqtt():
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("[x] - Connected to MQTT Broker!")
        else:
            print("[!] - Failed to connect to MQTT Broker!")

    
    client = mqtt_client.Client(
        client_id=client_id, 
        protocol=mqtt_client.MQTTv5
    )

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# Handles publishing to the MQTT broker from the sensor controller. Right now
# it publishes random sensor data for testing
def publish(client):
    while True:
        try:
            moisture = read_moist()
            time.sleep(0.1)
            [temp, humidity] = read_temp_hum()

            print(f'Reading: M={moisture}%, T={temp} C, H={humidity}%')

            publish_results = {}

            if moisture is not None:
                moisture_msg = f'{moisture:.2f}'
                info = client.publish(moisture_topic, moisture_msg)
                publish_results[moisture_topic]= (info, moisture_msg)

            if temp is not None:
                temp_msg = f'{temp:.2f}'
                info = client.publish(temp_topic, temp_msg)
                publish_results[temp_topic] = (info, temp_msg)

            if humidity is not None:
                humidity_msg = f'{humidity:.2f}'
                info = client.publish(humidity_topic, humidity_msg)
                publish_results[humidity_topic] = (info, humidity_msg)

            for topic, (info, msg) in publish_results.items():
                if info.rc == mqtt_client.MQTT_ERR_SUCCESS:
                    print(f'[x] - Sent `{msg}` to topic `{topic}`')
                else:
                    print(f'[!] - Failed to send message to topic `{topic}` (RC: {info.rc})')


            time.sleep(5)

        except KeyboardInterrupt:
            print("\nKilling the program...")
            break

        except Exception as e:
            print(f'An error has occurred in publish loop: {e}')
            time.sleep(5)


def run():
    client = connect_mqtt()
    client.loop_start()

    publish(client)
    
    client.loop_stop()
    


if __name__ == "__main__":
    run()

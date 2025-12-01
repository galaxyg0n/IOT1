from paho.mqtt import client as mqtt_client
import random
import time

broker = "localhost"
port = 1883
client_id = f'sensor-{random.randint(0, 1000)}'
moisture_topic = f'sensors/moisture/{client_id}'
temp_topic     = f'sensors/temperature/{client_id}'
humidity_topic = f'sensors/humidity/{client_id}'


        
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
    topics = [moisture_topic, temp_topic, humidity_topic]
    msg_count = 1

    # Here the real sensor reading would get implemented
    while True:
        time.sleep(1)
        msg = f'message: {msg_count + random.randint(0, 1000)}'

        publish_results = {}

        for topic in topics:
            info = client.publish(topic, msg)
            publish_results[topic] = info

        for topic, info in publish_results.items():
            if info.rc == mqtt_client.MQTT_ERR_SUCCESS:
                print(f'[x] - Send `{msg}` to topic `{topic}`')
            else:
                print(f'[!] - Faild to send message to topic `{topic}`')


        msg_count += 1
        if msg_count > 5:
            break

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()
    


if __name__ == "__main__":
    run()
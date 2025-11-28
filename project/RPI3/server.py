from paho.mqtt import client as mqtt_client
import random
import time

broker = "localhost"
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'



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


def subscribe(client: mqtt_client):
    def on_message(client, userdate, msg):
        print(f'Recieved: `{msg.payload.decode()}` from `{msg.topic}`')

    client.subscribe(topic)
    client.on_message = on_message 

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    


if __name__ == "__main__":
    run()
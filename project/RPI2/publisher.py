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


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f'message: {msg_count}'
        info = client.publish(topic, msg)

        if info.rc == mqtt_client.MQTT_ERR_SUCCESS:
            print(f'[x] - Send `{msg}` to topic `{topic}`')
        else:
            print(f'[!] - Failed to send message to topic `{topic}`')

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
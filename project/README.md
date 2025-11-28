# IOT project

Smart Greenhouse / Terrarium Network 

Concept: Create a self-regulating miniature ecosystem distributed across three zones (the Pis).

Pi Roles:

    Pi 1 (Soil Station): Uses Soil Moisture Sensor and Temperature/Humidity Sensor (DHT). Publishes local environment data.

    Pi 2 (Air & Light Station): Uses Air Quality Sensor and Light Sensor. Publishes atmospheric data.

    Pi 3 (Control & Broker): Runs the Mosquitto MQTT Broker, subscribes to all sensor data, and uses a Relay to control a simulated device (e.g., a fan or pump connected to the relay) based on thresholds from Pi 1 and Pi 2.

Scalability: Easily add more "zones" (new Pis) or more types of sensors (e.g., pH, UV) to the system without changing the central control logic.

## RPI roles
### RPI 1 - 172.16.33.31 (red)
The first RPI will be in control of the sensors close to the plants. Here there will be a soil moisture, a Temperature and a Humidity sensor.

### RPI2 - 172.16.33.31 (purple)
The second RPI will be in control of the general environment of the greenhouse. It will hold the air quality sensor and the sun light sensor.

### RPI3 - (black)
The third and last RPI will be in charge of the communication and logic. It will act as the broker for MQTT. 

## Sensors
- Temperature/Humidity Sensor
- Air pressure Sensor
- Light Sensor

## Actuators
- "Fan"


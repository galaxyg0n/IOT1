#!/bin/bash

# --- Configuration ---
SENSOR_SCRIPT="sensor_reader.py"
PUBLISHER_SCRIPT="mqtt_publisher.py"

echo "Stopping background services..."

# Find the PID (Process ID) for the sensor reader
PID_SENSOR=$(pgrep -f "$SENSOR_SCRIPT")
if [ -n "$PID_SENSOR" ]; then
    echo "Stopping Sensor Reader (PID: $PID_SENSOR)..."
    kill "$PID_SENSOR"
else
    echo "Sensor Reader is not running."
fi

# Find the PID for the MQTT publisher
PID_PUBLISHER=$(pgrep -f "$PUBLISHER_SCRIPT")
if [ -n "$PID_PUBLISHER" ]; then
    echo "Stopping MQTT Publisher (PID: $PID_PUBLISHER)..."
    kill "$PID_PUBLISHER"
else
    echo "MQTT Publisher is not running."
fi

echo "Services shutdown attempted."
sleep 1
./runapp.sh status

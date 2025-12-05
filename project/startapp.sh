#!/bin/bash

# --- Configuration ---
SENSOR_SCRIPT="sensor_reader.py"
PUBLISHER_SCRIPT="mqtt_publisher.py"
LOG_DIR="logs"
SENSOR_LOG="$LOG_DIR/sensor.log"
PUBLISHER_LOG="$LOG_DIR/publisher.log"

# Function to check the status of the running processes
status() {
    echo "--- Current Application Status ---"
    # Search for the processes using 'pgrep'
    PID_SENSOR=$(pgrep -f "$SENSOR_SCRIPT")
    PID_PUBLISHER=$(pgrep -f "$PUBLISHER_SCRIPT")

    if [ -n "$PID_SENSOR" ]; then
        echo "✅ Sensor Reader is RUNNING (PID: $PID_SENSOR). Log: $SENSOR_LOG"
    else
        echo "❌ Sensor Reader is STOPPED."
    fi

    if [ -n "$PID_PUBLISHER" ]; then
        echo "✅ MQTT Publisher is RUNNING (PID: $PID_PUBLISHER). Log: $PUBLISHER_LOG"
    else
        echo "❌ MQTT Publisher is STOPPED."
    fi
    echo "----------------------------------"
}

# Function to start the processes
start() {
    # Check if they are already running
    PID_SENSOR=$(pgrep -f "$SENSOR_SCRIPT")
    PID_PUBLISHER=$(pgrep -f "$PUBLISHER_SCRIPT")

    if [ -n "$PID_SENSOR" ] || [ -n "$PID_PUBLISHER" ]; then
        echo "Services appear to be already running. Run './runapp.sh status' to confirm."
        return 1
    fi

    # Create log directory if it doesn't exist
    mkdir -p $LOG_DIR
    
    echo "Starting Sensor Reader..."
    # 'nohup' runs the command immune to hangups. The output is redirected to the log file.
    nohup python3 $SENSOR_SCRIPT > $SENSOR_LOG 2>&1 &
    
    echo "Starting MQTT Publisher..."
    nohup python3 $PUBLISHER_SCRIPT > $PUBLISHER_LOG 2>&1 &

    sleep 2 # Give a moment for processes to start
    echo "--- Startup Complete ---"
    status
}

# --- Main Script Execution ---
case "$1" in
    start)
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: ./runapp.sh {start|status}"
        echo "Use './stopapp.sh' to stop the services."
        exit 1
esac

exit 0

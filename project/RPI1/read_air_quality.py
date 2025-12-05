#!/usr/bin/env python

import time
import grovepi

SENSOR_PIN = 1

grovepi.pinMode(SENSOR_PIN, "INPUT")

while True:
    try:
        sensor_value = grovepi.analogRead(SENSOR_PIN)

        if sensor_value > 700:
            print("High pollution")
        
        elif sensor_value > 300:
            print("Low pollution")

        else:
            print("Air quality nice...")

        print("Sensor: ", sensor_value) 
        time.sleep(0.5)

    except KeyboardInterrupt:
        break
    
    except IOError:
        print("IO error")

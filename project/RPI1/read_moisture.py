#!/usr/bin/env python

# Air : 350
# 

import time
import grovepi

SENSOR_PIN = 0 #A0 analog pin

grovepi.pinMode(SENSOR_PIN, "INPUT")

MIN_MOIST = 20
MAX_MOIST = 700



while True:
    try:
        CURRENT_READING = grovepi.analogRead(SENSOR_PIN)
        moist_percent = float((CURRENT_READING - MIN_MOIST) / (MAX_MOIST - MIN_MOIST)) * 100
        
        if moist_percent < 0:
            moist_percent = 0
        
        elif moist_percent > 100:
            moist_percent = 100

        print(f'Raw Reading: {CURRENT_READING}')
        print(f'Moisture Percentage: {moist_percent:.2f}%')
        time.sleep(1)

    except KeyboardInterrupt:
        break

    except IOError:
        print("Error in communicating with GrovePi")

    except Exception as e:
        print(f'Error: {e}')


#!/usr/bin/env python

import time
import math
import grovepi


MOIST_SENSOR_PIN = 0 # A0 Analog input
DHT_SENSOR_PIN   = 4 # D4 Digital input

grovepi.pinMode(MOIST_SENSOR_PIN, "INPUT")

# Roughly dirt min/max


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


while True:
    try:
        print(f'Moisture Percentage: {read_moist():.2f}%')
        
        time.sleep(0.1) # Delay for reading

        [temp, humidity] = read_temp_hum()
        print("Temp: %.02f C | Humidity: %.02f %%" % (temp, humidity))

        time.sleep(1)

    except KeyboardInterrupt:
        break

    except IOError:
        print("IO error")

    except Exception as e:
        print(f'Error: {e}')

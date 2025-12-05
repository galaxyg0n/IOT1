#!/usr/bin/env python

import time
import grovepi

SENSOR_PIN = 1

while True:
    try:
        temp = grovepi.temp(SENSOR_PIN, '1.1')
        print("temp = ", temp)
        time.sleep(5)

    except KeyboardInterrupt:
        break

    except IOError:
        print("IO Error")


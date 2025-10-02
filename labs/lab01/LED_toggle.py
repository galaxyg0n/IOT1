import time
import grovepi

pot_meter = 0

state = True

LED_1 = 5
LED_2 = 6

grovepi.pinMode(pot_meter, "INPUT")
grovepi.pinMode(LED_1, "OUTPUT")
grovepi.pinMode(LED_2, "OUTPUT")
time.sleep(1)

adc_ref = 5
grove_vcc = 5
full_angle = 400

MAX_TIME = 1.5
MIN_TIME = 0.1

while True:
    try:
        sensor_val = grovepi.analogRead(pot_meter)

        # Calculate voltage
        voltage = round((float)(sensor_val) * adc_ref / 1023, 2)

        # Linear mapping
        speed = 0.25 + (sensor_val / 1023.0) * (MAX_TIME - MIN_TIME)

        print("Speed = %.1f" %(speed))
        
        if(state):
            grovepi.analogWrite(LED_2, 0)
            grovepi.analogWrite(LED_1, 255)
            state = False
        else:
            grovepi.analogWrite(LED_1, 0)
            grovepi.analogWrite(LED_2, 255)
            state = True
        
        time.sleep(speed)


    except KeyboardInterrupt:
        grovepi.analogWrite(LED_1, 0)
        grovepi.analogWrite(LED_2, 0)

        break
    except IOError:
        print(f'Error: {IOError}')
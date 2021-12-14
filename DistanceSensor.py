# import RPi.GPIO as GPIO
# import time
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# TRIG = 15
# ECHO = 14
# print("Distance Measurement in Process")
# GPIO.setup(TRIG, GPIO.OUT)
# GPIO.setup(ECHO, GPIO.IN)
# print("Warning for Sensor To Settle")
# time.sleep(2)
# GPIO.output(TRIG, True)
# time.sleep(0.00001)
# GPIO.output(TRIG, False)
# while GPIO.input (ECHO)==0:
#     pulse_start = time.time()
# while GPIO.input(ECHO)==1:
#     pulse_end = time.time()
# pulse_duration=pulse_end-pulse_start
# distance = pulse_duration*17150
# distance = round(distance,2)
# print(f"Distance:", distance, "cm")
# GPIO.cleanup()


# 2nd Method
import RPi.GPIO as gpio
import time

def distance(measure='cm'):
    try:
        gpio.setmode(gpio.BCM)
        gpio.setup(15, gpio.OUT)
        gpio.setup(14, gpio.IN)
        
        gpio.output(15, False)
        while gpio.input(14) == 0:
            nosig = time.time()

        while gpio.input(14) == 1:
            sig = time.time()

        tl = sig - nosig

        if measure == 'cm':
            distance = tl / 0.000058
        elif measure == 'in':
            distance = tl / 0.000148
        else:
            print('improper choice of measurement: in or cm')
            distance = None

        gpio.cleanup()
        return distance
    except:
        distance = 100
        gpio.cleanup()
        return distance

		
if __name__ == "__main__":
    print(distance('cm'))
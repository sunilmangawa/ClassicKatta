#predifined liabraries
from time import sleep
import time
from datetime import date, datetime
import RPi.GPIO as GPIO
from threading import Thread


# PIN Setting for Katta Button & LED
GPIO.setmode(GPIO.BCM) # use GPIO numbering
GPIO.setwarnings(True)
overload = 27

GPIO.setup(overload, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(overload,GPIO.IN)

# Overload Check
# count=100
def overload():
    try:
        sleep(3)
        while True:
            # count <=200
            if GPIO.input(overload)==1:
                counter_overload = 0
                print("Not Overloaded & Do This")
                time.sleep(1)
            else:
                counter_overload += 1
                print(f'"Overloaded count", {counter_overload}')
                time.sleep(1)
                if counter_overload>=5:
                    print('Mall off for 10 Seconds')
                    time.sleep(10)
                else:
                    continue

    except KeyboardInterrupt:
        print("Quit")
        #GPIO.cleanup()

def exit_test():
    if sys.argv== signal.SIGINT:
        os.kill()
        raise KeyboardInterrupt

if __name__ == '__main__':
    Thread(target = overload).start()
    Thread(target = exit_test).start()
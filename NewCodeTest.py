from datetime import datetime
from gpiozero import Button
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # use GPIO numbering
GPIO.setwarnings(True)
button = 5
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(button,GPIO.IN)
count=0
startTime=time.time()
while True:
    if GPIO.input(button)==0:
        # t1= time.time()
        print(f'Katta laga hua hai')
        time.sleep(2)
        # t2= time.time()
        # print(t2-t1)
        # time.sleep(1)
    elif GPIO.input(button)==1:
        t3= time.time()
        # print(f"Katta Out")
        time.sleep(2)
        if GPIO.input(button)==0:
            if (time.time()-t3)>=2.0:
                count += 1
                endTime=time.time()
                try:
                    if startTime:
                        fillTime=endTime-startTime
                        startTime=0
                        otherTime=endTime
                        x=datetime.now().strftime("%H:%M:%S")
                        print(f"{count}'Katta Bhar Gaya in TIME ' {round(fillTime,2)}' '{x}")
                    elif otherTime:
                        fillTime=otherTime-endTime
                        otherTime=endTime
                        x=datetime.now().strftime("%H:%M:%S")
                        print(f"{count}'Katta Bhar Gaya in TIME ' {round(fillTime,2)}''{x}")
                    else:
                        print(f'Katta Laga Hua HAI')
                except:
                    pass
        else:
            continue
    else:
        if GPIO.input(button)==0:
            t3= time.time()
            print(f'"The button was released! .....2 second........" {t3}')
            time.sleep(2)
#predifined liabraries
import os
import sys
sys.path.append('/home/pi/.local/lib/python3.10/site-packages/gpiozero/__init__.py')
from gpiozero import LED, Button
from time import sleep
import time
from datetime import date, datetime
import RPi.GPIO as GPIO
from threading import Thread
import signal
import mysql.connector


# PIN Setting for Katta Button & LED
GPIO.setmode(GPIO.BCM) # use GPIO numbering
GPIO.setwarnings(True)
button = 5
led = 22 #GPIO22  PIN NO 22
overloadbtn = 27

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

GPIO.setup(overloadbtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(overloadbtn,GPIO.IN)

#led.source=button

#Database Configuration
mydb = mysql.connector.connect(
  host="localhost",
  user="coder",
  password="w24",
  database="c2m1"
)
curA = mydb.cursor(buffered=True)
sql = "INSERT INTO small(katta, filltime, date, time, avgkatta) VALUES(%s, %s, %s, %s, %s)"

# Auto timer PIN setting for Vibrator & Conveyar
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.HIGH)

GPIO.setup(19,GPIO.OUT)
GPIO.output(19,GPIO.HIGH)

GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.HIGH)

GPIO.setup(21,GPIO.OUT)
GPIO.output(21,GPIO.HIGH)


dateToday=date.today()
counted_bag=0
startTime=time.time()
#firstTime=time.time()

def katta_counter():
    global counted_bag, dateToday, startTime, firstTime
    while True:
        if GPIO.input(button)==0:
            # t1= time.time()
            # print(f'Katta laga hua hai')
            GPIO.output(led, 0)
            time.sleep(2)
            # t2= time.time()
            # print(t2-t1)
            # time.sleep(1)
        elif GPIO.input(button)==1:
            t3= time.time()
            GPIO.output(led, 1)
            # print(f"Katta Out")
            time.sleep(2)
            if GPIO.input(button)==0:
                if (time.time()-t3)>=2.0:
                    GPIO.output(led, 0)
                    counted_bag += 1
                    endTime=time.time()
                    kattatime=datetime.now().strftime("%H:%M:%S")
                    try:
                        if startTime:
                            firstTime=endTime-120
                            fillTime=round((endTime-firstTime),2)
                            otherTime=endTime
                            averageKatta=round(((counted_bag/(endTime-firstTime))*3600),2)
                            print(f" Katta FULL ! No. {counted_bag} Filling_Time {fillTime} Clock_Time {kattatime} Average = {averageKatta}")
                            val = (counted_bag, fillTime, dateToday, kattatime, averageKatta)
                            #curA.execute(sql, val)
                           #mydb.commit()
                            startTime=0

                        elif otherTime:
                            fillTime=round((endTime-otherTime),2)
                            otherTime=endTime
                            averageKatta=round(((counted_bag/(endTime-firstTime))*3600),2)
                            print(f" Katta FULL ! No. {counted_bag} Filling_Time {fillTime} Clock_Time {kattatime} Average = {averageKatta}")
                            val = (counted_bag, fillTime, dateToday, kattatime, averageKatta)
                            #curA.execute(sql, val)
                            #mydb.commit()
                        else:
                            print(f'Katta Laga Hua HAI')
                    except:
                        pass
            else:
                continue
        # else:
        #     if GPIO.input(button)==0:
        #         t3= time.time()
        #         print(f'"The button was released! .....2 second........" {t3}')
        #         time.sleep(2)

# Auto timer function to control Vibrator & Conveyar
count=100
def timeauto():
    try:
        counter_overload = 0
        sleep(60)
        while True:
            count <=200
            if GPIO.input(overloadbtn)==1:
                print("System start")
                GPIO.output(21,GPIO.LOW)
                print("vibrator on")
                time.sleep(2)
                GPIO.output(21,GPIO.HIGH)
                time.sleep(2)

                for i in range(1,10):
                    if GPIO.input(overloadbtn) != 0:
                        GPIO.output(19,GPIO.LOW)   #mall pin on
                        print("mall on")
                        time.sleep(2)
                        GPIO.output(19,GPIO.HIGH) # 1loop mallpin low
                        time.sleep(13)
                        GPIO.output(13,GPIO.LOW)
                        print("mall off")
                        time.sleep(2)
                        GPIO.output(13,GPIO.HIGH)
                        time.sleep(1)
                        time.sleep(23)
                time.sleep(40)
                GPIO.output(26,GPIO.LOW)
                time.sleep(1)
                print("vibrator off")
                time.sleep(2)
                GPIO.output(26,GPIO.HIGH)
                time.sleep(1)
                print("All off")
                time.sleep(430)

            else:
                counter_overload += 1
                if counter_overload>=5:
                    print('OverLoaded So Mall off for 1200 Seconds')
                    time.sleep(1200)
                    
    except KeyboardInterrupt:
        print("Quit")
        #GPIO.cleanup()
def exit_test():
    if sys.argv== signal.SIGINT:
        os.kill()
        raise KeyboardInterrupt

if __name__ == '__main__':
    Thread(target = katta_counter).start()
    #Thread(target = timeauto).start()
    Thread(target = exit_test).start()
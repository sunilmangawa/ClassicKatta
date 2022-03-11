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

GPIO.setmode(GPIO.BCM) # use GPIO numbering
GPIO.setwarnings(True)
button = 5
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(button,GPIO.IN)

mydb = mysql.connector.connect(
  host="localhost",
  user="coder",
  password="w24",
  database="c2m1"
)

curA = mydb.cursor(buffered=True)

sql = "INSERT INTO small(katta, filltime, date, time, avgkatta) VALUES(%s, %s, %s, %s, %s)"
dateToday=date.today()
counted_bag=0
startTime=time.time()
firstTime=time.time()
while True:
    if GPIO.input(button)==0:
        # t1= time.time()
        # print(f'Katta laga hua hai')
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
                counted_bag += 1
                endTime=time.time()
                kattatime=datetime.now().strftime("%H:%M:%S")
                try:
                    if startTime:
                        fillTime=round((endTime-startTime),2)
                        otherTime=endTime
                        averageKatta=round(((counted_bag/(endTime-firstTime))*3600),2)
                        print(f" Katta FULL ! No. {counted_bag} Filling_Time {fillTime} Clock_Time {kattatime} Average = {averageKatta}")
                        val = (counted_bag, fillTime, dateToday, kattatime, averageKatta)
                        curA.execute(sql, val)
                        mydb.commit()
                        startTime=0

                    elif otherTime:
                        fillTime=round((endTime-otherTime),2)
                        otherTime=endTime
                        averageKatta=round(((counted_bag/(endTime-firstTime))*3600),2)
                        print(f" Katta FULL ! No. {counted_bag} Filling_Time {fillTime} Clock_Time {kattatime} Average = {averageKatta}")
                        val = (counted_bag, fillTime, dateToday, kattatime, averageKatta)
                        curA.execute(sql, val)
                        mydb.commit()
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
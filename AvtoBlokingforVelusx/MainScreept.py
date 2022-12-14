import sys
from socket import *
import serial
import time
import RPi.GPIO as GPIO
import threading

import sys, os
from xml.dom import minidom

def LoadData(itemName):
    location = os.path.abspath(os.path.dirname(sys.argv[0]))
    way = location+"/Data.xml" 
    mydoc = minidom.parse(way)
    items = mydoc.getElementsByTagName(itemName)
    return items[0].firstChild.data

def SaveData(itemName,value):
    location = os.path.abspath(os.path.dirname(sys.argv[0]))
    way = location+"/Data.xml" 
    mydoc = minidom.parse(way)
    items = mydoc.getElementsByTagName(itemName)
    items[0].firstChild.data = value

    fw = open(way, 'w')
    fw.write(mydoc.toxml())
    fw.close()

def checkCode(arg):
    masMask = ["831377", "863724", "834293", "831459", "835070", "830809", "869068", "863753"]
    #masMask = LoadData("MasOfMasks").split(";")
    mask = arg[0:6]
    for s in masMask:
        if mask==s:
            return True
    return False
def HTTP_Server():
    print("HTTP_Server_Thread start!")



try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)  # set up pin 17
    GPIO.output(17, 1)  # turn on pin 17
    GPIO.setup(18, GPIO.OUT)  # set up pin 17
    GPIO.output(18, 1)  # turn on pin 17

    #conection to scaner
    start  = bytearray([0x4C, 0x4F,0x4E, 0x0D])
    end = bytearray([0x4C, 0x4F,0x46,0x46 ,0x0D])
    #ser = serial.Serial(port=2,baudrate=115200, timeout = 1)
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.flushInput()
    ser.flushOutput()
    encoding = 'utf-8'
    data = ""
    print("Start work!")
    #tSleep = 1200
    bSleep = False
    b = False

    #Start thread for HTTP severa
    HTTP_Server_Thread = threading.Thread(target=HTTP_Server)
    HTTP_Server_Thread.start()

    while True:
        try:
            c =ser.read()
            if c==b'\r':
                    if len(data)>5:
                        b = checkCode(data)
                        if b!=bSleep:
                            bSleep = b
                            print("Start wayt tSleep")
                            SaveData("LastScan", data[0:6])
                            time.sleep(int(LoadData("DelayTime")))
                            #clear buer in sereal port
                            ser.flushInput()
                            ser.flushOutput()
                            
                            print("Stop wayt tSleep")
                        if b:
                            print("rele ON")
                            GPIO.output(17, 0)
                            GPIO.output(18, 0)
                            SaveData("ReleStatus", "ON")
                        else:
                            print("rele OFF")
                            GPIO.output(17, 1)
                            GPIO.output(18, 1)
                            SaveData("ReleStatus", "OFF")
                    #print(data)
                    
                    c =ser.read()
                    data = ""
            data = data+c.decode(encoding)
        except Exception:
            print("Was exception!")
        time.sleep(0.001)
    ser.close()
except Exception:
    print("Was exception in main screep!")
    

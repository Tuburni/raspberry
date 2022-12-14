import sys, os
from xml.dom import minidom
import time

def SaveData(itemName,value):
    location = os.path.abspath(os.path.dirname(sys.argv[0]))
    way = location+"/Data.xml" 
    mydoc = minidom.parse(way)
    items = mydoc.getElementsByTagName(itemName)
    items[0].firstChild.data = value

    fw = open(way, 'w')
    fw.write(mydoc.toxml())
    fw.close()

def LoadData(itemName):
    location = os.path.abspath(os.path.dirname(sys.argv[0]))
    way = location+"/Data.xml" 
    mydoc = minidom.parse(way)
    items = mydoc.getElementsByTagName(itemName)
    return items[0].firstChild.data

def checkMaskArray():
    masks = LoadData("MasOfMasks").split(";")
    
    print (masks)



SaveData("ReleStatus", "OFF")


while(True):
    time.sleep(1)
    checkMaskArray()





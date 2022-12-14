from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from xml.dom import minidom
import sys, os
import threading

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
    
def getListOfMask(dataText):
    return dataText.split(sep=";")

class S(BaseHTTPRequestHandler):
        
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            #print(self.path)
            
            
            self._set_response()
            location = os.path.abspath(os.path.dirname(sys.argv[0]))
            #print(location)
            wayPath = location + self.path
            index = ""
            #wayPath = 'C:/Users/2259070/source/repos/AvtoBloking for Velusx' + self.path
            if self.path== "/" :
                wayPath = location + "/Home.html"
                page = open(wayPath,'r')
                index = page.read()[3:]
                self.wfile.write(index.encode('utf-8'))
            if self.path== "/Home.html" :
                page = open(wayPath,'r')
                index = page.read()[3:]
                self.wfile.write(index.encode('utf-8'))
            if self.path == "/Style_Home.css" :
                page = open(wayPath,'r')
                index = page.read()[3:]
                self.wfile.write(index.encode('utf-8'))
            if self.path == "/Script_Home.js":
                page = open(wayPath,'r')
                index = page.read()
                self.wfile.write(index.encode('utf-8'))
            if self.path == "/Jabil_Logo.jpg" :
                page = open(wayPath,'rb')
                index = page.read()
                self.wfile.write(index)
            if self.path== "/favicon.ico" :
                page = open(wayPath,'rb')
                index = page.read()
                self.wfile.write(index)
            if self.path == "/Masks":
                ms = ""
                for m in mask:
                    ms = ms + m + ";"
                #print(ms)
                self.wfile.write(ms[:-1].encode('utf-8'))
            if self.path == "/DealyTime":
                self.wfile.write(str(delayTime).encode('utf-8'))
            if self.path == "/Rele":
                self.wfile.write(LoadData("ReleStatus").encode('utf-8'))
            if self.path == "/TimeToCheng":
                self.wfile.write(timeToChengStatus.encode('utf-8'))
            if self.path == "/LastScan":
                self.wfile.write(LoadData("LastScan").encode('utf-8'))
            #print(index)
            #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        except:
            print("Dont wory! GET!")
        

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
            if self.path =="/SaveMask":
                msg = post_data.decode('utf-8')
                print(msg)
                SaveData("MasOfMasks",msg)
                global mask
                mask = getListOfMask(msg)
                print("Post: " + str(mask))
                self._set_response()
                index = "SaveMask"
                self.wfile.write(format(index).encode('utf-8'))
                #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
            if self.path =="/SaveTimeDelay":
                msg = post_data.decode('utf-8')
                print(msg)
                SaveData("DelayTime",msg)
                global delayTime
                delayTime = int(msg)
                print("Post: " + str(delayTime))
                self._set_response()
                index = "SaveDelayTime"
                self.wfile.write(format(index).encode('utf-8'))
                #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        except:
            print("Dont wory! POST!")


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


def Server():
    try:
        print("Server run")
        if __name__ == '__main__':
            from sys import argv
            if len(argv) == 2:
                run(port=int(argv[1]),MasksItems = mask, DelayTime = delayTime)
            else:
                run()
    except Exception:
        
        print("Server Error!")

global mask
global delayTime
global rele
global timeToChengStatus
global lastScan

mask = getListOfMask(LoadData("MasOfMasks"))
delayTime = int(LoadData("DelayTime"))
lastScan = LoadData("LastScan")
rele = "ON"
timeToChengStatus = "1200"

#lastScan = "88888"

t = threading.Thread(target=Server)
t.start()




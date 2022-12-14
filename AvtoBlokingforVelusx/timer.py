import time
import math


def actualTime(wayt):
    was = time.time()
    k=0
    while wayt>k:
        k = time.time() - was
        print("K=",k)
        time.sleep(0.1)
    print("End!")

#def actualTimeNow:
    
actualTime(3)

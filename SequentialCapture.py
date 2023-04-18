## A trial GUI for DED control - click - capture

from sre_constants import IN
from tkinter import *
from tkinter import filedialog
from tokenize import Name
#from tkinter import ttk
from datetime import datetime


import numpy as np
from cmath import pi
#from MCSControl_PythonWrapper import *
import time
import sys
import ctypes as ct
import pypixet

pypixet.start()
pixet = pypixet.pixet

isTPX3 = False

devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)
if not devices:
    print("No devices connected")
else:
    dev = devices[0] # use  the first device
    #dev.loadFactoryConfig()
    dev.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
    #tfield.insert(INSERT, f"Connected to: {dev} and set to Event+iToT mode.\n")
    print(f"Connected to: {dev} and set to Event+iToT mode.")
    isTPX3 = True

frame_time = [0.0001, 0.001, 0.005, 0.01, 0.05, 0.1]
# frame_time = [0.0001, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05]
#frame_time = [0.0001, 0.001]
frame_num = 50

path = 'C:\\Users\\tianbi\\Documents\\TKD\\20230407_al\\r1s7_r2'

for i in range(len(frame_time)):
    current_frame_time = frame_time[i]
    
    frametime_string = str(current_frame_time).replace(".","")
    filename = path + "\\" + f"{frametime_string}s_{frame_num}fs.h5"
    
    

    try:
        rc = dev.doSimpleAcquisition(frame_num, frame_time[i], pixet.PX_FTYPE_AUTODETECT, filename)
        #rc = dev.doSimpleIntegralAcquisition(1, 0.01, pixet.PX_FTYPE_AUTODETECT, filename)
        #CurrentTime = RecordTime()
        if rc == 0:
            #tfield.insert(INSERT, f"{CurrentTime}: Acquired to {filename}.\n")
            print(f"Acquired to: {filename}.")
        else:
            #tfield.insert(INSERT, "No devices connected. \n")
            print(f"No devices connected.")
    except NameError:
        ##tfield.insert(INSERT, "No devices connected. \n")
        print(f"No devices connected.\n")
    
    time.sleep(0.1)

    
pypixet.exit()
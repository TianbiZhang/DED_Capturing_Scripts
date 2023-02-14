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
    dev.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
    #tfield.insert(INSERT, f"Connected to: {dev} and set to Event+iToT mode.\n")
    print(f"Connected to: {dev} and set to Event+iToT mode.")
    isTPX3 = True

frame_time = [0.0001, 0.001, 0.005, 0.01, 0.05, 0.1]
#frame_time = [0.0001, 0.001]
frame_num = 50

path = 'C:\\Users\\tianbi\\Documents\\TKD\\SeqAcqTrial'

for i in range(len(frame_time)):
    current_frame_time = frame_time[i]
    filename = path + "\\" + f"{current_frame_time}s_{frame_num}fs.h5"
    
    

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
    if isTPX3:
        #CurrentTime = RecordTime()
        temp = dev.temperature(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)
        rounded_temperature = '{0:.5g}'.format(temp)
        ##tfield.insert(INSERT, f"{CurrentTime}: T = {rounded_temperature}. \n")
        print(f"T={rounded_temperature}")
    
    time.sleep(0.5)

    
pypixet.exit()
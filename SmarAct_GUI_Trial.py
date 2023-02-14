## A trial GUI for Martin's SmarAct work

from tkinter import *
import asynctkinter as at

#from tkinter import ttk

import numpy as np
from cmath import pi
from MCSControl_PythonWrapper import *
import time
from datetime import datetime
import sys
import ctypes as ct

mcsHandle = ct.c_ulong()
error_msg = ct.c_char_p()
status = ct.c_ulong()
status_find = ct.c_ulong()
status_open = ct.c_ulong()
error_msg = ct.c_char_p()

def RecordTime():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
    return timestampStr

def TextOutputWithTime(text):
    CurrentTime = RecordTime()
    tfield.insert(INSERT, f"{CurrentTime} " + text + "\n")
    tfield.see("end")

class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
 
        self.title("The Most Primitive Controller by Martin Heller and Tianbi Zhang")
        self.minsize(640,480)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)

def SmarActReadAngular():
    ## TextOutputWithTime("a")

    global angle_ct 
    global rev_ct
    angle_ct = ct.c_ulong()
    rev_ct = ct.c_ulong()

    status = SA_GetAngle_S(mcsHandle, 2, angle_ct, rev_ct)
    if(status != SA_OK):
        print("Error reading current angle!")
        return False
    else:
        TextOutputWithTime(f"{angle_ct.value}, {rev_ct.value}")
        #TextOutputWithTime(f"{rev_ct.value}")
    return

def SmarActInitialize():
    ## Initialize the SmarAct API and connect to the controller.
    # Find all available MCS systems
    outBuffer = ct.create_string_buffer(17) 
    ioBufferSize = ct.c_ulong(18)
    status_find = SA_FindSystems('', outBuffer, ioBufferSize) #will report a 'MCS error: query-buffer size' if outBuffer, ioBufferSize is to small
    
    if(status_find != SA_OK):
        SA_GetStatusInfo(status_find, error_msg)
        TextOutputWithTime('MCS error: {}'.format(error_msg.value[:].decode('utf-8')))
        return
    else:
        TextOutputWithTime('MCS address: {}'.format(outBuffer[:18].decode("utf-8"))) #connect to first system of list

    # If there is no error (a system is found), proceed to open the system
    status_open = SA_OpenSystem(mcsHandle,outBuffer, bytes('sync,reset',"utf-8")) #// open the first MCS with USB interface in synchronous communication mode

    if(status_open != SA_OK):
        SA_GetStatusInfo(status_open, error_msg)
        TextOutputWithTime('MCS error: {}'.format(error_msg.value[:].decode('utf-8')))
        return
    else:
        TextOutputWithTime("System initialized.")
    
    return 

# SmarActRotateCW and CCW: rotate the stage according to the angle selected in the drop-down menu
# GotoAngleRelative_S is used, where the 3rd argument is the rotation angle in micro-degrees (1E-6)
# positive value: ccw; negative : cw
# A 3-second wait is built in to allow for full rotation (this can be made optional)

def SmarActRotateCW():
    ## Rotate clockwise
    # Read from the drop-down menu
    rotationanglestring = optionsAngleSelection.get()

    rotationangle = int(rotationanglestring) * (-1) * (10 ** 6)
    rotationangle_ct =  ct.c_long(rotationangle)

    # Excecute the rotation
    status = SA_GotoAngleRelative_S(mcsHandle, 2, rotationangle_ct, 0, 0)

    # Chick if there is error
    if(status != SA_OK):
        SA_GetStatusInfo(status, error_msg)
        TextOutputWithTime('MCS error: {}'.format(error_msg.value[:].decode('utf-8')))
    else:
        time.sleep(3)
        TextOutputWithTime("Rotated clockwise by " + rotationanglestring + " deg.")
    
    return

def SmarActRotateCCW():
    ## Rotate counterclockwise
    # this is essentially the same as rotate clockwise, but a CCW rotation is positive in SmarAct's sense.
    rotationanglestring = optionsAngleSelection.get()
    
    rotationangle = int(rotationanglestring) * (10 ** 6)
    rotationangle_ct =  ct.c_long(rotationangle)

    status = SA_GotoAngleRelative_S(mcsHandle, 2, rotationangle_ct, 0, 0)

    if(status != SA_OK):
        SA_GetStatusInfo(status, error_msg)
        TextOutputWithTime('MCS error: {}'.format(error_msg.value[:].decode('utf-8')))
        return
    else:
        time.sleep(3)
        TextOutputWithTime("Rotated counterclockwise by " + rotationanglestring + " deg.")
    return

def SmarActCompucentric():
    ## Placeholder
    TextOutputWithTime("Excecution finished. ")
    return

def SmarActExit():
    # Exit SmarAct control API. This is recommended before closing the window if a controller is connected.
    status = SA_CloseSystem(mcsHandle)

    if(status != SA_OK):
        SA_GetStatusInfo(status, error_msg)
        TextOutputWithTime('MCS error: {}'.format(error_msg.value[:].decode('utf-8')))
    return

##

def SmarActCheckAngular():

    iter = 405
    log_freq = 40
    sleeptime = 20/log_freq

    TextOutputWithTime("Test Started.")
    TextOutputWithTime("Record Initial position.")
    for k in range(10):
        SmarActReadAngular()
        time.sleep(0.5)

    for i in range(iter):
        SmarActRotateCCW()
        readstatus = SmarActReadAngular()
        if readstatus == False:
            return

        for j in range(log_freq):
            
            time.sleep(sleeptime)
            readstatusin = SmarActReadAngular()
            if readstatusin == False:
                return
    return

def WriteLogFile():
    filename = "logfile.txt"

    with open(filename, 'w') as f:
        f.writelines(tfield.get("1.0",END))
        f.close
    
    TextOutputWithTime(f"Log file generated at: {filename}.")

# Initialize the GUI window
root = Root()

# Button for initialization
b_initialize = Button(root, text="Initialize SmarAct", font=("Arial", 10), command=SmarActInitialize, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_initialize.grid(column=0,row=0,sticky=W, padx=5, pady=5)

# Drop-down menu for rotation angle selection
optionsAngleSelection = StringVar(root)
optionsAngleSelection.set("5")

labelAngleSelection = Label(root, text='Select Rotation Angle (degrees)', width=30 )  
labelAngleSelection.grid(column=2, row=1, sticky=E, padx=5,pady=5) 
AngleList = ["1", "2", "3", "5", "6", "12", "15", "30", "60", "90", "180", "360"] # Change this list when needed
menuAngleSelection = OptionMenu(root, optionsAngleSelection, *AngleList) # menu option from the list
menuAngleSelection.grid(column=3, row=1, sticky=W, padx=5,pady=5)


# Button for rotation, CW and CCW
b_rotatecw=Button(root, text="Rotate CW", font=("Arial", 10), command=SmarActRotateCW, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_rotatecw.grid(column=0, row=1, sticky=W, padx=5, pady=5)

b_rotateccw=Button(root, text="Rotate CCW", font=("Arial", 10), command=SmarActRotateCCW, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_rotateccw.grid(column=1, row=1, sticky=W, padx=1, pady=5)

# Button for compucentric correction
b_compucentric=Button(root, text="Compucentric Correction", font=("Arial", 10), command=SmarActCompucentric, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_compucentric.grid(column=1, row=2, sticky=W, padx=1, pady=5)

# Button for close SmarAct control (API)
b_exitsmaract=Button(root, text="Close SmarAct", font=("Arial", 10), command=SmarActExit, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_exitsmaract.grid(column=0, row=3, sticky=W, padx=5, pady=5)

# Button for closing the window
exit_button = Button(root, text="Exit Program", command=root.destroy, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
exit_button.grid(column=1, row=3, sticky=W, padx=1, pady=5)

testlog_button = Button(root, text="Test Program", command=SmarActCheckAngular, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
testlog_button.grid(column=2, row=3, sticky=W, padx=1, pady=5)

logrec_button = Button(root, text="Write Log", command=WriteLogFile, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
logrec_button.grid(column=3, row=3, sticky=W, padx=1, pady=5)

labelExitNotice = Label(root, text='Please close SmarAct controls first before closing the window.')
labelExitNotice.grid(column=2, row=7, columnspan=3, sticky=W, padx=5, pady=5)

# Console
labelConsole = Label(root, text='Output console') # Label
labelConsole.grid(column=0, row=4, sticky=W, padx=5, pady=1)
tfieldScroll = Scrollbar(root) # Scroll bar
tfield = Text(root, width=60, height=15) # text field itself
tfieldScroll.grid(column=5, row=5, sticky=N+S+W)
tfield.grid(column=0, row=5, columnspan = 5, sticky=W, padx=5, pady=5)
tfieldScroll.config(command=tfield.yview)
tfield.config(yscrollcommand=tfieldScroll.set)

# Copyright Declaration
labelCopyinfo = Label(root, text='This widget is developed by Martin Heller and Tianbi Zhang, Septemebr 2022. All rights reserved.', width=80 )  
labelCopyinfo.grid(column=0, row=6, columnspan = 4, sticky=W, padx=5,pady=1) 

root.mainloop()
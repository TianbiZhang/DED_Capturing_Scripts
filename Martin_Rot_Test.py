## A trial GUI for Martin's SmarAct work
import numpy as np
from cmath import pi
from MCSControl_PythonWrapper import *
import time
from datetime import datetime
import sys
import ctypes as ct

def RecordTime():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
    return timestampStr

def TextOutputWithTime(text):
    CurrentTime = RecordTime()
    print(f"{CurrentTime} " + text)


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
        exit()
    else:
        TextOutputWithTime("System initialized.")
    
    return 

# SmarActRotateCW and CCW: rotate the stage according to the angle selected in the drop-down menu
# GotoAngleRelative_S is used, where the 3rd argument is the rotation angle in micro-degrees (1E-6)
# positive value: ccw; negative : cw
# A 3-second wait is built in to allow for full rotation (this can be made optional)

def SmarActRotateCCW(angle):
    rotationangle = int(angle) * (10 ** 6)
    rotationangle_ct =  ct.c_long(rotationangle)

    status = SA_GotoAngleRelative_S(mcsHandle, 2, rotationangle_ct, 0, 0)

    if(status != SA_OK):
        SA_GetStatusInfo(status, error_msg)
        TextOutputWithTime('MCS error: {}'.format(error_msg.value[:].decode('utf-8')))
    else:
        time.sleep(3)
        TextOutputWithTime(f"Rotated counterclockwise by {angle} deg.")
    return

def SmarActReadAngular():
    ## TextOutputWithTime("a")

    global angle_ct 
    global rev_ct
    angle_ct = ct.c_ulong()
    rev_ct = ct.c_ulong()

    status = SA_GetAngle_S(mcsHandle, 2, angle_ct, rev_ct)
    if(status != SA_OK):
        print("Error reading current angle!")
        return
    else:
        TextOutputWithTime(f"{angle_ct.value/(10**6)}, {rev_ct.value}")
    return

def SmarActExit():
    # Exit SmarAct control API. This is recommended before closing the window if a controller is connected.
    status = SA_CloseSystem(mcsHandle)

    if(status != SA_OK):
        SA_GetStatusInfo(status, error_msg)
        TextOutputWithTime('MCS error: {}'.format(error_msg.value[:].decode('utf-8')))
    else:
        TextOutputWithTime("SmarAct Closed.")
    return

mcsHandle = ct.c_ulong()
error_msg = ct.c_char_p()
status = ct.c_ulong()
status_find = ct.c_ulong()
status_open = ct.c_ulong()
error_msg = ct.c_char_p()

def main():
    SmarActInitialize()

    time.sleep(2)

    total_rot = 3
    wait_time = 5 * 60
    rec_freq = 10 #Hz
    rec_intv = 1 / rec_freq
    total_rec = wait_time * rec_freq

    ## Get some data to plot the initial angular reading
    for k in range(100):
        SmarActReadAngular()
        time.sleep(0.01)

    ## Main loop: rotate
    for i in range(total_rot):
        SmarActRotateCCW(5)
        time.sleep(0.5)

        ## Give it some time to settle, then start logging for 5 minutes, and repeat
        for j in range(total_rec):
            time.sleep(rec_intv)
            SmarActReadAngular()
        time.sleep(0.1)

    
    TextOutputWithTime("Test Completed.")
    SmarActExit()

    

if __name__ == "__main__":
    main()
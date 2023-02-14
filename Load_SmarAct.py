# Load_SmarAct.py
# This is a short script that initializes and connect the SmarAct MCS system.
# Can be used for quick testing and debugging of MCS.
# Created by Tianbi Zhang, October 2021

## Load libraries
# Necessary libraries?
import numpy as np
import time # for timing

## SmarAct libraries and required ctype library
from MCSControl_PythonWrapper import *
import ctypes as ct

# check dll version
smaract_version = ct.c_ulong()
SA_GetDLLVersion(smaract_version)
print('DLL-version: {}'.format(smaract_version.value))

## Connect to SmarAct

# Obtain state variables of the MCS system
# Find all available MCS systems
# The following code will connect to first system on the list
outBuffer = ct.create_string_buffer(17) 
ioBufferSize = ct.c_ulong(18)
SA_FindSystems('', outBuffer, ioBufferSize)
print('MCS address: {}'.format(outBuffer[:18].decode("utf-8"))) 
sensorEnabled = ct.c_ulong(0) #initialize sensorEnbaled variable
mcsHandle = ct.c_ulong() #initialize MCS control handle

# Open the first MCS with USB interface in synchronous communication mode
# If running this line alone and succesfully, you should hear a click and an output of 0.
SA_OpenSystem(mcsHandle, outBuffer, bytes("sync,reset", "utf-8"))

SA_GetSensorEnabled_S(mcsHandle,sensorEnabled)

# Print MCS status. Will change this into a one-line function call.
if (sensorEnabled.value == SA_SENSOR_DISABLED): 
    print("Sensors are disabled: {}\n".format(sensorEnabled.value))
elif (sensorEnabled.value == SA_SENSOR_ENABLED): 
    print("Sensors are enabled: {}\n".format(sensorEnabled.value)) 
elif (sensorEnabled.value == SA_SENSOR_POWERSAVE): 
    print("Sensors are in power-save mode: {}\n".format(sensorEnabled.value)) 
else:
    print("Error: unknown sensor power status: {}\n".format(sensorEnabled.value))

[Position_C0, Position_C1, Position_C2] = [ct.c_ulong(), ct.c_ulong(), ct.c_ulong()]

SA_GetPosition_S(mcsHandle, ct.c_int(0), Position_C0)
SA_GetPosition_S(mcsHandle, ct.c_int(1), Position_C1)
SA_GetPosition_S(mcsHandle, ct.c_int(2), Position_C2)
        
positions_n = [Position_C0.value, Position_C1.value, Position_C2.value]

print(positions_n)
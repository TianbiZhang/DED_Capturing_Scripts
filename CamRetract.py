## CamRetract.py
# This script will perform a synchronized task by the SmarAct stage and the DED (PIXET)
# combining stage motion and image capturing.
# Created by: Tianbi Zhang in October 2021.
# Translated from the original MATLAB script by Alex Foden and T. Ben Britton.

# Note: We used python 3.7 to accomodate PIXET 1.7.5.915 and the new MiniPix TimePix 3 DED. 
# Other versions of python, older or newer, will not work!

## Load libraries
# Necessary libraries?
import numpy as np
import time # for timing
import click # for keyboard input confirmation

## SmarAct libraries and required ctype library
from MCSControl_PythonWrapper import *
import ctypes as ct

## Pixet: load library, software and check connection
import pypixet # Official pypixet library

## Connect to SmarAct
# check SmarAct/MCS dll version
smaract_version = ct.c_ulong()
SA_GetDLLVersion(smaract_version)
print('DLL-version: {}'.format(smaract_version.value))

# Obtain state variables of the MCS system
# Find all available MCS systems
outBuffer = ct.create_string_buffer(17) 
ioBufferSize = ct.c_ulong(18)
SA_FindSystems('', outBuffer, ioBufferSize)
print('MCS address: {}'.format(outBuffer[:18].decode("utf-8"))) 

#connect to first system of list
sensorEnabled = ct.c_ulong(0) #initialize sensorEnbaled variable
mcsHandle = ct.c_ulong() #initialize MCS control handle

# Open the first MCS with USB interface in synchronous communication mode
# If running this line alone and succesfully, you should hear a click and an output of 0.
SA_OpenSystem(mcsHandle, outBuffer, "sync,reset".encode("utf-8"))

# Print MCS status. Will change this into a one-line function call.
SA_GetSensorEnabled_S(mcsHandle,sensorEnabled)

if (sensorEnabled.value == SA_SENSOR_DISABLED): 
    print("Sensors are disabled: {}\n".format(sensorEnabled.value))
elif (sensorEnabled.value == SA_SENSOR_ENABLED): 
    print("Sensors are enabled: {}\n".format(sensorEnabled.value)) 
elif (sensorEnabled.value == SA_SENSOR_POWERSAVE): 
    print("Sensors are in power-save mode: {}\n".format(sensorEnabled.value)) 
else:
    print("Error: unknown sensor power status: {}\n".format(sensorEnabled.value))

# Load PIXET interface
pypixet.start()
pixet = pypixet.pixet # get pixet API
print("PIXET Version: " + pixet.pixetVersion()) # print pixet version

# Detect connected devices: list all Medipix/Timepix devices and use the first one
# N.B. use PX_DEVTYPE_MPX2 for old Minipix DEDs, and PX_DEVTYPE_TPX3 for the newer TimePix3 DED
devices = pixet.devicesByType(pixet.PX_DEVTYPE_MPX2)

if not devices:
    print("No PIXET devices connected")
    exit()

# use the first device on the list
pixet_device = devices[0]

## Preamble; define constants
## Parameters and constants
# SmarAct
dist_z = 100 * 10 # Distance to move in um (microns)
dist_x = 1 # in um (microns)

# Camera parameters
exp_num = 0 # Number of exposures (N.B. Python 0 --> 1 exposure)
acqCount = 100 # Number of frames
acqTime = 0.05 # time per frame in seconds
n_to_run = int(50 / 10) # Number of retractions

# Make an array of positions to go to. Positions of each stage occupies a
# row in the np array.
# N.B. int32 in MATLAB = int in py
positions_n = np.zeros((3, n_to_run), dtype=int)

## Capturing routines
tic = time.time() # start timing

# First for loop: from the starting position, move the camera and take a picture at each increment
try:
    # First for loop: move the Z-stage incrementally and capture an image at each position.
    for n in range(0, n_to_run):
        print(n)

        dist_z_real = -1 * dist_z * 1000 # convert distance into nm
        dist_x_real = -1 * dist_x * 1000 # convert distance into nm

        # Index of channels (stages): 
        # 0 = x, 1 = y, 2 = z by default (Same as MCE Config)
        # Pay attention to the index should you use a different hybrid stage setup!
       
        # Move the stage by the given increment
        SA_GotoPositionRelative_S(mcsHandle, 2, dist_z_real, 1) # Move z stage # MCS,channel,distance,hold_time=1
        SA_GotoPositionRelative_S(mcsHandle, 0, dist_x_real, 1) # Move x stage # MCS,channel,distance,hold_time=1

        # Create a directory to store the captured images and log files
        # Change to relative directory, so there is no need to change the directory when running on other computers
        
        # Create and write the log file with file name and camera parameters
        f = open('images\dummy.txt','w')
        h5_file = 'retract_z' + '{:03}'.format(n) + '.h5'
        h5_name = 'C:\\Users\\tianbi\\Documents\\DED_script_new\\images\\' + h5_file # file name
        f.write('%s\n' % h5_name )
        f.write('%s\n' % exp_num)
        f.write('%s\n' % acqCount)
        f.write('%s\n' % acqTime)
        f.close()
        
        time.sleep(2) # Pause for 2 seconds to let it settle
        
        # Reset the position of the stage
        # SA_GotoPositionAbsolute_S(mcsHandle, 0, 0, 1)

        # Get the positions of the stages and record in a vector
        Position_C0, Position_C1, Position_C2 = ct.c_int(), ct.c_int(), ct.c_int()
        # N.B. for SA_GetPosition_S, simply initialize the position variables 
        # and use them as the third argument. 
        # Do not do the following: Position_C0 = SA_GetPosition_S(mcsHandle, ct.c_int(0), Position_C0)
        # That will result in an putput of 0 (since the function successfully excecuted)
        SA_GetPosition_S(mcsHandle, ct.c_int(0), Position_C0)
        SA_GetPosition_S(mcsHandle, ct.c_int(1), Position_C1)
        SA_GetPosition_S(mcsHandle, ct.c_int(2), Position_C2)
        
        positions_n[0][n], positions_n[1][n], positions_n[2][n] = Position_C0.value, Position_C1.value, Position_C2.value
        
        # Call the DED capturing py script, stop clock
        # The python script will read parameters from the logfile.
        # Will change this to a more direct path by importing the py script
        # and feed the arguments. Log file will be written separately.
        pixet_device.doSimpleAcquisition(acqCount, acqTime, pixet.PX_FTYPE_AUTODETECT, h5_name)
        
        toc = time.time()
        elapsed = toc - tic
        print("Time elapsed = ", elapsed, "s")

    # Prompt keyboard input to retrieve the stage
    #if click.confirm('Please defocus the beam now (CTRL+M on microscope)> [Y] > ', default = True):
        #pass

    # A short pause
    time.sleep(2)

    # Second for loop to retract camera, then extend it, and capture at each incremental position
    for n in range(0, n_to_run):
        # Move stage to positions stored in the position array
        SA_GotoPositionAbsolute_S(mcsHandle, 0, ct.c_int(positions_n[0][n]), 1)
        SA_GotoPositionAbsolute_S(mcsHandle, 1, ct.c_int(positions_n[1][n]), 1)
        SA_GotoPositionAbsolute_S(mcsHandle, 2, ct.c_int(positions_n[2][n]), 1)

        # Write patterns into h5 files.
        # Give names to the h5 files. This will be updated each iteration.
        f = open('C:\\Users\\tianbi\\Documents\\DED_script_new\\images\\dummy.txt','w')
        h5_file = 'retract_z_bg' + '{:03}'.format(n) + '.h5'
        h5_name = 'C:\\Users\\tianbi\\Documents\\DED_script_new\\images\\' + h5_file # file name
        f.write('%s\n' % h5_name )
        f.write('%s\n' % exp_num)
        f.write('%s\n' % acqCount)
        f.write('%s\n' % acqTime)
        f.close()

        time.sleep(2) # pause to let it settle

        [Position_C0, Position_C1, Position_C2] = [ct.c_ulong(), ct.c_ulong(), ct.c_ulong()]
        # N.B. for SA_GetPosition_S, simply initialize the position variables 
        # and use them as the third argument. 
        # Do not do the following: Position_C0 = SA_GetPosition_S(mcsHandle, ct.c_int(0), Position_C0)
        # That will result in an putput of 0 (since the function successfully excecuted)
        SA_GetPosition_S(mcsHandle, ct.c_int(0), Position_C0)
        SA_GetPosition_S(mcsHandle, ct.c_int(1), Position_C1)
        SA_GetPosition_S(mcsHandle, ct.c_int(2), Position_C2)
        
        # What is the purpose of this?
        positions_nbg = [Position_C0, Position_C1, Position_C2]

        ## Call the capturing function
        pixet_device.doSimpleAcquisition(acqCount, acqTime, pixet.PX_FTYPE_AUTODETECT, h5_name)

        toc = time.time()
        elapsed = toc - tic
        print("Time elapsed = ", elapsed, "s")
    
    # Out of the capturing loop
    # Close SmarAct
    print('Closing SmarAct')
    SA_CloseSystem(mcsHandle)
    print('Code complete')

except SystemError:
    print('Closing SmarAct')
    SA_CloseSystem(mcsHandle)
    print('Code complete with error')


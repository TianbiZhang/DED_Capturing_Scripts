# This script calls the PIXET API, captures an image and save the image to a file.
# A threshold energy is set.
# Use for tuning, profiling and debugging only.

## Preamble
# import os # This might be needed when migrating everything from python
#! /usr/bin/env python
from cgi import print_environ
import pypixet
# import time

# This reads all variables from the main script that calls this script.
#from __main__ import *

# initialize pixet
# Please check version of PIXET. For TimePix 3, must use latest version of PIXET. 
# tic1 = time.time()

pypixet.start()

# get pixet API
pixet = pypixet.pixet

# print pixet version
# print(pixet.pixetVersion())

# List all Medipix/Timepix devices and use the first one
# N.B. use PX_DEVTYPE_MPX2 for old Minipix DEDs, and PX_DEVTYPE_TPX3 for the newer TimePix3 DED

devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)

if not devices:
    print("No devices connected")
    exit()

device = devices[0] # use  the first device

# exp_num = 0 # Number of exposures (N.B. Python 0 --> 1 exposure)
# acqCount = 1 # Number of frames
# acqTime = 5 # time per frame in seconds


## Acquisition (save to files)
# Adapted from the example script provided by Advacam.
# See script/acquisition_example.py in the installation directory of PIXET Pro for details.

#rc = device.doSimpleAcquisition(acqCount, acqTime, pixet.PX_FTYPE_AUTODETECT, outputFile)

#print(device.threshold(0, pixet.PX_THLFLG_ENERGY))

init_ths = device.threshold(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)
rounded_init_ths = '{0:.5g}'.format(init_ths)

print("Initial Threshold: " + str(rounded_init_ths) + " keV")

print("Threshold sweep will start from 3 keV with 3 keV increments until 60 keV.")

# Default threshold is 3 keV
energy = 3.000 # keV

for i in range(20):
    if energy <= 60:
        device.setThreshold(pixet.PX_MPXDACS_CHIP_ALL, energy, pixet.PX_THLFLG_ENERGY)
    
        ##outputFile = "images\ethtest"+str(energy)+".h5"
    
        # device.doSimpleAcquisition(acqCount, acqTime, pixet.PX_FTYPE_AUTODETECT, outputFile)

        #print("Image taken at threshold (keV):" + str(device.threshold(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)))
        threshold_read = device.threshold(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)
        rounded_ths = '{0:.5g}'.format(threshold_read)
        print("Threshold (keV): " + rounded_ths)

        energy += 3.000

pypixet.exit()
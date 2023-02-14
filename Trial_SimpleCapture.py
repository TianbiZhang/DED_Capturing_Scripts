# This script calls the PIXET API, captures an image and save the image to a file.
# Use for tuning, profiling and debugging only.

## Preamble
# import os # This might be needed when migrating everything from python
#! /usr/bin/env python
import pypixet
#import time

# This reads all variables from the main script that calls this script.
#from __main__ import *

# initialize pixet
# Please check version of PIXET. For TimePix 3, must use latest version of PIXET. 
#tic1 = time.time()

#pypixet.start()

# get pixet API
pixet = pypixet.pixet

# print pixet version
#print("Pixet Version:" + pixet.pixetVersion())

# List all Medipix/Timepix devices and use the first one
# N.B. use PX_DEVTYPE_MPX2 for old Minipix DEDs, and PX_DEVTYPE_TPX3 for the newer TimePix2 DED

#devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)

#if not devices:
#    print("No devices connected")
#    exit()

# add the exit() so that the last error message is "no device connected".

#device = devices[0] # use  the first device

exp_num = 0 # Number of exposures (N.B. Python 0 --> 1 exposure)
acqCount = 100 # Number of frames
acqTime = 0.05 # time per frame in seconds
outputFile = "test.h5"
#tic2 = time.time()
## Acquisition (save to files)
# Adapted from the example script provided by Advacam.
# See script/acquisition_example.py in the installation directory of PIXET Pro for details.

rc = device.doSimpleAcquisition(acqCount, acqTime, pixet.PX_FTYPE_AUTODETECT, outputFile)

#toc = time.time()
#elapsed = toc-tic2
#print("loading time: " + str(tic2-tic1) + 's')
#print("capturing time: " + str(elapsed) + "s")
#print("total time: " + str(toc-tic1) + 's')

# pypixet.exit()
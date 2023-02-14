## pyCap2_new.py
# This script calls the PIXET API, captures an image and save the image to a file.

## Preamble
# import os # This might be needed when migrating everything from python
#! /usr/bin/env python
import pypixet

# This reads all variables from the main script that calls this script.
from __main__ import *

# initialize pixet
# Please check version of PIXET. For TimePix 3, must use latest version of PIXET. 
pypixet.start()

# get pixet API
pixet = pypixet.pixet

# print pixet version
print(pixet.pixetVersion())

# List all Medipix/Timepix devices and use the first one
# N.B. use PX_DEVTYPE_MPX2 for old Minipix DEDs, and PX_DEVTYPE_TPX3 for the newer TimePix2 DED

devices = pixet.devicesByType(pixet.PX_DEVTYPE_MPX2)

if not devices:
    print("No devices connected")
    exit()

# add the exit() so that the last error message is "no device connected".

device = devices[0] # use  the first device

## Acquisition (save to files)
# Adapted from the example script provided by Advacam.
# See script/acquisition_example.py in the installation directory of PIXET Pro for details.

def acqExample1():
    
    # read the file text for the filename
    # Again, for convenience, may better use relative directory.
    # the filename of the image to be saved
    # Suggestion: keep the log file, but pass directly the variables (parameters) from the main file. This should shorten it significantly

    # The block below should not matter anymore if read variables successfullyt from the main script.
    # They are kept here for debugging purposes.
    #filename_txt = open('C:\\Users\\tianbi\\Documents\\DED_Stage\\images\\dummy.txt','r')
    #f1=filename_txt.read()
    #filename_txt.close()
    # Read the parameters from the text file
    #n1=f1.find('\n')
    #filename=f1[0:n1]
    
    #exposure time
    s2=f1[n1+1:]
    n2=s2.find('\n')
    exp_num=int(s2[0:n2])
    
    #aquire count
    s3=s2[n2+1:]
    n3=s3.find('\n')
    acqCount=int(s3[0:n3])
    
    #time per exposure, s
    s4=s3[n3+1:]
    n4=s4.find('\n')
    acqTime=float(s4[0:n4])
    
    #outputFile = filename + ".h5"
    #for i in range(exp_num):

    # capture
    rc = device.doSimpleAcquisition(acqCount, acqTime, pixet.PX_FTYPE_AUTODETECT, outputFile)
    

acqExample1()


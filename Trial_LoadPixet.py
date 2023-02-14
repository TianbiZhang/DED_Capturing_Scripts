# For testing purposes only

## Preamble
# import os # This might be needed when migrating everything from python
#! /usr/bin/env python
import pypixet

# This reads all variables from the main script that calls this script.
#from __main__ import *

# initialize pixet
# Please check version of PIXET. For TimePix 3, must use latest version of PIXET. 

pypixet.start()

# get pixet API
pixet = pypixet.pixet

# print pixet version
print("Pixet Version:" + pixet.pixetVersion())

devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)

if not devices:
    print("No devices connected")
    exit()

# add the exit() so that the last error message is "no device connected".

device = devices[0] # use the first device

#pypixet.exit()
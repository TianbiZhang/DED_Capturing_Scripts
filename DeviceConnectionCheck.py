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
    devices = "No devices detected."
    print(devices)
else:
    for device in devices:
        print(device)

pypixet.exit()
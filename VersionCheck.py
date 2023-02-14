# This script calls the PIXET API, captures an image and save the image to a file.
# Use for tuning, profiling and debugging only.

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

pypixet.exit()
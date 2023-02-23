"""
mask.trial.py

Tianbi Zhang, February 2023

This script generates an approximately circular mask in the detector pixel array.

Inputs: 
    PC_x, PC_y: x, y coordinates of the centre of the circle. This could be the pattern centre of your TKP, etc.
    radius: radius of the circle mask

Outputs:
    Masked device (the mask will not reset when you open Pixet Pro)
    Optional: new configuration file as an .xml file.

This script is originally written for MiniPIX TPX3 devices. 
The factory configuration is stored in the detector and can be reset using the loadFactoryConfig() function, or using the PIXET Pro GUI.

For older devices such as a Medipix-based MiniPIX, please do the following first: 
    (1) Update the decive type identifier (from TPX3 to e.g. MPX2)
    (2) Locate the factory configuration file and read it in lieu of using loadFactoryConfig() (see line 72)
"""

import pypixet

# initialize pixet 
pypixet.start()

# get pixet API
pixet = pypixet.pixet

# List all Timepix3 devices and use the first one:
devices = pixet.devicesByType(pixet.PX_DEVTYPE_MPX2)
if not devices:
    raise "No devices connected"
device = devices[0] # use the first device

devicename = device.deviceID()
print(devicename)

# load factory config to reset; otherwise the new mask will overlap with previously applied ones
#device.loadFactoryConfig()
# Use the line below for older devices
loadfactoryconfig = device.loadConfigFromFile("C:\\Users\\billy\\Documents\\GitHub\\DEDCapturingScripts\\CustomConfig\\C08-W0294.xml")

# Create a reference to the pixel configuration
dpc = device.pixCfg()

# Mask pixels one by one in the calculated list
rc1 = dpc.maskRect(0,0,148,256, True) # mask the left half
rc2 = dpc.maskRect(128,0,128,148, True) # mask the bottom right quarter
rc3 = dpc.maskRect(128,250,128,6,True) # mask the upper rows
rc3 = dpc.maskRect(250,0,6,256,True) # mask the rightmost rows

# Save new configuration to a file
configname = "C:\\Users\\billy\\Documents\\GitHub\\DEDCapturingScripts\\CustomConfig\\NewMaskConfig_MPX2.xml"
device.saveConfigToFile(configname)

# exit
pypixet.exit()
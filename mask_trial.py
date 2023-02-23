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

# User inputs: PC and radius
PC_x = 128
PC_y = 128
radius = 20

# Calculate all the coordinates and convert them to pixel ID (0-65535)
def coordinates(PCx, PCy, R):
    for x in range(-R, R+1):
        Y = int((R*R - x*x)**0.5)
        for y in range(-Y, Y+1):
            xcoord = x+PCx
            ycoord = y+PCy
            yield (xcoord, ycoord)

coords = coordinates(PC_x, PC_y, radius)
pixelID = []

while True:
    try:
        this_coord = next(coords)
        this_coord_x = this_coord[0]
        this_coord_y = this_coord[1]
        this_pixel_ID = this_coord_y * 256 + this_coord_x

        pixelID.append(this_pixel_ID)
    except StopIteration:
        break

# initialize pixet 
pypixet.start()

# get pixet API
pixet = pypixet.pixet

# List all Timepix3 devices and use the first one:
devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)
if not devices:
    raise "No devices connected"
device = devices[0] # use the first device

devicename = device.deviceID()
print(devicename)

# load factory config to reset; otherwise the new mask will overlap with previously applied ones
device.loadFactoryConfig()
# Use the line below for older devices
# loadfactoryconfig = device.loadConfigFromFile("C:\\Users\\billy\\Documents\\GitHub\\DEDCapturingScripts\\CustomConfig\\C08-W0294.xml")

# Create a reference to the pixel configuration
dpc = device.pixCfg()

# Mask pixels one by one in the calculated list
for pixel in pixelID:
    rc = dpc.mask(pixel, 1)

# Save new configuration to a file
configname = "C:\\Users\\billy\\Documents\\GitHub\\DEDCapturingScripts\\CustomConfig\\NewMaskConfig.xml"
device.saveConfigToFile(configname)

# exit
pypixet.exit()
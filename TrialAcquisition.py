#! /usr/bin/env python
import pypixet

pypixet.start()

# get pixet API
pixet = pypixet.pixet

TPX3_INDEX = 0
TPX3_TOT = 1
TPX3_TOA = 2

# get first Timepix3 device:
devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)

if not devices:
    print("Error: no devices connected")
    exit()

dev = devices[0]

# set Timepix3 operation mode:
#dev.setOperationMode(pixet.PX_TPX3_OPM_TOATOT)
dev.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
#dev.setOperationMode(pixet.PX_TPX3_OPM_TOA)
#dev.setOperationMode(pixet.PX_TPX3_OPM_TOT_NOTOA)

# set the threshold
energy = 20.00 #keV

dev.setThreshold(pixet.PX_MPXDACS_CHIP_ALL, energy, pixet.PX_THLFLG_ENERGY)
    
# make 10 frames acquisition, 0.1 s acq time and save it to file:
#dev.doSimpleAcquisition(10, 0.1, pixet.PX_FTYPE_AUTODETECT, "/tmp/test1.pmf")

# make integral acquisition 100 frames, 0.1 s and save to file
filename = "trialcapture\\test.h5"
dev.doSimpleIntegralAcquisition(10, 0.05, pixet.PX_FTYPE_AUTODETECT, filename)

print("DED capture saved to: " + filename)

pypixet.exit()
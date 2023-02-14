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

threshold_read = dev.threshold(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)

bias_read = dev.bias()

print("DED capture saved to: " + '{0:.5g}'.format(threshold_read) + " keV")

print("Bias is set at: " + str(bias_read) + " V")

pypixet.exit()
# Sequential Threshold Capturing

import pypixet
import time

# initialize pixet 
pypixet.start()

# get pixet API
pixet = pypixet.pixet

# List all Timepix3 devices and use the first one:
devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)
if not devices:
    print("No devices connected")
else:
    dev = devices[0] # use  the first device
    dev.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
    print(f"Connected to: {dev} and set to Event+iToT mode.")

devicename = dev.deviceID()
print(devicename)

dev.loadFactoryConfig()

frametime = 0.0005
framenumber = 200

filename = "C:\\Users\\tianbi\\Documents\\TKD\\20230301_gain_frame\\30kV_00005s_200f_"

rc = dev.doSimpleAcquisition(framenumber, frametime, pixet.PX_FTYPE_AUTODETECT, filename + "th3.h5")
print(f"Acquired to: {filename}th3.h5")

th_list = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 35]

for thres in th_list:
    dev.setThreshold(pixet.PX_MPXDACS_CHIP_ALL, thres, pixet.PX_THLFLG_ENERGY)
    rc = dev.doSimpleAcquisition(framenumber, frametime, pixet.PX_FTYPE_AUTODETECT, filename + f"th{thres}.h5")
    print(f"Acquired to: {filename}th{thres}.h5")
    time.sleep(0.5)


    
print("Acquisition finished.")

pypixet.exit()
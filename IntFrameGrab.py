## IntFrameGrab.py
## This file takes the input (frame number ans exposure time) from the ZeissTrial SEM GUI as DED parameters
## and perform an integral grab. 

import pypixet
import sys

pypixet.start()

# get pixet API
pixet = pypixet.pixet

# print pixet version
# print("Pixet Version:" + pixet.pixetVersion())

# List all Medipix/Timepix devices and use the first one
# N.B. use PX_DEVTYPE_MPX2 for old Minipix DEDs, and PX_DEVTYPE_TPX3 for the newer TimePix2 DED

devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)

if not devices:
    print("No devices connected!")
    exit()

# add the exit() so that the last error message is "no device connected".

dev = devices[0] # connect

# 
# sys.argv[0] is the name of the script that is in the C# code.
th_input = float(sys.argv[1])
bias_input = int(sys.argv[2])
frames_input = int(sys.argv[3])
frame_time_input = float(sys.argv[4])
identifier_input = str(sys.argv[5])
directory_input = str(sys.argv[6])

def IntFrameGrab(threshold, bias, frames, frame_time, identifier, directory):
    # dev.setThreshold(pixet.PX_MPXDACS_CHIP_ALL, threshold, pixet.PX_THLFLG_ENERGY)
    # dev.setBias(bias)
    # filename = directory + "\\"+ str(identifier) + "_th" + str(threshold) + "_bias" + str(bias) + "_" + str(frames) + "f_" + str(frame_time) + "s.h5"
    filename = directory + "\\"+ str(identifier) + ".h5"
    # print(filename)
    # //Pattern will be saved as "identifier_th_bias_framesxframetime.h5".
    capture = dev.doSimpleIntegralAcquisition(frames, frame_time, pixet.PX_FTYPE_AUTODETECT, filename)

    if capture == 0:
        print("Successfully captured to: " + filename)


IntFrameGrab(th_input, bias_input, frames_input, frame_time_input, identifier_input, directory_input)

temp = dev.temperature(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)
rounded_temperature = '{0:.5g}'.format(temp)
print("DED temperature (C): " + rounded_temperature)

pypixet.exit()
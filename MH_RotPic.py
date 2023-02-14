# /**********************************************************************
# * Copyright (c) 2017 SmarAct GmbH
# *
# * This is a Python programming example for the Modular Control System 
# * API.
# *
# * THIS  SOFTWARE, DOCUMENTS, FILES AND INFORMATION ARE PROVIDED 'AS IS'
# * WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING,
# * BUT  NOT  LIMITED  TO,  THE  IMPLIED  WARRANTIES  OF MERCHANTABILITY,
# * FITNESS FOR A PURPOSE, OR THE WARRANTY OF NON-INFRINGEMENT.
# * THE  ENTIRE  RISK  ARISING OUT OF USE OR PERFORMANCE OF THIS SOFTWARE
# * REMAINS WITH YOU.
# * IN  NO  EVENT  SHALL  THE  SMARACT  GMBH  BE  LIABLE  FOR ANY DIRECT,
# * INDIRECT, SPECIAL, INCIDENTAL, CONSEQUENTIAL OR OTHER DAMAGES ARISING
# * OUT OF THE USE OR INABILITY TO USE THIS SOFTWARE.
# **********************************************************************/

# Import MCSControl_PythonWrapper.py 
from cmath import pi
from MCSControl_PythonWrapper import *
import time
import sys
import ctypes as ct
import math
import numpy as np

#/* All MCS commands return a status/error code which helps analyzing 
#   problems */
def ExitIfError(status):
    #init error_msg variable
    error_msg = ct.c_char_p()
    if(status != SA_OK):
        SA_GetStatusInfo(status, error_msg)
        print('MCS error: {}'.format(error_msg.value[:].decode('utf-8')))
    return

# ### implement getchar() function for single character user input
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _GetchWindows()

def main():
    rot_angle = int(sys.argv[1])
    
    #print(rot_angle)
    
    rot_angle = rot_angle * (10 ** 6)
    rot_angle_ct =  ct.c_long(rot_angle)

    error = ct.c_ulong(SA_OK)
    mcsHandle = ct.c_ulong()
    numOfChannels = ct.c_ulong(0)
    channel = ct.c_ulong(0)
    sensorType = ct.c_ulong()
    linearSensorPresent = 0
    rotSensorPresent = 0
    key = ct.c_int(0)
    status = ct.c_ulong()
    position = ct.c_int()
    #step_angle = 1000000
    lin_step = 100000
    steps = 200

    #print("We reached 1.")

    #// ----------------------------------------------------------------------------------
    #find all available MCS systems
    outBuffer = ct.create_string_buffer(17) 
    ioBufferSize = ct.c_ulong(18)
    ExitIfError( SA_FindSystems('', outBuffer, ioBufferSize) ) #will report a 'MCS error: query-buffer size' if outBuffer, ioBufferSize is to small
    print('MCS address: {}'.format(outBuffer[:18].decode("utf-8"))) #connect to first system of list

    #print("We reached 2.")

    #// open the first MCS with USB interface in synchronous communication mode
    ExitIfError( SA_OpenSystem(mcsHandle,outBuffer, bytes('sync,reset',"utf-8")) )

    #// Rotate
    # the 3rd argument is the rotation angle in micro-degrees (1E-6)
    # positive value: ccw; negative : cw
    #ExitIfError( SA_GotoAngleRelative_S(mcsHandle, 2, rot_angle, 0, 1000) )

    ExitIfError( SA_GotoAngleRelative_S(mcsHandle, 2, rot_angle_ct, 0, 0) )

    ##print("We reached 3.")
    
    ExitIfError( SA_CloseSystem(mcsHandle) )

    return
    


if __name__ == "__main__":
    main()
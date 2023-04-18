## A trial GUI for DED control - click - capture

from sre_constants import IN
from tkinter import *
from tkinter import filedialog
from tokenize import Name
#from tkinter import ttk
from datetime import datetime


import numpy as np
from cmath import pi
#from MCSControl_PythonWrapper import *
import time
import sys
import ctypes as ct
import pypixet

pypixet.start()
pixet = pypixet.pixet

def RecordTime():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%H:%M:%S")
    return timestampStr

def TextOutputWithTime(text):
    CurrentTime = RecordTime()
    tfield.insert(INSERT, f"{CurrentTime} " + text + "\n")
    tfield.see("end")

class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
 
        self.title("DED Controller 1.0.1")
        self.minsize(640,480)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)

def DEDInitializeMPX2():
    ## Initialize the SmarAct API and connect to the controller.
    # Find all available MCS systems
    devices = pixet.devicesByType(pixet.PX_DEVTYPE_MPX2)
    global dev 
    global isMPX2
    if not devices:
        TextOutputWithTime("No devices connected.")
        #tfield.insert(INSERT, "No devices connected.\n")
    else:
        dev = devices[0] # use  the first device
        #tfield.insert(INSERT, f"Connected to: {dev}.\n")
        TextOutputWithTime(f"Connected to: {dev}.")
        isMPX2 = True
    
def DEDInitializeTPX3():
    ## Initialize the SmarAct API and connect to the controller.
    # Find all available MCS systems
    devices = pixet.devicesByType(pixet.PX_DEVTYPE_TPX3)
    global dev 
    global isTPX3
    if not devices:
        #tfield.insert(INSERT, "No devices connected.\n")
        TextOutputWithTime("No devices connected.")
    else:
        dev = devices[0] # use  the first device
        dev.setOperationMode(pixet.PX_TPX3_OPM_EVENT_ITOT)
        #tfield.insert(INSERT, f"Connected to: {dev} and set to Event+iToT mode.\n")
        TextOutputWithTime(f"Connected to: {dev} and set to Event+iToT mode.")
        isTPX3 = True

def UpdateTemp():
    global rounded_temperature    
    temp = dev.temperature(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)
    rounded_temperature = '{0:.5g}'.format(temp)

def acqExample2():
    global rounded_temperature
    global fileindex
    global dev
    global isTPX3
    filepath = folder_path.get()
    if filepath == "":
        #tfield.insert(INSERT, "Please select a directory!.\n")
        TextOutputWithTime(f"Please select a directory!.")
        return
    filename = folder_path.get() + f"/Spot{fileindex}.h5"
    
    try:
        rc = dev.doSimpleAcquisition(1, 0.005, pixet.PX_FTYPE_AUTODETECT, filename)
        CurrentTime = RecordTime()
        if rc == 0:
            #tfield.insert(INSERT, f"{CurrentTime}: Acquired to {filename}.\n")
            TextOutputWithTime(f"Acquired to {filename}.")
            fileindex += 1
        else:
            #tfield.insert(INSERT, "No devices connected. \n")
            TextOutputWithTime(f"No devices connected.")
    except NameError:
        ##tfield.insert(INSERT, "No devices connected. \n")
        TextOutputWithTime(f"No devices connected.")
    if isTPX3:
        CurrentTime = RecordTime()
        temp = dev.temperature(pixet.PX_MPXDACS_CHIP_ALL, pixet.PX_THLFLG_ENERGY)
        rounded_temperature = '{0:.5g}'.format(temp)
        ##tfield.insert(INSERT, f"{CurrentTime}: T = {rounded_temperature}. \n")
        TextOutputWithTime(f"T={rounded_temperature}")
    # except NameError:
    #     tfield.insert(INSERT, "No devices connected. \n")
        

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)

def WriteLogFile():
    filepath = folder_path.get()
    if filepath == "":
        #tfield.insert(INSERT, "Please select a directory!.\n")
        TextOutputWithTime(f"Please select a directory!.")
        return
    filename = folder_path.get() + "/logfile.txt"

    with open(filename, 'w') as f:
        f.writelines(tfield.get("1.0",END))
        f.close
    
    TextOutputWithTime(f"Log file generated at: {filename}.")


def DEDExit():
    pypixet.exit()
    global isMPX2
    global isTPX3
    isMPX2 = False
    isTPX3 = False
    ## tfield.insert(INSERT, "Pixet interface closed. Reconnect or quit this program. \n")
    TextOutputWithTime(f"Pixet interface closed. Reconnect or quit this program.")

# Initialize the GUI window
root = Root() 
root.geometry("640x480+1250+500")

folder_path = StringVar()
rounded_temperature = StringVar()
fileindex = 1
isMPX2 = False
isTPX3 = False

# Button for initialization
b_initialize_mpx2 = Button(root, text="Init. MPX2 Dev.", font=("Arial", 10), command=DEDInitializeMPX2, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_initialize_mpx2.grid(column=0,row=0,sticky=W, padx=5, pady=5)
b_initialize_mpx2["state"] = "disabled"

b_initialize_tpx3 = Button(root, text="Init. TPX3 Dev.", font=("Arial", 10), command=DEDInitializeTPX3, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_initialize_tpx3.grid(column=1,row=0,sticky=W, padx=5, pady=5)

# Button for capture
b_capture = Button(root, text = "Capture",font=("Arial", 10), command=acqExample2, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10 )
b_capture.grid(column=2,row=0,sticky=W, padx=5, pady=5)
# Textbox displaying selected directory
lbldirectory = Label(master=root,textvariable=folder_path, font=("Arial", 10),wraplength=250, justify="left")
lbldirectory.grid(column=0, row=2, columnspan=2)

# Button for directory selection
b_browse = Button(root, text="Browse...", font=("Arial", 10), command=browse_button, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_browse.grid(column=2, row=2, sticky=W, padx=1, pady=5)

# Button to update temperature reading
b_readtemp = Button(root, text="Read Temp. (TPX3 only!)", font=("Arial", 10), command=UpdateTemp, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_readtemp.grid(column=3, row=2, sticky=W, padx=1, pady=5)

# Label to show temperature (TPX3 only)
lbltemp = Label(root, textvariable=f'T={rounded_temperature}')
lbltemp.grid(column=4, row=2)

# Button for close API
b_exitded=Button(root, text="Close PIXET API", font=("Arial", 10), command=DEDExit, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_exitded.grid(column=0, row=3, sticky=W, padx=5, pady=5)

# Button for close API
b_exitded=Button(root, text="Generate Log File", font=("Arial", 10), command=WriteLogFile, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b_exitded.grid(column=1, row=3, sticky=W, padx=5, pady=5)

# Button for closing the window
exit_button = Button(root, text="Exit Program", font=("Arial", 10), command=root.destroy, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
exit_button.grid(column=2, row=3, sticky=W, padx=1, pady=5)

labelExitNotice = Label(root, text='Please close DED controls first before closing the window.', font=("Arial", 10),wraplength=250, justify="left")
labelExitNotice.grid(column=3, row=3, columnspan=3, sticky=W, padx=5, pady=5)

# Console
labelConsole = Label(root, text='Output console') # Label
labelConsole.grid(column=0, row=4, sticky=W, padx=5, pady=1)
tfieldScroll = Scrollbar(root) # Scroll bar
tfield = Text(root, width=60, height=15) # text field itself
tfieldScroll.grid(column=5, row=5, sticky=N+S+W)
tfield.grid(column=0, row=5, columnspan = 5, sticky=W, padx=5, pady=5)
tfieldScroll.config(command=tfield.yview)
tfield.config(yscrollcommand=tfieldScroll.set)

# Copyright Declaration
labelCopyinfo = Label(root, text='This widget is developed by Tianbi Zhang, October 2022. All rights reserved.', width=80 )  
labelCopyinfo.grid(column=0, row=6, columnspan = 4, sticky=W, padx=5,pady=1) 

root.mainloop()
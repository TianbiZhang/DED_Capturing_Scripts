# DED_Capturing_Scripts

Tianbi Zhang

Last updated: November 20, 2023

This a series of python scripts for automated operations with the Advacam Minipix Timepix3 direct electron detector (DED). This project only includes my custom python scripts. After downloading, please paste the scripts (not the home folder) to your PIXETPro installation directory (alternatively, insert your own path in the scripts).

The Python library for the DED, pypixet, is already included in your PIXET Pro installation. It required Python 3.7.0.

Additional python packages needed:

- `asynctkinter` for the sequential capture GUI.
- `numpy`

## DED GUI Trial

This is a python GUI I wrote for capturing patterns in a sequence for scenarios such as EBSD mapping. You will need to connect to the DED (Init. TP3 Dev.) first, then set the directory where you want to store the patterns. The patterns will be named as "spot1.h5", "spot2.h5", etc. Note that to reset the counter you need to restart the GUI. After each capture, there will be a message in the textbox reporting the time stamp, pattern name, and detector temperature. You can store this into a log file.

The frame number integrated and exposure time can be changed in the ``acq_Example2`` function.

## Sequential Capture

This script was used to collect data at a series of exposure times (an example is [here](https://arxiv.org/abs/2306.14167)). Again, you need to manually adjust the exposure times and frames captured (no integration here).


## Notes

- It is strongly suggested that you install PIXET Pro outside ``C://Program Files`` (or directories where you need admin priviliges to write data).
- For custom versions of these scripts, you may need to change the device type from TPX3 to your own device model.

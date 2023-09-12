# DED Capturing Scripts

By Tianbi Zhang

This a series of python scripts for automated operations with the Advacam Timepix3 direct electron detector (DED). This project only includes my custom python scripts. After downloading, please paste the scripts (not the home folder) to your PIXETPro installation directory. PIXET Pro is available for download on [Advacam's official website](https://advacam.com/downloads/).

If you wish to use the scripts in another directory, it is advised to add the following code before `import pypixet` in the python scripts:

```
import sys
sys.path.insert(0, 'C:\\Users\\billy\\Documents\\PIXetPro') 
```

In addition. it is strongly suggested that you install PIXET Pro outside ``Program Files`` (or directories where you need admin priviliges) for easy editing of your scripts.

The Python library for the DED, pypixet, is already included in the PIXET Pro installation or the SDK. The python wrapper for SmarAct (MCS; originally in C++) is included in this project and are available on the SmarAct website as well. **Note: looks like the SmarAct modules will not run under Windows 11, so please be careful!**

Additional python packages needed:

- `asynctkinter` for the sequential capture GUI.
- `numpy`

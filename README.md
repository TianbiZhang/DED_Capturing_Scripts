# DED_Capturing_Scripts

Tianbi Zhang

This a series of python scripts for automated operations with the Advacam Timepix3 direct electron detector (DED) and SmarAct linear stages.

This project only includes my custom python scripts. After downloading, please paste the scripts (not the home folder) to your PIXETPro installation directory.

If you wish to use the scripts elsewhere, please add the following code before `import pypixet` in the python scripts:

```
import sys
sys.path.insert(0, 'C:\\Users\\billy\\Documents\\PIXetPro') 
```

In addition. it is strongly suggested that you install PIXET Pro outside ``Program Files`` (or directories where you need admin priviliges).

The Python library for the DED, pypixet, is already included in the PIXET Pro installation. The python wrapper for SmarAct (MCS; originally in C++) is included in this project and are available on the SmarAct website as well. **Note: looks like the SmarAct modules will not run under Windows 11!**

Additional python packages needed:

- `asynctkinter` for the sequential capture GUI.
- `numpy`

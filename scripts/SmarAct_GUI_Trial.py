## A trial GUI for Martin's SmarAct work

from tkinter import *
from tkinter import ttk

import numpy as np
from cmath import pi
from MCSControl_PythonWrapper import *
import time
import sys
import ctypes as ct


from PIL import Image, ImageTk
 
class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
 
        self.title("The most primitive Controller by Martin Heller and Tianbi Zhang")
        self.minsize(500,400)
 
def coinFlip():
    result = np.random.binomial(1,0.5)
    tfield.delete("1.0", "end")
 
    if(result == 1):
        tfield.insert(INSERT, " It's ————> HEADS")
         
    else:
        tfield.insert(INSERT, " It's ————> TAILS")

root = Root()

tfield = Text(root, width=52, height=5)
tfield.pack()

b1=Button(root, text="Toss the Coin", font=("Arial", 10), command=coinFlip, bg='teal', fg='white', activebackground="lightblue", padx=10, pady=10)
b1.pack()



root.mainloop()
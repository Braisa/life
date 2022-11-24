# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:58:55 2022

@author: brais
"""

import numpy as np
import PIL.Image as img

names = np.genfromtxt("names.txt", dtype = "str")

while True:
    filename = input("File? ")
    try:
        img.open(filename + ".png")
    except IOError:
        input("File not found.")
        continue
    
    if filename in names[:, 1]:
        equiv = names[np.where(names == filename)[0], 0][0]
        edit = input(f"Current equivalence for {filename} is {equiv}. Edit? ")
        if not edit == "":
            names[np.where(names == filename)[0], 0] = edit
            print(f"Equivalence for {filename} changed from {equiv} to {edit}.")
            input("Enter to save.")
        else:
            input("Equivalence unedited.")
    else:
        edit = ""
        while edit == "" or edit in names[:, 0]:
            edit = input("Equivalence? ")
        names = np.vstack((names, np.array([edit, filename])))
        print(f"Equivalence for {filename} established as {edit}.")
        input("Enter to save.")
    
    np.savetxt("names.txt", names, fmt = "%s")

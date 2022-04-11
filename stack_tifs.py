#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: roberthuntlab

Prompts for a directory of files. 
All .tif files in that directory will be stacked into a new array and written as a new stack named "stacked.tif".

"""
import tkinter
import tkinter.filedialog
from tifffile import imwrite, imread
import glob
import natsort
import numpy as np
import os

# Prompt for directory of .tif files
root = tkinter.Tk()
root.withdraw()
dirname = tkinter.filedialog.askdirectory(
    parent=root,
    initialdir="/",
    title='Select directory of .tif files')

# Retrive all .tif files in selected directory
tif_list = glob.glob(dirname + '/*.tif')

# Sort list of .tif files 
tif_list = natsort.natsorted(tif_list)
    
# Read .tif files into memory
tif_planes = []
for count, value in enumerate((tif_list)):
    plane = imread(tif_list[count])
    tif_planes.append(plane)

# Stack individual planes into a new 3D array
tif_planes_3d = np.dstack(tif_planes)
print('Shape of the original array: ', tif_planes_3d.shape)

# Transpose YXZ to ZYX
tif_planes_3d = np.transpose(tif_planes_3d, (2, 1, 0))
print('Shape of the transposed array: ', tif_planes_3d.shape)

# Create a new filename for the 3D array
final_file_name = os.path.join(dirname, "stacked.tif")

# Write new array as .tif stack
print("Saving: ", final_file_name)
imwrite(final_file_name, data=tif_planes_3d, photometric='minisblack')

# Cleanup
del count, dirname, final_file_name, plane, root, tif_list, tif_planes, tif_planes_3d, value

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: roberthuntlab

Convert a 3D numpy array generated with ClearMap to a series of TIF files. 
Since ClearMap uses formats axes in XYZ, data are transposed to ZYX first, then YX arrays are written one Z at a time.

You will be prompted for: 
    1. Path to a 3D .npy file
    2. Directory to save the .tif series
    3. Prefix to name the files
    4. A threshold value to set background values to 0
    5. Z slice position to start at
    6. Z slice position to end at

"""
#%% import dependencies
import os
import numpy as np
import gc
from tifffile import imwrite

#%% define function

def array_to_tif_subset(npy_path, save_path, image_name, threshold, start_slice, end_slice, transpose_axes=True):
    
    print('Loading: ', npy_path)
    data = np.load(npy_path)
    
    if transpose_axes == True:
        # ClearMap uses XYZ by default, for TIF stack we need ZYX
        data = data.transpose(2,1,0) 
    else:
        pass
    #select Z slices between start and end specified
    data = data[start_slice:end_slice,:,:] 
    
    for count, array_slice in enumerate(data):
        # Create filename for individual .tif slice
        file_name = str(image_name) + '_' + str(count) + '.tif' 
        
        # Create a path to save the .tif slices
        file_path = os.path.join(save_path, file_name) 
        
        # Set values below threshold to 0
        array_slice[array_slice <= threshold] = 0 
        
        # Save array as 16-bit TIF
        print('Saving: ', file_path)
        imwrite(file_path, array_slice, photometric = 'minisblack')
        
    # Free memory back up      
    gc.collect() 
    
# Function for True/False prompt

def get_bool(prompt):
    while True:
        try:
           return {"true":True,"false":False}[input(prompt).lower()]
        except KeyError:
           print ("Invalid input please enter True or False!")

#%% run script 

# Prompts
npy_array = str(input('Path to .npy file: '))
save_directory = str(input('Path to save directory: '))
image_name = str(input('Filename prefix: '))
threshold = int(input('Value to threshold intensity: '))
start_slice = int(input('Z slice start : '))
end_slice = int(input('Z slice end : '))
clearmap_tf = get_bool('Is .npy in ClearMap format (XYZ), type True or False: ')

# Execute script
array_to_tif_subset(npy_array, save_directory, image_name, threshold, start_slice, end_slice, transpose_axes= clearmap_tf)

# Delete all generated objects
del clearmap_tf, image_name, npy_array, save_directory, threshold, start_slice, end_slice

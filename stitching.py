#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Imaris file stitching script
@author: roberthuntlab

Following conversion of a raw .CZI file (Zeiss) to a series of .IMS (Bitplane Imaris) files, this script will extract individual channels and stitch them using WobblyStitcher (from ClearMap2; @ChristophKirst) and register the data to the Allen Brain Atlas using Brainreg (@brainglobe).
Since data is preprocesses into .IMS files (a type of hierarchical data format), the raw data can be downsampled up to a factor of 2^5, with the option of working with any n number of channels, or individual channels can be selected.
Initially the resolution level and number of channels is defined before being prompted for a directory of .IMS files.
From the .IMS files, each channel is extracted as a separate .npy array. Information about tile placement is retrieved from the .IMS filename and converted to a numbered array for interfacing with ClearMap. Axes are transposed from ZYX to XYZ for ClearMap.
Each channel is stitched using WobblyStitcher, allowing for non-rigid stitching of TB-sized data.

"""
#%% Import dependencies
import sys 
import os
import h5py
import glob
import numpy as np
import tkinter
import tkinter.filedialog

# Path to local ClearMap2 directory
sys.path.append('path/to/ClearMap2')
from ClearMap.Environment import settings, io, wsp, st, stw, ano, p3d

#%% Create a path to the raw data within each channel of Imaris (.h5) file

# Downsampling by a factor of 2 in each dimension = 2^3, factor of 4 in each dimension = 4^3, etc
resolution_level = input("Choose resolution level; 0 for original, 1 for downsampled by 2^3, 2 for downsampled by 4^3, etc. : ")
no_of_channels = 3

# Create a list to append a series of .h5 paths for each channel
selected_dataset = []

for channel in range(no_of_channels):
    h5_path_to_channel = 'DataSet/ResolutionLevel ' + resolution_level + '/TimePoint 0/Channel ' + str(channel) + '/Data'
    selected_dataset.append(h5_path_to_channel)
    
#%% Define pixel:micron conversions

# Orientation refers to BrainGlobe oriention of origin pixel, here it is left, anterior, inferior
orientation = 'lai'

# Axial resolution (thickness of Z plane in um)
z_resolution = str(9.87)

# Lateral resolution (XY microns per pixel)
y_resolution = str(1.8245)
x_resolution = str(1.8245)

#%% retrieve a list of .ims files from a directory and define where to save new .npy files

# Define where the .ims files are #
root = tkinter.Tk()
root.withdraw()
ims_dirname = tkinter.filedialog.askdirectory(
    parent=root,
    initialdir="/",
    title='Select directory of Imaris files')

# Create a list of .ims files from the selected directory
ims_list = glob.glob(ims_dirname + '/*.ims')

# Define where to save the .npy files 
ims_save_path = tkinter.filedialog.askdirectory(
    parent=root,
    initialdir="/",
    title='Select save directory')
    
print('\n')
print('Number of Imaris files found: ', len(ims_list))
print('The directory where files will be saved: ', ims_save_path)

#%% Specify animal ID and tile positions

split_ims = ims_list[0].split('_')
for i in range(len(split_ims)):
    index = str(i) + ': ' + str(split_ims[i])
    print(index)
animal_id_input = int(input('Type the index value containing the animal ID: '))
tile_letter_input = int(input('Type the index value containing the tile letter: '))

print("Animal is: ", ims_list[0].split('_')[animal_id_input])
print("Tile letter is: ", ims_list[0].split('_')[tile_letter_input])

#%% Create a dictionary to convert tile letters to XY tile grid

tile_dict = {
        "a": "[1 x 7]",
        "b": "[2 x 7]",
        "c": "[3 x 7]",
        "d": "[4 x 7]",
        "e": "[4 x 6]",
        "f": "[3 x 6]",
        "g": "[2 x 6]",
        "h": "[1 x 6]",
        "i": "[1 x 5]",
        "j": "[2 x 5]",
        "k": "[3 x 5]",
        "l": "[4 x 5]",
        "m": "[4 x 4]",
        "n": "[3 x 4]",
        "o": "[2 x 4]",
        "p": "[1 x 4]",
        "q": "[1 x 3]",
        "r": "[2 x 3]",
        "s": "[3 x 3]",
        "t": "[4 x 3]",
        "u": "[4 x 2]",
        "v": "[3 x 2]",
        "w": "[2 x 2]",
        "x": "[1 x 2]",
        "y": "[1 x 1]",
        "z": "[2 x 1]",
        "aa": "[3 x 1]",
        "ab": "[4 x 1]",
       }

tile_dict_2 = {
        "a": "[1 x 9]",
        "b": "[2 x 9]",
        "c": "[3 x 9]",
        "d": "[4 x 9]",
        "e": "[4 x 8]",
        "f": "[3 x 8]",
        "g": "[2 x 8]",
        "h": "[1 x 8]",
        "i": "[1 x 7]",
        "j": "[2 x 7]",
        "k": "[3 x 7]",
        "l": "[4 x 7]",
        "m": "[4 x 6]",
        "n": "[3 x 6]",
        "o": "[2 x 6]",
        "p": "[1 x 6]",
        "q": "[1 x 5]",
        "r": "[2 x 5]",
        "s": "[3 x 5]",
        "t": "[4 x 5]",
        "u": "[4 x 4]",
        "v": "[3 x 4]",
        "w": "[2 x 4]",
        "x": "[1 x 4]",
        "y": "[1 x 3]",
        "z": "[2 x 3]",
        "aa": "[3 x 3]",
        "ab": "[4 x 3]",
        "ac": "[4 x 2]",
        "ad": "[3 x 2]",
        "ae": "[2 x 2]",
        "af": "[1 x 2]",
        "ag": "[1 x 1]",
        "ah": "[2 x 1]",
        "ai": "[3 x 1]",
        "aj": "[4 x 1]",
    }


#%%
# Use the length of the .ims file list to determine which tile mapping to use
if len(ims_list) == 28:
    print("28 tile (4x7) mapping used.")
elif len(ims_list) == 32:
    tile_dict = tile_dict_2
    print("36 tile (4x9) mapping used.")
elif len(ims_list) == 36:
    tile_dict = tile_dict_2
    print("36 tile (4x9) mapping used.")
else:
    print("Length of .ims file list does not match a known mapping.")

#%%
def imaris_extract(h5_path):
    # Split h5 path
    split_h5_path = h5_path.split('/') 
    
    # Select channel #
    channel_no = split_h5_path[3] 
    channel_suffix = ""
    if channel_no == 'Channel 0':
        channel_suffix = '_546'
    elif channel_no == 'Channel 1':
        channel_suffix = '_488'
    elif channel_no == 'Channel 2':
        channel_suffix = '_647'
        
    # Read ims file into memory
    f = h5py.File(ims_filename, 'r') 
    
    # Select individual channel
    dset = f[h5_path] 
    
    # Convert channel into numpy array
    np_array = np.asarray(dset) 
    
    # Subset the the array for testing
    #np_array = np_array[1100:,:,:] 
    
    # Transpose from ZYX to XYZ
    np_transposed = np.transpose(np_array, (2, 1, 0)) 
    print("The shape of the transposed array is: ", (np_transposed.shape))
    
    # Create filename from animal ID and tile letter
    ims_filename_split = ims_filename.split('_') 
    animal_id = ims_filename_split[animal_id_input]
    tile_key = ims_filename_split[tile_letter_input]
    
    # Replace letter with [X x Y] tile position
    tile_value = tile_dict.get(tile_key)
    print("The tile letter: ", tile_key, ' has been replaced by: ', tile_value)
    
    # Concatenate file name
    npy_filename = animal_id + '_' + tile_value + channel_suffix
    
    # Save npy array
    final_path = os.path.join(ims_save_path, npy_filename)
    print('Saving file: ' + final_path)
    print('\n')
    np.save(final_path, np_transposed)
    
    # Free up memory
    del np_array, np_transposed
    return 

#%% iterate through each channel and create a single channel array for each tile

#First part of the loop allows for a single .ims file or a list of .ims files to be passed through the extraction function
for ims in range(len(ims_list)):
    # Ims_list will be length 1 if single file
    if len(ims_list) == 1:
        ims_filename = (ims_list[0])
        print('Selected: %s' % (ims_filename))
    else:
        # ims_list will be >1 if list of files
        ims_filename = ims_list[ims] 
        print('Selected: %s' % (ims_filename))
    
    # Second part of the loop allows for a single channel or list of channels to be interated over the extraction function
    for i in range(len(selected_dataset)):
        # Selected_dataset will be a string if one channel is selected
        if type(selected_dataset) is str:
            h5_path = selected_dataset
            imaris_extract(h5_path)
            break
        else:
            # Selected_dataset will be a list if more than one channel is selected
            h5_path = selected_dataset[i]
            imaris_extract(h5_path)
            continue
#%% only run this to initialize sample data for testing!
ims_list = list(range(28))
split_ims = 'test'
animal_id_input = 1
#%%
# Define directories and files for ClearMap initialization
directory = 'path/to/npy_arrays'   

expression_rabies     = split_ims[animal_id_input] + '_[<X,1> x <Y,1>]_546.npy'
expression_auto     = split_ims[animal_id_input] + '_[<X,1> x <Y,1>]_488.npy'
expression_gfp     = split_ims[animal_id_input] + '_[<X,1> x <Y,1>]_647.npy'



resources_directory = settings.resources_path
ws_name = split_ims[animal_id_input]
ws = wsp.Workspace(ws_name, directory=directory);
ws.update(rabies=expression_rabies, gfp=expression_gfp, autofluorescence=expression_auto)
ws.info()

#%% Initialize alignment 

# Initialize atlas and alignment files
annotation_file, reference_file, distance_file=ano.prepare_annotation_files(
    slicing=(slice(None),slice(None),slice(0,246)), orientation=(1,-2,3),
    overwrite=False, verbose=True);

# Create alignment files   
align_channels_affine_file   = io.join(resources_directory, 'Alignment/align_affine.txt')
align_reference_affine_file  = io.join(resources_directory, 'Alignment/align_affine.txt')
align_reference_bspline_file = io.join(resources_directory, 'Alignment/align_bspline.txt')

#%% Rigid z-alignment 

layout = stw.WobblyLayout(expression=ws.filename('rabies'), tile_axes=['X','Y'], overlaps=(93, 93));  

st.align_layout_rigid_mip(layout, depth=[93, 93, None], max_shifts=[(-60,60),(-60,60),(-5,5)],
                          ranges = [None,None,None], background=(300, 100), clip=25000, 
                          processes=None, verbose=True)

st.place_layout(layout, method='optimization', min_quality=-np.inf, lower_to_origin=True, verbose=True)

st.save_layout(ws.filename('layout', postfix='aligned_axis'), layout)

# Wobbly alignment
                       
stw.align_layout(layout, axis_range=(None, None, 3), max_shifts=[(-100,100),(-100,100),(0,0)], axis_mip=None,
                 validate=dict(method='foreground', valid_range=(200, None), size=None),
                 prepare =dict(method='normalization', clip=None, normalize=True),
                 validate_slice=dict(method='foreground', valid_range=(350,65600), size=200),
                 prepare_slice =None,
                 find_shifts=dict(method='tracing', cutoff=3*np.sqrt(2)),
                 processes=None, verbose=True)

# Wobbly placement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               #%% Wobbly placement

stw.place_layout(layout, min_quality = -np.inf, 
                 method = 'optimization', 
                 smooth = dict(method = 'window', window = 'bartlett', window_length = 100, binary = None), 
                 smooth_optimized = dict(method = 'window', window = 'bartlett', window_length = 20, binary = 10),                             
                 fix_isolated = False, lower_to_origin = True,
                 processes = None, verbose = True)

st.save_layout(ws.filename('layout', postfix='placed'), layout)

# Wobbly stitching - 546 rabies 

layout = st.load_layout(ws.filename('layout', postfix='placed'));

stw.stitch_layout(layout, sink = ws.filename('stitched'), method = 'interpolation', processes='!serial', verbose=True)

#%% Wobbly stitching - 488 channel

layout = st.load_layout(ws.filename('layout', postfix='placed'));


layout.replace_source_location(expression_rabies, expression_auto, method='expression')

stw.stitch_layout(layout, sink = ws.filename('stitched', postfix='auto'),
                  method = 'interpolation', processes='!serial', verbose=True)

#%% Wobbly stitching - 647 channel
layout = st.load_layout(ws.filename('layout', postfix='placed'));

layout.replace_source_location(expression_rabies, expression_gfp, method='expression')

stw.stitch_layout(layout, sink = ws.filename('stitched', postfix='gfp'),
                  method = 'interpolation', processes='!serial', verbose=True)
#%% visualize stitched .npy arrays

#type %gui qt into console
#type p3d.plot('path/to/array.npy')
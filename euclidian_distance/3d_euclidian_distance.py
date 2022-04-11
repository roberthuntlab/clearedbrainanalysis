#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 15:58:33 2021

@author: roberthuntlab
Calculate Euclidian distance from a starter cell centroid to each presynaptic point and plot the distributions.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bg_atlasapi import BrainGlobeAtlas
import seaborn as sns
import os

#%% define local directory
local_directory = '/path/to/folder/containing/euclidian_distance'
local_directory = '/media/huntlab/HuntData1/code_upload/scripts/euclidian_distance'

#%% load atlas and create dataframes to reference
atlas = BrainGlobeAtlas("allen_mouse_10um", check_latest=False)
atlas_df = atlas.lookup_df

reference_image = atlas.reference

list_of_animals = ['sst163']    #if more than one animal, list all animal data folders here

animal_group_dict = {'sst163': 'control'}       #if more than one animal, list all animal numbers here with respecitve group names (eg. ctrl vs tbi)

#%%
for i in range(len(list_of_animals)):
    selected_animal = i
    id_str = list_of_animals[selected_animal]
    
    presynaptic_csv_path = os.path.join(local_directory, str(list_of_animals[selected_animal]), 'final_rabies/all_points.csv')
    starter_csv_path = os.path.join(local_directory, str(list_of_animals[selected_animal]), 'final_starter/all_points.csv')
    folder_path = os.path.join(local_directory, str(list_of_animals[selected_animal]))
    
    # calculate centriod
    df = pd.read_csv(starter_csv_path)
    
    voxel_size = 10
    
    zero_axis_0 = int(df['coordinate_atlas_axis_0'].sum() / len(df['coordinate_atlas_axis_0']))
    zero_axis_1 = int(df['coordinate_atlas_axis_1'].sum() / len(df['coordinate_atlas_axis_1']))
    zero_axis_2 = int(df['coordinate_atlas_axis_2'].sum() / len(df['coordinate_atlas_axis_2']))
    
    print("Centroid coordinates are: 0:{0}, 1:{1}, 2:{2}".format(zero_axis_0, zero_axis_1, zero_axis_2))
    
    # calculate Euclidian distance
    df = pd.read_csv(presynaptic_csv_path)
    
    # create new column with relative micron distance from zero reference point
    df['normalized_axis_0'] = df['coordinate_atlas_axis_0'] - zero_axis_0
    df['normalized_axis_1'] = df['coordinate_atlas_axis_1'] - zero_axis_1
    df['normalized_axis_2'] = df['coordinate_atlas_axis_2'] - zero_axis_2
    
    # create new columns containing the square of each normalized axis
    df['normalized_axis_0_squared'] = df['normalized_axis_0'] ** 2
    df['normalized_axis_1_squared'] = df['normalized_axis_1'] ** 2
    df['normalized_axis_2_squared'] = df['normalized_axis_2'] ** 2
    
    # create new column containing the sum of squares of the three axes an
    df['3d_vector_abs_length'] = np.sqrt(df['normalized_axis_0_squared'] + 
                                           df['normalized_axis_1_squared'] + 
                                           df['normalized_axis_2_squared']
                                            )
    
    # create new column to convert absolute distance from reference point to distance from either side of reference
    df['vector_sign'] = [-1 if x > 0 else 1 for x in df['normalized_axis_1']]
    df['3d_vector_length'] = (df['3d_vector_abs_length'] * voxel_size)
    print('Mean Euclidian distance for ', list_of_animals[i], ' : ', df['3d_vector_length'].mean())
    
    #make even number of bins
    bins = int()
    
    if int(df['3d_vector_length'].max() / 100) % 2 == 0:
        bins = int(df['3d_vector_length'].max() / 100)
    else:
        bins = int(df['3d_vector_length'].max() / 100) - 1
    # create and save KDE plot
    sns.kdeplot(data=df,
               x='3d_vector_length',
               common_norm=False,
               shade=False,
               bw_adjust=0.5)
    kde_save_path = str(local_directory +
                                '/euclidian_distance_kde_' +
                                id_str +
                                '.pdf')
    plt.savefig(kde_save_path, format='pdf')
    plt.clf()
    
    
    #export distance values as csv
    df['animal_id'] = list_of_animals[i]
    df['group'] = animal_group_dict[list_of_animals[i]]
    df_truncated = df[['3d_vector_length', 'animal_id', 'group']].copy()
    df_truncated.to_csv(os.path.join(local_directory, 'euclidian_distance_df.csv'))
    
#%% histogram

df = df_truncated
sns.histplot(data= df, 
             x='3d_vector_length',
             stat="probability", 
             binwidth= 100,
             binrange = ([0,6000]),
             common_norm=False,
             )
plt.xlim([0,6000])
plt.ylim([0,0.25])
plt.savefig('path/to/save/folder/histogram.pdf')
plt.show()
plt.clf()


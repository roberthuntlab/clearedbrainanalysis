#!/usr/bin/env python
# coding: utf-8

"""
Created on Fri May 21 09:26:15 2021

@author: roberthuntlab

Import summary.csv files from cellfinder output, then plot the distribution of cells along the anterior/posterior, dorsal/ventral, or medial/lateral axis.
"""
#import dependencies

import pandas as pd
from bg_atlasapi import BrainGlobeAtlas
import seaborn as sns
import matplotlib.pyplot as plt
import os

#%% define local directory

local_directory = 'path/to/folder/containing/cell_distribution_kde'

#%% load atlas used to register cell positions and create dataframes to reference

atlas = BrainGlobeAtlas("allen_mouse_25um", check_latest=False)
atlas_df = atlas.lookup_df

reference_image = atlas.reference

#%%  create a list of file paths

control_path = os.path.join(local_directory, 'sst163/final_rabies/all_points.csv')

#%% read in csv as data frame 

control_df = pd.read_csv(control_path)

#%% create kde plot

df = control_df

#change x according to which axis you want to visualize (0 for anterior/posterior, 1 for dorsal/ventral, or 2 for medial/lateral)

sns.kdeplot(data=df,
           x='coordinate_atlas_axis_0',
           common_norm=False,
           shade=True,
           bw_adjust=0.5)

#x axis max is determined from the atlas shape
plt.xlim([0,reference_image.shape[0]])
save_path = os.path.join(local_directory, 'cell_distribution_kde_plot.pdf')
plt.savefig(save_path)
plt.show()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 13:49:55 2021

@author: roberthuntlab

Render coronal atlas plates with overlaid presynaptic cell positions.
"""

#%% import dependencies
from brainrender import Scene, settings
from brainrender.actors import Points
from vedo import embedWindow, Plotter, show
from paper.figures import INSET, root_box
import numpy as np
import os

local_directory = 'path/to/folder/containing/coronal_atlas_plate_plot'
screenshot_path = os.path.join(local_directory, 'screenshots')

#%% create list of regions to avoid over-plotting cortical cell layers
regions = [
    #isocortex
    'FRP',
    'MOp',
    'MOs',
    'SSp',
    'SSs',
    'GU',
    'VISC',
    'AUDd',
    'AUDp',
    'AUDv',
    'VISal',
    'VISam',
    'VISl',
    'VISp',
    'VISpl',
    'VISpm',
    'VISli',
    'VISpor',
    'ACAd',
    'ACAv',
    'PL',
    'ILA',
    'ORBl',
    'ORBm',
    'ORBvl',
    'AId',
    'AIp',
    'AIv',
    'RSPagl',
    'RSPd',
    'RSPv',
    'PTLp',
    'VISa',
    'VISrl',
    'TEa',
    'PERI',
    'ECT',
    'VISC',
    #hpf
    'CA1',
    'CA2',
    'CA3',
    'DG-mo',
    'DG-po',
    'DG-sg',
    'ENTl',
    'FC',
    'IG',
    'ENTm',
    'PAR',
    'POST',
    'PRE',
    'SUB',
    'ProS',
    'HATA',
    'APr',
    #striatum
    'STRd',
    'CP',
    'STRv',
    'ACB',
    'FS',
    'OT',
    'LSX',
    'LS', 
    'SF',
    'SH',
    'sAMY',
    'AAA',
    'BA',
    'CEA', 
    'IA',
    'MEA',
    #pallidum
    'PALd',
    'GPe',
    'GPi',
    'PALv',
    'SI',
    'MA',
    'PALm',
    'MSC',
    'MS',
    'NDB',
    'TRS',
    'PALc',
    'BST',
    'BAC'
    #cb
    'CBX',
    'VERM',
    'LING',
    'CENT',
    'CENT2',
    'CENT3',
    'CUL',    
    'DEC', 
    'FOTU', 
    'PYR', 
    'UVU', 
    'NOD', 
    'HEM', 
    'SIM', 
    'AN', 
    'PRM', 
    'COPY', 
    'PFL', 
    'FL', 
    'CBN', 
    'FN', 
    'IP', 
    'DN', 
    'VeCB',
    #mb
    'MBsen', 'SCs', 'SCop', 'SCsg', 'SCzo', 'IC', 'ICc', 'ICd', 'ICe', 'NB', 'SAG', 'PBG', 'MEV', 'SCO', 'MBmot', 'SNr', 'VTA', 'PN', 'RR', 'MRN', 'SCm', 'SCdg', 'SCdw', 'SCiw', 'SCig', 'PAG', 'PRC', 'INC', 'ND', 'Su3', 'PRT', 'APN', 'MPT', 'NOT', 'NPC', 'OP', 'PPT', 'RPF', 'CUN', 'RN', 'III', 'MA3', 'EW', 'IV', 'Pa4', 'VTN', 'AT', 'LT', 'DT', 'MT', 'MBsta', 'SNc', 'PPN', 'RAmb', 'IF', 'IPN', 'IPR', 'IPC', 'IPA', 'IPL', 'IPI', 'IPDM', 'IPDL', 'IPRL', 'RL', 'CLI', 'DR',
    #thal
    'DORsm', 'VENT', 'VAL', 'VM', 'VP', 'VPL', 'VPLpc', 'VPM', 'VPMpc', 'PoT', 'SPF', 'SPFm', 'SPFp', 'SPA', 'PP', 'GENd', 'MG', 'MGd', 'MGv', 'MGm', 'LGd', 'LGd-sh', 'LGd-co', 'LGd-ip', 'DORpm', 'LAT', 'LP', 'PO', 'POL', 'SGN', 'Eth', 'ATN', 'AV', 'AM', 'AMd', 'AMv', 'AD', 'IAM', 'IAD', 'LD', 'MED', 'IMD', 'MD', 'SMT', 'PR', 'MTN', 'PVT', 'PT', 'RE', 'Xi', 'ILM', 'RH', 'CM', 'PCN', 'CL', 'PF', 'PIL', 'RT', 'GENv', 'IGL', 'IntG', 'LGv', 'SubG', 'EPI', 'MH', 'LH',
    #hy
    'PVZ', 'SO', 'ASO', 'PVH', 'PVa', 'PVi', 'ARH', 'PVR', 'ADP', 'AVP', 'AVPV', 'DMH', 'MEPO', 'MPO', 'OV', 'PD', 'PS', 'PVp', 'PVpo', 'SBPV', 'SCH', 'SFO', 'VMPO', 'VLPO', 'MEZ', 'AHN', 'MBO', 'LM', 'MM', 'MMme', 'MMl', 'MMm', 'MMp', 'MMd', 'SUM', 'TM', 'TMd', 'TMv', 'MPN', 'PMd', 'PMv', 'PVHd', 'VMH', 'PH', 'LZ', 'LHA', 'LPO', 'PST', 'PSTN', 'PeF', 'RCH', 'STN', 'TU', 'ZI', 'FF', 'ME',
    #p
    'P-sen', 'NLL', 'PSV', 'PB', 'KF', 'SOC', 'POR', 'SOCm', 'SOCl', 'P-mot', 'B', 'DTN', 'PDTg', 'PCG', 'PG', 'PRNc', 'SG', 'SUT', 'TRN', 'V', 'P5', 'Acs5', 'PC5', 'I5', 'P-sat', 'CS', 'LC', 'LDT', 'NI', 'PRNr', 'RPO', 'SLC', 'SLD',
    #my
    'MY-sen', 'AP', 'CN', 'DCO', 'VCO', 'DCN', 'CU', 'GR', 'ECU', 'NTB', 'NTS', 'SPVC', 'SPVI', 'SPVO', 'Pa5', 'MY-mot', 'VI', 'VII', 'ACVII', 'AMB', 'AMBd', 'AMBv', 'DMX', 'GRN', 'ICB', 'IO', 'IRN', 'ISN', 'LIN', 'LRN', 'LRNm', 'LRNp', 'MARN', 'MDRN', 'MDRNd', 'MDRNv', 'PARN', 'PAS', 'PGRN', 'PGRNd', 'PGRNl', 'PHY', 'NR', 'PRP', 'PPY', 'VNC', 'LAV', 'MV', 'SPIV', 'SUV', 'x', 'XII', 'y', 'MY-sat', 'RM', 'RPA', 'RO',
    #subplate
    'CLA', 'EP', 'EPd', 'EPv', 'LA', 'BLA', 'BLAa', 'BLAp', 'BLAv', 'BMA', 'BMAa', 'BMAp', 'PA',
    #olf
    'MOB', 'AOB', 'AOBgl', 'AOBgr', 'AOBmi', 'AON', 'TT', 'TTd', 'TTv', 'DP', 'PIR', 'NLOT', 'NLOT1', 'NLOT2', 'NLOT3', 'COA', 'COAa', 'COAp', 'COApl', 'COApm', 'PAA', 'TR',
    #vs
    # 'VL', 'SEZ', 'chpl', 'V3', 'AQ', 'V4', 'V4r', 'c',
    #fiber tracts
    'lfbs'
    ]


#%% brainrender settings
embedWindow(None)
scene = Scene(inset=INSET, screenshots_folder=screenshot_path)
root_box(scene)
scene.root.alpha(0.1)
scene.root._silhouette_kwargs['lw'] = 15    #lw = line weight; increases thickness
settings.SHOW_AXES = False
settings.LW = 15
settings.BACKGROUND_COLOR = [247, 241, 236]

#%% for regions specified above, add region to scene 
subs = regions
for sub in subs:
    try:
        reg = scene.add_brain_region(sub, silhouette=False, alpha=0.01)
        scene.add_silhouette(reg, lw=15, color="black")
    except FileNotFoundError:
        pass
    
#%% specify slice position and thickness
pos_start = 4400    #anterior/posterior atlas position (eg 4.4mm is 4400)
pos_end = pos_start + 1
pos_1 = pos_start - 125      #thickness of plate
pos_2 = pos_start + 125
#slice positions
plane = scene.atlas.get_plane(pos=[pos_start, 3650, 5700], norm=(1,0,0))
plane_2 = scene.atlas.get_plane(pos=[pos_end, 3650, 5700], norm=(-1,0,0))
#slice before adding cells
scene.slice(plane)
scene.slice(plane_2)

#%% load input cell positions
# plotted point size
radius_size = 55 

coordinates_path = os.path.join(local_directory, 'final_rabies/points.npy')
coordinates = np.load(coordinates_path)
list_of_presynaptic_points = [coordinates]


#%% subset presynaptic points within start coordinate and +- start and end positions

#ctrl
new_list_of_presynaptic_points_ctrl = []

for array in list_of_presynaptic_points:
    subset_array = []
    for element in array:
        if element[0] < pos_2 and element[0] > pos_1:
            subset_array.append(element)
        else:
            continue
    np_subset_array = np.array(subset_array)
    new_list_of_presynaptic_points_ctrl.append(np_subset_array)

for count, value in enumerate(new_list_of_presynaptic_points_ctrl):
    cell_count = str(len(value))
    print('Number of cells to be plotted for animal number: ', count, cell_count)   


#%% add points to scene
res = 8

ctrl_points = scene.add(Points
          (new_list_of_presynaptic_points_ctrl[0],
                 name="ctrl-1",
                 colors='#4797D2',
                 radius=radius_size,
                 res=res
                 )
          )

#%% scale bar generator
#generates a 1000um scale bar

list_of_points = []

for i in range(1000):
    new_point = np.empty([3,])
    new_point[0] = pos_start
    new_point[1] = 0
    new_point[2] = i
    list_of_points.append(new_point)

scale_bar = np.array(list_of_points)

scene.add(Points
          (scale_bar,
                 name="scale_bar",
                 colors='magenta',
                 radius=25
                 )
          )
#%% specify camera settings
#injection on left
cam =    {
     'pos': (-7330, 827, -5734),
     'viewup': (0, -1, 0),
     'clippingRange': (25, 25035),
     'focalPoint': (pos_1, 3750, -5697),
     'distance': 15658,
     }
#injection on right
cam =    {
      'pos': (23745, 3827, -5734),
      'viewup': (0, -1, 0),
      'clippingRange': (25, 25035),
      'focalPoint': (pos_1, 3750, -5697),
      'distance': 15658,
      }

#%% render scene
scene.render(camera=cam, axes=True)
name = str(pos_start) + '_pfc'          
scene.screenshot(name=name, scale=8)    #scale changes resolution; >1 means better res, must be whole numbers
scene.close()
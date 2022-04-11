#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 15:27:43 2021

@author: roberthuntlab

Plot registered cell positions (.npy) in brainrender and take a screenshot.
"""
#import dependencies

from brainrender import Scene
from brainrender.actors import Points
import numpy as np
import os

#import settings to change axes, color, style, and transparency
from brainrender import settings    
settings.SHOW_AXES = False
settings.ROOT_COLOR = [220, 219, 217]
settings.SHADER_STYLE = 'cartoon'
settings.ROOT_ALPHA = 0.4

#%%
#set directory and load cell locations

local_directory = '/path/to/folder/containing/wholebrain_screnshot'
screenshot_path = os.path.join(local_directory, 'screenshot')
coordinates = np.load(os.path.join(local_directory, 'points.npy'))  #where cell position data file is located - points.npy from brainreg output

# ------------------------------- Create scene ------------------------------- #

scene = Scene(screenshots_folder=screenshot_path)
scene.root._needs_silhouette = False

text_size = 200
alpha_value = .2

#For starter cells: only added DG and CA3 regions; for rabies, all regions below were included


dg = scene.add_brain_region('DG',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      )



ca1 = scene.add_brain_region('CA1',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      )


ca3 = scene.add_brain_region('CA3',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      )



entl = scene.add_brain_region('ENTl',
                       alpha=alpha_value,
                       silhouette=False,
                       #hemisphere='left'
                       hemisphere = 'both'
                      )


entm = scene.add_brain_region('ENTm',
                       alpha=alpha_value,
                       silhouette=False,
                       #hemisphere='left'
                       hemisphere = 'both'
                      )



ms = scene.add_brain_region('MS',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      )


ndb = scene.add_brain_region('NDB',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      )



cs = scene.add_brain_region('CS',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      )


ma = scene.add_brain_region('MA',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      ) 



avpv = scene.add_brain_region('AVPV',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      ) 

avp = scene.add_brain_region('AVP',
                       alpha=alpha_value,
                       silhouette=False,
                       hemisphere='both'
                      )

#%% add points

radius_size = 55

scene.add(Points
          (coordinates,
                  name="ctrl-1",
                  colors='black',
                  radius=radius_size
                  )
          )

#%% cameras with additional parameters

top =  {
     'pos': (7760, -31645, -5943),
     'viewup': (-1, 0, 0),
     'clippingRange': (27247, 46008),
     'focalPoint': (6588, 3849, -5638),
     'distance': 35515
   }     

sag =     {
     'pos': (5431, 96, 13876),
     'viewup': (0, -1, 0),
     'clippingRange': (7301, 35820),
     'focalPoint': (6588, 3849, -5638),
     'distance': 19905
   }

ec_cam =    {
     'pos': (4860, -464, 6544),
     'viewup': (0, -1, 0),
     'clippingRange': (33, 33246),
     'focalPoint': (8398, 4447, -2922),
     'distance': 11236
   }

msc_cam =    {
     'pos': (-1489, 5101, -804),
     'viewup': (0, -1, 0),
     'clippingRange': (31, 31162),
     'focalPoint': (6770, 5883, -6649),
     'distance': 10148
   }

raphae_cam =     {
     'pos': (6304, 3468, -2751),
     'viewup': (0, -1, 0),
     'clippingRange': (20, 19943),
     'focalPoint': (7725, 4105, -4059),
     'distance': 2034,
   }

hpc_cam =    {
     'pos': (3121, -1059, 1362),
     'viewup': (0, -1, 0),
     'clippingRange': (32, 31582),
     'focalPoint': (8352, 3738, -5891),
     'distance': 10148
   }

 
front =    {
     'pos': (-19199, -1428, -5763),
     'viewup': (0, -1, 0),
     'clippingRange': (11670, 44828),
     'focalPoint': (6588, 3849, -5688),
     'distance': 26321
   }

#%% render scene
screenshot_cam =     {
     'pos': (7219, -11628, 7020),
     'viewup': (0, -1, -1),
     'clippingRange': (7589, 35722),
     'focalPoint': (7182, 4137, -5363),
     'distance': 20047
   }

scene.render(camera=screenshot_cam)
scene.screenshot(name='wholebrain_render', scale=5)     #changing scale >1 increases resolution; must be whole numbers
scene.close()

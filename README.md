# clearedbrainanalysis
Scripts to process light-sheet data acquired with a Zeiss Z1 Light Sheet microscope. 
Stitching, registration, and visualization of data analyzed using tools from ClearMap2 (@ChristophKirst) and @brainglobe suites.

SYSTEM REQUIREMENTS

Hardware Requirements
All scripts can be run on the example data using standard desktop hardware.

Software Requirements
Linux: Ubuntu 18.04.5 LTS
We have not tested the functionality on Windows or MacOS.

INSTALLATION GUIDE

All scripts were run in an Anaconda enviornment using Python 3.8.8.
Installation time is between 1-2 hours.

Detailed instructions for creating a new Anaconda enviornment for testing this software can be found here:
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

Dependencies and versions used: 
Python 3.8.8
brainrender 2.0.2.5
bg-atlasapi 1.0.0
h5py 2.10.0
matplotlib 3.3.4
numpy 1.19.5
pandas 1.2.3
scipy 1.6.1
seaborn 0.11.1
spyder 4.1.4
tifffile 2020.8.13
tk 8.6.10
vedo 2020.4.2

All dependencies can be installed from PyPi using:
pip install package_name

For stitching, users will need to install ClearMap2. Detailed instructions are provided here:
https://christophkirst.github.io/ClearMap2Documentation/html/installation.html

DEMO

Scripts #1, 5, 6, 7, and 8 are best run within a Python IDE (we use Spyder) but can also be run from a command line interface using:
python name_of_script

Where name_of_script corresponds to the filepath of any one of the scripts listed below.

Scripts #2, 3, and 4 should be run from the command line.


1. stitching.py: 
Stitch raw image data non-rigidly to a .npy array and export as .tif file series. Run in ClearMap environment.
Expected run time: 5 minutes.
	1. Run the code blocks up to line 29 to initialize dependencies.
	2. Lines 28-87 are only needed to extract .npy arrays from .ims files. These arrays are already provided as sample data, thus can be ignored for testing the sample.
	3. Run lines 88-159.
	4. Lines 160-250 are only needed to extract .npy arrays from .ims files. These arrays are already provided as sample data, thus can be ignored for testing the sample.
	5. Run lines 251-254. These lines are only run to test sample data.
	6. Update the 'directory' variable to the filepath containing 'arrays'.
	7. Run lines 255-329. All lines that follow are only needed for processing full-multichannel datasets.
	8. Output will be a stitched 3D numpy array (stitched.npy)
	9. Stitched .npy files can be inspected using the p3d.plot function within ClearMap (Lines 347-350).
		a. Run the code block to initialize the ClearMap dependencies
		b. Type %gui qt into the console.
		c. Type p3d.plot(path/to/array.npy) and press enter, with path/to/array.npy being the filepath to the .npy array.
		d. Detailed instructions for using p3d.plot can be found here:
		https://christophkirst.github.io/ClearMap2Documentation/html/TubeMap.html#Visualization

2. npystack_to_tif_series.py: 
Convert 3D .npy array to series of .tif images.
Expected run time: 1 minute.

	Instructions:
	1. Run the script from the command line.
	example: python /home/huntlab/Desktop/code_test/code_upload/scripts/npystack_to_tif_series.py
	2. Provide the .npy file path (sample data provided in the 'arrays' folder)
	3. Provide a path to a folder to save exported .tif files
	4. Type a prefix to save the image series.
	5. Type an intensity value to threshold values at (values at threshold will be replaced with 0).
	6. When prompted, type 'true' since .npy arrays are in XYZ format instead of typical ZYX .tif standard.
	7. Outputs a series of 16-bit .tif files, open in ImageJ and adjust brightness for inspection.

3. npystack_to_tif_series_subset.py: 
Convert and subset 3D .npy array to series of .tif images.
Expected run time: 1 minute.

	Instructions:
	1. Run the script from the command line.
	example: python /home/huntlab/Desktop/code_test/code_upload/scripts/npystack_to_tif_series_subset.py
	2. Provide the .npy file path (sample data provided in the 'arrays' folder)
	3. Provide a path to a folder to save exported .tif files
	4. Type a prefix to same the image series.
	5. Type an intensity value to threshold values at (values at threshold will be replaced with 0).
	6. Type the Z position to start at.
	7. Type the Z position to end at.
	8. When prompted, type 'true' since .npy arrays are in XYZ format instead of typical ZYX .tif standard.
	9. Outputs a series of 16-bit .tif files, open in ImageJ and adjust brightness for inspection.

4. stack_tifs.py: 
Convert series of .tif planes to a single 3D .tif stack.
Expected run time: 1 minute.

	Instructions:
	1. Run the script from the command line. Prompts for a directory of 2D .tif files, stacks them and writes a new 3D .tif stack.
	2. Output will be a single 3D .tif file


Note: Cells were manually counted in cellfinder and registered in atlas space using brainreg before moving on to the following steps


5. wholebrain_screenshot.py:
Render registered cell positions from cellfinder output in a brainrender scene.
Expected run time: 1 minute.

	1. Update the 'local_directory' variable to the folder containing the 'wholebrain_screenshot' folder on your local machine.
	2. Run the script.
	3. Press the 'q' key to exit the brainrender scene.
	4. Output will be a .png screenshot.


6. 3d_euclidian_distance.py: 
Calculate 3D Euclidian distance in standard atlas space. Registered starter cell and presynaptic cell positions are contained in .csv files within the 'control' folder.
Expected run time: 1 minute.

	Instructions:
	1. Update the 'local_directory' variable to the folder containing the 'euclidian_distance' folder on your local machine.
	2. Run the script.
	3. Outputs include:
	a. Euclidian distance vectors as a csv (euclidian_distance_df.csv).
	b. Kernel density plots of the vector lengths (euclidian_distance_kde_sst163.pdf).

7. cell_distribution_kde_plot.py: 
Plot registered cell positions using seaborn kernel density estimate plot function.
Expected run time: 1 minute.

	Instructions:
	1. Update the 'local_directory' variable to the folder containing the 'cell_distribution_kde' folder on your local machine.
	2. Run the script.
	3. Outputs include:
	a. Kernel density plot of the distribution of presynaptic cells (cell_distribution_kde_plot.pdf).

8. coronal_atlas_plate_plot.py: 
Input registered cell positions (.npy) and plot them in a brainrender scene.
Expected run time: 1 minute.

	Instructions:
	1. Update the 'local_directory' variable to the folder containing the 'coronal_atlas_plate_plot' folder on your local machine.
	3. Run the script.
	4. Press the 'q' key on the keyboard once the brainrender scene has rendered to save the screenshot.
	5. Outputs include:
	a. Image of coronal atlas plate at 4.4mm with presynaptic cell positions in blue (4400_pfc.png).


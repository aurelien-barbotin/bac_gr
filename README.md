bac_gr
======

A simple script to extract the growth rate from a (series of) segmented stacks. This was developed to be used on stacks of images segmented with Ilastik but can be extended to any segmented stack.

Usage
-----
* This script takes data located in a folder 		to_process/		, located in the directory of this script. If no such directory exists or you are unsure, just run the script first using 		run_bacteria_growth.bat		, it will create the folder for you. 
* Put the segmented stacks you want processed in the folder to_process/. The first dimension of the stack is expected to be time, other dimensions x and y.
* Run this script, either by double clicking  		run_bacteria_growth.bat		or by running the script in a command line.

Output
------
Two outputs are generated per stack:
* a png file, showing in order the first, last frame of the stack and the fitted growth curve
* a csv file containing the raw growth curve
 A final csv file is generated, "doubling_time.csv" that contains the doubling time calculated both from an exponential fit and by calculating the ratio between the number of segmented pixels in the first and in the last frame.

Install
-------
The command to install it using pyinstaller is:

	pyinstaller growth_rate.py --onefile --name measure_growth --console --hidden-import='PIL._tkinter_finder' --noconfirm


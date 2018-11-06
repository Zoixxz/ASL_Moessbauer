import numpy as np 
import scipy 
import scipy.stats
import os

#loading files
calibration = []
calibration_names = []
paths = os.getcwd() + '/Fe10_90TestCallibration'

def file_reader_sort(path, array):
	"""
	This function adds the values to the input array
	no output!
	"""
	
	#catch paths which end wih backslash
	if path.endswith('/'):
		return print('invalid path shape, remove the backslash at the end of the path')

	__file_names = [] #internal use only, saves the names of the files
	for i in os.listdir(path):
		__file_names.append(i)
	__file_names.sort()

	for i in __file_names:
		array.append(np.loadtxt(open(path + '/' + i)))
	return

file_reader_sort(paths, calibration)


# configuration of the speaker with different aplitudes

# peak measurement
# moessbauer measurement
#
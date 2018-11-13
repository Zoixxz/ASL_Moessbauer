import numpy as np 
import matplotlib.pyplot as plt 
import scipy 
import scipy.stats
import os

#loading files
test_calibration = []
calibration_names = []
path_test_calibration = os.getcwd() + '/Fe10_90TestCallibration'

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
	print(__file_names)

	for i in __file_names:
		array.append(np.loadtxt(open(path + '/' + i)))
	return

file_reader_sort(path_test_calibration, test_calibration)


# configuration of the speaker with different aplitudes

# peak measurement
path_measurements = os.getcwd() + '/Measurements'
measurement_array = []
file_reader_sort(path_measurements, measurement_array)

bin_array = np.arange(np.shape(measurement_array)[1]) 
plt.plot(bin_array, measurement_array[1], 'b.' )
plt.show()


# moessbauer measurement
#
import numpy as np 
import matplotlib.pyplot as plt 
import scipy 
from scipy.interpolate import interp1d, Rbf, InterpolatedUnivariateSpline, UnivariateSpline
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
		return False

	__file_names = [] #internal use only, saves the names of the files
	for i in os.listdir(path):
		__file_names.append(i)
	__file_names.sort()
	print(__file_names)

	for i in __file_names:
		array.append(np.loadtxt(open(path + '/' + i)))
	return


def local_minima(values, number_of_minima, intervall_radius):
	"""
	Returns a list with the local minima starting from the lowest.
	In total the #number_of_minima lowest minima will be caluclated 
	assuming the inervall radius is large enough.
	"""
	__values = np.ndarray.tolist(values)
	__array = []
	for i in range(number_of_minima):
		__array.append(min(__values))
		#check for cases where the intervall radius goes beyond the index of the array of values
		if (__values.index(min(__values)) - intervall_radius > 0):
			lower_bound = __values.index(min(__values)) - intervall_radius
		else:
			lower_bound = 0
		if (__values.index(min(__values)) + intervall_radius < len(values)):	
			upper_bound = __values.index(min(__values)) + intervall_radius
		else:
			upper_bound = len(values)

		__values = __values[:lower_bound] + __values[upper_bound:] 

	return __array

"""
Start of evaluation:
1. Get all the measured data and cut the measurements to be able to process them 
2. Calibration measurement
3. Preparation of data
"""
################################################
# 1. getting the measured data from the csv file
################################################

file_reader_sort(path_test_calibration, test_calibration)

path_measurements = os.getcwd() + '/Measurements'
measurement_array = []
file_reader_sort(path_measurements, measurement_array)
print(path_measurements)


################################################
# 2. calibration
################################################

calibrations = measurement_array[-5:]

x_ax = np.arange(512)

low_cut = 18
high_cut = 29
cut_dimension = 512 - (low_cut + high_cut)

cut_calibration = [calibrations[i][low_cut:-high_cut] for i in range(len(calibrations))]

#fit the calibration measurements with a straight line
width = [50, 20, 15, 15, 15]
minima_num = [4, 6, 6, 6, 6]

values_of_minima = [local_minima(cut_calibration[i], minima_num[i], width[i]) for i in range(5)]	
print(values_of_minima)

x_vals = [np.ndarray.tolist(cut_calibration[0]).index(values_of_minima[0][i]) for i in range(4)]

#TODO: sort calibration values by index position in ascending order
x_vals.sort()
y_vals = [cut_calibration[0][x_vals[i]] for i in range(4)]

fit = np.polyfit(x_vals, [values_of_minima[0][i] for i in range(4)], 1)

#create array for polyfit

################################################
# 3. evaluation of measurements
################################################
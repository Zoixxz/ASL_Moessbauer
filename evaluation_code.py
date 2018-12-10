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
low_cut = 18
high_cut = 29
cut_dimension = 512 - (low_cut + high_cut)
width = [50, 20, 15, 15, 15]
minima_num = [4, 6, 6, 6, 6]
voltages = [30., 40., 50., 60., 70.]
calibrations = measurement_array[-5:]

x_ax = np.arange(512)


cut_calibration = [calibrations[i][low_cut:-high_cut] for i in range(len(calibrations))]

#fit the calibration measurements with a straight line


values_of_minima = [local_minima(cut_calibration[i], minima_num[i], width[i]) for i in range(5)]	
print(values_of_minima)

x_vals = [[np.ndarray.tolist(cut_calibration[j]).index(values_of_minima[j][i]) for i in range(minima_num[j])] for j in range(5)]


#TODO: sort calibration values by index position in ascending order
sorted_x_vals = []
for i in range(5): #sort the x_vals in ascending order
	__sorted_local_x_vals = x_vals[i]
	__sorted_local_x_vals.sort()
	sorted_x_vals.append(__sorted_local_x_vals)

sorted_y_vals = [[cut_calibration[i][sorted_x_vals[i][j]] for j in range(minima_num[i])] for i in range(5)]
print('sorted_x_vals: ', sorted_x_vals)
print(sorted_y_vals)
#polyfit
fit_coefficients = []
for i in range(6):
	if (i == 0 or i == 5): #leave the first intervall of the 30 V measurement out as there is no 1st and 6th peak
		__fit = np.polyfit([voltages[j] for j in range(1,5)], [sorted_x_vals[j][i] for j in range(1,5)] , 1)
		fit_coefficients.append(__fit)
	else:	
		__fit = np.polyfit([voltages[j] for j in range(5)], [sorted_x_vals[j][i] for j in range(5)], 1)
		fit_coefficients.append(__fit)

fit_functions = [np.poly1d(fit_coefficients[i]) for i in range(5)]
print(fit_functions)
print(fit_coefficients)
for i in range(5):
	plt.plot(voltages, fit_functions[i](voltages), 'b-')
plt.show()



"""
fit = np.polyfit(x_vals, [values_of_minima[0][i] for i in range(4)], 1)
fit_fn = np.poly1d(fit)
"""

#create array for polyfit

################################################
# 3. evaluation of measurements
################################################

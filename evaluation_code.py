import numpy as np 
import scipy 
import scipy.stats
import os

#loading files
calibration = []
for i in os.listdir():
	if i.endswith('.txt'):
		calibration.append(open(i))

# configuration of the speaker with different aplitudes

# peak measurement
# moessbauer measurement
#
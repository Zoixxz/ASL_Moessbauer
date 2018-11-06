import numpy as np
import scipy
import scipy.stats
import sys, os
from matplotlib import pyplot as plt




file="/Fe10_90TestCallibration/Fe10.txt"
path=os.getcwd()+file
fp=open(path,'r+')

test = np.loadtxt(fp)
print(test)
x = np.linspace(0, np.size(test), np.size(test))

plt.plot(x, test)
plt.show()

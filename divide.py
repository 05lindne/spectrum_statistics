#!/usr/bin/env python

""" File: divide.py
	Author: Sarah Lindner
	Date of last change: 05.04.2016

	
"""


import numpy as np
import scipy.integrate as integrate


data1, data2 = np.loadtxt('/mnt/Daten/measurements/SiV/BASD/sidepeak_intensity/data/amplitude1_amplitude2.txt', delimiter="\t", usecols=(0,1), unpack=True)
# y = np.loadtxt('/mnt/Daten/measurements/SiV/BASD/sidepeak_intensity/data/integrated_xc2.txt', delimiter="\t", usecols=(0,), unpack=True)

out_file = open('divided_amplitude1_amplitude2.txt', 'w')

print('...dividing')

for d1, d2 in zip(data1, data2):
	result=d1/d2
	out_file.write('{0}\n'.format(result))


out_file.close()

print ('...thank you and have a nice day :)')
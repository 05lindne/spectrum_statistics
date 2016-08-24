#!/usr/bin/env python

""" File: integrate_lorentz.py
	Author: Sarah Lindner
	Date of last change: 04.04.2016

	
"""


import numpy as np
import argparse
import scipy.integrate as integrate

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output file; without extension')
parser.add_argument('in_file', help = 'input filename') 
parser.add_argument('-c', nargs = 3, type=int, help = 'columns with data containing \n column 1: amplitude \n column 2: width \n column 3: x position')
args = parser.parse_args() 


print('...reading file {0}'.format(args.in_file))

amplitude_all, width_all, xpos_all  = np.loadtxt( args.in_file, delimiter="\t", usecols=args.c, unpack=True)

param_file = open(args.out_filename + '.txt', 'w')

print('...calculating integral')

for amplitude, width, xpos in zip(amplitude_all, width_all, xpos_all):
	result = integrate.quad(lambda x: 2*amplitude/np.pi*width/(4*(x-xpos)**2), -np.inf, np.inf)

	# write fit parameters into file
	param_file.write("{0}\t{1}\n".format( result[0], result[1]))

param_file.close()

print ('...thank you and have a nice day :)')
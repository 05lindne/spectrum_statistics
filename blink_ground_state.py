#!/usr/bin/env python

""" File: blink_ground_state.py
	Author: Sarah Lindner
	Date of last change: 02.08.2016

	
"""

import sys
sys.path.append('/Volumes/EXTSAHARA/work/plot/')

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import filename_handling

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('on_off_file', help = 'input .csv filename with on/off times of blinking states')
# parser.add_argument('cps_file', help = 'input .csv filename of the whole countrate timetrace')
parser.add_argument('cps', type=float, help = 'cps of ground state')

args = parser.parse_args() 


def main():

	df = pd.read_csv(args.on_off_file)
	# df_end = pd.read_csv(args.cps_file)

	# get last time tag of entire measurement
	# t_end = df_end.time.tail(1)

	df_sort = df.sort_values('flank_on')

	# print(df_sort)

	# construct series of on flanks of ground state
	ser_zero = pd.Series([])
	ser_ground_on = ser_zero.append(df_sort.flank_off)
	max_index = ser_ground_on.tolist().index(max(ser_ground_on.tolist()))
	ser_ground_on = ser_ground_on.drop( ser_ground_on.index[max_index] )
	# print(ser_ground_on)

	# construct series of off flanks of ground state
	ser_ground_off = pd.Series([])
	ser_ground_off = ser_ground_off.append(df_sort.flank_on)
	min_index = ser_ground_off.tolist().index(min(ser_ground_off.tolist()))
	ser_ground_off = ser_ground_off.drop( ser_ground_off.index[min_index] )	
	# print(ser_ground_off)


	df_ground_on = pd.DataFrame( {'flank_on':ser_ground_on} )
	df_ground_off = pd.DataFrame( {'flank_off':ser_ground_off} )

	df_ground_on.reset_index(drop=True, inplace=True)
	df_ground_off.reset_index(drop=True, inplace=True)

	# print(df_ground_on)
	# print(df_ground_off)

	df_ground = pd.concat( [df_ground_on, df_ground_off], axis=1)

	# print(df_ground)

	df_all = pd.concat([df, df_ground], ignore_index=True )
	# print (df_all)

	result = df_all.fillna(args.cps)
	# print(result)


	result.to_csv( filename_handling.pathname( args.on_off_file ) + "/" + filename_handling.filestub( args.on_off_file )  + '_with_ground_state.csv', index=False)

if __name__ == '__main__':
	main()
#!/usr/bin/env python

""" File: blink_periods.py
	Author: Sarah Lindner
	Date of last change: 01.08.2016

	
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
# parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_file', help = 'input filename with on/off flank times')
args = parser.parse_args() 


def main():

	df = pd.read_csv(args.in_file)

	print(df)

	diff =  pd.Series( df[ "flank_off" ] - df[ "flank_on" ] , name = 'diff')

	df_diff = pd.concat( [df, diff ], axis = 1 )

	# remove values where difference = 0 -> bad data point
	df_diff = df_diff.query('diff != 0')

	# print (df_diff)


	df_diff = df_diff.groupby('blink_state').apply( (lambda grouped: compute_percentage( grouped, df_diff['diff'].sum()) ) )
	df_diff = df_diff.groupby('blink_state').apply( (lambda grouped: get_stats( grouped) ) )
	print(df_diff.head())

	df_result = pd.DataFrame( df_diff.loc[:,['blink_state', 'state_percentage', 'count', 'min', 'max', 'mean', 'std', 'median']])
	df_result = df_result.drop_duplicates()
	print (df_result)


	df_diff.to_csv( filename_handling.pathname( args.in_file ) + "/" + filename_handling.filestub( args.in_file )  + '_retention_all.csv')
	df_result.to_csv( filename_handling.pathname( args.in_file ) + "/" + filename_handling.filestub( args.in_file )  + '_retention_summary.csv')


def compute_percentage( grouped, t_column_sum ):

	# the grouped object contains the data grouped according to the values in 'CPS'
	# we can grab its "t" column and apply functions normally
	# adding the result to the grouped object adds the result to the original data frame

	# print grouped["t"]
	# print t_column_sum

	grouped['t_column_sum'] = t_column_sum
 	grouped['t_block_sum'] = grouped['diff'].sum()
 	grouped['state_percentage'] = grouped['t_block_sum'] / t_column_sum
	
	return grouped

def get_stats(grouped):

	grouped['count'] = grouped['diff'].count()
	grouped['min'] = grouped['diff'].min()
	grouped['max'] = grouped['diff'].max()
	grouped['mean'] = grouped['diff'].mean()
	grouped['std'] = grouped['diff'].std()
	grouped['median'] = grouped['diff'].median()

	return grouped

if __name__ == '__main__':
	main()
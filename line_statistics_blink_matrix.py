#!/usr/bin/env python

""" File: line_statistics_regression.py
	Author: Sarah Lindner
	Date of last change: 11.08.2016

	
"""



import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import filename_handling

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_file', nargs = '*', help = 'input filename')
args = parser.parse_args() 

sns.set_context("poster")
# sns.set_context("paper")
sns.set_style("whitegrid")

def main():

	filename_handling.check_overwrite( args.out_filename )


	df = pd.read_csv(args.in_file)


	sns.pairplot(df, vars=["sepal_width", "sepal_length"])


	plt.savefig( ( args.out_filename +'.pdf'))
	plt.savefig( ( args.out_filename +'.svg'))

	sns.plt.show()



if __name__ == '__main__':
	main()
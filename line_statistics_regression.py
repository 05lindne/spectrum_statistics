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
parser.add_argument('in_files', nargs = '*', help = 'input filenames')
args = parser.parse_args() 

sns.set_context("poster")
# sns.set_context("paper")
sns.set_style("whitegrid")

def main():

	filename_handling.check_overwrite( args.out_filename )

	df = pd.DataFrame()
	my_list = []

	for item in args.in_files:
	    df1 = pd.read_csv(item)
	    my_list.append(df1)
	df = pd.concat(my_list)


	df_reg = df.loc[(df["position"] > 737) & (df["position"] < 745) & (df["width"] > 4)]

	regression_plot = sns.lmplot(x="position", y="width", data=df_reg, robust=True)


	regression_plot.set_axis_labels('ZPL Center (nm)', 'Width (nm)')

	

	plt.savefig( ( args.out_filename +'.pdf'))
	plt.savefig( ( args.out_filename +'.svg'))

	sns.plt.show()




if __name__ == '__main__':
    main()
#!/usr/bin/env python

""" File: line_statistics_blink.py
	Author: Sarah Lindner
	Date of last change: 11.07.2016

	
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


	scatterplot = sns.regplot(x="position", y="width", data=df, fit_reg = False,  )

	
	df_g2 = df.loc[(df["g2"] == 1)]
	df_blink = df.loc[(df["blink"] == 1)]
	df_no_blink = df.loc[(df["blink"] == 0) & (df["g2"] == 1)]


	scatterplot.plot("position", "width", 'r.', data=df_g2, label=''  )
	scatterplot.plot("position", "width", 'm.', data=df_blink, label='blinking' )
	scatterplot.plot("position", "width", 'k.', data=df_no_blink, label='not blinking' )

	plt.xlabel('ZPL Center (nm)')
	plt.ylabel('Width (nm)')
	plt.ylim(0,20)
	plt.legend()


	plt.savefig( ( args.out_filename +'.pdf'))
	plt.savefig( ( args.out_filename +'.svg'))

	sns.plt.show()



if __name__ == '__main__':
    main()
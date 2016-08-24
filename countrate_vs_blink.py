#!/usr/bin/env python

""" File: line_statistics_blink.py
	Author: Sarah Lindner
	Date of last change: 11.07.2016

	
"""
import sys
sys.path.append('/Volumes/EXTSAHARA/work/plot/')

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import filename_handling
from matplotlib.lines import Line2D
from six import iteritems


# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_file', help = 'input filename')
parser.add_argument('-xlim', nargs = 2, type=int, help = 'lower and upper limits for x-axis')
parser.add_argument('-ylim', nargs = 2, type=int, help = 'lower and upper limits for y-axis')
args = parser.parse_args() 

sns.set_context("poster")
# sns.set_context("paper")
sns.set_style("whitegrid")

def main():

	filename_handling.check_overwrite( args.out_filename )


	df = pd.read_csv(args.in_file)

	# print (Line2D.markers)

	# my_markers = ['s','|','x','^','d','h','+','*','o','.','1','p','3','2','4','H','v','8','<','>']
	# my_markers = [0, 1, 2, 3, 4,'D', 6, 7,'s','|','x', 5,'_','^','d','h','+','*','o','.','1','p','3','2','4','H','v','8','<','>']
	# df_g2 = df.loc[(df["g2"] == 1)]
	# df_blink = df.loc[(df["blink"] == 1)]
	# df_no_blink = df.loc[(df["blink"] == 0) & (df["g2"] == 1)]


	scatterplot = sns.lmplot(x="blink_state", y="median", data=df, hue='filename', fit_reg = False, legend = False, truncate = True)

	# scatterplot.plot("position", "width", 'r.', data=df_g2, label=''  )
	# scatterplot.plot("position", "width", 'm.', data=df_blink, label='blinking' )
	# scatterplot.plot("position", "width", 'k.', data=df_no_blink, label='not blinking' )

	plt.xlabel('Countrate (cps)')
	plt.ylabel('Median Retention Time (s)')

	plt.xlim(0,) 
	plt.ylim(0,) 
	plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
	# plt.xticks(rotation='vertical')
	plt.tight_layout()

	if args.ylim:
		plt.ylim(args.ylim[0],args.ylim[1])
	if args.xlim:
		plt.xlim(args.xlim[0],args.xlim[1])
	# plt.legend()

	if args.ylim or args.xlim:	
		plt.savefig( ( args.out_filename +'_lim.pdf'))
		plt.savefig( ( args.out_filename +'_lim.svg'))
	else:
		plt.savefig( ( args.out_filename +'.pdf'))
		plt.savefig( ( args.out_filename +'.svg'))

	sns.plt.show()



if __name__ == '__main__':
    main()
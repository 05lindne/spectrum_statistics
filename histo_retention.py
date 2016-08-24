#!/usr/bin/env python

""" File: plot_blink_periods.py
	Author: Sarah Lindner
	Date of last change: 12.08.2016


	
"""


import sys
sys.path.append('/Volumes/EXTSAHARA/work/plot/')
import matplotlib
matplotlib.use('TkAgg')

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import filename_handling
from scipy import stats
# import statsmodels

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_file', help = 'input filenames')
parser.add_argument('-xlim', nargs = 1, type=int, help = 'lower and upper limits for x-axis')
parser.add_argument('-ylim', nargs = 2, type=int, help = 'lower and upper limits for y-axis')
parser.add_argument('-emitter', nargs = 1, help = 'only use one emitter for data evaluation')
args = parser.parse_args() 

sns.set_context("poster")
# sns.set_context("paper")
sns.set_style("whitegrid")
# print (sns.axes_style())
def main():

	# filename_handling.check_overwrite( args.out_filename )
	print ('Reading file ' + args.in_file)
	df = pd.read_csv(args.in_file)
	if args.xlim:
		df_lim = df[df['diff'] < args.xlim[0] ]
	else:
		df_lim = df

	# print df_lim.head()

	if args.emitter:
		df_plot = df_lim[df_lim['filename'] == str(args.emitter[0])]
	else:
		df_plot = df_lim

	df_grouped = df_plot.groupby('blink_state')
	groups = [df_grouped.get_group(x) for x in df_grouped.groups]

	print('plotting')

	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	# sns.distplot(df_lim['diff'], kde=False, rug=True)
	# ax = sns.distplot(df_plot['diff'], kde=False, rug=True)
	# sns.distplot(df_plot['diff'], kde=False, rug=True, fit=stats.expon)
	# sns.rugplot(df_plot['diff'])
	# sns.kdeplot(df_plot['diff'], cut=0, gridsize=1000)
	# ax = sns.distplot(df_plot['diff'], rug=True, kde_kws={"cut": 0}, hist=True, fit=stats.expon)
	# ax = sns.distplot(df_plot['diff'], rug=True, kde_kws={"cut": 0}, hist=True)
	# ax = sns.distplot(df_plot['diff'], rug=False, hist=True)
	ax1 = sns.distplot(groups[0]['diff'], rug=True, hist=True, kde=False)
	# ax2 = sns.distplot(groups[1]['diff'], rug=False, hist=True)
	# ax2 = ax1.twinx()
	# ax2 = sns.distplot(groups[1]['diff'], rug=True, hist=True, color = 'r', kde=False)
	# ax2.grid(None)


	plt.xlabel('Retention Time (s)')
	if args.xlim:
		plt.xlim(0,args.xlim[0])
	else:
		plt.xlim(0,)


	if args.xlim:
		plt.savefig( ( args.out_filename + '_xlim' + str(args.xlim[0]) + '.pdf'))
		plt.savefig( ( args.out_filename + '_xlim' + str(args.xlim[0]) + '.svg'))
	else:
		plt.savefig( ( args.out_filename +'.pdf'))
		plt.savefig( ( args.out_filename +'.svg'))

	sns.plt.show()

	print('now that was fun!')


if __name__ == '__main__':
	main()
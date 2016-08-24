#!/usr/bin/env python

""" File: line_statistics_seaborn.py
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

# sns.set_context("poster")
sns.set_context("paper")
sns.set_style("whitegrid")

def main():

	filename_handling.check_overwrite( args.out_filename )

	df = pd.DataFrame()
	my_list = []

	for item in args.in_files:
	    df1 = pd.read_csv(item)
	    my_list.append(df1)
	df = pd.concat(my_list)

	# fig, ax = plt.subplots()

	# df_reg = df.loc[(df["position"] > 737) & (df["position"] < 745) & (df["width"] > 4)]


	original_plot = sns.jointplot(x="position", y="width", data=df, stat_func = None, ylim=(0,20))
	# original_plot = sns.jointplot(x="position", y="width", marker = 'o', data=df, size=5, stat_func = None, ylim=(0,20))

	# sns.lmplot(x="position", y="width", data=df_reg, robust=True)

	# sns.jointplot(x="position", y="width", data=df, kind="kde")
	# sns.plt.show()

	# g = sns.jointplot(x="position", y="width", data=df, kind="kde", color="b")
	# g.plot_joint(plt.scatter, c="k", s=30, linewidth=1, marker="+")
	# g.ax_joint.collections[0].set_alpha(0)
	
	df_g2 = df.loc[(df["g2"] == 1)]
	# df_blink = df.loc[(df["blink"] == 1)]
	# df_no_blink = df.loc[(df["blink"] == 0) & (df["g2"] == 1)]


	original_plot.ax_joint.plot("position", "width", 'ro', data=df_g2 )
	# original_plot.ax_joint.plot("position", "width", 'm.', markersize = 5, data=df_blink )
	# original_plot.ax_joint.plot("position", "width", 'k.', markersize = 5, data=df_no_blink )

	# original_plot.ax_joint.cla()
	original_plot.set_axis_labels('ZPL Center (nm)', 'Width (nm)')

	# original_plot.xlabel('ZPL Center (nm)')
	# plt.ylabel('Width (nm)')

	plt.savefig( ( args.out_filename +'.pdf'))
	plt.savefig( ( args.out_filename +'.svg'))

	sns.plt.show()


	# sns.distplot(df.position)
	# sns.plt.show()

	# sns.distplot(df.width)
	# sns.plt.show()
	


if __name__ == '__main__':
    main()
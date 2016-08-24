#!/usr/bin/env python

""" File: line_statistics_seaborn.py
	Author: Sarah Lindner
	Date of last change: 11.07.2016

	
"""



import argparse
import pandas as pd
import seaborn as sns


# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_file', help = 'input filenames')
args = parser.parse_args() 



def main():

	df = pd.read_csv(args.in_file)

	sns.jointplot(x="position", y="width", data=df)

	sns.jointplot(x="position", y="width", data=df, kind="kde")
	sns.plt.show()

	g = sns.jointplot(x="position", y="width", data=df, kind="kde", color="m")
	g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
	g.ax_joint.collections[0].set_alpha(0)
	

	sns.distplot(df.position)
	sns.plt.show()
	
	sns.distplot(df.width)
	sns.plt.show()
	


if __name__ == '__main__':
    main()
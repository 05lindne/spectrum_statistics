#!/usr/bin/env python


""" File: plot_countrate.py
	Author: Sarah Lindner
	Date of last change: 02.08.2016

	plot countrate from cvs file

"""

import sys
sys.path.append('/Volumes/EXTSAHARA/work/plot/')
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import argparse
import filename_handling
import pandas as pd
import pylab




print ('Backend: ')
print( plt.get_backend() )
# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('in_file', help = 'input filename as .csv file')
parser.add_argument('binsize', help = 'size of bin in seconds')
parser.add_argument('-pick', action = 'store_true', help = "pick time data points of flanks")
parser.add_argument('-notitle', action = 'store_true', help = "don't display plot title")
parser.add_argument('-xlimits', nargs = 2, type=int,help = 'lower and upper limits for x-axis')
parser.add_argument('-ylimits', nargs = 2, type=int, help = 'lower and upper limits for y-axis')

args = parser.parse_args()

mutable_save_x = [] 
mutable_save_n = [] 
mutable_save_f = [] 
# mutable_on_off = {'flank': 'd'}

fig = plt.figure()
ax = fig.add_subplot(111)
mutable_cid = {}

def main():

	my_filestub = filename_handling.filestub( args.in_file )
	df = pd.read_csv(args.in_file)

	print ("Plotting file: {0}".format(args.in_file))


	mutable_cid['cid'] = 0


	fig, ax = plotdata(df.time, df.countrate, my_filestub)

	if (args.pick):
		print( 'Press key "n" or "f" and click on data point to select point as flank_on or flank_off of the blinking state')
		ax.figure.canvas.mpl_connect('key_press_event', on_off)


	plt.savefig( ( filename_handling.pathname( args.in_file ) + "/" + my_filestub +'.pdf'))
	plt.savefig( ( filename_handling.pathname( args.in_file ) + "/" + my_filestub +'.svg'))

	print ("...had fun creating an interesting plot.")

	plt.show()

	if (args.pick):
		print ('mutable_save_n {0}'.format(mutable_save_n))
		print ('mutable_save_f {0}'.format(mutable_save_f))

		df_flank_on = pd.DataFrame({'flank_on':mutable_save_n})
		df_flank_off = pd.DataFrame({'flank_off':mutable_save_f})
		df_flank_on_off = df_flank_on.join(df_flank_off)


		df_flank_on_off.to_csv( filename_handling.pathname( args.in_file ) + "/" + my_filestub +'_flank_on_off.csv')


def plotdata(xdata, ydata, my_filestub):


	fig = plt.plot(xdata, ydata, linestyle = "-", color = 'black', marker = '.', markersize=2, picker=2)

	# aestectic cosmetics
	if args.notitle == False:
		plt.title(my_filestub, fontsize = 23)
	plt.xlabel('Time (s)', fontsize = 23)
	plt.ylabel('Countrate (cps)', fontsize = 23)
	plt.tick_params(axis = 'both', labelsize = 23)

	if (args.xlimits):
		plt.xlim(args.xlimits[0], args.xlimits[1]) # zoom in on the x-axis
	else:
		plt.xlim([min(xdata),max(xdata)])
	if (args.ylimits):
		plt.ylim(args.ylimits[0], args.ylimits[1]) # zoom in on the y-axis
	else:
		plt.ylim([min(ydata),max(ydata)])

	plt.tight_layout() # suppress chopping off labels

	return fig, ax



def datapick_n (event):
	thisline = event.artist
	pickx = thisline.get_xdata()
	ind = event.ind
	print('flank_on: ', np.take(pickx, ind))

	mutable_save_n.append(np.take(pickx, ind).tolist())

def datapick_f (event):
	thisline = event.artist
	pickx = thisline.get_xdata()
	ind = event.ind
	print('flank_off: ', np.take(pickx, ind))

	mutable_save_f.append(np.take(pickx, ind).tolist())


def on_off (event):
	if event.key == 'n':
		ax.figure.canvas.mpl_disconnect(mutable_cid['cid'])
		mutable_cid['cid'] = ax.figure.canvas.mpl_connect('pick_event', datapick_n)
		# print('event key {0}, mutable_cid[cid] {1}'.format(event.key, mutable_cid['cid']))
	elif event.key == 'f':
		ax.figure.canvas.mpl_disconnect(mutable_cid['cid'])
		mutable_cid['cid'] = ax.figure.canvas.mpl_connect('pick_event', datapick_f)
		# print('event key {0}, mutable_cid[cid] {1}'.format(event.key, mutable_cid['cid']))


	# print ('mutable_cid[cid] {0}'.format(mutable_cid['cid']))


if __name__ == '__main__':
    main()

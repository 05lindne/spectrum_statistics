#!/usr/bin/env python

""" File: plot_blink_periods.py
	Author: Sarah Lindner
	Date of last change: 11.07.2016


	run with files:

	python /mnt/Daten/my_programs/plot/countrate/plot_blink_periods.py try_plot /mnt/Daten/measurements/SiV/milled/Ir22/ox/150305/countrate/Ir_22_spektrum_scan-40x4y4_I_ton_toff_with_ground_state_retention_all.csv /mnt/Daten/measurements/SiV/milled/Ir22/ox/150305/countrate/Ir_22_spektrum_scan-40x4y4_II_ton_toff_with_ground_state_retention_all.csv /mnt/Daten/measurements/SiV/milled/M02-16/160713/countrate/g2_sat113_5mW_countrate_0_01_conv_flank_on_off_with_ground_state_retention_all.csv /mnt/Daten/measurements/SiV/milled/M03-16/160720/countrate/g2_018_countrate_0_08_conv_flank_on_off_with_ground_state_retention_all.csv /mnt/Daten/measurements/SiV/milled/Ir25M/ox/galina/single/20150727/countrate/g2_countrate_0_01_conv_flank_on_off_with_ground_state_retention_all.csv /mnt/Daten/measurements/SiV/milled/Ir25M/ox/galina/single/20150805/countrate/g2_2_countrate_0_007_conv_flank_on_off__with_ground_state_retention_all.csv /mnt/Daten/measurements/SiV/milled/Ir25M/ox/galina/single/20150812/countrate/g2_Ir25M_f166_ox_countrate_0_01_conv_flank_on_off_with_ground_state_retention_all.csv /mnt/Daten/measurements/SiV/milled/Ir9/20141208_Ir9_vak_vak_luft/countrate/g2zuSpektrum3_6_countrate_0_01_conv_flank_on_off_with_ground_state_retention_all.csv /mnt/Daten/measurements/SiV/milled/Ir8/20141112_Ir8_nach_erstem_oxidieren_einzelner/countrate/g2zuSpektrum8_15_5_countrate_0_01_conv_flank_on_off_with_ground_state_retention_all.csv


	
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

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_files', nargs = '*', help = 'input filenames')
args = parser.parse_args() 

sns.set_context("poster")
# sns.set_context("paper")
sns.set_style("whitegrid")
# print (sns.axes_style())
def main():

	# filename_handling.check_overwrite( args.out_filename )

	df = pd.DataFrame()
	df1 = pd.read_csv(args.in_files[0])
	df1['filename'] = filename_handling.filestub( args.in_files[0] )

	for item in args.in_files:
	    df = pd.read_csv(item)
	    df['filename'] = filename_handling.filestub( item )
	    df1 = df1.append(df, ignore_index=True)

	

	# ax_box = sns.boxplot(data=df1, hue='filename', x='blink_state', y='diff', linewidth = 1, width = 3)
	# ax_box = sns.boxplot(data=df1, hue='filename', x='blink_state', y='diff', linewidth = 1, width = 3)

	# ylim = 1
	# plt.ylim(0, ylim)
	# plt.legend().set_visible(False)
	# plt.xticks(rotation='vertical')
	# plt.tight_layout() # suppress chopping off labels



	# plt.savefig( ( args.out_filename + '_ylim'+ str(ylim) +'.pdf'))
	# plt.savefig( ( args.out_filename + '_ylim'+ str(ylim) +'.svg'))


	# plt.savefig( ( args.out_filename +'.pdf'))
	# plt.savefig( ( args.out_filename +'.svg'))



	# sns.plt.show()

	
	# limit = 1
	# df_limit = df1[df1['diff'] < limit]

	# ax_hist = sns.distplot(df_limit['diff'], kde=False, rug=True, )
	# plt.xlabel('Retention Time (s)')
	# plt.savefig( ( args.out_filename + '_lim'+ str(limit) +'.pdf'))
	# plt.savefig( ( args.out_filename + '_lim'+ str(limit) +'.svg'))

	# # plt.savefig( ( args.out_filename +'.pdf'))
	# # plt.savefig( ( args.out_filename +'.svg'))

	# sns.plt.show()


	limit = 100
	df_limit = df1[df1['state_percentage'] < limit]

	ax_hist = sns.distplot(df_limit['state_percentage'], kde=True, rug=True, bins=8 )
	plt.xlabel('Percentage in State')
	# plt.savefig( ( args.out_filename + '_lim'+ str(limit) +'.pdf'))
	# plt.savefig( ( args.out_filename + '_lim'+ str(limit) +'.svg'))

	# sns.kdeplot(df_limit['state_percentage'])
	# sns.kdeplot(df_limit['state_percentage'], bw=.1, label="bw: 0.1")
	# sns.kdeplot(df_limit['state_percentage'], bw=.2, label="bw: 0.2")
	# plt.legend();


	plt.savefig( ( args.out_filename +'_kde.pdf'))
	plt.savefig( ( args.out_filename +'_kde.svg'))

	sns.plt.show()



if __name__ == '__main__':
    main()
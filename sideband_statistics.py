#!/usr/bin/env python

""" File: sideband_statistics.py
    Author: Sarah Lindner
    Date of last change: 14.12.2015

    
"""
import sys
sys.path.append('/mnt/Daten/my_programs/plot/')


from sys import argv
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as col
from mpl_toolkits.mplot3d import Axes3D
from scipy import constants as const
from scipy import stats # linear regression
# import matplotlib.cm as cm
import pickle # save plots in pickle format which can be opened in interactive window
import argparse

import filename_handling # custom functions for working with filenames & directories


# define global variables
color_scale = 'CMRmap'
legend_fontsize = 18
tick_fontsize = 23
label_fontsize = 23
title_fontsize = 23
legend_entries = ["one sideband peak", "1", "1",  "1", "1", "1", "1", "1", "1",]
markers = ['o', 's', 'v', 'D', 'p', '<', 'd', '>', 'h','*']


# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_files', nargs = '*', help = 'input filenames')
args = parser.parse_args() 


def main():

    # argv is your commandline arguments, argv[0] is your program name, so skip it
    check_overwrite( args.out_filename )

    zpl_position_all = []
    sideband_all = []
    linewidth_all = []
    distance_all_nm = []
    distance_all =[]




    #read in data
    
    for in_file in args.in_files:
        print('--> reading file ' + in_file) #print out the filename we are currently processing

        zpl_position, sideband = np.loadtxt( in_file, delimiter = "\t", usecols = (0, 1), unpack = True)
        zpl_position, sideband, linewidth = np.loadtxt( in_file, delimiter = "\t", usecols = (0, 1, 2), unpack = True)

        # zpl_position_all = np.concatenate( ( zpl_position_all, zpl_position ), axis = 0)
        # sideband_all = np.concatenate( ( sideband_all, sideband ), axis = 0)
        # linewidth_all = np.concatenate( ( linewidth_all, linewidth ), axis = 0)
        # distance_all_nm = np.concatenate( ( distance_all,np.absolute( np.subtract( zpl_position, sideband ) )), axis = 0)

        zpl_position_all.append( zpl_position )
        sideband_all.append( sideband )
        linewidth_all.append( linewidth )
        distance_all_nm.append( np.absolute( np.subtract( zpl_position, sideband ) ))

    zpl_ev = convert_wavelength_electronvolt(zpl_position_all)
    sideband_ev = convert_wavelength_electronvolt( sideband_all )


    for (zpl, sideband) in zip(zpl_ev, sideband_ev):
        distance_all.append(np.absolute( np.subtract(zpl, sideband) ))


    sideband_histo(sideband_all,'Sidepeak Position (nm)','_sidepeak', binwidth = 1)
    sideband_histo(zpl_position_all,  'ZPL Position (nm)', '_zpl_position' , binwidth = 0.5)
    sideband_histo(distance_all_nm, 'Distance ZPL - Sideband (meV)', '_distance', binwidth = 2)
    sideband_scatter(zpl_position_all, sideband_all, 'ZPL Position (nm)', 'Sidepeak Position (nm)','_sideband_vs_zpl', fit=False)
    sideband_scatter(sideband_all, distance_all, 'Sidepeak Position (nm)', 'Distance (meV)','_sideband_vs_distance', fit=False)
    sideband_scatter(zpl_position_all, distance_all, 'ZPL Position (nm)', 'Distance (meV)', '_zpl_vs_distance', fit=True)
    sideband_scatter(linewidth_all, distance_all, 'Linewidth (nm)', 'Distance (meV)', '_linewidth_vs_distance', fit=False)
    sideband_scatter(linewidth_all, sideband_all, 'Linewidth (nm)', 'Sidepeak Position (nm)', '_linewidth_vs_sideband', fit=False)
    sideband_scatter3d(zpl_position_all, distance_all, linewidth_all, 'ZPL Position (nm)', 'Distance (meV)', 'Linewidth (nm)', '_zpl_vs_distance_vs_linewidth')
    # print np.median(sideband_all)
    # print np.median(zpl_position_all)
    # print np.median(distance_all)
    


def sideband_histo(position_all, x_axis, filename, binwidth=1):

    # make histogram of the line position data

    ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

    # n, bins, patches = plt.hist(position_all, bins = np.arange((min(position_all) - binwidth), (max(position_all) + binwidth), binwidth), histtype='stepfilled', stacked=True, label=legend_entries)
    n, bins, patches = plt.hist(position_all, bins = np.arange((min(np.concatenate(position_all)) - binwidth), (max(np.concatenate(position_all)) + binwidth), binwidth), histtype='stepfilled', facecolor='k', stacked=True, label=legend_entries)



    # prepare colors for histogram bars
    coloring = plt.get_cmap(color_scale, len(patches)+1) #+1 to avoid white as color
    # # apply color
    # for index, item in enumerate(patches):
    #     item.set_facecolor(coloring(index))

    # apply color
    if len(patches) > 1:
        for index, item in enumerate(patches):
            for patch in item:
                patch.set_facecolor(coloring(index))

    plt.xlabel(x_axis, fontsize = label_fontsize)
    plt.ylabel('Quantity', fontsize = label_fontsize)
    # plt.title('Title', fontsize = title_fontsize)

    # Set the tick labels font
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(tick_fontsize)

    plt.tight_layout()

    # print legend in reveresed plot order (to match input order) and adjust font size
    handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles[::-1], labels[::-1], prop={'size':legend_fontsize}, loc = 2)
    
    plt.grid(True)
    bin_sizes = np.hstack(n)
    highest_bin = bin_sizes.max()
    plt.ylim(0, highest_bin+1)

    plt.savefig( (args.out_filename + filename +'.png'))
    plt.savefig( (args.out_filename + filename +'.pdf'))
    pickle.dump(ax, file( (args.out_filename + filename +'.pickle'), 'w'))

    print '--> saved figure(s) ' + args.out_filename + filename


    plt.show()



def sideband_scatter(position_all, distance_all, x_axis, y_axis, filename, fit):

    ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

    # prepare colors for markers
    coloring = plt.get_cmap(color_scale, len(distance_all)+1) #+1 to avoid white as color

    # fit data
    if fit:
        # prepare file for storing fit parameters
        param_file = open(args.out_filename + '_params.txt', 'w')
        param_file.write("slope\tintercept\tr_value\tp_value\tslope_std_error\n")
        # fit linear regression
        slope, intercept, r_value, p_value, slope_std_error = stats.linregress( np.concatenate( position_all ), np.concatenate( distance_all ) )
        # write fit parameters into file
        param_file.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format( slope, intercept, r_value, p_value, slope_std_error))
        param_file.close()
        # construct linear regression line
        predict_distance_all = intercept + slope *  np.concatenate( position_all )
        # plot line
        print "np.concatenate( position_all ):\n"
        print np.concatenate( position_all )
        print "predict_distance_all:\n"
        print predict_distance_all
        plt.plot( np.concatenate( position_all ), predict_distance_all )

    # plot data
    plt.plot( np.concatenate( position_all ), np.concatenate( distance_all ), 'k.' )


    plt.xlabel(x_axis , fontsize = label_fontsize)
    plt.ylabel(y_axis, fontsize = label_fontsize)
    # plt.title('Title', fontsize = title_fontsize)
    # Set the tick labels font
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(tick_fontsize)

    plt.tight_layout()

    plt.grid(True)

    plt.savefig( (args.out_filename + filename +'.png'))
    plt.savefig( (args.out_filename + filename +'.pdf'))
    plt.savefig( (args.out_filename + filename +'.svg'))
    pickle.dump(ax, file( (args.out_filename + filename +'.pickle'), 'w'))

    print '--> saved figure(s) ' + args.out_filename + filename

    plt.show()



def sideband_scatter3d(position_all, distance_all, linewidth_all, x_axis, y_axis, z_axis, filename):

    position_all = np.concatenate( position_all )
    distance_all = np.concatenate( distance_all )
    linewidth_all = np.concatenate( linewidth_all )


    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    # ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

    # ax.plot( position_all, distance_all, linewidth, 'k.' )
    ax.scatter( position_all, distance_all, linewidth_all, c=distance_all, s=40, norm=col.LogNorm() )
    # plt.scatter( position_all, linewidth_all, c=distance_all, s=40 )
    # plt.scatter( position_all, linewidth_all, c=distance_all, norm=col.LogNorm() )

    # cbar = plt.colorbar()
    # cbar.set_label('Sideband Distance (nm)', fontsize = label_fontsize, rotation = 90)

    # plt.xlabel(x_axis , fontsize = label_fontsize)
    # plt.ylabel(z_axis, fontsize = label_fontsize)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_zlabel(z_axis)
    ax.w_xaxis.set_pane_color((0, 0, 0, 0))
    ax.w_yaxis.set_pane_color((0, 0, 0, 0))
    ax.w_zaxis.set_pane_color((0, 0, 0, 0))

    # Set the tick labels font
    # for label in (cbar.ax.get_yticklabels() + ax.get_xticklabels() + ax.get_yticklabels()):
        # label.set_fontname('Arial')
        # label.set_fontsize(tick_fontsize)

    plt.tight_layout()
    # legend = plt.legend(reversed(plot_list), reversed(legend_entries), prop={'size':legend_fontsize})
    # legend = plt.legend(plot_list, legend_entries, prop={'size':legend_fontsize}, loc = 4)
    plt.grid(True)

    plt.savefig( (args.out_filename + filename +'.png'))
    plt.savefig( (args.out_filename + filename +'.pdf'))
    plt.savefig( (args.out_filename + filename +'.svg'))
    pickle.dump(ax, file( (args.out_filename + filename +'.pickle'), 'w'))

    print '--> saved figure(s) ' + args.out_filename + filename

    plt.show()



def check_overwrite( file ):
    if os.path.isfile(filename_handling.path_filename(file)):
        response = raw_input("Overwrite " + file + " ? - y/n\n")
        if response.lower().startswith("n"):
            print("Sayoonara")
            exit()


def convert_wavelength_electronvolt( wavelength ):
    electronvolt_all = []
    for item in wavelength:
        electronvolt = ( const.h*const.c / (item*10**(-9) ))
        electronvolt_all.append( electronvolt/const.physical_constants['electron volt-joule relationship'][0] *1000 )
    return electronvolt_all

if __name__ == '__main__':
    main()
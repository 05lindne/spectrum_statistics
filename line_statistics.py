#!/usr/bin/env python

""" File: line_statistics.py
	Author: Sarah Lindner
	Date of last change: 18.09.2015

	
"""


from sys import argv
import os
import numpy as np
from matplotlib import pyplot as plt
import pickle # save plots in pickle format which can be opened in interactive window
import argparse
from scipy import stats # linear regression

# define appearance
color_scale = 'CMRmap'
legend_fontsize = 23
tick_fontsize = 23
label_fontsize = 23
title_fontsize = 23
legend_entries = []

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_files', nargs = '*', help = 'input filenames')
parser.add_argument("-g2", action = "store_true", help = "indicate g2 data") 


args = parser.parse_args() 

if args.g2: 
    print 'data exhibiting g2 dip will be indicated in plot'


def main():

    check_overwrite( args.out_filename )

    line_position_all = []
    line_width_all = []
    g2_exist_all = []

    # legend_entries = []




    #read in data
    for in_file in args.in_files:
        print('--> reading file ' + in_file) #print out the filename we are currently processing

        line_position, line_width, g2_exist  = np.loadtxt( in_file, delimiter="\t", usecols=(0, 1, 2), unpack=True)

        line_position_all.append(line_position)
        line_width_all.append(line_width)
        g2_exist_all.append(g2_exist)

        # prepare legend entries from file name
        file_parts = in_file.split('/')
        last_part = file_parts[len(file_parts)-1]
        last_part_split = last_part.split('.')
        legend_entry = last_part_split[len(last_part_split)-2] # take item before last dot

        legend_entries.append(legend_entry)

    # linewidth(line_width_all)
    # zpl_postition(line_position_all )
    width_position(line_width_all, line_position_all, g2_exist_all, fit=True)


def linewidth(line_width_all):
    # make the histogram of the line width data

    ax = plt.subplot()# Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font 

    binwidth = .5 #nm
    n, bins, patches = plt.hist(line_width_all, bins = np.arange(0, max(np.concatenate(line_width_all)) + binwidth, binwidth), histtype='stepfilled', stacked=True, label=legend_entries)

    # prepare colors for histogram bars
    coloring = plt.get_cmap(color_scale, len(patches)) #+1 to avoid white as color
    # coloring = plt.get_cmap(color_scale, len(patches)+1) #+1 to avoid white as color
    # apply color
    for index, item in enumerate(patches):
        for patch in item:
            patch.set_facecolor(coloring(index))

    plt.xlabel('Linewidth (nm)', fontsize = label_fontsize)
    plt.ylabel('Quantity', fontsize = label_fontsize)
    # plt.title('Title', fontsize = title_fontsize)

    # Set the tick labels font
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(tick_fontsize)

    plt.tight_layout()
    plt.legend(prop={'size':legend_fontsize})
    plt.grid(True)

    plt.savefig( (args.out_filename +'_width.png'))
    plt.savefig( (args.out_filename +'_width.pdf'))
    pickle.dump(ax, file( (args.out_filename +'_width.pickle'), 'w'))

    print '--> saved figure ' + args.out_filename +'_width.png'
    print '--> saved figure ' + args.out_filename +'_width.pdf'

    plt.show()




def zpl_postition(line_position_all):
    # make histogram of the line position data

    ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

    binwidth = 5 #nm
    n, bins, patches = plt.hist(line_position_all, bins = np.arange(700, max(np.concatenate(line_position_all)) + binwidth, binwidth), histtype='stepfilled', stacked=True, label=legend_entries)

    # prepare colors for histogram bars
    coloring = plt.get_cmap(color_scale, len(patches)) #+1 to avoid white as color
    # coloring = plt.get_cmap(color_scale, len(patches)+1) #+1 to avoid white as color
    # apply color
    for index, item in enumerate(patches):
        for patch in item:
            patch.set_facecolor(coloring(index))

    plt.xlabel('ZPL Center (nm)', fontsize = label_fontsize)
    plt.ylabel('Quantity', fontsize = label_fontsize)
    # plt.title('Title', fontsize = title_fontsize)

    # Set the tick labels font
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(tick_fontsize)

    plt.tight_layout()
    legend = plt.legend(prop={'size':legend_fontsize})
    plt.grid(True)

    plt.savefig( (args.out_filename +'_position.png'))
    plt.savefig( (args.out_filename +'_position.pdf'))
    pickle.dump(ax, file( (args.out_filename +'_position.pickle'), 'w'))

    print '--> saved figure ' + args.out_filename +'_position.png'
    print '--> saved figure ' + args.out_filename +'_position.pdf'

    plt.show()



def width_position(line_width_all, line_position_all, g2_exist_all, fit):

    ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

    # prepare colors for markers
    # coloring = plt.get_cmap(color_scale, len(line_position_all)+1) #+1 to avoid white as color
    coloring = plt.get_cmap(color_scale, len(line_position_all)) #+1 to avoid white as color

    plot_list = []
    # plot
    for index, (line, width, g2_exist) in enumerate( zip(line_position_all, line_width_all, g2_exist_all) ):
        # plot = plt.scatter(line, width, color='k', lw=0.5, s=50, marker='o', facecolor=coloring(index), label = legend_entries[index])
        plot = plt.scatter(line, width, color='k', lw=0.5, s=50, marker='o', facecolor='k', label = legend_entries[index])
        plot_list.append(plot)

        line_position_g2 = [p for p,g in zip(line, g2_exist) if g == 1]
        line_width_g2 = [w for w,g in zip(width, g2_exist) if g == 1]

        plot = plt.scatter(line_position_g2, line_width_g2, edgecolor='r', lw=3, s=100, marker='o', facecolor = 'none')
        plot_list.append(plot)


    # fit data
    if fit:
        line_width_fit = []
        line_position_fit = []

        line_width_temp = []
        line_position_temp = []

        for index,( item1, item2 ) in enumerate( zip( np.concatenate(line_width_all), np.concatenate(line_position_all) ) ):
            if item1 >= 5:
                # print line_width_all 
                # print "\n\n"
                # print np.concatenate(line_width_all)
                line_width_temp.append( np.concatenate(line_width_all )[index] )
                line_position_temp.append( np.concatenate(line_position_all )[index] )

        # line_width_fit = np.array(filter(lambda x: x >= 5, np.concatenate(line_width_all) ) )

        # print line_width_fit
        # print"\n\n\n"
        # print line_position_fit
        # print "\n\n\n"
        # print len(line_width_fit)
        # print "\n\n\n"
        # print len(line_position_fit)

        line_width_fit = np.array(line_width_temp)
        line_position_fit = np.array(line_position_temp)

        # prepare file for storing fit parameters
        param_file = open(args.out_filename + '_params.txt', 'w')
        param_file.write("slope\tintercept\tr_value\tp_value\tslope_std_error\n")
        # fit linear regression
        slope, intercept, r_value, p_value, slope_std_error = stats.linregress( line_position_fit, line_width_fit )
        # write fit parameters into file
        param_file.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format( slope, intercept, r_value, p_value, slope_std_error))
        param_file.close()
        # construct linear regression line
        predict_line_position_all = intercept + slope * line_position_fit 
        # plot line
        plt.plot( line_position_fit , predict_line_position_all )


    plt.xlabel('ZPL Center (nm)', fontsize = label_fontsize)
    plt.ylabel('Width (nm)', fontsize = label_fontsize)
    # plt.title('Title', fontsize = title_fontsize)
    # Set the tick labels font
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(tick_fontsize)

    plt.tight_layout()
    plt.ylim(0,plt.ylim()[1])
    # legend = plt.legend(prop={'size':legend_fontsize})
    plt.grid(True)

    plt.savefig( (args.out_filename +'_width_position.png'))
    plt.savefig( (args.out_filename +'_width_position.pdf'))
    pickle.dump(ax, file( (args.out_filename +'_width_position.pickle'), 'w'))

    print '--> saved figure ' + args.out_filename +'_width_position.png'
    print '--> saved figure ' + args.out_filename +'_width_position.pdf'

    plt.show()



def path_filename( file ):
   return os.path.dirname( os.path.realpath( file ) ) + "/" + os.path.basename( file )




def check_overwrite( file ):
    if os.path.isfile(path_filename(file)):
        response = raw_input("Overwrite " + file + " ? - y/n\n")
        if response.lower().startswith("n"):
            print("Sayoonara")
            exit()





if __name__ == '__main__':
    main()
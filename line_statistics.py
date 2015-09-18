#!/usr/bin/env python

""" File: line_statistics.py
	Author: Sarah Lindner
	Date of last change: 18.09.2015

	
"""


from sys import argv
import numpy as np
from matplotlib import pyplot as plt
import argparse
import collections

# define appearance
color_scale = 'CMRmap'
legend_fontsize = 23
tick_fontsize = 23
label_fontsize = 23
title_fontsize = 23


parser = argparse.ArgumentParser()
parser.add_argument('out_filename', help = 'name for output files; without extension')
parser.add_argument('in_files', nargs = '*', help = 'input filenames')
parser.add_argument("-g2", action = "store_true", help = "indicate g2 data") 
parser.add_argument("-v", "--verbose", action = "store_true", help = "increase output verbosity") 

args = parser.parse_args() 
if args.verbose: 
    print 'verbose output'
    if args.g2: 
        print 'data having g2 dip will be indicated in plot'
print parser.parse_args()



line_position_all = []
line_width_all = []
g2_exist_all = []

legend_entries = []




#read in data
for in_file in args.in_files:
    print('--> reading file ' + in_file) #print out the filename we are currently processing

    line_position, line_width, g2_exist = np.loadtxt( in_file, usecols=(0, 1, 2), unpack=True)

    line_position_all.append(line_position)
    line_width_all.append(line_width)
    g2_exist_all.append(g2_exist)

    # prepare legend entries from file name
    file_parts = in_file.split('/')
    last_part = file_parts[len(file_parts)-1]
    last_part_split = last_part.split('.')
    legend_entry = last_part_split[len(last_part_split)-2] # take item before last dot

    legend_entries.append(legend_entry)








# make the histogram of the line width data

ax = plt.subplot()# Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font 

binwidth = 1 #nm
n, bins, patches = plt.hist(line_width_all, bins = np.arange(0, max(np.concatenate(line_width_all)) + binwidth, binwidth), histtype='stepfilled', stacked=True, label=legend_entries)

# prepare colors for histogram bars
coloring = plt.get_cmap(color_scale, len(patches))
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

print '--> saved figure ' + args.out_filename +'_width.png'
print '--> saved figure ' + args.out_filename +'_width.pdf'

plt.show()





# make histogram of the line position data

ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

binwidth = 1 #nm
n, bins, patches = plt.hist(line_position_all, bins = np.arange(0, max(np.concatenate(line_position_all)) + binwidth, binwidth), histtype='stepfilled', stacked=True, label=legend_entries)

# prepare colors for histogram bars
coloring = plt.get_cmap(color_scale, len(patches))
# apply color
for index, item in enumerate(patches):
    for patch in item:
        patch.set_facecolor(coloring(index))

plt.xlabel('Position (nm)', fontsize = label_fontsize)
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

print '--> saved figure ' + args.out_filename +'_position.png'
print '--> saved figure ' + args.out_filename +'_position.pdf'

plt.show()



# for item in g2_exist_all:
    # legend_entries.append("g2")

ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

# prepare colors for markers
coloring = plt.get_cmap(color_scale, len(line_position_all))

plot_list = []
# plot
for index, (line, width, g2_exist) in enumerate( zip(line_position_all, line_width_all, g2_exist_all) ):
    plot = plt.scatter(line, width, color='k', lw=1, s=20, marker='o', facecolor=coloring(index), label = legend_entries[index])
    plot_list.append(plot)

    line_position_g2 = [p for p,g in zip(line, g2_exist) if g == 1]
    line_width_g2 = [w for w,g in zip(width, g2_exist) if g == 1]

    plot = plt.scatter(line_position_g2, line_width_g2, color='k', lw=1, s=20, marker='o', facecolor="r", label = 'g2')
    plot_list.append(plot)



plt.xlabel('Position (nm)', fontsize = label_fontsize)
plt.ylabel('Width (nm)', fontsize = label_fontsize)
# plt.title('Title', fontsize = title_fontsize)
# Set the tick labels font
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')
    label.set_fontsize(tick_fontsize)

plt.tight_layout()
# legend = plt.legend(reversed(plot_list), reversed(legend_entries), prop={'size':legend_fontsize})
# legend = plt.legend(collections.OrderedSet(plot_list), collections.OrderedSet(legend_entries), prop={'size':legend_fontsize})
# legend = plt.legend(plot_list, legend_entries, prop={'size':legend_fontsize})
# legend1 = plt.legend(plot_list, legend_entries, prop={'size':legend_fontsize})
# ax = plt.gca().add_artist(legend1)
legend2 = plt.legend(prop={'size':legend_fontsize})
plt.grid(True)

plt.savefig( (args.out_filename +'_width_position.png'))
plt.savefig( (args.out_filename +'_width_position.pdf'))

print '--> saved figure ' + args.out_filename +'_width_position.png'
print '--> saved figure ' + args.out_filename +'_width_position.pdf'

plt.show()

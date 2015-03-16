#!/usr/bin/env python

""" File: line_statistics.py
	Author: Sarah Lindner
	Date of last change: 03.03.2015

	
"""


from sys import argv
import numpy as np
from matplotlib import pyplot as plt

# define appearance
color_scale = 'CMRmap'
legend_fontsize = 23
tick_fontsize = 23
label_fontsize = 23
title_fontsize = 23


# argv is your commandline arguments, argv[0] is your program name, so skip it
out_filename = argv[1]
in_files = argv[2:]

line_position_all = []
line_width_all = []

legend_entries = []




#read in data
for in_file in in_files:
    print('--> reading file ' + in_file) #print out the filename we are currently processing

    line_position, line_width = np.loadtxt( in_file, delimiter="\t", usecols=(0, 1), unpack=True)

    line_position_all.append(line_position)
    line_width_all.append(line_width)

    # prepare legend entries from file name
    file_parts = in_file.split('/')
    last_part = file_parts[len(file_parts)-1]
    last_part_split = last_part.split('.')
    legend_entry = last_part_split[len(last_part_split)-2] # take item before last dot

    legend_entries.append(legend_entry)






ax = plt.subplot()# Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font 

# the histogram of the line width data
n, bins, patches = plt.hist(line_width_all, bins = 15, histtype='stepfilled', stacked=True, label=legend_entries)

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

plt.savefig( (out_filename +'_width.png'))
plt.savefig( (out_filename +'_width.pdf'))

plt.show()





# make histogram of the line position data

ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

n, bins, patches = plt.hist(line_position_all, bins = 15, histtype='stepfilled', stacked=True, label=legend_entries)

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

plt.savefig( (out_filename +'_position.png'))
plt.savefig( (out_filename +'_position.pdf'))

plt.show()





ax = plt.subplot() # Defines ax variable by creating an empty plot; needed for tuning appearance, e.g. axis ticks font

# prepare colors for markers
coloring = plt.get_cmap(color_scale, len(line_position_all))

plot_list = []
# plot
for index, (line, width) in enumerate( zip(line_position_all, line_width_all) ):
    plot = plt.scatter(line, width, color='k', lw=1, s=20, marker='o', facecolor=coloring(index))
    plot_list.append(plot)


plt.xlabel('Position (nm)', fontsize = label_fontsize)
plt.ylabel('Width (nm)', fontsize = label_fontsize)
# plt.title('Title', fontsize = title_fontsize)
# Set the tick labels font
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')
    label.set_fontsize(tick_fontsize)

plt.tight_layout()
legend = plt.legend(plot_list, legend_entries, prop={'size':legend_fontsize})
plt.grid(True)

plt.savefig( (out_filename +'_width_position.png'))
plt.savefig( (out_filename +'_width_position.pdf'))

plt.show()

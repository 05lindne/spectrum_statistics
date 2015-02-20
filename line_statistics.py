#!/usr/bin/env python

""" File: line_statistics.py
	Author: Sarah Lindner
	Date of last change: 17.02.2015

	
"""


from sys import argv
import numpy as np
from matplotlib import pyplot as plt


# argv is your commandline arguments, argv[0] is your program name, so skip it
out_filename = argv[1]
# in_files = ['Ir8_ann.txt', 'Ir8_ann_ox.txt', 'Ir8_ann_ox_ann_ox.txt', 'Ir21_no.txt', 'Ir21_ox.txt', 'Ir21_ox_ox.txt', 'Ir9_ann.txt', 'Ir9_ann_ann_ox.txt', 'Ir20_ox.txt', 'G4_no.txt', 'mirror.txt']
in_files = argv[2:]

line_position_all = []
line_width_all = []

legend_entries = []
# my_colors = ['MediumBlue', 'Green', 'Yellow', 'Red', 'Black', 'Cyan', 'Lime', 'OrangeRed', 'MediumVioletRed', 'Grey', 'MidnightBlue', 'Olive', 'LightSalmon', 'DarkRed']

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
    legend_entry = last_part_split[len(last_part_split)-2]

    legend_entries.append(legend_entry)

ax = plt.subplot() # Defines ax variable by creating an empty plot

# the histogram of the line width data
n, bins, patches = plt.hist(line_width_all, bins = 15, histtype='stepfilled', stacked=True, label=legend_entries)

coloring = plt.get_cmap('CMRmap', len(patches))

for index, item in enumerate(patches):
    for patch in item:
        patch.set_facecolor(coloring(index))

plt.xlabel('Linewidth (nm)', fontsize = 20)
plt.ylabel('Quantity', fontsize = 20)
plt.title('Title', fontsize = 23)
# Set the tick labels font
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')
    label.set_fontsize(20)
plt.tight_layout()
plt.legend()
plt.grid(True)

plt.savefig( (out_filename +'_width.png'))
plt.savefig( (out_filename +'_width.pdf'))

plt.show()






ax = plt.subplot() # Defines ax variable by creating an empty plot
# the histogram of the line position data
n, bins, patches = plt.hist(line_position_all, bins = 15, histtype='stepfilled', stacked=True, label=legend_entries)


coloring = plt.get_cmap('CMRmap', len(patches))

for index, item in enumerate(patches):
    for patch in item:
        patch.set_facecolor(coloring(index))

plt.xlabel('Position (nm)', fontsize = 20)
plt.ylabel('Quantity', fontsize = 20)
plt.title('Title', fontsize = 23)
# Set the tick labels font
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')
    label.set_fontsize(20)
plt.tight_layout()
legend = plt.legend()
plt.grid(True)

plt.savefig( (out_filename +'_position.png'))
plt.savefig( (out_filename +'_position.pdf'))

plt.show()





ax = plt.subplot() # Defines ax variable by creating an empty plot

coloring = plt.get_cmap('CMRmap', len(line_position_all))

for index, (line, width) in enumerate( zip(line_position_all, line_width_all) ):

    plt.scatter(line, width, color='k', lw=1, s=20, marker='o', facecolor=coloring(index))


plt.xlabel('Position (nm)', fontsize = 20)
plt.ylabel('Width (nm)', fontsize = 20)
plt.title('Title', fontsize = 23)
# Set the tick labels font
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontname('Arial')
    label.set_fontsize(20)
plt.tight_layout()
plt.grid(True)

plt.savefig( (out_filename +'_width_position.png'))
plt.savefig( (out_filename +'_width_position.pdf'))

plt.show()

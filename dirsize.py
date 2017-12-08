"""
get_dirsize.py will display the total size of each main directory in the
given path sorted by size. The use case for the script is to quickly determine
which directories are consuming the most disk space. The user can then run the
script against that directory to drill down further.

The script accepts inputs like . or ..\ or ~ and works with both Windows and
MacOS.

I used the following StackOverflow thread as a starting point but made many
modifications to it:
https://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python

Author: Doron Chosnek, Cisco Systems, November 2017
"""

# pylint: disable=invalid-name

import os
import sys
import argparse

# =============================================================================
# ARGPARSE
# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Show total size of each subfolder for the specified path.')
parser.add_argument('path', help='filesystem path')
args = parser.parse_args()

# ============================================================================
# Functions
# ----------------------------------------------------------------------------

def get_children(path):
    """
    Returns the top level directories at the given path. This function is not recursive.
    The os.path.expanduser command converts path symbols like ~ in MacOS. I don't believe
    that it does anything useful in Windows environments.
    """
    d = os.path.expanduser(path)
    return [os.path.join(d, x) for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]

def get_size(path):
    """
    Returns the total size of a given directory. This function does a recursive
    walk of each subdirectory to include the size of every file.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except:
                total_size += 0
    return total_size

def progress_write(percent, width=50):
    """
    Display a progress bar with a numeric percentage readout. I got the idea from the
    following link but modified it to be a variable width that can be specified when
    calling the function.
    https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
    """
    bar_size = percent * width / 100
    sys.stdout.write('\r')
    sys.stdout.write("[%-*s] %d%%" % (width, '='*bar_size, percent))
    sys.stdout.flush()

def dict_to_table(user_dict):
    """
    This function takes a dictionary, sorts it by its value (rather than key), and
    prints it in a formatted table. This is a very specialized function that expects
    the dictionary value to be a file size in bytes. It will display the output in
    either B, KB, MB, GB, etc. based on the size of the largest entry.
    """
    # create a sorted list and grab the largest item from the list
    slist = sorted(user_dict.items(), key=lambda x: int(x[1]))
    largest = slist[-1]

    # decide if the output should be expressed in bytes, KB, MB, etc. based on
    # the size of the largest directory
    abbreviations = ['B ', 'KB', 'MB', 'GB', 'TB']
    (divisor, suffix) = (1.0, abbreviations[0])
    for (sf, dv) in [(abbreviations[i], float(1024**i)) for i in range(len(abbreviations))]:
        (suffix, divisor) = (sf, dv) if largest[1] > dv else (suffix, divisor)

    # print the list, largest items first; remove the 'reversed' function to
    # print the list in ascending order instead
    for directory in reversed(slist):
        size = float(directory[1])/divisor
        print "{:10.4f} {} {}".format(size, suffix, directory[0])
    return None

# ============================================================================
# Main
# ----------------------------------------------------------------------------

# There is an odd behavior in Windows where args.path ends with a quotation mark
# if the pathname contains a space. This line prunes that final character if it
# is detected.
repaired_path = args.path[:-1] if args.path.endswith('"') else args.path

# get the first level of directories that exist at the specified path and only
# proceed if there is at least one directory there
print ''
toplevel = get_children(repaired_path)
if len(toplevel):
    dirDict = {}
    iteration = 0
    # for each directory at the top level, determine its total size by doing a
    # recursive search using the get_size function in this script
    for longname in toplevel:
        iteration += 1
        shortname = os.path.basename(longname)
        progress_write(iteration * 100 / len(toplevel), width=60)
        dirDict[shortname] = get_size(longname)

    print '\n'
    dict_to_table(dirDict)
    print ''
else:
    print "No directories found at this path: {}".format(args.path)

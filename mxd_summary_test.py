"""
A script that takes user input of a directory containing .mxd files and calls the get_mxd module. 
Summary files for all .mxd files will be created.

Author: Chad Belisle
Date: 12/03/2018

Created in Python 2.7

"""

# import modules
import os
from mxd_summary import get_mxd


while True:
    # Take user input for a directory, validate input
    while True:   
        
        # ***Example File Path***
        # C:\user\folder1\folder2\maps
        input_directory = raw_input("Enter directory path to search for mxd files: ")
        if os.path.isdir(input_directory):    
            print 'Input directory entered: ' + input_directory 
            break
        else:
            print 'Directory path invalid'   

    # Provide warning for overwritting of previous files.
    while True:
        warning = raw_input('WARNING: Previous summary files will be overwritten \
would you like to continue? Enter "Yes" to continue or "No" to quit: ')
        if warning.lower() == 'no':
            exit()
        elif warning.lower() == 'yes': 
            print 'Great choice, one moment while the directory is searched.'
            break
        elif warning.lower() != 'no' or 'yes':
            print 'I said YES or NO...'
            

    # call get_mxd function
    get_mxd(input_directory)

    # Stop python window from closing to view results
    continuescript = raw_input('Press enter to search another directory or close the window to exit')
    
'''
A script that takes user input, searches through a directory, 
locates .mxd files that have been created using ArcGIS Map,
creates a summary report for each one. Information returned includes: title, summary, author,
date last saved, data frame and layer information including
datasource paths. Writes all information to a new summary.txt file named
same as .mxd and stored in the same location.   

Author: Chad Belisle
Date: 12/02/2018

Created in Python 2.7

'''

# import modules
import os
import arcpy
import datetime
import textwrap


def get_mxd(input_directory):
    # Create empty list to store mapfile paths
    mapfile_list = []

    # Loop through directory tree in search for .mxd files
    for root, dirs, files in os.walk(input_directory):
        for mapfile in files:
            if mapfile.lower().endswith(".mxd"):
                
                # assign mapfile name to summaryfilename variable for naming of .txt output
                summaryfilename = mapfile
                
                # Create full path and append to mapfile_list
                mapfile_list.append(os.path.join(root, mapfile))    
                
                # End script if no .mxd files are found in directory
                if len(mapfile_list) == 0:
                    print 'No .mxd files found'
                    exit()
                if len(mapfile_list) > 0:
                    print mapfile + ' summary file is being created'

                # Use each .mxd in list as arguement in arcpy.mapping.MapDocument module 
                for mapfile in mapfile_list:
                        mxd = arcpy.mapping.MapDocument(mapfile)
                
                # Assign map overview information to variables with N/A as alternative for blank fields
                if mxd.title == "":
                    title = 'N/A'
                else: 
                    title = mxd.title
                if mxd.summary == "":
                    map_description = 'N/A'
                else:
                    map_description = mxd.summary
                if mxd.author == "": 
                    author = 'N/A'
                else: 
                    author = mxd.author
                if mxd.dateSaved == "":
                    dateSaved = 'N/A'
                else:
                    dateSaved = mxd.dateSaved

                # Generate textfile summary report for each map, name same as map and store in same
                # location as .mxd file               
                summary = open(mapfile.strip('.mxd') + '.summary.txt', 'w')
                summary_date = datetime.date.today()

                # Write map overview section to summary.txt
                summary.write('Summary for: ' + '"' + summaryfilename + '"\n')
                summary.write('Created On: ' + str(summary_date) + '\n\n')
                summary.write('\n')
                summary.write('Map Title: ' + title + '\n')
                summary.write('File Path: ' + mapfile + '\n')
                summary.write('Description: ' + textwrap.fill(map_description, width=70) + '\n')
                summary.write('Author: ' + author + '\n')
                summary.write('Date Last Saved: ' + str(dateSaved) + '\n')
                summary.write('\n')

                # List dataframes using arcpy.mapping.ListDataFrames for .mxd file
                dataframes = arcpy.mapping.ListDataFrames(mxd)
                for dataframe in dataframes:
                    if dataframe.name == "":
                        dataframename = 'N/A'
                    else: 
                        dataframename = dataframe.name

                        # Write data frame information to open summary.txt
                        summary.write('\n[Dataframe: ' + dataframename + ']' + '\n')
                        summary.write('\n')

                        # List layers using arcpy.mapping.ListLayers for .mxd file
                        layers = arcpy.mapping.ListLayers(mxd, "", dataframe)   
                        for layer in layers:
                            
                            # Will crash for uncompatiable layer types without try statement 
                            try:
                                summary.write('Layername: ' + layer.datasetName + '\n')                           
                            except:
                                summary.write('Layername: ' + 'N/A' + '\n')
                            
                            # Compile broken data source list
                            broken_source_list = arcpy.mapping.ListBrokenDataSources(mxd)
                            
                            # Assign layer information to variables with N/A as alternative for blank fields
                            if layer.supports('dataSource'):
                                if layer in broken_source_list:
                                    layerdatasource = '*Data source NOT found, link is broken*'
                                else:
                                    layerdatasource = layer.dataSource
                            if layer.description == "":
                                layerdescription = "N/A"
                            else:
                                layerdescription = layer.description
                        
                            # Try statement to avoid crash if dataset type uncompatiable
                            try:
                                summary.write('Layer Data Type: ' + arcpy.Describe(layer.dataSource).datasettype + "\n")
                            except:
                                summary.write('Layer Data Type: Unknown \n')    
                            summary.write('Layer File Path: ' + layerdatasource + '\n')
                            summary.write('Layer Description: ' + textwrap.fill(layerdescription, width=70) + '\n')
                            summary.write('\n')

                # Close each summary 
                summary.close()    

    # Tell user whether directory was not found or the process is complete
    if len(mapfile_list) == 0:
        print 'There were no .mxd files found in the directory'
    else:
        print 'Summary text files have been created and are stored in .mxd locations.' 

if __name__ == '__main__':
    
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

    while True:
        warning = raw_input('WARNING: Previous summary files will be overwritten if \
they have not been renamed. Would you like to continue? Enter "Yes" to continue or "No" to quit: ')
        if warning.lower() == 'no':
            print 'Script will now exit'
            exit()
        elif warning.lower() == 'yes': 
            print 'Great choice, one moment while the directory is searched'
            break
        elif warning.lower() != 'no' or 'yes':
            print 'I said YES or NO...'

    get_mxd(input_directory)


   
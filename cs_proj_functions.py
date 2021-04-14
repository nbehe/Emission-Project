#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS 5010 Project

"Global Warning"

Nima Beheshti (nb9pp)
Jess Cheu (jc4vg)
Ben Feciura (bmf3bw)
Gary Mitchell (gm3gq)

FUNCTIONS
This portion of the project contains the functions we have written to be
reusable throughout the other portions of the project. These are related
to subsetting data and producing visualizations.

"""

import pandas as pd
import matplotlib.pyplot as plt

### Ask user before exporting results of query to CSV
def ExportCSV(dataframe):
    export = input("Do you want to export to CSV? [Y/N] ")
    if export.upper() == 'Y':
        filename = input("Provide filename: ")
        dataframe.pd.to_csv(filename)
    else:
        return 

### Subset for range of year
def subset_by_year(dataFrame, start_year, stop_year = None):
    # If this argument is None, set it to be the same as the start year
    if stop_year == None:
        stop_year = start_year
    # Then subset appropriately
    subset = dataFrame[(dataFrame['Year'] >= start_year) & (dataFrame['Year'] <= stop_year)]
    # Reset the indices.
    subset.reset_index(inplace = True, drop = True)
    return subset

### Subset for given country
def subset_by_entity(dataFrame, entities):
    # If only a single entity is given, put it into a list with length 1.
    if type(entities) == str:
        entities = [entities]
    # Subset the data appropriately using .isin()
    subset = dataFrame[(dataFrame['Entity'].isin(entities))]
    # Reset the indices.
    subset.reset_index(inplace = True, drop = True)
    return subset

### (3) Line plot of data over time

def line_plot(data, country_filter, start_year = 1751, stop_year = 2017, max_emissions = 7e9, fn = None):
    # Set up the figure and axes.
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    # Plot the data for each country passed into the function
    for country in country_filter:
        frame = data[data['Entity'] == country]
        plt.plot(frame['Year'], frame['Emissions'], label = frame['Entity'].iloc[0])
    # Set the lengths of the axes appropriately (Default to maximum domain x of
    # dataset and large enough range y to fit all emissions values in the data)
    plt.xlim(start_year, stop_year)
    plt.ylim(0, max_emissions)
    # Add labels
    plt.xlabel('Year')
    plt.ylabel('Emissions')
    plt.title('Emissions over Time')
    # Mark axes
    ax.set_xticks(range(start_year, stop_year, 3))
    ax.set_xticklabels(range(start_year, stop_year, 3))
    # Add legend
    plt.legend(loc=2, prop={'size': 7})
    
    # If the user provided a filename, save the file and notify them.
    if fn != None:
        plt.savefig(fn)
        print("Exported line plot to {}".format(fn))
    
    # Show the visual
    plt.show()
    return

def pie_chart(dataFrame, year, size_limit = 25, countries = None, fn = None):
    # In case the user passed in a dF with more than one year, subset to one
    # specified year
    subset = subset_by_year(dataFrame, year)
    # We want to show the values in descending order to put the largest
    # slices first (Excluding "other")
    subset.sort_values(by = ['Emissions'], ascending = False, inplace = True)
    # Fix the indices so the dF remains iterable
    subset.reset_index(inplace = True, drop = True)
    labels = []
    slices = []
    other = 0
    # If the user didn't provide a list of countries, take the specified number
    # for size limit
    if countries == None:
        for i in range(size_limit):
            # Add names to list with emissions values
            labels.append(subset['Entity'][i])
            slices.append(subset['Emissions'][i])
        for i in range(size_limit, len(subset['Entity'])):
            # Add all others to "other"
            other += subset['Emissions'][i]
    # Otherwise use the provided countries
    else:
        for i in range(len(subset['Entity'])):
            # If the country is in the user-specified list, add its name and
            # emissions
            if subset["Entity"][i] in countries:
                labels.append(subset['Entity'][i])
                slices.append(subset['Emissions'][i])
            # otherwise, add it into "other"
            else:
                other += subset['Emissions'][i]
                
    # Add other to the bottom of the lists so its slice comes last
    slices.append(other)
    labels.append('Other')

    # Set up the chart type
    fig, ax = plt.subplots()
    # Format the percentages shown
    ax.pie(slices, labels=labels, autopct='%.4f', startangle=90, radius = 3)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Set the size to be large enough to be legible and add a title
    fig = plt.gcf()
    fig.set_size_inches(12,12)
    fig.suptitle("Percentage of Global Emissions by Country in {}".format(year))
   
    # If the user provided a filename, save it and notify them
    if fn != None:
        plt.savefig(fn)
        print("Exported pie chart to {}".format(fn))
   
    plt.show()
    
    
# Provides some contextual information for a given entity and year's emissions
def entityemissionsforyear(entity, year, dataFrame):
    emissionsforsubset = subset_by_year(subset_by_entity(dataFrame, entity), int(year))["Emissions"]
    print("----")
    print("The total C02 emissions is: " + str(float(emissionsforsubset.values)) + " metric tons." + "\nIt will take " + str(round(float(emissionsforsubset.values/.3),1)) + " years for an individual removing all single use plastic (approximately 50 kg plastic/year/person) to equal " + entity + " CO2 emissions in " + str(year) + ". This is equal to " + str(round(float(emissionsforsubset.values/98400000),1)) + " years of the entire population of the US (328.2 million) removing single use plastic.")
    print("----")
    print("It will take " + str(round(float(emissionsforsubset.values/3.15648),1)) + " years for an individual using non emissions transmitting methods to travel to and from work (approximately 32 miles round trip, 5 days a week for 48 weeks) to equal " + entity + " CO2 emissions in " + str(year) + ". This is equal to " + str(round(float(emissionsforsubset.values/1035325440),1)) + " years of the entire population of the US using non emissions transmitting methods to travel to and from work.")    
    print("----")
    print("It will take " + str(round(float(emissionsforsubset.values/0.155129),1)) + " years for an individual showering 2 minutes fewer every shower to equal " + entity + " CO2 emissions in " + str(year) + ". This is equal to " + str(round(float(emissionsforsubset.values/50882312),1)) + " years of the entire population of the US showering 2 minutes fewer every shower.")
    print("----")   

    
    
    
    
    
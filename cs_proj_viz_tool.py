#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS 5010 Project

"Global Warning"

Nima Beheshti (nb9pp)
Jess Cheu (jc4vg)
Ben Feciura (bmf3bw)
Gary Mitchell (gm3gq)

VISUALIZATION TOOL
This portion of the project allows the user to select what types of queries to
perform on the data (by country and year) and produce appropriate
visualizations.

"""

from cs_proj_functions import *
import pandas as pd

print("|| Global Warning Visualization Tool ||")
print("CS 5010 Semester Project | Fall 2020")
print("Authors:")
print("Nima Beheshti (nb9pp)")
print("Jess Cheu (jc4vg)")
print("Ben Feciura (bmf3bw)")
print("Gary Mitchell (gm3gq)")
print()

# Ask until the user provides a valid filename
while True:
    try:
        fn = input("Please provide a filename for the dataset: ")
        full_data = pd.read_csv(fn, )
        break
    except:
        print("File not found!")
# Notify the user
print("Loaded {0}\n".format(fn))

# Global variables
data = full_data # Copy of full dataset
country_filter = ["All"] # List of countries (default value ["All"])
start_year = -1 # First year of range in filter (default value -1)
stop_year = -1 # Last year of range in filter (default value -1)
entries = len(data) # Number of entries in subset (initialize on full dataset)

# Print out the current state of the subset and the menu options.
def print_menu():
    print("\n{0} observations found.\n".format(entries))
    print("--Filters--")
    print("Countries:")
    print(*country_filter, sep = ", ")
    print("Years:")
    # Print all if the start year is at the default value
    if start_year == -1:
        print("All")
    # Only print 1 year if stop_year is the same as start_year
    elif start_year == stop_year:
        print(start_year)
    # Otherwise, format the sentence nicely
    else:
        print("{0} to {1}".format(start_year, stop_year))
    print("\n[1] Filter by Country")
    print("[2] Filter by Year")
    print("[3] Clear Filters")
    print("[4] Produce Visualization")
    print("[5] Export Data")
    print("[6] Learn about emissions in context")
    print("")
    print("[0] Quit")    

# Takes a country or several countries by which to filter the data.
def filter_country():
    global data
    global country_filter
    # Only run this syntax if the list is the default value; if so, 
    # replace with a blank list and take input for the first country.
    # This ensures that "all" doesn't remain in the list and that later
    # operations relying on the length of the list work correctly even with
    # a single entry.
    if country_filter == ["All"]:
        country_filter = []
        country = input("Enter first country: ")
        country_filter.append(country)
    # Continue to ask for additional countries using the other syntax until 
    # the user enters DONE
    while True:
        print("\nIncluded Countries:")
        print(*country_filter, sep = ", ")
        country = input("Enter another country (or if finished, enter DONE): ")
        if country == "DONE":
            break
        else:
            country_filter.append(country)
    # subset data appropriately; we want to ensure that we always filter the
    # full dataset when we add a new country, since no entries for the new
    # country would exist in a previous subset.
    data = subset_by_entity(full_data, country_filter)
    # Because of this, if there was a filter on the year already, we need to
    # apply it again.
    if start_year != -1:
        data = subset_by_year(data, start_year, stop_year)
    
# Takes a year or range of years by which to filter the data
def filter_year():
    global data
    global start_year
    global stop_year
    # Ask if the user wants to input a single year or a range.
    print("[1] Single Year")
    print("[2] Range of Years")
    selection = int(input("Please make a selection: "))
    if selection == 1:
        start_year = int(input("Enter year: "))
        # set the stop year the same as the start year (this will be used in
        # later checks to determine if the filter is for a single year)
        stop_year = start_year
    elif selection == 2:
        start_year = int(input("Enter first year: "))
        stop_year = int(input("Enter last year: "))
    else:
        print("Invalid Selection.")
        return
    # Subset the data appropriately. Similarly to before, we need to use
    # the full dataset.
    data = subset_by_year(full_data, start_year, stop_year)
    # So we also reapply the country filter if there is one.
    if country_filter != ["All"]:
        data = subset_by_entity(data, country_filter)

# Resets filters
def clear_filters():
    global full_data
    global data
    global country_filter
    global year_filter
    global start_year
    global stop_year
    print("Reset which filters?")
    print("[1] Countries")
    print("[2] Years")
    print("[3] All")
    selection = int(input("Please make a selection: "))
    if selection == 1:
        # If the user only wants to reset the country filter, we reset
        # it to the default value and replace data with the appropriate
        # dataset...
        country_filter = ["All"]
        # ... if there was no year filter, we just use the full data...
        if start_year == -1:
            data = full_data
        # ... and if there was, we re-filter by year.
        else:
            data = subset_by_year(full_data, start_year, stop_year)
    elif selection == 2:
        # If the user wants to reset only the years, replace with the default
        # values.
        start_year = -1
        stop_year = -1
        # If no country filter, replace with full data.
        if country_filter == ["All"]:
            data = full_data
        # Else, filter by countries again.
        else:
            data = subset_by_entity(data, country_filter)
    elif selection == 3:
        # If user wants to clear everything, reset default values and replace
        # data with the full data.
        country_filter = ["All"]
        start_year = -1
        stop_year = -1
        data = full_data
    else:
        print("Invalid selection.")

def produce_visualization(data, country_filter, start_year, stop_year):
    print("Which type of visualization?")
    print("[1] Pie Chart (Compare contributions of selected countries to")
    print("    total global emissions for selected year)")
    print("[2] Line Graph (Compare selected countries' emissions over")
    print("    selected range of years)")
    print()
    selection = int(input("Please make a selection: "))
    if selection == 1:
        # Pie charts support many countries but a single year.
        size_limit = 0
        # If all countries are in the list, have the user choose a number
        # to show (and the rest will be grouped into "other"; else, the
        # graph will be impossible to read.)
        if country_filter == ["All"]:
            countries = None
            size_limit = int(input("Show __ largest contributors: "))
        # Otherwise, use the countries they've selected
        else:
            countries = country_filter
        # If no year is specified, get the user to specify one.
        if start_year == -1:
            year = int(input("Please specify a year: "))
        # If a range of years is selected, have the user pick one within their
        # selected range
        elif start_year != stop_year:
            print("Multiple years selected.")
            year = int(input("Please choose a year between {0} and {1}: ".format(start_year, stop_year)))
        else:
            year = start_year
        # Ask if the user wants to save the visualization to a file.
        save = input("Export visualization? [Y/N] ")
        if save == "Y" or "y":
            fn = input("Provide filename: ")
        else:
            fn = None
        # If the size limit is 0, the function will take the subset of countries
        # to use. Otherwise, the subset value will be used.
        # We always need to pass the full dataset as the pie chart compares
        # against world totals.
        pie_chart(full_data, year, size_limit, countries, fn)
    if selection == 2:
        # Line chart supports many countries over many years. If at least
        # a subset is not taken, ask the user to filter.
        if country_filter == ["All"]:
            print("Please filter by a subset of countries first.")
            return
        # Ask if the user wants to save the graph to a file.
        save = input("Export visualization? [Y/N] ")
        if save.upper() == "Y":
            fn = input("Provide filename: ")
        else:
            fn = None
        line_plot(data, country_filter, data['Year'].min(), data['Year'].max(), data['Emissions'].max(), fn)
    return
    
# Export the filtered data to a new CSV.
def export_subset(data):
    fn = input("Name of output file: ")
    data.to_csv(fn, index = False)
    print("Exported {0}".format(fn))
    
    
def in_context():
    # Requires a single country and year to be selected. If the criteria
    # are not met, prompt the user to filter accordingly.
    if country_filter == ["All"]:
        print("Please filter by a single country and year.")
        return
    if len(country_filter) != 1:
        print("Please filter by a single country and year.")
        return
    if start_year == -1:
        print("Please filter by a single country and year.")
        return
    if stop_year != start_year:
        print("Please filter by a single country and year.")
        return
    
    entityemissionsforyear(country_filter[0], start_year, data)
    
  
while True:
    print_menu()
    selection = int(input("Please make a selection: "))
    # Filter by country
    if selection == 1:
        filter_country()
        # Whenever we change the dataset, we reset entries to show the right
        # number.
        entries = len(data)
        continue
    # Filter by year
    elif selection == 2:
        filter_year()
        # Reset entries
        entries = len(data)
    # Reset Filters
    elif selection == 3:
        clear_filters()
        entries = len(data)
    # Produce visualization
    elif selection == 4:
        produce_visualization(data, country_filter, start_year, stop_year)
    # Export subsetted data
    elif selection == 5:
        export_subset(data)
    # View information about context
    elif selection == 6:
        in_context()
    # Quit
    elif selection == 0:
        break
    else:
        print("Invalid selection.")

# Thank the user!
print("Thank you for using our visualization utility!")
        
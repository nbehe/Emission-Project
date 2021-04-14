#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS 5010 Project

"Global Warning"

Nima Beheshti (nb9pp)
Jess Cheu (jc4vg)
Ben Feciura (bmf3bw)
Gary Mitchell (gm3gq)

PROCESSING and ANALYSIS
This portion of the project includes our data preprocessing, cleaning, feature
engineering, queries, visualization, and storage.

Please note some functions used in querying and visualization are moved into
the module cs_proj_functions to improve readability of our analysis, simplify
unit testing, and for use in the visualization tool portion.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math as m
from cs_proj_functions import *

'''
DATA CLEANING
'''
# Read raw data
data = pd.read_csv("co2_emission.csv")

# Rename the terribly named C02 Emissions Column.
data.rename(columns = {"Annual CO₂ emissions (tonnes )": "Emissions"}, inplace = True)
print(data.head())

# Get summary statistics for our dataset
print("\nSummary Statistics:\n")
print(data.describe())

# We see that there are negative values for emission... find out why.
print("\nNegative Emissions Values:\n")
print(data[data["Emissions"] < 0].head())

# We see that there are some entities in the dataset that are not countries,
# like "statistical differences".

# Ideally, for most of our analyses we would like to make comparisons between
# countries, so these other entities shouldn't be included in the same dataset
# (though could be useful in other queries).

# Get and print a list of all the Entities in the dataset to find other non-
# countries
country_names = []

for countries in data["Entity"]:
    if countries not in country_names:
        country_names.append(countries)

print("\nAll Entities:\n")        
print(country_names)
        
# List entities from that list which we want to exclude (continents, special
# categories, negative emission value, etc.)
entities_to_exclude = ['Africa', 'Americas (other)', 'Antarctic Fisheries', 'Asia and Pacific (other)', 'Christmas Island', 'Czechoslovakia', 'EU-28', 'Europe (other)', 'Gibraltar', 'Greenland', 'International transport', 'Kyrgyzstan', 'Lesotho', 'Middle East', 'New Caledonia', 'Reunion', 'Sint Maarteen', 'Statistical Differences','Statistical differences', 'World', 'Wallis and Futuna Islands']

# And subset the dataset so as to exclude those
data_countries = data[~data["Entity"].isin(entities_to_exclude)]
data_countries.reset_index(inplace = True, drop = True)

# This cleaned version of our data is what we will use for much of our
# analysis. We will not, however, export it yet as we would like to engineer
# a few additional features to use in our queries.

# Additionally, we do can make use of a few of the entities we excluded, and can
# create separate dataframes for them (and export them appropriately).

# Subset the data to show only global data
#world = data[data['Entity'] == 'World'].reset_index(drop = True)
world = subset_by_entity(data, "World")

# Subsbet to show only emissions from international transport
trans = data[data['Entity'] == 'International transport'].reset_index(drop = True)

# Likewise, we can add a few features to these, so won't export yet.

#-----------------------------------------------------------------------------

'''
FEATURE ENGINEERING
'''

# We want to add a column that calculates the year over year change for each country.
# We'll make a list to store this info in and turn into a column; the first entry
# will be 0 because there is no prior year to compare to.
yearly_change = [0]

for i in range(1, len(data_countries['Entity'])):
    # If we find the country name changes, it's the first entry for that 
    # country so the percent change should be 0.
    if data_countries['Entity'][i] != data_countries['Entity'][i-1]:
        yearly_change.append(0)
        continue
    # Otherwise, find percent change.
    else:
        difference = data_countries['Emissions'][i] - data_countries['Emissions'][i-1]
        # If the previous value was 0, avoid divide by 0 error
        if data_countries['Emissions'][i-1] == 0:
            # If the current value is nonzero, make sure the percentage change
            # ends up being 100 by setting denominator = numerator
            if data_countries['Emissions'][i] != 0:
                denominator = data_countries['Emissions'][i]
            # Otherwise ensure percentage change is 0 by calculating 0/1
            else:
                denominator = 1
        else:
            denominator = data_countries['Emissions'][i-1]
            
        pct_change = (difference*100) / denominator
    
        yearly_change.append(pct_change)
        
# Create a column to add to our cleaned data
data_countries['YoY_Pct_Change'] = pd.Series(yearly_change)

# We'll do the same thing for World and International Transport (simpler since
# there's only one entity in each of these dataframes).
yearly_change = [0]

for i in range(1, len(world['Entity'])):
   
    # Calculate percent change
    difference = world['Emissions'][i] - world['Emissions'][i-1]
    # If the previous value was 0, avoid divide by 0 error
    if world['Emissions'][i-1] == 0:
    # If the current value is nonzero, make sure the percentage change
    # ends up being 100 by setting denominator = numerator
        if world['Emissions'][i] != 0:
            denominator = world['Emissions'][i]
        # Otherwise ensure percentage change is 0 by calculating 0/1
        else:
            denominator = 1
    else:
        denominator = world['Emissions'][i-1]
        
    pct_change = (difference*100) / denominator

    yearly_change.append(pct_change)

# Create a column to add to our cleaned data
world['YoY_Pct_Change'] = pd.Series(yearly_change)

yearly_change = [0]

for i in range(1, len(trans['Entity'])):
   
    # Calculate percent change
    difference = trans['Emissions'][i] - trans['Emissions'][i-1]
    # If the previous value was 0, avoid divide by 0 error
    if trans['Emissions'][i-1] == 0:
    # If the current value is nonzero, make sure the percentage change
    # ends up being 100 by setting denominator = numerator
        if trans['Emissions'][i] != 0:
            denominator = trans['Emissions'][i]
        # Otherwise ensure percentage change is 0 by calculating 0/1
        else:
            denominator = 1
    else:
        denominator = trans['Emissions'][i-1]
        
    pct_change = (difference*100) / denominator

    yearly_change.append(pct_change)

# Create a column to add to our cleaned data
trans['YoY_Pct_Change'] = pd.Series(yearly_change)


# Additionally, for the countries dataset we can add a column that shows each
# country's contribution as a percentage of the global emissions for that year.
percent_of_global = [] #empty list for percent of global emissions for the year by every country

for i in range(len(data_countries['Year'])):
    year = data_countries['Year'][i]
    global_amt = world[world['Year'] == year]['Emissions'].iloc[0]
    pctCountry = data_countries['Emissions'][i]/global_amt*100   #I don't think I have the original dataset - global emissions already removed 
    percent_of_global.append(pctCountry)
    
data_countries['Pct_Global'] = pd.Series(percent_of_global)

# And we can export our cleaned datasets.
data_countries.to_csv("data_cleaned.csv", index = False)
world.to_csv("world.csv", index = False)
trans.to_csv("transport.csv", index = False)


#-----------------------------------------------------------------------------
'''
SUBSETTING
'''
# In our examination of the dataset, we see that many years from long before
# the industrialized era are included, which are relevant for context but
# which skew our observations.

# We decided to subset the data to only show years greater than or equal to 
# the mean year for all countries as we felt this would ensure nearly all included
# countries had data available for all years, as another option for inclusion
# in our analysis.
data_modern = subset_by_year(data_countries, m.ceil(data_countries['Year'].mean()), data_countries['Year'].max())
data_modern.reset_index(inplace = True, drop = True)
print("\nSummary for {0} onward:\n".format(m.ceil(data_countries['Year'].mean())))
print(data_modern.describe())
data_modern.to_csv("modern.csv", index = False)

#-----------------------------------------------------------------------------
'''
QUERIES and AGGREGATES
'''
# We can perform our queries and take a look at a few aggregates now; looking
# at aggregates is particularly instructive for an individual country or year, 
# to look at their average contribution over time, the total contribution over
# time, the total among all countries within a year, etc.


# Greatest periods of increase: when did a country's emissions more than double
# from the previous year?
doubles = data_countries[data_countries['YoY_Pct_Change'] >= 100]
print("\nInstances of >2x Year-over-year increase in emissions:\n")
print(doubles.head())
doubles['Year'].value_counts()
# We see that 1950 had 26 different entities more than double from the previous
# year. We can look at which countries
print(doubles[doubles['Year'] == 1950])
# Wonder if particular world events correspond to these increases, or if
# this was just a rapid period of industrialization. Postwar economy?


# On a more optimistic note, when did a country's emissions decrease?
reduced = data_countries[data_countries['YoY_Pct_Change'] < 0]
print("\nInstances where countries cut their emissions:\n")
len(reduced)
# Almost 5000 entries! We can do a similar search to see when most decreases 
# happened; I would guess in the 21st century thanks to climate agreements?
reduced['Year'].value_counts()
# Interesting results. Half of the world's countries saw a decrease in 2009.
# Would be interesting to look into world events that relate to other dates
# in this list.


# Any carbon-zero years in the modern era?
no_carbon = data_modern[(data_modern['Emissions'] == 0)]
print("\nModern isntances of carbon-zero years?:\n")
print(no_carbon.head())
print("{0} instances of carbon-zero years.".format(len(no_carbon['Entity'])))
print(no_carbon['Entity'].unique())
# These seem like countries that just for some reason or another were not
# reporting at this time, since it's only two and they're sequential years...
# So, seemingly, no.


### Check percentage of global emission contributed by International Transport
transport = []
for i in trans['Emissions']:
    transport.append(i)
world_total = []
for i in world['Emissions']:
    world_total.append(i)
t = np.array(transport, dtype=np.float)
wt = np.array(world_total, dtype=np.float)

Percentage_of_total_emissions_from_international_transport = 100*(t/wt)
trans['% of world emissions'] = Percentage_of_total_emissions_from_international_transport
print(trans)


### Emission statistics by continent
continents_filter = data.Entity.isin(['Africa', 'Americas (other)','Asia and Pacific (other)','Europe (other)','Australia','Antarctic Fisheries'])
print(data[continents_filter])


# Query to see how long it would take for individuals to combat US CO2 emissiosn in 2017, 2010, and 1950
print(entityemissionsforyear("United States",2017, data_countries))
print(entityemissionsforyear("United States",2010, data_countries))
print(entityemissionsforyear("United States",1950, data_countries))

# Query to see how long it would take for individuals to combat world CO2 emissiosn in 2017, 2010, and 1950
print(entityemissionsforyear("World",2017,world))
print(entityemissionsforyear("World",2010,world))
print(entityemissionsforyear("World",1950,world))


# Obtain world emissions data for the last 50 years
worldlast50 = subset_by_year(world, world['Year'].max() - 50, world['Year'].max())
last50years = worldlast50["Year"]
totalemissionslast50 = worldlast50["Emissions"]
np.polyfit(np.log(last50years), totalemissionslast50, 1)
# array([ 8.74994891e+11, -6.62363734e+12])
# estimated equation: y = 8.74994891e+11*log(x) - 6.62363734e+12
# "Safe limit" possibly 100 - 500 billion metric tons of CO2/year
# What is the estimated year we hit 100 billion metric tons of CO2 emissions 
totalemissions = 100e9
estimatedyear = np.exp((totalemissions + 6.62363734e+12)/8.74994891e+11)
print(round(estimatedyear,0))

#-----------------------------------------------------------------------------

'''
VISUALIZATION
'''

### Pie chart based on 2017 emission quantities
    
pie_chart(data_countries, 2017, size_limit = 25, fn = "2017global")

### Line plot of global emission over time
world = data[(data['Entity'] == 'World')]
world.plot(x = 'Year',y='Emissions')


### Plot of change during Great Depression and WWII
### Find years where global emissions fell over 20% to determine year range for graph 
years_decrease = []
for i in range(1,len(data_countries['Year'])):
    year = data_countries['Year'][i]
    year_last = data_countries['Year'][i-1]
    if world[world['Year'] == year]['Emissions'].iloc[0] < 0.8*world[world['Year'] == year_last]['Emissions'].iloc[0]:
        years_decrease.append(year)

years_decrease.sort()
years_decrease = list(dict.fromkeys(years_decrease))
#print(years_decrease)

### global emissions from 1927 to 1948
### search highest emissions for 1927
highemission_1927 = data_countries[data_countries['Year'] == 1927]
highemission_1927 = highemission_1927.sort_values(by=['Pct_Global'])
#print(highemission_1927.head())
#print(highemission_1927.tail())

### create data frame for top 5 energy producers during time frame and global emissions
### United States, Germany, UK, France, Canada, and global emissions
def countrydf(countryName):
    countrydf = data_countries.loc[data_countries['Entity'] == countryName]
    return countrydf

UnitedStatesdf = countrydf('United States')
UnitedKingdomdf = countrydf('United Kingdom')
Germanydf = countrydf('Germany')
Francedf = countrydf('France')
Canadadf = countrydf('Canada')

### Create dataframe of all countries and world from 1927-1947
def countrydfyr(dataframe):
    new_data = []
    for year in range(1927,1948):
        data = dataframe.loc[dataframe['Year'] == year]
        new_data.append(data)
        final = pd.concat(new_data)
    return final
    
US = countrydfyr(UnitedStatesdf)
UK = countrydfyr(UnitedKingdomdf)
Germany = countrydfyr(Germanydf)
France = countrydfyr(Francedf)
Canada = countrydfyr(Canadadf)
World = countrydfyr(world)
dflst = [US, UK, Germany, France, Canada, World]
years_decrease_df = pd.concat(dflst)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
for frame in [US, UK, Germany, France, Canada, World]:
    plt.plot(frame['Year'], frame['Emissions'], label = frame['Entity'].iloc[0])
    
plt.xlim(1927,1947)
plt.ylim(0,6e9)
plt.xlabel('Year')
plt.ylabel('Emissions')
plt.title('Emissions over the Years')
ax.set_xticks(range(1927,1948,3))
ax.set_xticklabels(range(1927,1948,3))
plt.legend(loc=2, prop={'size': 7})
plt.show()

### Graph total emissions per continent over time

Africa = data[continents_filter].loc[data['Entity'] == 'Africa']
Americas = data[continents_filter].loc[data['Entity'] == 'Americas (other)']
Asia = data[continents_filter].loc[data['Entity'] == 'Asia and Pacific (other)']
Europe = data[continents_filter].loc[data['Entity'] == 'Europe (other)']
Australia = data[continents_filter].loc[data['Entity'] == 'Australia']
Antarctic = data[continents_filter].loc[data['Entity'] == 'Antarctic Fisheries']
cntlst = [Africa, Americas, Asia, Europe, Australia, Antarctic]
cntlst = pd.concat(cntlst)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
for framee in [Africa, Americas, Asia, Europe, Australia, Antarctic]:
    plt.plot(framee['Year'], framee['Emissions'], label = framee['Entity'].iloc[0])
    
plt.xlim(1940,2017)
plt.xlabel('Year')
plt.ylabel('Emissions')
plt.title('Continental Emissions over the Years')
ax.set_xticks(range(1940,2017,10))
ax.set_xticklabels(range(1940,2017,10))
plt.legend(loc=2, prop={'size': 7})
plt.show()


### Change during a selection of significant world events

# Syria during Civil War 2011-2017
# Significant decrease in emissions
syria_df = subset_by_year(subset_by_entity(data, 'Syria'), 2000,2017)
print(syria_df)
syria_df.plot.line(x = 'Year', y = 'Emissions')

# Lebanon during civil war 1975-1990
# No noticable changes to slope
lebanon_df = subset_by_year(subset_by_entity(data, 'Lebanon'), 1970,2017)
print(lebanon_df)
lebanon_df.plot.line(x = 'Year', y = 'Emissions')

# Global internet age 2000-2017
# No significant changes to slope
transport_df = subset_by_year(subset_by_entity(data, 'International transport'), 1980,2017)
print(transport_df)
transport_df.plot.line(x = 'Year', y = 'Emissions')

# North Korea
# Decrease in emissios during the past 30 years
nkorea_df = subset_by_year(subset_by_entity(data, 'North Korea'), 1980, 2017)
print(nkorea_df)
nkorea_df.plot.line(x = 'Year', y = 'Emissions')




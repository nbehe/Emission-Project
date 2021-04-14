#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS 5010 Project

"Global Warning"

Nima Beheshti (nb9pp)
Jess Cheu (jc4vg)
Ben Feciura (bmf3bw)
Gary Mitchell (gm3gq)

UNIT TESTING
This portion of the project contains the unit testing we performed on the
functions we wrote to ensure they were subsetting and querying the data
appropriately.

"""

import unittest
from cs_proj_functions import *
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal
from numpy.testing import assert_array_equal

# Sample data import and cleaning
data = pd.read_csv("co2_emission.csv")
data.rename(columns = {"Annual CO₂ emissions (tonnes )": "Emissions"}, inplace = True)
countries_to_exclude = ['Africa', 'Americas (other)', 'Antarctic Fisheries', 'Asia and Pacific (other)', 'Christmas Island', 'Czechoslovakia', 'EU-28', 'Europe (other)', 'Gibraltar', 'Greenland', 'International transport', 'Kyrgyzstan', 'Lesotho', 'Middle East', 'New Caledonia', 'Reunion', 'Sint Maarteen', 'Statistical Differences','Statistical differences', 'World', 'Wallis and Futuna Islands']
exclude = []
for entity in data["Entity"]:
    if entity in countries_to_exclude:
        exclude.append(True)
    else:
        exclude.append(False)
data["Exclude"] = pd.Series(exclude)
data_countries = data[(data["Exclude"]) == False]
data_countries.drop(columns = ['Exclude'], inplace = True)
data_countries.reset_index(inplace = True, drop = True)


class SubsetYearTestCase(unittest.TestCase):
    
    def test_is_subset_year_handling_single_year(self):
        # Use the function on a single year
        sampledf = subset_by_year(data_countries, 2005)
        # Get all the values for year in the result using .unique()
        years_included = sampledf['Year'].unique()
        # Test
        self.assertEqual(years_included, [2005])
        
    def test_does_year_not_in_df_return_None(self):
        # create incidence of a dataframe
        dataFrame = pd.DataFrame(
            {
                "Name": ["Bob","Clark","Janet","Dora","Katherine"],
                "Year": [1999,2000,2001,2002,2003],
                "Number": [1,2,3,4,5]    
                }
            )
        # does a year not in the dataframe return empty dataframe
        # using assertEqual()
        subset = subset_by_year(dataFrame, 2021)
        
        ### Note - assert statement for arrays not built in to unittest
        # Use a numpy assert statement to test results
        assert_array_equal(subset["Year"].unique(),np.array([], dtype=int))   
        # Should return:
        # Empty DataFrame
        # Columns: [Name,Year,Number]
        # Index: [])
        
    def test_does_only_start_year_return_df(self):
        # create incidence of a dataframe
        dataFrame = pd.DataFrame(
            {
                "Name": ["Bob","Clark","Janet","Dora","Katherine"],
                "Year": [1999,2000,2001,2002,2003],
                "Number": [1,2,3,4,5]    
                }
            )
        # does a year not in the dataframe return empty dataframe
        ### Note - assert statement for arrays not built in to unittest
        # Use a numpy assert statement to test results.
        assert_frame_equal(subset_by_year(dataFrame, 2000).reset_index(drop = True),pd.DataFrame(
            {
                "Name": ["Clark"],
                "Year": [2000],
                "Number": [2]
                }
            ))       
  
    def test_subset_by_year_method(self):
        # Create a subset to represent the expected result using build in pandas
        # methods
        subset_test = data_countries[(data_countries['Year'] >= 1970) & (data_countries['Year'] <= 1990)]
        # Use the subset by year method
        subset_actual = subset_by_year(data_countries,1970,1990)
        # Compare the results
        n = len(subset_test['Year'])
        self.assertEqual(subset_test['Year'].iloc[0],subset_actual['Year'].iloc[0])
        self.assertEqual(subset_test['Year'].iloc[n-1],subset_actual['Year'].iloc[n-1])
        
    def test_subset_by_year(self):
        # Try nesting the functions for a range of years.
        test1 = subset_by_year(subset_by_entity(data_countries ,'Syria'), 1970, 2000)
        # Create a sample list of the years we expect to find.
        years = []
        for i in range(1970, 2001):
            years.append(i)
        
        ### Note - assert statement for arrays not built in to unittest
        # Use a numpy assert statement to test results.
        assert_array_equal(test1['Year'].unique(), np.array(years))
    
class SubsetEntityTestCase(unittest.TestCase):
    
    def test_is_subset_entity_working(self):
        # Use the subset function
        sampledf = subset_by_entity(data_countries, 'Ecuador')
        # Get a list of all included entities using .unique()
        entities_included = sampledf['Entity'].unique()
        # Test
        self.assertEqual(entities_included, ['Ecuador'])
        
    def test_subset_by_entity_method(self):
        # Ue built in pandas methods
        subset_test_entity = data_countries[(data_countries['Entity'] == 'North Korea')]
        # Use function
        subset_actual_entity = subset_by_entity(data_countries,'North Korea')
        # Test
        self.assertEqual(subset_test_entity['Entity'].iloc[0],subset_actual_entity['Entity'].iloc[0])
    
    def test_by_entity(self):
        # Use the function
        test2 = subset_by_entity(data_countries, 'Syria')
        # Compare the unique entities in the result to an array with the only
        # expected value in it.
        self.assertEqual(test2['Entity'].unique(), np.array(['Syria']))
    
if __name__ == '__main__':
    unittest.main()            
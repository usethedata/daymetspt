#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:57:34 2020

@author: Bruce Wilson
"""

# This file is intended as a module for making calls to the Daymet Single Pixel Tool
# 

# Define some global variables
URL = 'https://daymet.ornl.gov/single-pixel/api/data'
SKIPROWS = 7   # Number of rows to skip at the top of the response
DATA_CITATION = 'Thornton; P.E.; M.M. Thornton; B.W. Mayer; Y. Wei; R. Devarakonda; R.S. Vose; and R.B. Cook. 2016. Daymet: Daily Surface Weather Data on a 1-km Grid for North America; Version 3. ORNL DAAC; Oak Ridge; Tennessee; USA. http://dx.doi.org/10.3334/ORNLDAAC/1328'
import io
import requests
import pandas

def version():
    return "04"

def get_data(loc):
    """
    Calls the Daymet single pixel tool to return the a dataframe of the data at a specified location:
        loc: a Tuple with the latitude and longitude
        Returns: a Pandas dataframe with the resulting data
    """
    
    # Do error checking.  Latitude must be between -90 and +90.  Longitude must be between -180 and +180.  
    # Note, however, that Daymet at this point only has data for North America, Hawaii, and Puerto Rico, 
    # so the restriction could be tighter.  We will let the single pixel tool handle that issue.  
    assert (loc[0] >= -90 and loc[0] <= 90), "Latitude must be a number between -90 and +90"
    assert (loc[1] >= -180 and loc[1] <= 180), "Longitude must be a number between -180 and +180"

    
    # The SPT takes four arguments (parameters), of which two, lat and lon are required.  
    # The other three are the variables to be returned and the date range (start/stop).
    # See https://daymet.ornl.gov/web_services for details.  For now, just populate 
    # the lat and lon
    params = {'lat':loc[0], 'lon':loc[1]}
    
    # call the SPT to get the data
    response = requests.get(URL, params)
    if response.status_code != 200:
        print('Call to Single Pixel Tool failed, status='+str(response.status_code))
        exit(1)
    
    print('     debug: SPT data at lat=%3.3f and lon=%3.3f retrieved' % (loc[0],loc[1]) )
    
    text_str = str(response.content,'utf-8')
    response.close
    mydata = io.StringIO(text_str)
    df = pandas.read_csv(mydata, skiprows=SKIPROWS)
    
    return df
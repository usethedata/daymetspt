#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:57:34 2020

@author: Bruce Wilson
"""

# Set a parameter to determine if debug features/restrictins are turned on.
DEBUG = 0

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

def citation():
    return DATA_CITATION

def get_data(loc):
    """
    Get Daymet data from the Daymet Single Pixel Extraction Tool for a location.
    
    The SPET provides a REST Web service that returns a CSV with multiple header rows 
    containing the Daymet data for the pixel that contains the specified coordinates 
    (latituded and longitude)
    
    Parameters
    ----------
        loc: Dictionary 
            Dictionary with information about the location, including lat and lon elements
            
    Returns
    -------
        df: DataFrame
            a Pandas DataFrame with the resulting data
    """
    
    # Do error checking.  Latitude must be between -90 and +90.  Longitude must be between -180 and +180.  
    # Note, however, that Daymet at this point only has data for North America, Hawaii, and Puerto Rico, 
    # so the restriction could be tighter.  We will let the single pixel tool handle that issue.  
    assert (loc['lat'] >= -90 and loc['lat'] <= 90), "Latitude must be a number between -90 and +90"
    assert (loc['lon'] >= -180 and loc['lon'] <= 180), "Longitude must be a number between -180 and +180"

    # The SPT takes the following parameters (see https://daymet.ornl.gov/web_services for more details)
    #    lat (required) -- the latitude of the pixel to be returned
    #    lon (required) -- the longitude of the pixel to be returned
    #    vars -- a text filed containing a comma separated list of variables to be returned (defaults to all)
    #    years -- a text field containing a list of years to return (defaults to all)
    #    start -- Start date in yyyy-mm-dd format (1980-01-01 or later)
    #    end -- End date in (yyyy-mm-dd) format (curretly 2019-12-31 or earlier)

    params = {'lat':loc['lat'], 'lon':loc['lon']}
    if (DEBUG > 0) :
        params['years'] = "2017,2018,2019"
    
    # call the SPT to get the data
    response = requests.get(URL, params)
    if (DEBUG > 0) : 
        print('     debug: SPT data at lat=%3.3f and lon=%3.3f retrieved' % (loc[0],loc[1]) )
        print('        elapsed time (sec): ' + str(response.elapsed.seconds))
    
    if response.status_code != 200:
        print('*****Call to Single Pixel Tool failed, status='+response.status_code)
        exit(1)
    
    # Simpler way to do this than the previous version.  StackOverflow isn't always perfect
    mydata = io.StringIO(response.text)
    response.close
    
    df = pandas.read_csv(mydata, skiprows=SKIPROWS)
    
    # We know that the year, yday, and day length variables are all integers, so 
    # coerce those in the dataframe to make later things easier.
    df = df.astype({'year':'int64','yday':'int64','dayl (s)':'int64'})
    
    return df

def get_data_daterange(loc,yday,ydaywindow):
    """
    Get Daymet data from the Single Pixel Extraction Tool for a lcoation for a range of dates each year.
    
    The concept is that a user wants to know the historical range of weather conditions for a given location
    for a given period of time each year, such as for planning a vacation.  The SPET provides a start date and
    stop date option, but will then return all data between those two days.  This routine takes a julian day of
    year and a window size, so that (for example) asking for day 25 with a window of 5 will return just the
    data for days 20 through 30 for each year that Daymet data is available.  
    
    Parameters
    ----------
    loc: Dictionary
        Dictionary with information about the location, including lat and lon elements
    yday: int
        Julian day of year [1,365] that is at the center of the range of desired dates
    ydaywindow: int
        Number of days [0,182] on either side of yday to include in the results
        
    Returns
    -------
    df: DataFrame
        a Pandas DataFrame with the resulting data
    """
    
    # As an implementation issue, it would be possible to make multiple calls to the SPET
    # and then stitch the results together.  I choose to implement this instead by getting
    # all of the data and slicing out just what's needed.
    
    # Validate inputs
    #   Assume get_data will sanitize loc
    my_yday = int(yday)
    assert ((my_yday >= 1) and (my_yday <=365)), "Yday must be within the range of 1 to 365"
    my_ydaywindow = int(ydaywindow)
    assert ( (my_ydaywindow >= 0) and (my_ydaywindow <=182)), "Yday window must be within the range of 0 to 182"

    # get the data from the SPET
    df = get_data(loc)
    
    # Compute the range of yeardays desired, taking into account that they must be between 1 and 365.
    # We've already sanitized the inputs, so I know that the overall range will be < 365 days.  If
    # ydaymin comes out less than zero, then add 365 to it, which puts it at the end of the (previous)
    # year.  Likewise if ydaymax > 365, then subtract 365 to get the data from the start of the next year.
    ydaymin = my_yday - my_ydaywindow
    ydaymax = my_yday + my_ydaywindow
    if (ydaymin < 1) : 
        ydaymin += 365
        
    if (ydaymax > 365):
        ydaymax -= 365
        
    # Now slice out the data that we're after. The logic is slightly different if we're spanning years.
    # If we're entirely within a given year, then ydaymin will be less than ydaymax.  If we're spanning years,
    # then ydaymax will be less than ydaymin.  If we're within a single year, then we want the intersection.
    # Otherwise, we want the union set.
    if (ydaymin <= ydaymax):
        df = df[ (df.yday >=ydaymin) & (df.yday <= ydaymax) ]
    else:
        df = df[(df.yday >= ydaymin) | (df.yday <= ydaymax) ]
    
    return df
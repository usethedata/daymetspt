# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:57:34 2020

@author: Bruce Wilson
"""

# This is a the main execution program for the code to display the climate conditions at a single location
import daymet_05 as daymet
import pandas


# A way to look at this problem is that I need to first get a location (where do we want the data),
# then I need the date range for which we want the data. Then get the data we want, the plot out the data.
# So, stub out the subroutines needed, then have a main section that actually calls those routines.

# for this version of the routine, I will hard code this to the location of FPC.
def get_location():
    print('&&&&& TODO: get_location function still needs to be finished')
    return (35.884,-84.162)
    
    #end: get_location()
    
def get_date_range():
    print('&&&&& TODO: get_date_range still needs to be defined')
    
    # for the moment, pick a window for a week in the middle of summer
    return {'yday': 183, 'ydaywindow':4}
    # end: get_date_range()
    
def get_weather_data(loc,daterange):
    
    df = daymet.get_data_daterange(loc, daterange['yday'], daterange['ydaywindow'])
    print('&&&&& TODO: get_weather_data still needs to be finished')
    
    return df
    #end: get_weather_data()
    
def plot_weather_data(df):
    print('&&&&& TODO: plot_weather_data still needs to be defined')
    
    # end: plot_weather_data

# ----------------------------------------------------
# Main routine
    
myloc = get_location()
mydates = get_date_range()
df = get_weather_data(myloc, mydates)
print('  debug: got dataframe with %i rows and %i columns' % df.shape)

plot_weather_data(df)


    



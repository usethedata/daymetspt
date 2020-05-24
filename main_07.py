# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:57:34 2020

@author: Bruce Wilson
"""

# This is a the main execution program for the code to display the climate conditions at a single location
import daymet_07 as daymet
import pandas
import matplotlib.pyplot as plt


# A way to look at this problem is that I need to first get a location (where do we want the data),
# then I need the date range for which we want the data. Then get the data we want, the plot out the data.
# So, stub out the subroutines needed, then have a main section that actually calls those routines.


def get_location():
    """
    Present the user with a list of locations and let them choose one, returning the lat, lon, and title
    
    In the current implementation, the user is presented with a list of known locations, and is
    asked to choose one.
    
    Parameters
    ----------
        none
        
    Returns
    -------
        loc: Dictionary
            A Dictionary containing information about the location, including the latitude (lat), 
            longitude (lon), and description (desc)
    """

    # Here is a list of known locations, which I manually gelocated using Google Maps (click What's here)
    # Save pattern for row {'lat': , 'lon': , 'desc': ''}
    known_locations = [
        {'lat': 35.884, 'lon':  -84.162, 'desc': 'Farragut Presbyterian Church (Farragut, TN)'},
        {'lat': 35.779, 'lon':  -84.683, 'desc': 'Camp Buck Toms (Rockwood, TN)'},
        {'lat': 39.054, 'lon':  -86.430, 'desc': 'Ransburg Reservation (Bloomington, IN)'},
        {'lat': 36.465, 'lon': -104.944, 'desc': 'Philmont Base Camp (Cimmaron, NM)'},
        {'lat': 36.635, 'lon': -105.215, 'desc': 'Philmont Mount Baldy (Eagle Nest, NM)'},
        {'lat': 24.859, 'lon':  -80.732, 'desc': 'Sea Base (Islamorada, FL)'},
        {'lat': 47.989, 'lon':  -91.492, 'desc': 'Northern Tier Base (Ely, MN)'}
        ]
    
    # print out the list of known locations along with a selection number.  People
    # are happier counting from 1, so I'll need to adjust this when using the selection
    # number to go back into the array.  
    icnt = 1
    for loc in known_locations:
        print('(%i): %s' % (icnt, loc['desc']) )
        icnt += 1
    
    # Now ask the user to choose.  I'm going to let them keep trying until they get one
    # that's actually in the allowable range
    mychoice = 0
    while mychoice == 0:
        resp = input('Type the number of the location where you want to see the data: ')
        iresp = int(resp)           # convert to an integer
        if ( iresp > 0 and iresp <= len(known_locations) ):   
            mychoice = iresp
        else:
            print('Sorry, please choose one of the numbers above.')
            
    return known_locations[mychoice-1]  # Because Python numbers arrays from zero
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
    
def plot_weather_data(df, loc):
    # Reference: https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.html#module-matplotlib.pyplot
    print('&&&&& TODO: plot_weather_data still needs to be defined')
    
    plt.plot('year','tmin (deg c)', data=df, marker='2', ms=3, mfc='blue', ls='')
    plt.plot('year','tmax (deg c)', data=df, marker='1', ms=3, mfc='red', ls='')
    plt.legend()
    plt.title('Min and Max Temp for ' + loc['desc'])
    # end: plot_weather_data

# ----------------------------------------------------
# Main routine
    
myloc = get_location()
mydates = get_date_range()
df = get_weather_data(myloc, mydates)

plot_weather_data(df, myloc)


    



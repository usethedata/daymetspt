# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:57:34 2020

@author: Bruce Wilson
"""

# This is a the main execution program for the code to display the climate conditions at a single location
import daymet_08 as daymet
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
    known_locations = [
        {'lat': 35.884, 'lon':  -84.162, 'desc': 'Farragut Presbyterian Church', 'city': 'Farragut', 'state': 'TN'},
        {'lat': 35.779, 'lon':  -84.683, 'desc': 'Camp Buck Toms', 'city': 'Rockwood', 'state': 'TN'},
        {'lat': 39.054, 'lon':  -86.430, 'desc': 'Ransburg Reservation', 'city': 'Bloomington', 'state': 'IN'},
        {'lat': 36.465, 'lon': -104.944, 'desc': 'Philmont Base Camp', 'city': 'Cimmaron', 'state': 'NM'},
        {'lat': 36.635, 'lon': -105.215, 'desc': 'Mount Baldy', 'city': 'Eagle Nest', 'state': 'NM'},
        {'lat': 24.859, 'lon':  -80.732, 'desc': 'Sea Base', 'city': 'Islamorada', 'state': 'FL'},
        {'lat': 47.989, 'lon':  -91.492, 'desc': 'Northern Tier Base', 'city': 'Ely', 'state': 'MN'},
        {'lat': 37.916, 'lon':  -81.123, 'desc': 'Summit Bechtel Reserve', 'city': 'Glen Jean', 'state': 'WV'}
        ]
    
    # print out the list of known locations along with a selection number.  People
    # are happier counting from 1, so I'll need to adjust this when using the selection
    # number to go back into the array.  
    icnt = 1
    for loc in known_locations:
        print('(%i): %s (%s,%s)' % (icnt, loc['desc'],loc['city'],loc['state']) )
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
    """
    Prompt user for the month, day of month, and number of days either side
    
    Determines the day of year for a month and day provided by the user and also gets
    the date window width for the daymet calls
    
    Returns
    -------
    dates: Dictionary
        A Dictionary containing the month, day of month, day of year, and the date window 
        width (number of days on either side of the selected day for which data is desired)
    """
    
    # There are multiple ways of computing day of year, and note that Daymet always has 365 days (ignores dec 31 for leap years)
    # This is straightforward.  Use 
    # len(month_lengths)  
    # sum(month_lengths) 
    # as two checks that I got this array right
    month_lengths= (31,28,31,30,31,30,31,31,30,31,30,31)
    month_names = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    
    imonth = 0
    while (imonth == 0):
        month_resp = input('Enter the month number (between 1 and 12): ')
        imonth_resp = int(month_resp)
        if (imonth_resp >= 1 and imonth_resp <= 12):
            imonth = imonth_resp
        else:
            print('Sorry.  Month needs to be between 1 and 12.  Try again.')

    iday = 0
    while (iday == 0):
        day_resp = input('Enter the day of month (between 1 and ' + str(month_lengths[imonth-1]) + '): ')
        iday_resp = int(day_resp)
        if (iday_resp >= 1 and iday_resp <= month_lengths[imonth-1]):
            iday = iday_resp
        else:
            print('Sorry. The day of the month needs to be between 1 and %i' % (month_lengths[imonth-1]))
    
    iwindow = -1
    while (iwindow < 0):
        window_resp = input('Enter the number of days on either side of the day (between 0 and 182): ')
        iwindow_resp = int(window_resp)
        if (iwindow_resp >= 0 and iwindow_resp <= 182):
            iwindow = iwindow_resp
        else:
            print('Sorry.  The number of days has to be between 0 and 182')
    
    # Now compute the day of year for the selected day
    yday = iday
    if imonth > 1:
        for i1 in range(0, imonth-1):
            yday += month_lengths[i1]
        
    # Build the dictionary that has the information needed
    dates = {
        'yday': yday,
        'ydaywindow': iwindow,
        'month_num': imonth,
        'dayofmonth': iday,
        'month_name': month_names[imonth-1]
        }            
    
    print('The computed day of year for %s %i is %i' % (dates['month_name'],dates['dayofmonth'],dates['yday']) )
    # for the moment, pick a window for a week in the middle of summer
    return dates
    # end: get_date_range()
    
def get_weather_data(loc,dates):
    
    df = daymet.get_data_daterange(loc, dates['yday'], dates['ydaywindow'])
    
    return df
    #end: get_weather_data()
    
def plot_weather_data(df, loc, dates):
    # Reference: https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.html#module-matplotlib.pyplot
    
    plt.plot('year','tmin (deg c)', data=df, marker='2', ms=3, mfc='blue', ls='')
    plt.plot('year','tmax (deg c)', data=df, marker='1', ms=3, mfc='red', ls='')
    plt.ylabel('Temperature (deg C)')
    plt.xlabel('Year')
    plt.title('Tmin and Tmax for ' + loc['desc'] +  ' ' + dates['month_name'] + ' ' + 
              str(dates['dayofmonth']) + '+/-' + str(dates['ydaywindow']) + 'd')
    # end: plot_weather_data

# ----------------------------------------------------
# Main routine
    
myloc = get_location()
mydates = get_date_range()
df = get_weather_data(myloc, mydates)

plot_weather_data(df, myloc, mydates)


    



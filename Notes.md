Notes for Historica Weather Work for T444 Programming MB
========================================================

# Overall objective

The objective for this work is to develop a Python program that will display a graph of the typical weather conditions for a period of time at a specified location.  This is an example for the work for the Troop 444 work on Programming Merit badge.

As an example, consider the use case of wanting to know what range of temperature to expect if you were at Camp Buck Toms for the first week in June.  Let's go a bit further and ask how those temperatures compare to the temperatures at Philmont Base Camp, Mount Baldy in Philmont, Sea Base, and Northern Tier High Adventure Base.  

# Before you start notes

## Spyder

I prefer to have lines wrap.  Go into Spyder | Python menu | Preference | Editor.  Check "wrap lines"

I created a new Spyder project for this (Projects Menu).

## Python and Ananconda

The standard base environment in Anaconda has everything needed.  I didn't have to install anything extra.

I would normally not do what I did here, which is to name things main_01, main_02, .... I would normally use a version tracking tool, like git (e.g. GitHub.com).  However, working with git is beyond what we are doing, and the different versions of the files is how I'm showing the progression of building this up from scratch.

## Getting the lat/lon coordinates for locations

There are a couple of different ways to do this.  For this exercise, I decided to go with a pre-defined list of locations, with the user choosing from that pre-defined list.  That makes error checking a whole lot easier.

There is an XKCD comic that is about [getting geolocation](https://xkcd.com/2170/).  It is also relevant to the whole discussion of *signficant figures*.  

There are a lot of different ways to get lat/lon coordinates for a location.  One is on [mapdevelopers.com](https://www.mapdevelopers.com/geocode_tool.php).  Another way is to use Google Maps and get the pin where you want it, then right click on "What's here".

## Historical weather data

This project is making use of a data product that my group produces, called Daymet (see [daymet.ornl.gov](https://daymet.ornl.gov)).  In particular, we are using a web service that taps into the [Daily Surface Weather Data on a 1 km Grid for North America](https://doi.org/10.3334/ORNLDAAC/1328) dataset.  This provides daily values (1980-2019) for the minimum and maximum temperature, the amount of precipitation, day length, something relatid to humidity, and a measure of the solar energy available.  Daymet was developed by one of my colleagues (Peter Thornton), for doing ecological models, and we continue to update it annually.

We are specifically using what's called the Single Pixel Extraction Tool (SPET). SPET has a Graphical User Interface (GUI) that is available at [daymet.ornl.gov/single-pixel](https://daymet.ornl.gov/single-pixel/).  It also has what's called an Application Programming Interface (API) available at `https://daymet.ornl.gov/single-pixel/api/data`  People access a tool using a GUI.  Computer programs access a tool using an API.  In this particular case, the API is what is called a **Web Service**, which means that it's an API that's designed to be called over the Internet.  Python has a built-in module called `requests` which is designed for getting data from web services.  Rather than having to download all of Daymet (nearly a terabyte), we call this web service to get the data for the 1km by 1km pixel that contains our location of interest.

# Building the program

## Baby Steps -- version 01

I'm separating the code to work with getting Daymet data into a separate module -- the first version of which is `daymet_01.py`.  I've defined a function `get_data`.  This doesn't actually do anything -- it just prints out a message saying what it would do.  This is an example of what's called **stubbbing** out a piece of code.  I'm just building a framework, and I'll add in pieces as I go.

So, version 01 doesn't actually do anything useful.  It just tells you what needs to be done to build out the program.

Note that the coordinates are for Farragut Presbyterian Church, which I got using Google Maps, as described above.

## Still Baby Steps -- version 02

In version 01, I started the Daymet module. In version 02, I'm thinking a bit more about what the program itself will need to do.  I need to get a location, then get the date range, then get the weather data for that location and time, then make a plot of that weather data.

So, all I've done here is to stub out those four functions that I'm going to need to build out.  Note that `&&&&&` is a convention I adopted a long time ago.  That series of five ampersands (and character), means that there's something still to be done.  I can search through all of the files in a directory and find all of those todos. In this case, I'm also adding "TODO:" after that, which is a bit of overkill, but there are tools that are designed to look specifically for "TODO:" as well, so both sets of tools will work.

## A Bit Further -- version 03

In this versino, I started to add some functinality to these stubs in main.  In particular, my `get_location` function now works, as long as the answer you want is the location for FPC.  The `get_weather_data` function now imports the Daymet module and calls the `get_data` function within that module (which still doesn't do anything).

## Actually Getting Some Data -- verison 04

In this version, I've built out the get_data function into something that actually calls the Daymet web service.  There are actually a lot of changes.  

Notice at the top of `daymet_04` that I've defined some variables in all caps.  This is a convention for a constant.  The idea here is that I define these at the top of the file, even if I only use them once elsewhere in the file.  If, for some reason, the URL for the Daymet web service were to change, I know that I can just go to the top of the file, change it it in one place, and that's all I have to worry about.  

Also note that I've now imported three modules:  `io`, `pandas`, and `requests`.  As mentioned above, `requests` makes it easy to call a web service.  `pandas` is something often used in data science.  I want it because it makes parsing comma separated values (which is what the Daymet SPET service returns) pretty easy.  It also has something called a `DataFrame`, which bascially a python equivalent of a spreadsheet.

My `get_data` routine just takes a location, as what Python calls a `Tuple`. The main thing to know is that `loc[0]` should have the latitude and `loc[1]` should have the longitude.  I've done some basic error checking here, to make sure that the location is at least somewhere on earth.  I should probably have added a TODO to indicate that I should really check that the point is in North America -- since that's all that Daymet covers, but I didn't get to the error checking to make sure that the Daymet service actually returned data.  It will fail if the user asks for a point that's not in North America.  It will also fail for points that Daymet thinks are water -- it's a "land surface" data product.  

After checking the location, I put those into the parameters that will be sent to the web service, then call the routine that does all of the hard work.  

A web service will return a status code of `200` if it worked correctly, so I check for that.  If I got anything else, then I basically print an error message and quit.  

The next block is an incantation that processes the csv string of text that I got back from the web service.  I got this by doing a search for something like `pandas dataframe parse csv from web service`.  That got me to the documentation that said I needed to convert what I got back from the web service to a Python string variable.  I then needed this `io.StringIO` function to make that string look like a file, then call `pandas.read_csv`.  I did some playing around with what I got back from the web service and figured out that I needed to skip the first 7 lines, which contain some extra information:

```
Latitude: 35.5  Longitude: -85.3
X & Y on Lambert Conformal Conic: 1276601.34 -630704.95
Tile: 11208
Elevation: 243 meters
All years; all variables; Daymet Software Version 3.0; Daymet Data Version 3.0.
How to cite: Thornton; P.E.; M.M. Thornton; B.W. Mayer; Y. Wei; R. Devarakonda; R.S. Vose; and R.B. Cook. 2016. Daymet: Daily Surface Weather Data on a 1-km Grid for North America; Version 3. ORNL DAAC; Oak Ridge; Tennessee; USA. http://dx.doi.org/10.3334/ORNLDAAC/1328 

year,yday,dayl (s),prcp (mm/day),srad (W/m^2),swe (kg/m^2),tmax (deg c),tmin (deg c),vp (Pa)
1980.0,1.0,34905.6015625,1.0,198.39999389648438,0.0,7.0,0.0,600.0
1980.0,2.0,34905.6015625,0.0,297.6000061035156,0.0,9.0,-5.5,400.0
```

So, now I have the data.  But, it's all of the data for 1980 - 2019.  I just want a bit of data, like for a particular day with a specific number of days before and after.

## Filtering To the Desired Timeframe -- version 05
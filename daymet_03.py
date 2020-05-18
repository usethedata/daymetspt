#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:57:34 2020

@author: Bruce Wilson
"""

# This file is intended as a module for making calls to the Daymet Single Pixel Tool
# 

def version():
    return "03"

def get_data(loc):
    """
    Calls the Daymet single pixel tool to return the data at a specified location:
        loc: a Tuple with the latitude and longitude
    """
    print('&&&&& TODL: This would get data at lat=%3.3f and lon=%3.3f' % (loc[0],loc[1]) )
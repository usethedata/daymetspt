# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:57:34 2020

@author: Bruce Wilson
"""

# This is a the main execution program for the code to display the climate conditions at a single location

import daymet_01 as daymet

print('Current Daymet module version is %s' % daymet.version())

daymet.get_data(35.8835,-84.1624)


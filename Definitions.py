from math import *

#Row definitions
rowIndex = {'Time':0, 'Roll':1, 'Pitch':2, 'Yaw':3, 'Altitude':4}

#Definition of text options
#Each one contains a lambda expression to return a correctly format string
textOpt = {'Altitude Meter': lambda data, f: "Alt: {:.0f}m".format(data['Altitude'][f]),
           'Altitude Feet': lambda data, f: "Alt: {:.0f}ft".format(data['Altitude'][f]/.3048),
           'Roll Pitch Yaw Degrees': lambda data, f: "R: {:.0f}, P: {:.0f}, Y: {:.0f}".format(degrees(data['Roll'][f]),
                                                                                              degrees(data['Pitch'][f]),
                                                                                              degrees(data['Yaw'][f])),
           'Roll Pitch Yaw Radians': lambda data, f: "R: {:.0f}, P: {:.0f}, Y: {:.0f}".format(data['Roll'][f],
                                                                                              data['Pitch'][f],
                                                                                              data['Yaw'][f]),
           'Time Seconds': lambda data, f: "Time: {:.1f}s".format(data['Time'][f]/1000)
           }

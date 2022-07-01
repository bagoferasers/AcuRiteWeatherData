#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 05:33:32 2022
@author: colbybailey
Import statements.
"""
import pandas as pd
import matplotlib.pyplot as plt

#%%
"""
@author: colbybailey
Set value of b to True to print out plots as png files under ../../plots
"""
b = False

#%%
"""
@author: colbybailey
Read data into a dataframe using a list of header column names.
"""
col_list = [ "Sensor Name", "Sensor Type", "Timestamp", "Temperature ( F )", "Humidity ( RH )",
             "Dew Point ( F )",	"Heat Index ( F )",	"Feels Like ( F )",	"Wind Chill ( F )",	
             "Barometric Pressure ( INHG )", "Accumulated Rain ( IN )", "Wind Speed ( MPH )",	
             "Wind Average ( MPH )"	, "Wind Direction",	"Wired Sensor Temperature", "Wired Sensor Humidity", 
             "Soil & Liquid Temperature", "Water Detected", "UV Index", "Light Intensity", 
             "Measured Light", "Lightning Strike Count", "Lightning Closest Strike Distance" ]
df = pd.read_csv( "Data/June2022.csv", usecols = col_list )

#%%
""" 
author: colbybailey
Merge function to be used by mergeSort function.
:param sortListA: one of the two non-decreasingly sorted list of numbers.
:param sortListB: one of the two non-decreasingly sorted list of numbers.
:returns: the merged list.
"""
def merge (sortListA, sortListB ):
    """Given two non-decreasingly sorted list of numbers, 
       return a single merged list in non-decreasing order
    """
    # declare and initialize variables
    i = j = k = 0
    mergedList = sortListA + sortListB
    sizeA = len( sortListA )
    sizeB = len( sortListB )
    # merge & sort elements
    while ( i < sizeA and j < sizeB ):
        if ( sortListA[ i ] <= sortListB[ j ] ):
            mergedList[ k ] = sortListA[ i ]
            i += 1
            k += 1
        else:
            mergedList[ k ] = sortListB[ j ]
            j += 1
            k += 1
    # sort remaining elements
    while ( i < sizeA ):
        mergedList[ k ] = sortListA[ i ]
        k += 1
        i += 1
    while ( j < sizeB ):
        mergedList[ k ] = sortListB[ j ]
        k += 1
        j += 1
    return mergedList
#%%
"""
@author: colbybailey
mergeSort function that uses merge function.
:param numList: list of numbers in random order.
:returns: the list of numbers sorted low to high.
"""
def mergeSort( numList ):
    """
    Given a list of numbers in random order, 
    return a new list sorted in non-decreasing order, 
    and leave the original list unchanged.
    """
    if len( numList ) <= 1:
        return numList
    mid = len( numList ) // 2
    left = numList[ :mid ]
    right = numList[ mid: ]
    left = mergeSort( left )
    right = mergeSort( right )
    sortedList = merge( left, right )
    return sortedList
#%%
"""
@author: colbybailey
Plot all temperature data on line graph.
"""
plt.plot(df[ "Temperature ( F )" ], 'r-' )
plt.title( "Temperatures" )
plt.ylabel( "°F", rotation = 0  )
plt.xlabel( "# of inputs" )
plt.legend( [ 'Temperature' ] )
if( b == True ):
    plt.savefig('plots/temperatureAll.png')
plt.show( )

#%%
"""
@author = colbybailey
Find out how many days need to be checked for temperatures, loop through all dates and find 
the highest temperatures per day as well as the lowest, plot each highest & lowest temperature on a scatter plot. Merge sort
highest & lowest temperatures to find the correct ones for current data set.
"""
# declare and initialize variables
tf = False
count = 0
datesParsed = [ ]
iVal = 0
jVal = 0
dates = [ ]
highest = [ ]
lowest = [ ]
h = 0
l = 200
d = 0
# count number of days and add them to datesParsed[]
for i in df[ "Timestamp" ]:
    dateSplit = i.split( )
    dates.append( dateSplit[ 0 ] )
    if datesParsed == [ ]:
        datesParsed.append( dateSplit[ 0 ] )
        count += 1
    else:
        for j in datesParsed:
            if dateSplit[ 0 ] == j:
                tf = True
        if tf == False:
            datesParsed.append( dateSplit[ 0 ] )
            count += 1
    tf = False
final = [ dates, df[ "Temperature ( F )" ] ]
#loop all dates and find highest and lowest temperatures
for i in final[ 0 ]:
    # if i matches date d to check
    if i == datesParsed[ d ]:
        #loop through all temperatures for each date to find highest and lowest
        if final[ 1 ][ jVal ] > h:
            h = final[ 1 ][ jVal ]
        if final[ 1 ][ jVal ] < l:
            l = final[ 1 ][ jVal ]
    else:
        #increment date to check
        d += 1
        #store highest and lowest value
        highest.append( h )
        lowest.append( l )
        h = 0
        l = 200
    jVal += 1
# append last value
highest.append( h )
lowest.append( l )
# merge sort highest temps to find highest and lowest for set of data
high = mergeSort(highest)
low = mergeSort(lowest)
print( "Highest temperature for current data set = %.2f" % high[ len( high ) - 1 ] )
print( "Lowest temperature for current data set = %.2f" % low[ 0 ] )
# plot highest daily temperature data
plt.scatter( datesParsed, highest, c = "red" ) 
plt.plot( datesParsed, highest, c = "red", alpha = 0.4 )
plt.title( "Highest Daily Temperatures" )
plt.ylabel( "°F", rotation = 0 )
plt.xticks( datesParsed, rotation = 90 )
plt.legend( [ 'Temperature' ] )
if( b == True ):
    plt.savefig('plots/highestTemperatures.png')
plt.show( )

#%%
'''
@author = colbybailey
Plotting lowest daily temperatures
'''
plt.scatter( datesParsed, lowest, c = "blue" )
plt.plot( datesParsed, lowest, c = "blue", alpha = 0.4 )
plt.title( "Lowest Daily Temperatures" )
plt.ylabel( "°F", rotation = 0 )
plt.xticks( datesParsed, rotation = 90 )
plt.legend( [ 'Temperature' ] )
if( b == True ):
    plt.savefig('plots/lowestTemperatures.png')
plt.show( )
#%%
'''
@author = colbybailey
Plotting rain for current data set per day accumulation.
'''
'''
# declare and initialize variables
rain = df[ "Accumulated Rain ( IN )" ]
rainCurrent = 0
iVal = 0
rainParsed = [ ]
d = 0
finalRain = [ dates, "Accumulated Rain ( IN )" ]
# loop through date stamps and add up rain per day and add to rainParsed[ ]
for i in finalRain[ 0 ]:
    if i == datesParsed[ d ]:
        if iVal > 1:
            if df[ "Accumulated Rain ( IN )"][ iVal -1 ] != df[ "Accumulated Rain ( IN )" ][ iVal ]:
                rainCurrent += df[ "Accumulated Rain ( IN )" ][ iVal ]
    else:
        rainParsed.append( rainCurrent )
        d += 1
        rainCurrent = 0
    iVal += 1
# append last value
rainParsed.append( rainCurrent )
# loop through rainParsed and normalize any extremes to 10 inches
rainNormalized = [ ]
totalRain = 0
for i in rainParsed:
    if i > 10:
        i = 10
    totalRain += i
    rainNormalized.append( i )
print( "Total Rain Accumulation for current data set = %.2f" % totalRain )
# plot rain accumulation per day
plt.bar( datesParsed, rainNormalized )
plt.xticks( datesParsed, rotation = 90 )
plt.title( "Rain Accumulation ( Normalized values at 10 )" )
plt.ylabel( "Inches" )
plt.legend( [ 'Rain' ] )
if( b == True ):
    plt.savefig('plots/rainAccumulation.png')
plt.show( )
'''
#%%
'''
@author = colbybailey
avg wind speed vs highest wind speeds for days
'''
windSpeed = [ dates, df[ "Wind Speed ( MPH )" ] ]
jVal = 0
d = 0
count = 0
h = 0
averageWindSpeeds = [ ]
highestWindSpeeds = [ ]
highWind = [ ]
totalForAverage = 0
for i in windSpeed[ 0 ]:
    # if i matches date d to check
    if i == datesParsed[ d ]:
        #loop through all temperatures for each date to find highest and add total for avg
        if windSpeed[ 1 ][ jVal ] > h:
            h = windSpeed[ 1 ][ jVal ]
        totalForAverage += windSpeed[ 1 ][ jVal ]
        count += 1
    else:
        #increment date to check
        d += 1
        #store highest and average value
        #print(h)
        highestWindSpeeds.append( h )
        totalForAverage = totalForAverage / count
        averageWindSpeeds.append( totalForAverage )
        h = 0
        count = 0
        totalForAverage = 0
    jVal += 1
highestWindSpeeds.append( h )    
averageWindSpeeds.append( totalForAverage/287 )
highWind = mergeSort(highestWindSpeeds)

#print(highWind)
print( "Highest wind speed for current data set = %.2f" % highWind[ len( highWind ) - 1 ] )
plt.scatter( datesParsed, averageWindSpeeds, c = "green" )
plt.plot( datesParsed, averageWindSpeeds, c = "green", alpha = 0.4, label = "Average Wind Speeds" )
plt.scatter( datesParsed, highestWindSpeeds, c = "orange" )
plt.plot( datesParsed, highestWindSpeeds, c = "orange", alpha = 0.4, label = "Highest Wind Speeds" )
plt.title( "Daily Wind Speeds" )
plt.ylabel( "MPH" )
plt.ylim([0,highWind[len( highWind ) - 1 ] + 1] )
plt.xticks( datesParsed, rotation = 90 )
plt.legend( )
if( b == True ):
    plt.savefig('plots/WindSpeeds.png')
plt.show( )


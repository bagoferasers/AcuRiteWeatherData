#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: colbybailey
"""

import pandas as pd
import matplotlib.pyplot as plt

#%%

"""
OPTIONAL: Set value of b to True to print out plots as png files under ../../plots
"""

b = False

#%%

"""
Read data into a dataframe using a list of header column names.
"""

col_list = [ "Sensor Name", "Sensor Type", "Timestamp", "Temperature ( F )", "Humidity ( RH )",
             "Dew Point ( F )",	"Heat Index ( F )",	"Feels Like ( F )",	"Wind Chill ( F )",	
             "Barometric Pressure ( INHG )", "Accumulated Rain ( IN )", "Wind Speed ( MPH )",	
             "Wind Average ( MPH )"	, "Wind Direction",	"Wired Sensor Temperature", "Wired Sensor Humidity", 
             "Soil & Liquid Temperature", "Water Detected", "UV Index", "Light Intensity", 
             "Measured Light", "Lightning Strike Count", "Lightning Closest Strike Distance" ]
df = pd.read_csv( "Data/June2022.csv", usecols = col_list )

# Header for output
print( "CURRENT DATA SET: " )

#%%

""" 
Merge function to be used by mergeSort function.
:param sortListA: one of the two non-decreasingly sorted list of numbers.
:param sortListB: one of the two non-decreasingly sorted list of numbers.
:returns: the merged list.
"""

def merge ( sortListA, sortListB ):
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
Count how many days need to be checked.  Each day has many entries, 
and requires parsing them to find out how many days there actually are. Dates is unparsed.
"""
        
def getAllDates( ):
    dates = [ ]
    for i in df[ "Timestamp" ]:
        dateSplit = i.split( )
        dates.append( dateSplit[ 0 ] )
    return dates
        
def extractImportantDates( dates ):
    datesParsed = [ ]
    alreadyDate = False
    for i in dates:
        if datesParsed == [ ]:
            datesParsed.append( i )
        else:
            for j in datesParsed:
                if i == j:
                    alreadyDate = True
            if alreadyDate == False:
                datesParsed.append( i )
        alreadyDate = False
    return datesParsed
        
#%%

"""
Find out how many days need to be checked for temperatures, loop through all dates and find 
the highest temperatures per day as well as the lowest, plot each highest & lowest temperature on a scatter plot. Merge sort
highest & lowest temperatures to find the correct ones for current data set.
"""

# declare and initialize variables
tf = False
count = 0
iVal = 0
jVal = 0
#dates = [ ]
highest = [ ]
lowest = [ ]
h = 0
l = 200
d = 0


dates = getAllDates()
datesParsed = extractImportantDates(dates)

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
print( "\t- Highest temperature = %.2f °F" % high[ len( high ) - 1 ] )
print( "\t- Lowest temperature = %.2f °F" % low[ 0 ] )

#find how many dates are in dataset and store in date[]
date = [ ]
j = 1
k = 0
while k <= d:
    date.append( j )
    k += 1
    j += 1
#print(date)

# plot highest daily temperature data
plt.scatter( datesParsed, highest, c = "red" ) 
plt.plot( datesParsed, highest, c = "red", alpha = 0.4 )
plt.title( "Highest Daily Temperatures" )
plt.ylabel( "°F", rotation = 0 )
plt.xticks( datesParsed, rotation = 90 )
plt.grid( visible=True, axis="both" )
if( b == True ):
    plt.savefig( 'plots/highestTemperatures.png' )
plt.show( )

#%%

"""
Plotting lowest daily temperatures.
"""

plt.scatter( datesParsed, lowest, c = "blue" )
plt.plot( datesParsed, lowest, c = "blue", alpha = 0.4 )
plt.title( "Lowest Daily Temperatures" )
plt.ylabel( "°F", rotation = 0 )
plt.xticks( datesParsed, rotation = 90 )
plt.grid( visible=True, axis="both" )
if( b == True ):
    plt.savefig( 'plots/lowestTemperatures.png' )
plt.show( )

#%%

"""
Plotting rain accumulation per day for current data.
"""

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

"""
avg wind speed vs highest wind speeds for days
"""

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
highWind = mergeSort( highestWindSpeeds )
print( "\t- Highest wind speed = %.2f MPH" % highWind[ len( highWind ) - 1 ] )
averageSpeed = sum( averageWindSpeeds[ : ] ) / len( averageWindSpeeds ) 
print( "\t- Average wind speed = %.2f MPH" % averageSpeed )
plt.scatter( datesParsed, averageWindSpeeds, c = "green" )
plt.plot( datesParsed, averageWindSpeeds, c = "green", alpha = 0.4, label = "Average Wind Speeds" )
plt.scatter( datesParsed, highestWindSpeeds, c = "orange" )
plt.plot( datesParsed, highestWindSpeeds, c = "orange", alpha = 0.4, label = "Highest Wind Speeds" )
plt.title( "Daily Wind Speeds" )
plt.ylabel( "MPH" )
plt.ylim( [ 0,highWind[ len( highWind ) - 1 ] + 1 ] )
plt.xticks( datesParsed, rotation = 90 )
plt.legend( shadow=True, framealpha=1, edgecolor="green", fontsize="x-small", facecolor="silver" )
plt.grid( visible=True, axis="both" )
if( b == True ):
    plt.savefig( 'plots/WindSpeeds.png') 
plt.show( )

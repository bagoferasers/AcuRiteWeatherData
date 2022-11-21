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
getAllDates function uses the "Timestamp" header from the dataframe,
extracts just the date, and returns them all. This includes all duplicate dates
on purpose.
"""

def getAllDates( ):
    dates = [ ]
    for i in df[ "Timestamp" ]:
        dateSplit = i.split( )
        dates.append( dateSplit[ 0 ] )
    return dates
        
#%%

"""
extractImportantDates function takes in the argument dates (returned from getAllDates())
and removes the redundancy of multiple dates.  It stores them in datesParsed[] and 
returns the completed set.
:param dates: all of the dates from the df[ "Timestamp" ] header.
:returns: datesParsed wich is the dates without the redundancy.
"""

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
maxHeapify function is used to maintain the max-heap property.
After maxHeapify, subtree rooted at i is a max-heap.
:param A: list of doubles.
:param i: subtree rooted at i.
"""

def maxHeapify( A, i ):
    largest = i
    left = 2 * i
    right = 2 * i + 1
    # if left child is largest, set as largest
    if left < len( A ) and A[ left ] > A[ largest ]:
        largest = left
    # if right child is largest, set as largest
    if right < len( A ) and A[ right ] > A[ largest ]:
        largest = right
    # if largest isn't i, exchange root with i and maxHeapify
    if largest != i:
        ( A[ i ], A[ largest ] ) = ( A[ largest ], A[ i ] )
        maxHeapify( A, largest )

#%%
"""
buildMaxHeap function takes an unordered array and produces
a max-heap of n elements in A.
:param A: list of doubles.
:param n: size of heap.
"""

def buildMaxHeap( A, n ):
    n = len( A )
    for i in range( n // 2 - 1, -1, -1 ):
        maxHeapify( A, i )
        
#%%
"""
heapsort function builds a max-heap from the array. It then
starts with the root and places the maximum element in the correct
place by swapping with last element in array. Then it discards the
last node (being in the correct place) and calls upon maxHeapify()
on the new root. Repeats process until only one node is left.
:param A: list of doubles.
:param n: size of heap.
"""

def heapsort( A, n ):
    buildMaxHeap( A, n ) 
    for i in range( n, 2 ):
        ( A[ 1 ], A[ i ] ) = ( A[ i ], A[ 1 ] )
        n = n - 1
        maxHeapify( A, i )

#%%
"""
maxHeapMaximum function returns the rmax value.
:param A: list of doubles.
:returns: the max heap's root.
"""

def maxHeapMaximum( A ):
    if len( A ) < 1:
        raise ValueError( "A.size is less than 1" )
    return A[ 0 ]

#%%
"""
maxHeapMinimum function returns the minimum value.
:param A: list of doubles.
:returns: the last element in Array.
"""

def maxHeapMinimum( A ):
    if len( A ) < 1:
        raise ValueError( "A.size is less than 1" )
    return A[ len( A ) - 1 ]

#%% 

# find out the dates for the dataset and store in datesParsed
dates = getAllDates( )
datesParsed = extractImportantDates( dates )

#%%
"""
extractMaxPerDay function returns the maximum values per day 
within the dataframe column.
:param dataFrame: dataFrame column to be used.
:returns: the high values per day.
"""

def extractMaxPerDay( dataFrame ):
    high = [ ]
    final = [ dates, dataFrame ]
    j = 0
    for i in datesParsed:
        perDay = [ ]
        # while date is the same
        while j < len( dates ) and i == dates[ j ]:
            # extract each for day and put into array
            perDay.append( final[ 1 ][ j ] )
            j += 1
        heapsort( perDay, len( perDay ) )
        high.append( maxHeapMaximum( perDay ) )
    return high

#%%
"""
extractMinPerDay function returns the minimum values per day
within the dataframe column.
:param dataFrame: dataFrame column to be used.
:returns: the low values per day.
"""

def extractMinPerDay( dataFrame ):
    low = [ ]
    final = [ dates, dataFrame ]
    j = 0
    for i in datesParsed:
        perDay = [ ]
        # while date is the same
        while j < len( dates ) and i == dates[ j ]:
            # extract each for day and put into array
            perDay.append( final[ 1 ][ j ] )
            j+=1
        heapsort( perDay, len( perDay ) )
        low.append( maxHeapMinimum( perDay ) )
    return low

#%%

"""
Find the highest and lowest temperatures per day, plot each on a scatter plot.
"""

highest = extractMaxPerDay( df[ "Temperature ( F )" ] )
lowest = extractMinPerDay( df [ "Temperature ( F )" ] )
plt.scatter( datesParsed, highest, c = "red" ) 
plt.plot( datesParsed, highest, c = "red", alpha = 0.4 )
plt.scatter( datesParsed, lowest, c = "blue" )
plt.plot( datesParsed, lowest, c = "blue", alpha = 0.4 )
plt.title( "Highest and Lowest Daily Temperatures" )
plt.ylabel( "°F", rotation = 0 )
plt.xticks( datesParsed, rotation = 90 )
plt.ylim( min( lowest ) - 1, max( highest ) + 1 )
plt.grid( visible=True, axis="both" )
if( b == True ):
    plt.savefig( 'plots/highestTemperatures.png' )
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

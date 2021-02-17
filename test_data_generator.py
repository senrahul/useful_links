#Desired data types and correctponding control mechanisms
###
#Date: Format
#Datetime: Format
#String: startswith, endswith, (alphanumeric, howManyNumeric)
#Int: min, max
#Float: min, max, precision
#Bool: True/False, 1/0
###
#Categorical(Can be sub-class of String with repeatation)
#Timestamp (can be integer):

#Ideally, bind the following in a class
#Methods
#Exposed method to ask:
#   Type of columns, specifications
#   their respective quantity
#   respective names
#   Number of rows needed
#Perform basic check on the asked data should not be too large for a unctionality test, example more than 10000 rows.

#It will in turn call repective method incharge of creating respective series

import random, string

#dumb methods, to attempt success on typos?
def createStringSeries(seriesLen=10, startsWith='', endsWith='', minLen=10, maxLen=10, isAlphaNum=False, lenNum=0):
    lenOfFixes = 0
    if startsWith or endsWith:
        lenOfFixes = len(startsWith) + len(endsWith)
    if isAlphaNum and 0<lenNum<len(string.digits):
        chDigits = string.digits[:lenNum]
        lenOfFixes += lenNum
    if lenOfFixes > maxLen: return [startsWith+endsWith]*seriesLen
    charSet = string.ascii_letters
    stringSeries = []
    for i in range(seriesLen):
        lenRandString = random.randint(max(minLen, lenOfFixes), maxLen) - lenOfFixes
        randString = ''.join(random.choice(charSet) for i in range(lenRandString))
        #randDigs = ''.join(random.choice(digSet) for i in range(lenNum))
        stringSeries.append(startsWith + randString + chDigits + endsWith)
    return stringSeries


def createNumSeries(seriesLen=10, minNum=0, maxNum=99999999, isInt=False):
    if minNum > maxNum: minNum,maxNum = maxNum,minNum
    randNum = random.randint if isInt else random.uniform
    return [randNum(minNum, maxNum) for _ in range(seriesLen)]

import pandas as pd
def createDatetimeSeries(seriesLen=10, startDate = '2010-01-01', freq='D'):
    return pd.date_range(startDate, periods=seriesLen, freq=freq)

def createBoolSeries(seriesLen=10, probability=0.5):
    return np.random.choice(a=[False, True],
                     size=seriesLen,
                     p=[probability, 1-probability])


dfLen = 15
stringCols = {'numCols': 3, 'colNames': ['S1', 'S2', 'S3'], 'config': {'startsWith':'a', 'endsWith':'zz',
                                       'isAlphaNum':True, 'lenNum':4,
                                       'minLen':10, 'maxLen':20}}

intCols = {'numCols': 2, 'colNames': ['I1', 'I2'], 'config': {'minNum': 10, 'maxNum': 999}}

floatCols = {'numCols': 4, 'colNames': ['F1', 'F2', 'F3', 'F4'], 'config': {'minNum': 10, 'maxNum': 999}}

dateCols = {'numCols': 2, 'colNames': ['D1', 'D2'], 'config': {'startDate': 10, 'freq': 'D'}}


def createSampleDataframe(dfLen, stringCols, intCols, floatCols, dateCols):
    stringDf = pd.DataFrame(list(zip(*[createStringSeries(**stringCols['config']) for _ in range(stringCols['numCols'])])),
                            columns=stringCols['colNames'])
   
    intDf = pd.DataFrame(list(zip(*[createNumSeries(**intCols['config'], isInt=True) for _ in range(intCols['numCols'])])),
                            columns=intCols['colNames'])
   
    floatDf = pd.DataFrame(list(zip(*[createNumSeries(**floatCols['config']) for _ in range(floatCols['numCols'])])),
                            columns=floatCols['colNames'])
   
    dateDf = pd.DataFrame(list(zip(*[createDatetimeSeries(**dateCols['config']) for _ in range(dateCols['numCols'])])),
                            columns=dateCols['colNames'])
    return pd.concat([stringDf,intDf, floatDf, dateDf],axis=1)

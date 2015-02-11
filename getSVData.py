__author__ = 'Cyrus'
import re
import urllib2
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import numpy as np
import pandas
#import simplejson

addressList = dict(pullup_address = "http://stats.nba.com/js/data/sportvu/pullUpShootData.js",
    drives_address = "http://stats.nba.com/js/data/sportvu/drivesData.js", defense_address = "http://stats.nba.com/js/data/sportvu/defenseData.js",
    passing_address = "http://stats.nba.com/js/data/sportvu/passingData.js",
    touches_address = "http://stats.nba.com/js/data/sportvu/touchesData.js",
    speed_address = "http://stats.nba.com/js/data/sportvu/speedData.js", rebounding_address = "http://stats.nba.com/js/data/sportvu/reboundingData.js",
    catchshoot_address = "http://stats.nba.com/js/data/sportvu/catchShootData.js",
    shooting_address = "http://stats.nba.com/js/data/sportvu/shootingData.js")




def readIt(address):
    req = urllib2.Request(address, None)
    #web_page = readlines(address)
    opener = urllib2.build_opener()
    f = opener.open(req)
    file = f.read()
    #print file

    ## regex to strip javascript bits and convert raw to csv format
    x1 = re.sub("[\\{\\}\\]]", "", file)
    x2 = re.sub("[\\[]", "\n", x1)
    x3 = re.sub("\"rowSet\":\n", "", x2)
    x4 = re.sub("\;", ",", x3)
    x5 = re.sub("null", "NULL", x4)
    x5 = '\n'.join(x5.splitlines()[2:])

    csvToRead=StringIO(x5)
    # read the resulting csv with read.table()
    nba = pandas.read_csv(csvToRead)
    nba=nba.dropna(axis=1,how='all')
    #print nba
    #print nba
    return(nba)

count = 0
for address in addressList:
    if count ==0:
        #print addressList[address]
        df = readIt(addressList[address])

        count+=1
        #print df
    else:
        #print df
        #print addressList[address]'''
        df = df.merge(readIt(addressList[address]), on=['PLAYER_ID','TEAM_ABBREVIATION'], how="outer", copy=False)
df = df.T.drop_duplicates().T
df.to_csv('test.csv')



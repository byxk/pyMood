##PyMood
##Captures the generalized mood of the Twittersphere.
##Patrick Tseng
##Twython, GChartWrapper
##TODO
##1. Convert the pie chart into a timeline graph. (Intervals of once a day)
##2. Use a flatfile database to keep track of the history. Can't use MYSQL bc of memory issues on rpi.
##3. Put in checks to make sure timeline doesn't get wiped during crashes/outages.
##4. EXTRA FEATURES?!?!?!?!?!
from twython import TwythonStreamer
import time
import os
import thread
import sys
import math
import random
from GChartWrapper import *
import time
import urllib
import datetime
import ftplib
from gen import *

#period
timeinsec = 60
t0= time.time()
d0 = datetime.date.today()

#FTP info
FTP_USERNAME = ""
FTP_PASSWORD = ""
FTP_SERVER = ""

#Twitter info
APP_KEY = 'UxWDcrHo4OwwFtoGd9Jw'
APP_SECRET = 'pjHX2b1EXW6fCtLHf4t4UVo4E5USP9IIVbZqg87Q'
OAUTH_TOKEN = '765069332-Z30wNIz7OXirdTz42yyH9UIV2I9iyQhgiBWMGI17'
OAUTH_TOKEN_SECRET = 'byT2Q8lAJkZfQ4M0euZvMU4uW6vPJhytajPc0NiSNk'

#Start out with 1 (google charts api)
numoftweets = 1
totaltweets = 1

emotionCol = {}
#dayRecord = [d0.month + "." + str(d0.day).zfill(2)]
dayRecord = [1]

#for debugging purposes.
countingtada = 0

print "Grabbing Tweets"

#List of dictionaries of lists of keywords to identify emotions. (THE SECRET EMOTION EQUATION :D)
emotionCol['happy'] = {'q' : ["happy"], 'col':'000000', 'h':[0]}
emotionCol['sad'] = {'q' : ["sad"], 'col':'FF0000', 'h':[0]}
emotionCol['confident'] = {'q' : ["confident"], 'col':'444444', 'h':[0]}
emotionCol['worried'] = {'q' : ["worried"], 'col':'FF4444', 'h':[0]}
emotionCol['excited'] = {'q' : ["excited"], 'col':'888888', 'h':[0]}
emotionCol['bored'] = {'q' : ["bored"], 'col':'FF8888', 'h':[0]}

def writehourly(timestr,nt,tt):
    indexfile = open(timestr + ".html", "w+")
    indexfile.write("<title>" + timestr + "</title>")
    indexfile.write('<img src="' + timestr + '.jpg">')
    indexfile.write("Number of emotional tweets used: " + nt + "<br>")
    indexfile.write("Number of tweets total: " + tt)
    indexfile.close()

def uploadfiles(lof):
    session = ftplib.FTP(FTP_SERVER,FTP_USERNAME,FTP_PASSWORD)
    for i in lof:
        file = open(i,'rb')                  # file to send
        session.storbinary('STOR ' + i, file)
        file.close()                          # close file and FTP
    session.quit()

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        global t0
        global numoftweets
        global totaltweets
        global countingtada

        
        if time.time() - t0 > timeinsec:
            current_time = datetime.datetime.now().time()
            graph = LineXY( [dayRecord,
                             [0,10,20,30,40,50],
                             emotionCol['happy']['h'],
                             emotionCol['sad']['h'],
                             emotionCol['confident']['h'],
                             emotionCol['worried']['h'],
                             emotionCol['excited']['h'],
                             emotionCol['bored']['h']
                             ] )
            graph.title('pymood')
            graph.color(
                             emotionCol['happy']['col'],
                             emotionCol['sad']['col'],
                             emotionCol['confident']['col'],
                             emotionCol['worried']['col'],
                             emotionCol['excited']['col'],
                             emotionCol['bored']['col']
                             )
            print graph
            timestr = time.strftime("%Y%m%d-%H%M%S")
            urllib.urlretrieve(str(graph), timestr + ".jpg")

            # writehourly(timestr,str(numoftweets),str(totaltweets))
            f = open("index.html", "a")
            f.write('<a href="' + timestr + '.html">' + timestr + '</a><br>')
            f.close()

            #uploadfiles(['index.html',timestr + '.jpg',timestr + '.html'])
            
            self.disconnect()

            #Restart script within itself
            args = sys.argv[:]
            args.insert(0, sys.executable)
            if sys.platform == 'win32':
                args = ['"%s"' % arg for arg in args]
            os.execv(sys.executable, args)

            dayRecord.append(dayRecord[-1] + 1)
            for emotion in emotionCol:
                emotionCol[emotion]['h'].append(0)
            
            
        if 'text' in data:
           # print data['text'].encode('utf-8')
            for emotion in emotionCol:
                totaltweets += 1
                for i in emotionCol[emotion]['q']:
                    if i in data['text'].encode('utf-8'):
                        numoftweets += 1
                        countingtada += 1
                        emotionCol[emotion]['h'][-1] +=1
                        
        if countingtada > 100:
            countingtada = 0
            print emotion, emotionCol[emotion]['count']
                   # print data['text'].encode('utf-8')
             
            #data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code, data

# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


stream.statuses.sample()
#stream.user()  # Read the authenticated users home timeline (what they see on Twitter) in real-time
#stream.site(follow='twitter')

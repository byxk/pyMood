##PyMood
##Captures the generalized mood of the Twittersphere.
##Patrick Tseng
##Twython, GChartWrapper

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
t0= time.time()

FTP_USERNAME = ""
FTP_PASSWORD = ""
FTP_SERVER = ""
APP_KEY = 'UxWDcrHo4OwwFtoGd9Jw'
APP_SECRET = 'pjHX2b1EXW6fCtLHf4t4UVo4E5USP9IIVbZqg87Q'
OAUTH_TOKEN = '765069332-Z30wNIz7OXirdTz42yyH9UIV2I9iyQhgiBWMGI17'
OAUTH_TOKEN_SECRET = 'byT2Q8lAJkZfQ4M0euZvMU4uW6vPJhytajPc0NiSNk'
numoftweets = 1
totaltweets = 1
addtohistory = []
tweets = {}

countingtada = 0

##indexfile.close()
print "Grabbing Tweets"
tweets['happy'] = {'q' : ["happy", "yay", "yes", "wow", "amazing", "woot", ":)", "(:", ":D", "xD"], 'col':(255,0,0)}
tweets['sad'] = {'q' : ["sad", "annoyed", "can't believe", "sucks", ":(", "):", "D:"], 'col':(255,255,0)}
tweets['fear'] = {'q' : ["afraid", "scared", "can't tell"], 'col':(0,255,0)}
tweets['love'] = {'q' : ["love", "passionate", "like"], 'col':(0,255,255)}
tweets['anger'] = {'q' : ["angry", "wtf", "mad"], 'col':(0,0,255)}
tweets['surprise'] = {'q' : ["surprised", "wasn't expecting", "woah"], 'col':(255,0,255)}
tweets['jelly'] = {'q' : ["jealous", "i want"], 'col':(255,127,0)}
     


def writehourly(timestr,nt,tt):
    indexfile = open(timestr + ".html", "w+")
    indexfile.write("<title>" + timestr + "</title>")
    indexfile.write('<img src="' + timestr + '.jpg">')
    indexfile.write("Number of emotional tweets used: " + nt + "<br>")
    indexfile.write("Number of tweets total: " + tt)
    indexfile.close()


for emotion in tweets:
    tweets[emotion]['count'] = 0

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        global t0
        global numoftweets
        global totaltweets
        global countingtada
        if 'text' in data:
           # print data['text'].encode('utf-8')
            for emotion in tweets:
                totaltweets += 1
                for i in tweets[emotion]['q']:
                    if i in data['text'].encode('utf-8'):
                        numoftweets += 1
                        countingtada += 1
                        tweets[emotion]['count'] +=1
                        
                        if countingtada > 60:
                            countingtada = 0
                            print emotion, tweets[emotion]['count']
                   # print data['text'].encode('utf-8')
             
            #data['text'].encode('utf-8')
        # Want to disconnect after the first result? 14400
       # t = time.clock() - t0
       # print t
        
        if time.time() - t0 > 7200:
            current_time = datetime.datetime.now().time()
            pie = Pie3D([tweets['happy']['count'] / float(numoftweets),  # % calc, google charts api doesn't recognize massive numbers
                         tweets['sad']['count'] / float(numoftweets),
                         tweets['fear']['count'] / float(numoftweets),
                         tweets['love']['count'] / float(numoftweets),
                         tweets['anger']['count'] / float(numoftweets),
                         tweets['surprise']['count'] / float(numoftweets),
                         tweets['jelly']['count'] / float(numoftweets)],
                        encoding='text').size(750,300).title('2 hour range').color('yellow',
                                                                                             'blue',
                                                                                             'orange',
                                                                                             'red',
                                                                                             'black',
                                                                                             'purple',
                                                                                             'brown' ).label('happy' + str(tweets['happy']['count']),
                                                                                                             'sad' + str(tweets['sad']['count']),
                                                                                                             'fear' + str(tweets['fear']['count']),
                                                                                                             'love' + str(tweets['love']['count']),
                                                                                                             'anger' + str(tweets['anger']['count']),
                                                                                                             'surprise' + str(tweets['surprise']['count']),
                                                                                                             'jelly' + str(tweets['jelly']['count']))
            print pie
            timestr = time.strftime("%Y%m%d-%H%M%S")
            urllib.urlretrieve(str(pie), timestr + ".jpg")

            writehourly(timestr,str(numoftweets),str(totaltweets))
            f = open("index.html", "a")
            f.write('<a href="' + timestr + '.html">' + timestr + '</a><br>')
            f.close()
       
            session = ftplib.FTP(FTP_SERVER,FTP_USERNAME,FTP_PASSWORD)
            file = open('index.html','rb')                  # file to send
            session.storbinary('STOR index.html', file)     # send the file
            file = open(timestr + '.jpg', 'rb')
            session.storbinary('STOR ' + timestr + '.jpg', file)
            file = open(timestr + '.html', 'rb')
            session.storbinary('STOR ' + timestr + '.html', file)
            file.close()                                    # close file and FTP
            session.quit()
            
            self.disconnect()
            args = sys.argv[:]
            args.insert(0, sys.executable)
            if sys.platform == 'win32':
                args = ['"%s"' % arg for arg in args]
            os.execv(sys.executable, args)

    def on_error(self, status_code, data):
        print status_code, data

# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


stream.statuses.sample()
#print addtohistory[1]
#stream.user()  # Read the authenticated users home timeline (what they see on Twitter) in real-time
#stream.site(follow='twitter')

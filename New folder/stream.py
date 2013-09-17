##PyMood
##Captures the generalized mood of the Twittersphere.
##Patrick Tseng, Steven T.
##Twython, Google Charts API
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
import time
import urllib
import datetime
import ftplib
from gen import *
import pickle
from os import listdir
from os.path import isfile, join

#period
timeinsec = 86400
t0= time.time()
d0 = datetime.date.today()

#FTP info
FTP_USERNAME = "pymood@meowdesu.net"
FTP_PASSWORD = "meowdesu"
FTP_SERVER = "ftp.meowdesu.net"

#Twitter info
APP_KEY = 'cljOyaQNUv5KXG6qUvRmA'
APP_SECRET = 'pyjp9rKDRvRPhdOuxoHRoKUNRuVLUuz1xuyhXqZKttc'
OAUTH_TOKEN = '765069332-Z30wNIz7OXirdTz42yyH9UIV2I9iyQhgiBWMGI17'
OAUTH_TOKEN_SECRET = 'byT2Q8lAJkZfQ4M0euZvMU4uW6vPJhytajPc0NiSNk'

#Start out with 1 (google charts api)
numoftweets = 1
totaltweets = 1

#for debugging purposes.
countingtada = 0
print "Script has started"
print "Grabbing Tweets"

dayRecord = []
dayRecordFile = "dr.dat"
if (os.path.isfile(dayRecordFile)):
    fDR = open(dayRecordFile, "rb")
    dayRecord = pickle.load(fDR)
    dayRecord.append(dayRecord[-1].replace(day=dayRecord[-1].day+1))
else:
    dayRecord.append(datetime.date.today())
    
#List of dictionaries of lists of keywords to identify emotions. (THE SECRET EMOTION EQUATION :D)
emotionCol = {}
emotionColFile = "ecol.dat"

if (os.path.isfile(emotionColFile)):
    fEC = open(emotionColFile, "rb")
    emotionCol = pickle.load(fEC)
    print "Loaded a pickle"
else:
    emotionCol['happy'] = {'q' : ["happy"], 'col':'000000', 'h':[]}
    emotionCol['sad'] = {'q' : ["sad"], 'col':'FF0000', 'h':[]}
    emotionCol['confident'] = {'q' : ["confident"], 'col':'444444', 'h':[]}
    emotionCol['worried'] = {'q' : ["worried"], 'col':'FF4444', 'h':[]}
    emotionCol['excited'] = {'q' : ["excited"], 'col':'888888', 'h':[]}
    emotionCol['bored'] = {'q' : ["bored"], 'col':'FF8888', 'h':[]}

for emotion in emotionCol:
    emotionCol[emotion]['h'].append(0)


#should do a with open 
def uploadfiles(lof):
    session = ftplib.FTP(FTP_SERVER,FTP_USERNAME,FTP_PASSWORD)
    for i in lof:
        file = open(i,'rb')                  # file to send
        session.storbinary('STOR ' + i, file)
        file.close()                          # close file and FTP
    print "files uploaded"
    session.quit()

#basic class provided by twython example code.
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        global t0
        global numoftweets
        global totaltweets
        global countingtada
        global dayRecord
        global emotionCol    
            
        if 'text' in data:
           # print data['text'].encode('utf-8')
            for emotion in emotionCol:
                totaltweets += 1
                for i in emotionCol[emotion]['q']:
                    if i in data['text'].encode('utf-8'):
                        #print time.time()
                        #print data['text'].encode('utf-8')
                        numoftweets += 1
                        countingtada += 1
                        print str(totaltweets)
                        print str(numoftweets)
                        emotionCol[emotion]['h'][-1] +=1
        
        if time.time() - t0 > timeinsec:
            genGraph(dayRecord, emotionCol)
            self.disconnect()
            print "Disconnected from Twitter stream"
            print "Restarting script"
            files = [f for f in os.listdir('.') if os.path.isfile(f) and ".html" in f]
            print files
            uploadfiles(files)
            #Restart script within itself
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

#.sample - get all tweets
#.filter - filter out tweets.
stream.statuses.sample()
#stream.user()  # Read the authenticated users home timeline (what they see on Twitter) in real-time
#stream.site(follow='twitter')

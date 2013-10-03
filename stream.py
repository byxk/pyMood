##PyMood
##Captures the generalized mood of the Twittersphere.
##Patrick Tseng, Steven T.
##Twython, Google Charts API
##TODO
##1. Statistics?!
##2. Support console input! multithreading.
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
import subprocess
import threading
import Queue

#period
timeinsec = 3600
t0= time.time()
d0 = datetime.date.today()

#Twitter info is now stored in key.txt
#First line is APP_KEY
#Second is APP_SECRET, third is OAUTH_TOKEN, and fourth is OAUTH_TOKEN_SECRET
#Create the file first!
mykeyfile = open("key.txt", "r")
print "Reading keys..."
mykeys = mykeyfile.readlines()
APP_KEY =  mykeys[0].strip()
APP_SECRET =  mykeys[1].strip()
OAUTH_TOKEN =  mykeys[2].strip()
OAUTH_TOKEN_SECRET =  mykeys[3].strip()

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
    #dayRecord.append(dayRecord[-1].replace(day=dayRecord[-1].day+1))
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
    emotionCol['happy'] = {'q' : ["i'm happy", "yay"], 'col':'000000', 'h':[0]}
    emotionCol['sad'] = {'q' : ["i'm sad", "i'm disappointed"], 'col':'FF0000', 'h':[0]}
    emotionCol['confident'] = {'q' : ["i feel good", "confident"], 'col':'444444', 'h':[0]}
    emotionCol['worried'] = {'q' : ["worried", "can't believe"], 'col':'FF4444', 'h':[0]}
    emotionCol['excited'] = {'q' : ["excited", "i can't wait"], 'col':'888888', 'h':[0]}
    emotionCol['bored'] = {'q' : ["bored", "nothing to do"], 'col':'FF8888', 'h':[0]}

if dayRecord[-1] != datetime.date.today():
    for emotion in emotionCol:
        emotionCol[emotion]['h'].append(0)
    dayRecord.append(datetime.date.today())
    
def restartscript():
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

    #Why did i create this function?...not sure.
def genaGraph(dr, ec, nt):
    #genGraph(dayRecord, emotionCol, numoftweets)
    genGraph(dr, ec, nt)
    try:
        subprocess.check_call(['../dropbox_uploader.sh', 'upload', '../pymood', 'Public/PM'])
    except:
        restartscript()
    #Restart script within itself
    print "Restarting script..."
    restartscript()



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
            datastr = data['text'].encode('utf-8').lower()
          # print data['text'].encode('utf-8')
            for emotion in emotionCol:
                totaltweets += 1
                for i in emotionCol[emotion]['q']:
                    if i in datastr:
                        #print time.time()
                        #print data['text'].encode('utf-8')
                        numoftweets += 1
                        countingtada += 1
                        print "total tweets: " + str(totaltweets)
                        print "Number of tweets used: " + str(numoftweets)
                        emotionCol[emotion]['h'][-1] +=1
                        break
        
        if time.time() - t0 > timeinsec:
            self.disconnect()
            print "Disconnected from Twitter stream"
            print "Uploading files"
            #files = [f for f in os.listdir('.') if os.path.isfile(f)]
            #uploadfiles(files)
            genaGraph(dayRecord, emotionCol, numoftweets)

    def on_error(self, status_code, data):
        print status_code, data
        ##Copy and pasted restart code, lol.
        restartscript()

# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#.sample - get all tweets
#.filter - filter out tweets.
def runStream():
    try:
    ##not sure if this is only called once to established a connection
        stream.statuses.sample()
    except:
        restartscript()
#stream.user()  # Read the authenticated users home timeline (what they see on Twitter) in real-time
#stream.site(follow='twitter')

#Start streaming thread
t = threading.Thread(target=runStream)
t.daemon = True
t.start()

running = True
while running:
    userIn = raw_input(">>")
    if "data" in userIn:
        print "Number of tweets used: " + str(numoftweets)
        print "Total number of tweets mined: " + str(totaltweets)
    elif "restartscript" in userIn:
        restartscript()
    elif "gengraph" in userIn:
        print "Generating"
        genaGraph(dayRecord, emotionCol, numoftweets)
    elif "getstat" in userIn:
        try:
            str(emotionCol[userIn.split(" ")(1)]['h'][-1])
        except:
            print "error getting emotion stats for: " + userIn.split(" ")(1)
        
        


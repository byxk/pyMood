pyMood
======

Gathers the generalized mood of the Twittersphere


Simply download all the files, and run in terminal/cmd [python stream.py].
Uses Twython API.
Uses dropbox_uploader.sh to upload files directly on to Dropbox. FTP or other file uploading methods will work as well. Make sure script is located at root (changable).
Accepts lists of emotion keywords.
Auto restart on crash, network disconnect, or Twitter errors.
Default graph update is every hour.
Uses OAuth1, keys are kept in a seperate file for security(?) reasons.

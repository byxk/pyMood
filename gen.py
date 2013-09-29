import pickle
import datetime

##Generate a timeline graph using Google Charts
##Functions

##genGraph(ListOfDates, DicOfEmotions)
##ListofDates - ListOfDateTime
##DicOfEmotions - pass emoCOL
def genGraph(lofd, emotionCol, totaltweets):
    thedata = []
    for i in range(0,len(lofd)):
        thedata.append('[new Date('
                       + str(lofd[i].year) + "," + str(lofd[i].month - 1) + "," + str(lofd[i].day) + '),'
                       + str((emotionCol["happy"]['h'][i])/float(totaltweets)) + ","
                       + str((emotionCol["sad"]['h'][i])/float(totaltweets))  + ","
                       + str((emotionCol["confident"]['h'][i])/float(totaltweets))  + ","
                       + str((emotionCol["worried"]['h'][i])/float(totaltweets)) + ","
                       + str((emotionCol["excited"]['h'][i])/float(totaltweets)) + ","
                       + str((emotionCol["bored"]['h'][i])/float(totaltweets)) + "],\n")

    
    thedata[len(thedata) - 1] = thedata[len(thedata) - 1][0:-2] #trims the "," at the very end
    with open('template.txt', 'r') as file:
         data = file.readlines()
    #lazy mode. check this if template.txt is ever modified.
    for index, item in enumerate(data):
        if "%data%" in item:
            data[index] = "".join(thedata)
            
    with open(str(lofd[0].year) + "." + str(lofd[0].month).zfill(2) + '.html', 'w') as file:
         file.writelines(data)
         
    myfile = open("index.html", "a+")
    tempdata = myfile.readlines()
    tempdata1 = False
    for index, item in enumerate(tempdata):
        print item
        if '<a href="' + str(lofd[0].year) + "." + str(lofd[0].month).zfill(2) + '.html">'+ str(lofd[0].year) + "." + str(lofd[0].month).zfill(2) + '</a><br>\n' in item:
            tempdata1 = True
    if tempdata1 is False:
        myfile.write('<a href="'
                 + str(lofd[0].year) + "." + str(lofd[0].month).zfill(2) + '.html">'
                 + str(lofd[0].year) + "." + str(lofd[0].month).zfill(2) + '</a><br>\n')

    #pickle files for backup.
    if datetime.date.today().month == lofd[-1].month:
        pickle.dump(lofd, open("dr.dat", "wb"))
        pickle.dump(emotionCol, open("ecol.dat", "wb"))
    else:
        if os.path.isfile("dr.dat"):
                os.remove("dr.dat")
                os.remove("ecol.dat")

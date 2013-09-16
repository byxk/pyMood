import pickle

##Generate a timeline graph using Google Charts
##Functions

##references now
startoffile = ["<html>\n",
               "<head>\n",
               "<script type='text/javascript' src='http://www.google.com/jsapi'></script>\n",
               "<script type='text/javascript'>\n",
               "google.load('visualization', '1', {'packages':['annotatedtimeline']});\n",
               "google.setOnLoadCallback(drawChart);\n",
               "function drawChart() {\n",
               "var data = new google.visualization.DataTable();\n",
               "data.addColumn('date', 'Date');\n"]
               
endofile = ["var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('chart_div'));\n",
            "chart.draw(data, {displayAnnotations: true});\n",
            "}\n",
            "</script>\n",
            "</head>\n",
            "<body>\n",
            "<div id='chart_div' style='width: 700px; height: 240px;'></div>\n",
            "</body>\n",
            "</html>\n"]
            
##genGraph(ListOfDates, DicOfEmotions)
##ListofDates - ListOfDateTime
##DicOfEmotions - pass emoCOL
def genGraph(lofd, emotionCol):
    #pickle files for backup.
    pickle.dump(lofd, open("dr.dat", "wb"))
    pickle.dump(emotionCol, open("ecol.dat", "wb"))
    thedata = []
    for i in range(0,len(lofd)):
        thedata.append('[new Date('
                       + str(lofd[i].year) + "," + str(lofd[i].month - 1) + "," + str(lofd[i].day) + '),'
                       + str(emotionCol["happy"]['h'][i]) + ","
                       + str(emotionCol["sad"]['h'][i])  + ","
                       + str(emotionCol["confident"]['h'][i])  + ","
                       + str(emotionCol["worried"]['h'][i]) + ","
                       + str(emotionCol["excited"]['h'][i]) + ","
                       + str(emotionCol["bored"]['h'][i]) + "],\n")
    with open('template.txt', 'r') as file:
         data = file.readlines()
    #lazy mode. check this if template.txt is ever modified.
    data[16] = "".join(thedata)
     
    with open(str(lofd[0].year) + "." + str(lofd[0].month).zfill(2) + '.html', 'w') as file:
         file.writelines(data)
            
##split list at index
##partition(List, [index])
    
def partition(alist, indices):
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]     



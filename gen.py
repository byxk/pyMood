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
def genGraph(lofd, doe):
    #pickle files for backup.
    pickle.dump(lofd, open("dr.dat", "rb"))
    pickle.dump(doe, open("ecol.dat", "rb"))
    thedata = []
    for i in lofd:
        thedata.append('[new Date('
                       + str(i.year) + "." + str(i.month - 1) + "." + str(i.day) + '),'
                       + emotionCol["happy"]['h'][i] + ","
                       + emotionCol["sad"]['h'][i]  + ","
                       + emotionCol["confident"]['h'][i]  + ","
                       + emotionCol["worried"]['h'][i] + ","
                       + emotionCol["excited"]['h'][i] + ","
                       + emotionCol["bored"]['h'][i] + "],\n")
    with open('template.txt', 'r') as file:
         data = file.readlines()
    #lazy mode. check this if template.txt is ever modified.
         
    partition(data,[15,16])
    parts = data[0] + thedata + data[2]
     
    with open('index.html', 'w') as file:
         file.writelines(parts)
            
##split list at index
##partition(List, [index])
    
def partition(alist, indices):
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]     



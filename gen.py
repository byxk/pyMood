##Generate a timeline graph using Google Charts
##Functions
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
            
##genGraph(ListOfDates, DicOfEmotions, ListOfListEmotionsVars)
##ListofDates - Starting from earliest, form is yyyy.mm.dd, 00 is jan
##DicOfEmotions - pass emoCOL
##ListOfListEmotionsVar - TO BE CHANGED. For now, each index of emotion must match the dates AND the order of emotions
def genGraph(lofd, doe, lolev):
    #Look into appending instead of writing a new file each time....
    indexfile = open("index.html", "r+")
    indexfile.writelines(startoffile)
    for emotion in doe:
        indexfile.write("data.addColumn('number', '" + emotion + "');\n")
    indexfile.write("data.addRows([\n")
    for i in lofd:
        indexfile.write('[new Date(' + splitDate(i, "y") +
                        ',' + splitDate(i, "y") +
                        ','+ splitDate(i, "y") + '),' + getDel(i) + '],\n')

    ##CHECK FOR LAST LINE, doesn't need a comma
    indexfile.write("]);\n")
    indexfile.write(endoffile)
    indexfile.close()

##TODO: Create a def that compilies a line of the #'s of tweets in emotion order.
##EX: if the only emotions are happy, sad, and happy has 1000 while sad has 600, output should be
##"1000, 600"
##NOTE that each output is for a specific day. genGraph will iterate thru each day request a line like that
##Dateformat = yyyy.mm.dd?
def getDEL(date):
    count = 0
    
    

##splitDate(date in str, p is mode)
##p = "y", "m", or "d"
def splitDate(d,p):
    date = d.split(".")
    if p is "y":
        return date[0]
    if p is "m":
        return date[1]
    if p is "d":
        return date[2]
    return 

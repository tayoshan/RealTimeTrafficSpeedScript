import numpy as np
import urllib2
import datetime as dt

#Important concepts:
#A) Must check for incomplete lines first (missing ending quoatation) and then for whether lines missing data entries.
#---Opposite order will cause code to infinitely loop.
#B) Keeping a separate counter of the length of the list of lines since this is used to control the outter-most loop but
#---the list is changing dynmaically within inner functions


def checkColumns(line, numFields):          #function to check each line to see if it has the correct number of tab-delmited
    if len(line.split('\t')) < numFields:   #data entries given the number of fields in the first row
        return False
    else:
        return True

def fixLine(line, lines, count):            #Main function that checks each line and makes necessary format corrections
    if line[-2] != '"':                     #First check to see if the line ends with the proper "end-of-line" characters for this dataset
        line = line + lines[1]              #If not, add the next line in the list to the previous line
        lines.pop(0)                        #Remove the original line under revision from the list
        count -= 1                          #Remove one from the list count
    while checkColumns(line, numFields) == False:           #Second, check to see if the line has correct number of data entries
        line = line + lines[1]                              #As long as it does not, keep adding the next line to the one under revision
        lines.pop(1)                                        #And remove the added line from the list
        count -= 1                                          #Update list count
    lines.pop(0)                            #When the line has the correct number of data entries, remove it from the list
    count -= 1                              #And update list count
    return line, lines, count               #Return corrected line, updated lines list, and updated list count


lines = urllib2.urlopen('http://207.251.86.229/nyc-links-cams/LinkSpeedQuery.txt').read().rsplit("\n")  #Get text file from web service

numFields = len(lines[0].split("\t"))           #Get number of fields (tab-delimited fields in first line)
newLines = []                                   #New list to store reformatted lines
count = len(lines)                              #Number of  lines in original list
while count > 1:                                #While count is greater than 1 (should be 0 but for some reason there is a set of quotes that ends up being left over)
            line, lines, count = fixLine(lines[0], lines, count)            #Check and fix the current line
            line = line.replace("\r", "")                                   #Aferwards, remove extra carriage return markers
            newLines.append(line)                                           #Add reformmated line to new list

columns = newLines[0].split("\t")                                           #Columns will be the number of fields in first row
dataArray = np.ndarray((len(newLines),len(columns)), dtype = "object")      #Final array should be the size of the number of rows by the nubmer of fields
rows,cols = dataArray.shape                                                 #row and column counts
for row in range(rows):                                                     #Break lines up into numpy array
    line = newLines[row].split("\t")
    for col in range(cols):
        dataArray[row,col] = line[col]

current = dt.datetime.now()
date = str(current.month) + "_" + str(current.day) + "_" + str(current.year)[2:]
time = current.strftime("%H.%M.%S")
np.savetxt("RTTS" + "_" + date + "_ " + time + ".csv", dataArray, fmt = "%s", delimiter = ",")          #Save numpy array as a csv file

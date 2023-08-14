import linecache
import re
import pandas as pd
import os
from openpyxl import load_workbook
from datetime import date

#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
readPath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts " #I'm using Case# 23CV17209 for testing
writePath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts Output.xlsx"
companyName = "" #PLACEHOLDER
beginDate = "" #PLACEHOLDER
endDate = "" #PLACEHOLDER
caseKeywords = ["Case Number:", "Court:", "Case Caption:", "Judge:", "Filed Date:", "Case Type", "Nut", "Amount:", "Bannanna:"] #"Nut" and "Bannanna:" was/is used to test for unfindable keywords
partyCaseKeywords = ["Plaintiff Name", "Plaintiff Address", "Party", "Attorney", "Attorney Address", "Court ID", "Defendant Name", "Defendant Address", "Defendant Party"]
data = {}

def createExcelSheet(caseKeywords, partyCaseKeywords, writePath):
    #Source: https://saturncloud.io/blog/how-to-append-a-pandas-dataframe-to-an-excel-sheet-a-comprehensive-guide/
    #https://sparkbyexamples.com/pandas/pandas-write-to-excel-with-examples/#:~:text=Use%20pandas%20to_excel()%20function,sheet%20name%20to%20write%20to.
    #https://pythonbasics.org/write-excel/
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
    #Adds new dictionary keys for each case Keyword
    for keyword in range(0, len(partyCaseKeywords)):
        data[re.sub('[:]', "", partyCaseKeywords[keyword])] = []
    for keyword in range(0, len(caseKeywords)):
        data[re.sub('[:]', "", caseKeywords[keyword])] = []

def searchHTML(readPath, searchFor):
    #Source: https://pynative.com/python-search-for-a-string-in-text-files/#:~:text=Open%20a%20file%20in%20a,current%20line%20and%20line%20number.
    with open(readPath, 'r') as file:
        for lineNumber, line in enumerate(file):
            if str(searchFor) in line:
                return(lineNumber)
                break

def harvestData(readPath, caseKeywords, partyCaseKeywords):
    linebreak = 0
    #Case Summary Info (ln 277 - ln 302 in test page)
    for info in caseKeywords:
        #Check and see if caseKeyword is in the HTML file
        if str(searchHTML(readPath, info)) != "None":
            #Add the data into the "data" dictionary after removing unwanted characters
            data[re.sub("[:]", "", info)].append(re.sub("[/]", " ", re.sub("[<td>\n]", "", (linecache.getline(readPath, searchHTML(readPath, info) + 2)))))
        else:
            data[re.sub("[:]", "", info)].append("")

#Party/Attorney Info (ln 357 - ln 367 in test pag)
    #"aria-live" is the indicator because of its close proximity to the Part/Attorney Info
    #Source: https://stackoverflow.com/a/16432254
    for num in range(0, len(partyCaseKeywords)):
        if str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + 4)) != '</tr><tr role="row" class="even">\n':
            #replace unwanted characters
            #print(re.sub("[;/]", " ", (re.sub("[<td>&nbspr]", "", (str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + linebreak + 4)))))))
            data[partyCaseKeywords[num]].append((re.sub("[;/]", " ", (re.sub("[<td>&nbspr\n]", "", (str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + linebreak + 4))))))))
        else:
            linebreak = 1
            data[partyCaseKeywords[num]].append((re.sub("[;/]", " ", (re.sub("[<td>&nbspr\n]", "", (str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + 5))))))))



createExcelSheet(caseKeywords, partyCaseKeywords, writePath)
print("\n" + "Created (but empty) Excel Sheet: ")
for key, value in data.items():
    print(key, value)
print("\n" + "Harvested Data: ")
#for number in range(1, len(os.listdir(r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber")) + 1):
for number in range(1, 2 + 1):  # this is used since the current directory has other files that'll break the for loop
    harvestData(readPath + str(number) + ".html", caseKeywords, partyCaseKeywords)
for key, value in data.items():
    print(key, value)


#DEV NOTES/TO DO

#Add in a way to create a new excel sheet based off of input data
#Auto format the new excel sheet
#Create a way to make and add to the dictionary without having to access and modify the code
#Actually take the dictionary and export it into excel
#If possible, make the dictionary consolidation much cleaner

#TLDR: MAKE IT AS AUTOMATED AND EFFICIENT AS POSSIBLE!
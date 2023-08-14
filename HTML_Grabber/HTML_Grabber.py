import linecache
import re
import pandas as pd
from openpyxl import load_workbook
from datetime import date

#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
readPath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts.html" 
writePath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts Output.xlsx"
companyName = "" #PLACEHOLDER
beginDate = "" #PLACEHOLDER
endDate = "" #PLACEHOLDER
caseKeywords = ["Case Number:", "Court:", "Case Caption:", "Judge:", "Filed Date:", "Case Type", "Amount:", "Bannanna:"] #"Bannanna:" was/is used to test for unfindable keywords
data = {}

def formatExcelSheet(caseKeywords, writePath):
    #Source: https://saturncloud.io/blog/how-to-append-a-pandas-dataframe-to-an-excel-sheet-a-comprehensive-guide/
    #Adds new dictionary keys for each case Keyword
    for keyword in range(0, len(caseKeywords)):
        data[re.sub('[:]', "", caseKeywords[keyword])] = []

def searchHTML(readPath, searchFor):
    #Source: https://pynative.com/python-search-for-a-string-in-text-files/#:~:text=Open%20a%20file%20in%20a,current%20line%20and%20line%20number.
    with open(readPath, 'r') as file:
        for lineNumber, line in enumerate(file):
            if str(searchFor) in line:
                return(lineNumber)
                break

def harvestData(readPath, caseKeywords):
    #Party/Attorney Info (ln 357 - ln 367 in test pag)
    #"aria-live" is the indicator because of its close proximity to the Part/Attorney Info
    #Source: https://stackoverflow.com/a/16432254
    for num in range(10):
        if num != 6:
            #replace unwanted characters
            print(re.sub("[;/]", " ", (re.sub("[<td>&nbspr]", "", (str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + 4)))))))
            pass

    #Case Summary Info (ln 277 - ln 302 in test page)
    for info in caseKeywords:
        #Check and see if caseKeyword is in the HTML file
        if str(searchHTML(readPath, info)) != "None":
            #Add the data into the "data" dictionary after removing unwanted characters
            data[re.sub("[:]", "", info)].append(re.sub("[/]", " ", re.sub("[<td>\n]", "", (linecache.getline(readPath, searchHTML(readPath, info) + 2)))))
        else:
            data[re.sub("[:]", "", info)].append("")
    return str(re.sub("[</]", " ", (re.sub("[td>&nbsp;rd]", "", (linecache.getline(readPath, searchHTML(readPath, "aria-live") + 4))))))



formatExcelSheet(caseKeywords, writePath)
print("\n" + "Data 1: " + str(data))
companyName = harvestData(readPath, caseKeywords)
print("\n" + "Data 2: " + str(data))
print("\n" + "Company name: " + companyName)


#DEV NOTES/TO DO

#Find a better way to consolidate the data from Party/Attorney Info and Case Summary Info
#Add in a way to create a new excel sheet based off of input data
#Auto format the new excel sheet
#Create a way to make and add to the dictionary without having to access and modify the code
#Actually take the dictionary and export it into excel

#TLDR: MAKE IT AS AUTOMATED AS POSSIBLE!#TLDR: MAKE IT AS AUTOMATED AND EFFICIENT AS POSSIBLE!
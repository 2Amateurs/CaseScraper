import linecache
import re
import pandas as pd
from openpyxl import load_workbook
from datetime import date

#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
readPath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts.html" 
writePath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts Output.xlsx"
companyName = "MIDLAND"  #PLACEHOLDER
beginDate = "Year/Month/Date" #PLACEHOLDER
caseKeywords = ["Case Number:", "Court:", "Case Caption:", "Judge:", "Filed Date:", "Case Type", "Amount:"]

def searchHTML(readPath, searchFor):
#https://pynative.com/python-search-for-a-string-in-text-files/#:~:text=Open%20a%20file%20in%20a,current%20line%20and%20line%20number.
    with open(readPath, 'r') as file:
        for lineNumber, line in enumerate(file):
            if str(searchFor) in line:
                return(lineNumber)
                break

def harvestData(readPath, caseKeywords, number):
#Party/Attorney Info
#"aria-live" is the indicator that I used since that's right above where the party/attorney info is
#https://stackoverflow.com/a/16432254
    for num in range(11):
        if num != 7:
            print(re.sub("[</td>&nbspr;]", "", (str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + 3)))))
            

    #Case Summary Info
    for info in caseKeywords:
        print(re.sub("[</td>]", "", (str(linecache.getline(readPath, searchHTML(readPath, info) + 2)))))

harvestData(readPath, caseKeywords, 0)

def formatExcelSheet(caseKeywords, writePath):
#https://saturncloud.io/blog/how-to-append-a-pandas-dataframe-to-an-excel-sheet-a-comprehensive-guide/
    data = {}
    for keyword in range(0, len(caseKeywords)):
        data[re.sub('[:"]', "", caseKeywords[keyword])] = ""
    print(data)

"""    df = pd.DataFrame(data)
    df.to_excel(writePath)"""

formatExcelSheet(caseKeywords, writePath)


#DEV NOTES

#Add in a way to create a new excel sheet based off of input data
#Auto format the new excel sheet
#Create a way to make and add to the dictionary without having to access and modify the code
#Actually take the dictionary and export it into excel

#TLDR: MAKE IT AS AUTOMATED AS POSSIBLE!
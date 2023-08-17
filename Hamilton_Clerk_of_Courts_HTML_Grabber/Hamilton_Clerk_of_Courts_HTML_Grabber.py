import time
start_time = time.time()
import linecache
import re
import pandas as pd
import os
from datetime import date

#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
readFolder = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Data\Hamilton County Clerk of Courts"
readPath = readFolder + r"\Hamilton County Clerk of Courts "  #I'm using Case# 23CV17209 for testing
writePath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Hamilton_Clerk_of_Courts_HTML_Grabber\Output\ " #The space here is NECESSARY so that it can terminate the string 
countyName = "Hamilton" #PLACEHOLDER
companyNames = "" #PLACEHOLDER
dateToday = str(date.today())
caseKeywords = ["Case Number:", "Court:", "Case Caption:", "Judge:", "Filed Date:", "Case Type", "Nuts", "Amount:", "Bananas:"] #"Nut" and "Bannanna:" was/is used to test for unfindable keywords
partyCaseKeywords = ["Plaintiff Name", "Plaintiff Address", "Party", "Attorney", "Attorney Address", "Court ID", "Defendant Name", "Defendant Address", "Defendant Party"]
data = {}

def createDictionary(caseKeywords, partyCaseKeywords):
    #Source: https://sparkbyexamples.com/pandas/pandas-write-to-excel-with-examples/#:~:text=Use%20pandas%20to_excel()%20function,sheet%20name%20to%20write%20to.
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
    global companyNames 
    linebreak = 0
    skip = 0
    #Case Summary Info (ln 277 - ln 302 in test page)
    for info in caseKeywords:
        #Check and see if caseKeyword is in the HTML file
        if str(searchHTML(readPath, info)) != "None":
            if info == "Court:":
                data[re.sub("[:]", "", info)].append(re.sub("[/]", " ", re.sub("[<td>%\n]", "", (linecache.getline(readPath, searchHTML(readPath, info) + 2)))) + "Court of " + countyName + " County")
            else:
                if re.sub("[/]", " ", re.sub("[<td>%\n]", "", (linecache.getline(readPath, searchHTML(readPath, info) + 2)))).find("CERTIFICATE OF JUDGMENT ") != -1 or re.sub("[/]", " ", re.sub("[<td>%\n]", "", (linecache.getline(readPath, searchHTML(readPath, info) + 2)))).find("NOTICE OF APPEAL ") != -1:
                    skip = 1
                #Add the data into the "data" dictionary after removing unwanted characters
                data[re.sub("[:]", "", info)].append(re.sub("[/]", " ", re.sub("[<td>%\n]", "", (linecache.getline(readPath, searchHTML(readPath, info) + 2)))))
        else:
            data[re.sub("[:]", "", info)].append("")
#Party/Attorney Info (ln 357 - ln 367 in test pag)
    #"aria-live" is the indicator because of its close proximity to the Part/Attorney Info
    #Source: https://stackoverflow.com/a/16432254
    for num in range(0, len(partyCaseKeywords)):
        line = str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + linebreak + 4))
        while len(line) > 1 and line[-2] == "=":
            linebreak += 1
            line = str(line[:-2]) + str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + linebreak + 4))
        if str(line) != '</tr><tr role=3D"row" class=3D"even">' + "\n" and str(line) != "" and str(line) != '<td colspan=3D"3"></td>' + "\n":
            data[partyCaseKeywords[num]].append((re.sub("[;r/=]", " ", (re.sub("[<td>&nbspamp%\n]", "", line)))))
        else:
            linebreak += 1
            line = str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + linebreak + 4))
            data[partyCaseKeywords[num]].append((re.sub("[;/=]", " ", (re.sub("[<td>&nbspamp%\n]", "", line)))))
    if skip == 1:
        for keyword in range(0, len(partyCaseKeywords)):
            data[re.sub('[:]', "", partyCaseKeywords[keyword])].pop(-1)
        for keyword in range(0, len(caseKeywords)):
            data[re.sub('[:]', "", caseKeywords[keyword])].pop(-1)

def exportToExcel(data, writePath, countyName, companyName, dateToday):
    dataFrame = pd.DataFrame(data)
    dataFrame.to_excel(str(re.sub("[ ]", "", writePath)) + " " + countyName + " " + companyName + " " + dateToday + ".xlsx")

createDictionary(caseKeywords, partyCaseKeywords)
# print("\n" + "Created (but empty) Excel Sheet: ")
# for key, value in data.items():
#     print(key, value)
# print("\n" + "Harvested Data: ")
#String addition but easier.  Source: https://stackoverflow.com/questions/997797/what-does-s-mean-in-a-python-format-string
for number in range(1, len(os.listdir(readFolder)) + 1):
#for number in range(36, 36 + 1):  # this is used to test single files or a certain range of files
    harvestData(readPath + str(number) + ".mhtml", caseKeywords, partyCaseKeywords)
# for key, value in data.items():
#     print(key, value)
exportToExcel(data, writePath, countyName, companyNames, dateToday)

print("Process finished --- %s seconds ---" % (time.time() - start_time))
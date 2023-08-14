import linecache
import re
import pandas as pd
import os

#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
readPath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts " #I'm using Case# 23CV17209 for testing
writePath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Output\ " #The space here is NECESSARY so that it can terminate the string 
countyName = "Hamilton" #PLACEHOLDER
companyName = "Midland" #PLACEHOLDER
beginDate = "2023-8-6" #PLACEHOLDER
endDate = "2023-8-12" #PLACEHOLDER
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

def exportToExcel(data, writePath, countyName, companyName, beginDate, endDate):
    dataFrame = pd.DataFrame(data)
    dataFrame.to_excel(str(re.sub("[ ]", "", writePath)) + " " + countyName + " " + companyName + " " + beginDate + " to " + endDate + ".xlsx")

createDictionary(caseKeywords, partyCaseKeywords)
print("\n" + "Created (but empty) Excel Sheet: ")
for key, value in data.items():
    print(key, value)
print("\n" + "Harvested Data: ")
#for number in range(1, len(os.listdir(r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber")) + 1):
for number in range(1, 2 + 1):  # this is used since the current directory has other files that'll break the for loop
    harvestData(readPath + str(number) + ".html", caseKeywords, partyCaseKeywords)
for key, value in data.items():
    print(key, value)
exportToExcel(data, writePath, countyName, companyName, beginDate, endDate)
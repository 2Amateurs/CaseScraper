import time
start_time = time.time()
import linecache
import re
import pandas as pd
import os
from datetime import date

#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
readFolder = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Data\Montgomery County Clerk of Courts"
readPath = readFolder + r"\Montgomery County Clerk of Courts "  #I'm using Case# 23CV17209 for testing
writePath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Montgomery_Clerk_of_Courts_HTML_Grabber\Output\ " #The space here is NECESSARY so that it can terminate the string 
countyName = "Montgomery" #PLACEHOLDER
companyNames = "" #PLACEHOLDER
dateToday = str(date.today())

#party then summary
keyDictionary = {
    #Party:
    "Plaintiff Name": "PLAINTIFF", 
    "Plaintiff Address": "Address:", 
    "Party": "Null", 
    "Attorney": "Attorney:", #REMEMBER TO SUBSTITUTE THE "(s)"
    "Attorney Address": "<br>", 
    "Court ID": "Null", 
    "Defendant Name": "DEFENDANT", 
    "Defendant Address": "Address", 
    "Defendant Party": "Null", 

    #Summary:
    "Case Number": "CaseInf", 
    "Court": "Court:", 
    "Case Caption": "Null", 
    "Judge": "Null", 
    "Filed Date": "File Date:", 
    "Case Type": "Null", 
    "Nuts": "nuts", 
    "Amount": "Null", 
    "Bananas":"bananas" 
    }

#{'Plaintiff Name', 'Plaintiff Address', 'Party', 'Attorney', 'Attorney Address', 'Court ID', 'Defendant Name', 'Defendant Address', 'Defendant Party', 'Case Number', 'Court', 'Case Caption', 'Judge', 'Filed Date', 'Case Type', 'Nuts', 'Amount', 'Bananas'}
caseSummaryKeywords = ["PLAINTIFF", "DEFENDANT", "File Date:", "Nuts", "Court:", "Bananas:"] #"Nut" and "Bannanna:" was/is used to test for unfindable keywords
casePartyKeywords = ["Plaintiff Address", "Attorney", "Nuts", "Defendant Address", "Bananas:"]
data = {}

testString = "120340567089"
print(testString[1:])
print(testString[-1:])
print(testString[:1])
print(testString[:-1])
print(testString.find("0"))
testValue = 4/9
print(testValue)
testValue = round(testValue)
print(testValue)
print("\n")


def createDictionary(Keys):
    print("\nStart createDictionary:")
    #Adds new dictionary keys for each case Keyword
    for keyword in Keys:
        data[keyword] = []

def searchHTML(readPath, identifierString):
    with open(readPath, 'r') as file:
        for lineNumber, line in enumerate(file):
            if str(identifierString) in line:
                return(lineNumber + 1)

createDictionary(keyDictionary)
filenum = "6"
partyOrSummary = "Party"
filePath = readPath + partyOrSummary + " " + str(filenum) + ".mhtml"
linenum = searchHTML(filePath, "caseInfo_" + partyOrSummary)

# linenum = searchHTML(readPath + "Summary " + str(filenum) + ".mhtml", "caseInfo_Summary")
# print(linenum)
# print(linecache.getline(readPath + "Summary " + str(filenum) + ".mhtml", linenum))
# print(linecache.getline(readPath + "Summary " + str(filenum) + ".mhtml", linenum)[-2])


def makeLine(filePath):
    # print("\nStart makeLine:")
    linebreak = 0
    while str(linecache.getline(filePath, linenum + linebreak)[-2]) != "=":
        linebreak += 1
    line = str(linecache.getline(filePath, linenum + linebreak))[:-2]
    while str(linecache.getline(filePath, linenum + linebreak)[-2]) == "=":
        linebreak += 1
        line += str(linecache.getline(filePath, linenum + linebreak))[:-2]
    return(line)

print(makeLine(filePath))
# print(keyDictionary.keys())
# print(list(keyDictionary.keys())[0])
def harvestData():
    print("\nStart harvest Data:")
    line = makeLine(filePath)
    # print(list(keyDictionary.values())[0])
    for keyword in list(keyDictionary.values()):
        print("|")
        print(keyword)
        print(int(line.find(keyword)))
        if line.find(keyword) != -1:
            if keyword == "PLAINTIFF" or keyword == "DEFENDANT":
                line = line[int(line.find("<strong>")) + 8:]
                print(re.sub("[b]", " ", re.sub("[<r>]", "",line[:int(line.find("</strong>"))])))
                print("|\n")
            elif keyword == "Attorney:":
                line = line[int(line.find(keyword)) + len(keyword) + 13:]
                print(re.sub("[b]", " ", re.sub("[<r>]", "",line[:int(line.find("<br>"))])))
                print("|\n")
            else:
                line = line[int(line.find(keyword)) + len(keyword) + (round(len(keyword)/9) * 13):]
                print(re.sub("[b]", " ", re.sub("[<r>]", "",line[:int(line.find("</div>"))])))
                print("|\n")
        else:
            print("|\n")
harvestData()

    


#Party info #542 "Party Information" + 2 lines | caseInfo_Party | 
#Summary info #490 "Case Information" and "Judgment Information" | caseInfo_Summary



# createDictionary(caseSummaryKeywords, casePartyKeywords)
# filenum = "3"
# linenum = searchHTML(readPath + "Party " + str(filenum) + ".mhtml", "Address:") + 1
# line = linecache.getline(readPath + "Party " + str(filenum) + ".mhtml", linenum)
# #print(line)
# for info in casePartyKeywords:
#     print(line.find(info))
#     if line.find(info) != -1:
#         for counter in range(0, line.find(info) + len(info) + 1):
#             #Slicing 1st character off of the beginning of the string. Source: https://stackoverflow.com/a/64976733 AND https://www.scaler.com/topics/python-slice/ AND https://docs.python.org/3/library/functions.mhtml?highlight=slice#slice
#             #print(line)
#             line = line[1:]
#         print(line)
#         if line[0] == "s": #Source: https://stackoverflow.com/questions/8848294/how-to-get-char-from-string-by-index
#             line = line[3:]
#         elif line[0]== "<":
#             data[info].append("")
#         line = line[13:]
#     else:
#         pass
#     print(info + "\n")
#     print(line + "\n")
# print(data)

#MAKE SURE TO REMOVE THE "Plaintiff" and "Defendant" FROM THE BEGINNING OF THE ADDRESSES IN caseParty


#def harvestData(readPath, caseKeywords):
#    for info in caseKeywords:
#        print(re.sub("[<tbody id="tblPartyBody"><tr class="table-info"><td><div class="row"><div class="col-md-5"><strong>]", "",searchHTML(readPath, info) + 1), 99)

#    linebreak = 0
#    for info in caseKeywords:
#        #Check and see if caseKeyword is in the HTML file
#        if str(searchHTML(readPath, info)) != "None":
#            #Add the data into the "data" dictionary after removing unwanted characters
#            data[re.sub("[:]", "", info)].append(re.sub("[/]", " ", re.sub("[<td>\n]", "", (linecache.getline(readPath, searchHTML(readPath, info) + 2)))))
#        else:
#            data[re.sub("[:]", "", info)].append("")

##Party/Attorney Info (ln 357 - ln 367 in test pag)
#    #"aria-live" is the indicator because of its close proximity to the Part/Attorney Info
#    #Source: https://stackoverflow.com/a/16432254
#    for num in range(0, len(partyCaseKeywords)):
#        if str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + 4)) != '</tr><tr role="row" class="even">\n':
#            #replace unwanted characters
#            #print(re.sub("[;/]", " ", (re.sub("[<td>&nbspr]", "", (str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + linebreak + 4)))))))
#            data[partyCaseKeywords[num]].append((re.sub("[;/]", " ", (re.sub("[<td>&nbspr\n]", "", (str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + linebreak + 4))))))))
#        else:
#            linebreak = 1
#            data[partyCaseKeywords[num]].append((re.sub("[;/]", " ", (re.sub("[<td>&nbspr\n]", "", (str(linecache.getline(readPath, searchHTML(readPath, "aria-live") + num + 5))))))))

#def exportToExcel(data, writePath, countyName, companyName, beginDate, endDate):
#    dataFrame = pd.DataFrame(data)
#    dataFrame.to_excel(str(re.sub("[ ]", "", writePath)) + " " + countyName + " " + companyName + " " + beginDate + " to " + endDate + ".xlsx")

#createDictionary(caseSummaryKeywords, partyCaseKeywords)
#print("\n" + "Created (but empty) Excel Sheet: ")
#for key, value in data.items():
#    print(key, value)
#print("\n" + "Harvested Data: ")

#for number in range(1, len(os.listdir(r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber")) + 1):
#for number in range(1, 2 + 1):  # this is used since the current directory has other files that'll break the for loop
#    harvestData(readPartyPath + "Party " + str(number) + ".mhtml", partyCaseKeywords)
#    harvestData(readSummaryPath + "Summary " + str(number) + ".mhtml", caseSummaryKeywords)


#for key, value in data.items():
#    print(key, value)


#exportToExcel(data, writePath, countyName, companyName, beginDate, endDate)

print("Process finished --- %s seconds ---" % (time.time() - start_time))
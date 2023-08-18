import time
start_time = time.time()
import linecache
import re
import pandas as pd
import os
import datetime

#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
readFolder = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Data\Montgomery County Clerk of Courts"
readPath = readFolder + r"\Montgomery County Clerk of Courts "  #I'm using Case# 23CV17209 for testing
writePath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Montgomery_Clerk_of_Courts_HTML_Grabber\Output\ " #The space here is NECESSARY so that it can terminate the string 
countyName = "Montgomery" #PLACEHOLDER
endDate = datetime.date.today()
startDate = str((endDate - datetime.timedelta(days=7)).isoformat())
#party then summary
keyDictionary = {
    #Party:
    "Plaintiff Name": "PLAINTIFF", 
    "Plaintiff Address": "Address:", 
    "Party": "Party", 
    "Attorney": "Attorney:", #REMEMBER TO SUBSTITUTE THE "(s)"
    "Attorney Address": "<br>", 
    "Court ID": "Court ID", 
    "Defendant Name": "DEFENDANT", 
    "Defendant Address": "Address", 
    "Defendant Party": "Defendant Party", 

    #Summary:
    "Case Number": "CaseInf", 
    "Court": "Court:", 
    "Case Caption": "Case Caption", 
    "Judge": "Judge", 
    "Filed Date": "File Date:", 
    "Case Type": "Case Type", 
    "Nuts": "nuts", 
    "Amount": "Amount", 
    "Bananas":"bananas" 
    }

#{'Plaintiff Name', 'Plaintiff Address', 'Party', 'Attorney', 'Attorney Address', 'Court ID', 'Defendant Name', 'Defendant Address', 'Defendant Party', 'Case Number', 'Court', 'Case Caption', 'Judge', 'Filed Date', 'Case Type', 'Nuts', 'Amount', 'Bananas'}
caseSummaryKeywords = ["PLAINTIFF", "DEFENDANT", "File Date:", "Nuts", "Court:", "Bananas:"] #"Nut" and "Bannanna:" was/is used to test for unfindable keywords
casePartyKeywords = ["Plaintiff Address", "Attorney", "Nuts", "Defendant Address", "Bananas:"]
data = {}

# testString = "120340567089"
# print(testString[1:])
# print(testString[-1:])
# print(testString[:1])
# print(testString[:-1])
# print(testString.find("0"))
# testValue = 4/9
# print(testValue)
# testValue = round(testValue)
# print(testValue)
# print(keyDictionary["Plaintiff Name"])
# print(list(keyDictionary.keys())[list(keyDictionary.values()).index("PLAINTIFF")])

# print("\n")


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

def makeLine(filePath, lineNum):
    # print("\nStart makeLine:")
    linebreak = 0
    while str(linecache.getline(filePath, lineNum + linebreak)[-2]) != "=":
        linebreak += 1
    line = str(linecache.getline(filePath, lineNum + linebreak))[:-2]
    while str(linecache.getline(filePath, lineNum + linebreak)[-2]) == "=":
        linebreak += 1
        line += str(linecache.getline(filePath, lineNum + linebreak))[:-2]
    return(line)

def harvestData(readPath, filenum):
    print("\nStart harvest Data:")
    switchPage = "Party"
    filePath = readPath + switchPage + " " + str(filenum) + ".mhtml"
    lineNum = searchHTML(filePath, "caseInfo_" + switchPage)
    line = makeLine(readPath + switchPage + " " + str(filenum) + ".mhtml", lineNum)
    # print(list(keyDictionary.values())[0])
    for keyword in list(keyDictionary.values()):
        if list(keyDictionary.values())[9] == keyword:
            switchPage = "Summary"
            filePath = readPath + switchPage + " " + str(filenum) + ".mhtml"
            lineNum = searchHTML(filePath, "CaseInf")
            line = makeLine(readPath + switchPage + " " + str(filenum) + ".mhtml", lineNum)
            print("switched")
        print("|")
        print(keyword)
        print(int(line.find(keyword)))
        if line.find(keyword) != -1:
            if switchPage == "Party":
                if keyword == "PLAINTIFF" or keyword == "DEFENDANT":
                    line = line[int(line.find("<strong>")) + 8:]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</strong>"))])))
                    print(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</strong>"))])))
                    # data[partyCaseKeywords[num]].append(
                    print("|\n")
                elif keyword == "Attorney:":
                    line = line[int(line.find(keyword)) + len(keyword) + 13:]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("<br>"))])))
                    print(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("<br>"))])))
                    print("|\n")
                else:
                    line = line[int(line.find(keyword)) + len(keyword) + (round(len(keyword)/9) * 13):]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</div>"))])))
                    print(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</div>"))])))
                    print("|\n")
            else:
                if keyword == "CaseInf":
                    lineNum = searchHTML(filePath, keyword)
                    line = makeLine(readPath + switchPage + " " + str(filenum) + ".mhtml", lineNum)
                    line = line[int(line.find("CaseInfo")) + 9:]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;span/>]", "",line)))
                    print(re.sub("[b]", " ", re.sub("[<r&amp;span/>]", "",line)))

                    lineNum = searchHTML(filePath, "caseInfo_" + switchPage)
                    line = makeLine(readPath + switchPage + " " + str(filenum) + ".mhtml", lineNum)
                    print("|\n")
                else:
                    line = line[int(line.find(keyword)) + len(keyword) + 9:]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</td>"))])))
                    print(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</td>"))])))
                    print("|\n")
        else:
            if keyword == "PLAINTIFF":
                break
            data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append("")
            print("|\n")

def exportToExcel(data, writePath, countyName, startDate, endDate):
    dataFrame = pd.DataFrame(data)
    dataFrame.to_excel(str(re.sub("[ ]", "", writePath)) + countyName + " " + str(startDate) + " to " + str(endDate) + ".xlsx")

createDictionary(keyDictionary)
# filenum = "6"
# partyOrSummary = "Party"
# filePath = readPath + partyOrSummary + " " + str(filenum) + ".mhtml"
# lineNum = searchHTML(filePath, "caseInfo_" + partyOrSummary)
# harvestData(readPath, filenum)
# print(data)
for number in range(1, int((len(os.listdir(readFolder)) / 2)) + 1):
    harvestData(readPath, number)
print(data)
exportToExcel(data, writePath, countyName, startDate, str(endDate))

print("Process finished --- %s seconds ---" % (time.time() - start_time))
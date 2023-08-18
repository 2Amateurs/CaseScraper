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

def createDictionary(Keys):
    #Adds new dictionary keys for each case Keyword
    for keyword in Keys:
        data[keyword] = []

def searchHTML(readPath, identifierString):
    with open(readPath, 'r') as file:
        for lineNumber, line in enumerate(file):
            if str(identifierString) in line:
                return(lineNumber + 1)

def makeLine(filePath, lineNum):
    linebreak = 0
    while str(linecache.getline(filePath, lineNum + linebreak)[-2]) != "=":
        linebreak += 1
    line = str(linecache.getline(filePath, lineNum + linebreak))[:-2]
    while str(linecache.getline(filePath, lineNum + linebreak)[-2]) == "=":
        linebreak += 1
        line += str(linecache.getline(filePath, lineNum + linebreak))[:-2]
    return(line)

def harvestData(readPath, filenum):
    switchPage = "Party"
    filePath = readPath + switchPage + " " + str(filenum) + ".mhtml"
    lineNum = searchHTML(filePath, "caseInfo_" + switchPage)
    line = makeLine(readPath + switchPage + " " + str(filenum) + ".mhtml", lineNum)
    for keyword in list(keyDictionary.values()):
        if list(keyDictionary.values())[9] == keyword:
            switchPage = "Summary"
            filePath = readPath + switchPage + " " + str(filenum) + ".mhtml"
            lineNum = searchHTML(filePath, "CaseInf")
            line = makeLine(readPath + switchPage + " " + str(filenum) + ".mhtml", lineNum)
        if line.find(keyword) != -1:
            if switchPage == "Party":
                if keyword == "PLAINTIFF" or keyword == "DEFENDANT":
                    line = line[int(line.find("<strong>")) + 8:]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</strong>"))])))
                elif keyword == "Attorney:":
                    line = line[int(line.find(keyword)) + len(keyword) + 13:]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("<br>"))])))
                else:
                    line = line[int(line.find(keyword)) + len(keyword) + (round(len(keyword)/9) * 13):]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</div>"))])))
            else:
                if keyword == "CaseInf":
                    lineNum = searchHTML(filePath, keyword)
                    line = makeLine(readPath + switchPage + " " + str(filenum) + ".mhtml", lineNum)
                    line = line[int(line.find("CaseInfo")) + 9:]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;span/>]", "",line)))

                    lineNum = searchHTML(filePath, "caseInfo_" + switchPage)
                    line = makeLine(readPath + switchPage + " " + str(filenum) + ".mhtml", lineNum)
                else:
                    line = line[int(line.find(keyword)) + len(keyword) + 9:]
                    data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append(re.sub("[b]", " ", re.sub("[<r&amp;>ion/thedy]", "",line[:int(line.find("</td>"))])))
        else:
            if keyword == "PLAINTIFF":
                break
            data[list(keyDictionary.keys())[list(keyDictionary.values()).index(keyword)]].append("")

def exportToExcel(data, writePath, countyName, startDate, endDate):
    dataFrame = pd.DataFrame(data)
    dataFrame.to_excel(str(re.sub("[ ]", "", writePath)) + countyName + " " + str(startDate) + " to " + str(endDate) + ".xlsx")

createDictionary(keyDictionary)
for number in range(1, int((len(os.listdir(readFolder)) / 2)) + 1):
    harvestData(readPath, number)
exportToExcel(data, writePath, countyName, startDate, str(endDate))

print("Process finished --- %s seconds ---" % (time.time() - start_time))
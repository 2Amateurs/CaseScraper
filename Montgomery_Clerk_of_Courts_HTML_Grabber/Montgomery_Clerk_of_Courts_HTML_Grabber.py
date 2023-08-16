import linecache
import re
import pandas as pd
import os

#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
readPartyPath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Montgomery_Clerk_of_Courts_HTML_Grabber\Montgomery County Clerk of Courts " 
readSummaryPath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Montgomery_Clerk_of_Courts_HTML_Grabber\Montgomery County Clerk of Courts "
writePath = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\Montgomery_Clerk_of_Courts_HTML_Grabber\Output\ " #The space here is NECESSARY so that it can terminate the string 
countyName = "Montgomery" #PLACEHOLDER
companyName = "Midland" #PLACEHOLDER
beginDate = "2023-8-6" #PLACEHOLDER
endDate = "2023-8-12" #PLACEHOLDER
caseSummaryKeywords = ["CREDITOR", "DEBTOR", "File Date:", "Nuts", "Court:", "Bananas:"] #"Nut" and "Bannanna:" was/is used to test for unfindable keywords
casePartyKeywords = ["Plaintiff Address", "Attorney", "Nuts", "Defendant Address", "Bananas:"]
data = {}

def createDictionary(caseSummaryKeywords, casePartyKeywords):
    #Source: https://sparkbyexamples.com/pandas/pandas-write-to-excel-with-examples/#:~:text=Use%20pandas%20to_excel()%20function,sheet%20name%20to%20write%20to.
    #Adds new dictionary keys for each case Keyword
    for keyword in range(0, len(casePartyKeywords) - 1):
        data[re.sub('[:]', "", casePartyKeywords[keyword])] = []
    for keyword in range(0, len(caseSummaryKeywords) - 1):
        data[re.sub('[:]', "", caseSummaryKeywords[keyword])] = []        
        print(str(keyword))
        print(casePartyKeywords[keyword])
        # if str(keyword[-2]) != "s":
        #     data[re.sub('[:]', "", caseSummaryKeywords[keyword])] = []
        # else:
        #     print("NOPE")





#1: 2023 CVF 00952 W
#2: 2023 CVF 00949 W
#3: 2023 CJ 222904
#Summary info #490 "Case Information" and "Judgment Information"
#Party info #542 "Party Information" + 2 lines





def searchHTML(readPath, searchFor):
    #Source: https://pynative.com/python-search-for-a-string-in-text-files/#:~:text=Open%20a%20file%20in%20a,current%20line%20and%20line%20number.
    with open(readPath, 'r') as file:
        for lineNumber, line in enumerate(file):
            if str(searchFor) in line:
                return(lineNumber)
                break

createDictionary(caseSummaryKeywords, casePartyKeywords)
filenum = "3"
linenum = searchHTML(readPartyPath + "Party " + str(filenum) + ".mhtml", "Address:") + 1
line = linecache.getline(readPartyPath + "Party " + str(filenum) + ".mhtml", linenum)
#print(line)
for info in casePartyKeywords:
    print(line.find(info))
    if line.find(info) != -1:
        for counter in range(0, line.find(info) + len(info) + 1):
            #Slicing 1st character off of the beginning of the string. Source: https://stackoverflow.com/a/64976733 AND https://www.scaler.com/topics/python-slice/ AND https://docs.python.org/3/library/functions.mhtml?highlight=slice#slice
            #print(line)
            line = line[1:]
        print(line)
        if line[0] == "s": #Source: https://stackoverflow.com/questions/8848294/how-to-get-char-from-string-by-index
            line = line[3:]
        elif line[0]== "<":
            data[info].append("")
        line = line[13:]
    else:
        pass
    print(info + "\n")
    print(line + "\n")
print(data)

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
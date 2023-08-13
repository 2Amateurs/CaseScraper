import linecache
import re
#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
path = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts.html" 
caseKeywords = ["Case Number:", "Court:", "Case Caption:", "Judge:", "Filed Date:", "Case Type", "Amount:"]

def searchHTML(path, searchFor):
#https://pynative.com/python-search-for-a-string-in-text-files/#:~:text=Open%20a%20file%20in%20a,current%20line%20and%20line%20number.
    with open(path, 'r') as file:
        for lineNumber, line in enumerate(file):
            if str(searchFor) in line:
                return(lineNumber)
                break

def harvestData(path, caseKeywords):
#Party/Attorney Info
#"aria-live" is the indicator that I used since that's right above where the party/attorney info is
#https://stackoverflow.com/a/16432254
    for num in range(11):
        if num != 7:
            print(re.sub("[</td>&nbspr;]", "", (str(linecache.getline(path, searchHTML(path, "aria-live") + num + 3)))))

    #Case Summary Info
    for info in caseKeywords:
        print(re.sub("[</td>]", "", (str(linecache.getline(path, searchHTML(path, info) + 2)))))

harvestData(path, caseKeywords)
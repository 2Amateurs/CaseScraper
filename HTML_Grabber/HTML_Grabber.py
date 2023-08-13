import linecache
import re
#The "r" is neccesary because it converts a normal string to a raw string. See https://stackoverflow.com/questions/37400974/error-unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3
path = r"C:\Users\profs\Desktop\Joshua\CaseScraper\CaseScraper\HTML_Grabber\Hamilton County Clerk of Courts.html" 

#https://pynative.com/python-search-for-a-string-in-text-files/#:~:text=Open%20a%20file%20in%20a,current%20line%20and%20line%20number.
def searchHTML(path, searchFor):
    with open(path, 'r') as filePath:
        for lineNumber, line in enumerate(filePath):
            if str(searchFor) in line:
                return(lineNumber)
                break

def removeHTMLFormatting(line):
    return(re.sub("[</td>&nbspr;]", "", line))


#"aria-live" is the indicator that I used since that's right above where the party/attourney info is
#https://stackoverflow.com/a/16432254
for num in range(11):
    if num != 7:
        print(removeHTMLFormatting(str(linecache.getline(path, searchHTML(path, "aria-live") + num + 3))))
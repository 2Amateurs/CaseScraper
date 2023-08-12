from urllib.request import *
def getHTML(url):
    page = urlopen(url) #Store the URL
    html_bytes = page.read() #Explanation here -> https://docs.python.org/3/library/urllib.request.html#examples
    html = html_bytes.decode("utf-8") 
    return(html)

print("START \n \n")
print(getHTML("https://www.courtclerk.org/data/case_summary.php?sec=party&casenumber=23CV16448&submit.x=23&submit.y=21"))
print("\n \n END")
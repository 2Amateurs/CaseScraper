import re
from inspect import signature

import pandas as pd
from bs4 import BeautifulSoup


class KeywordMatch:
    """
    This class describes a match found by the html search engine.
    """
    def __init__(self, key: str, value: str):
        """
        :param key: The dictionary key that corresponds to the matched item
        :param value: The value of the matched item.  It will be assigned to the data dictionary with the 'key' variable
        """
        self.key = key
        self.value = value


class MatchConverter:
    """
    This is a class that has one variable: a function called convert that takes a string as a parameter and returns a KeywordMatch array.
    Text values from tags found by a KeywordMatch instance will be passed into this function (which can be whatever you want it to be).
    Using the defaultConverter method will generate an instance of this class with a convert that takes the value and simply makes a
    KeywordMatch instance with the desired key and the raw value.  However, by passing your own function, you can make something that takes
    text from a specific area and returns several KeywordMatches.  For instance, your match may return text from an html element that contains
    both 'Address' and 'Amount' information.  Your function would take this text, split up the data, and return two instances of KeywordMatch:
    1) A KeywordMatch object with the key set to 'Amount' and the value set to whatever the amount is.
    2) A KeywordMatch object with the key set to 'Address' and whatever the address is.

    Remember that the only requirement for an instance of this class is that the convert function takes only 1 parameter.  Thus, you could also
    process your data with regular expressions.
    """
    def __init__(self, convert):  # The convert function will take the inner text of the html node and return a list of KeywordMatches
        if len(signature(convert).parameters) == 1:
            self.convert = convert
        else:
            raise ValueError("The convert function must accept only 1 parameter")

    @staticmethod
    def defaultConverter(key):
        return MatchConverter(lambda value: [KeywordMatch(key, value)])


class KeywordPattern:
    """
    This class describes the type of pattern you want the html searcher to find.  The searcher will find a match if an element from the html string
    contains a sequence identical to that described by the 'keyword' variable of an instance of this class.  All html tags are listed in an array;
    thus, if you want to grab a tag 7 slots down from the tag that matches the keyword variable, set the indexOffset variable to the desired value.
    """
    def __init__(self, keyword: str, matchConverter: MatchConverter, indexOffset: int = 0):
        """
        :param keyword: The keyword to be searched for in the html string
        :param matchConverter A MatchConverter object that will process
        :param indexOffset: The amount that the index should be offset from that of the matched tag
        """
        self.keyword = keyword
        self.matchConverter = matchConverter
        self.indexOffset = indexOffset

    def getKeywordMatches(self, tags, matchIndex):  # Returns a KeywordMatch array
        return self.matchConverter.convert(tags[matchIndex + self.indexOffset].text)


class HtmlProcessor:

    @staticmethod
    def getBuilder():
        return HtmlProcessor.Builder()

    class Builder:  # countyName, companyName, startDate, endDate)
        def __init__(self):
            self.readPath = None
            self.writePath = None
            self.companyCaseKeywords = []
            self.partyCaseKeywords = []
            self.countyName = None
            self.companyName = None
            self.startDate = None
            self.endDate = None
            self.filterRegexes = ["<td *>", "</td>"]
            self.fileString = ""
            self.data = {}

        def setReadPath(self, readPath):
            self.readPath = readPath
            return self

        def setWritePath(self, writePath):
            self.writePath = writePath
            return self

        def setCompanyCaseKeywords(self, companyCaseKeywords):
            self.companyCaseKeywords = companyCaseKeywords
            return self

        def addCompanyCaseKeyword(self, companyCaseKeyword):
            self.companyCaseKeywords.append(companyCaseKeyword)
            return self

        def addPartyCaseKeyword(self, partyCaseKeyword):
            self.partyCaseKeywords.append(partyCaseKeyword)
            return self

        def setPartyCaseKeywords(self, partyCaseKeywords):
            self.partyCaseKeywords = partyCaseKeywords
            return self

        def setCountyName(self, countyName):
            self.countyName = countyName
            return self

        def setCompanyName(self, companyName):
            self.companyName = companyName
            return self

        def setBeginDate(self, startDate):
            self.startDate = startDate
            return self

        def setEndDate(self, endDate):
            self.endDate = endDate
            return self

        def setFilterRegex(self, filterRegex):
            self.filterRegexes = filterRegex

        def build(self):
            return HtmlProcessor(self)

    def __init__(self, builder):
        self.dictionary = {"Case Number": "Unavailable", "Court": "Unavailable", "Case Caption": "Unavailable", "Judge": "Unavailable", "Filed Date": "Unavailable",
                           "Case Type": "Unavailable", "Amount": "Unavailable", "Plaintiff Name": "Unavailable", "Plaintiff Address": "Unavailable", "Party": "Unavailable",
                           "Attorney": "Unavailable", "Attorney Address": "Unavailable", "Court ID": "Unavailable", "Defendant Name": "Unavailable",
                           "Defendant Address": "Unavailable", "Defendant Party": "Unavailable"}

        self.fileString = None
        self.readPath = builder.readPath
        self.writePath = builder.writePath
        self.companyCaseKeywords = builder.companyCaseKeywords
        self.partyCaseKeywords = builder.partyCaseKeywords
        self.countyName = builder.countyName
        self.companyName = builder.companyName
        self.startDate = builder.startDate
        self.endDate = builder.endDate
        self.filterRegexes = builder.filterRegexes
        self.data = {}
        self.fileString = self.openFile()
        self.soup = BeautifulSoup(self.fileString, "html.parser")
        self.tags = self.soup.find_all()

    @staticmethod
    def __addToDict(dictionary, keywordMatches):
        for keywordMatch in keywordMatches:
            dictionary[keywordMatch.key] = keywordMatch.value

    def __search(self, *keywordPatternArrays):
        for keywordPatternArray in keywordPatternArrays:
            for keywordPattern in keywordPatternArray:
                for i in range(len(self.tags)):
                    if keywordPattern.keyword in self.tags[i].text :
                        self.__addToDict(self.dictionary, keywordPattern.getKeywordMatches(tags=self.tags, matchIndex=i))

    def parseHTML(self):
        self.__search(self.companyCaseKeywords, self.partyCaseKeywords)
        print(self.dictionary)

    def openFile(self):
        with open(self.readPath, "r") as file:
            return file.read()

    def exportToExcel(self):
        dataFrame = pd.DataFrame(self.data)
        dataFrame.to_excel(str(re.sub(" ", "", self.writePath)) + " " + self.countyName + " " + self.companyName + " " + self.startDate + " to " + self.endDate + ".xlsx")
        pass


#Switching between sites is easy!  Just declare a new processor and build it however you want.
hamiltonHTMLProcessor = HtmlProcessor.getBuilder() \
    .setReadPath(r"/home/geelhood/PycharmProjects/CaseScraper/Data/HTML/week1.html") \
    .setWritePath(r"/Hamilton/Output") \
    .setCompanyCaseKeywords([KeywordPattern("Case Number:", MatchConverter.defaultConverter("Case Number"), 1),
                             KeywordPattern("Court:", MatchConverter.defaultConverter("Court"), 1),
                             KeywordPattern("Case Caption:", MatchConverter.defaultConverter("Case Caption"), 1),
                             KeywordPattern("Judge:", MatchConverter.defaultConverter("Judge"), 1),
                             KeywordPattern("Filed Date:", MatchConverter.defaultConverter("Filed Date"), 1),
                             KeywordPattern("Case Type:", MatchConverter.defaultConverter("Case Type"), 1),
                             KeywordPattern("Amount:", MatchConverter.defaultConverter("Amount"), 1)]) \
    .setPartyCaseKeywords([KeywordPattern("Name", MatchConverter.defaultConverter("Plaintiff Name"), 32), #The hard part is finding the offsets
                           KeywordPattern("Plaintiff Address:", MatchConverter.defaultConverter("Plaintiff Address"), 1),
                           KeywordPattern("Party:", MatchConverter.defaultConverter("Party"), 1),
                           KeywordPattern("Attorney:", MatchConverter.defaultConverter("Attorney"), 1),
                           KeywordPattern("Attorney Address:", MatchConverter.defaultConverter("Attorney Address"), 1),
                           KeywordPattern("Court ID:", MatchConverter.defaultConverter("Court ID"), 1),
                           KeywordPattern("Defendant Name:", MatchConverter.defaultConverter("Defendant Name"), 1),
                           KeywordPattern("Defendant Address:", MatchConverter.defaultConverter("Defendant Address"), 1),
                           KeywordPattern("Defendant Party:", MatchConverter.defaultConverter("Defendant Party"), 1)]) \
    .build()


def main():
    htmlProcessor = hamiltonHTMLProcessor  # Choose whichever processor you need for the job
    htmlProcessor.parseHTML()


if __name__ == "__main__":
    main()

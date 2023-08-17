import linecache
import re
import pandas as pd
from bs4 import BeautifulSoup
from utils.arrayUtils import *


def getBuilder():
    return HtmlProcessor.Builder()


class Keyword:
    def __init__(self, keyword: str, key: str):
        """
        :param keyword: The keyword to be searched for in the html string
        :param key: The key in the dictionary that corresponds to the keyword
        """
        self.keyword = keyword
        self.key = key


class KeywordMatch:
    def __init__(self, key: str, value: str):
        """
        :param key: The dictionary key that corresponds to the matched item
        :param value: The value of the matched item
        """
        self.key = key
        self.value = value


class HtmlProcessor:
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
            self.companyTagIndexOffsets = []
            self.partyTagIndexOffsets = []
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

        def setCompanyTagIndexOffsets(self, companyTagIndexOffsets):
            self.companyTagIndexOffsets = companyTagIndexOffsets
            return self

        def setPartyTagIndexOffsets(self, partyTagIndexOffsets):
            self.partyTagIndexOffsets = partyTagIndexOffsets
            return self

        def setFilterRegex(self, filterRegex):
            self.filterRegexes = filterRegex

        def build(self):
            return HtmlProcessor(self)

    def __init__(self, builder):
        self.companyDictionary = {"Case Number": "Unavailable", "Court": "Unavailable", "Case Caption": "Unavailable", "Judge": "Unavailable", "Filed Date": "Unavailable",
                                  "Case Type": "Unavailable", "Amount": "Unavailable"}
        self.partyDictionary = {"Plaintiff Name": "Unavailable", "Plaintiff Address": "Unavailable", "Party": "Unavailable", "Attorney": "Unavailable",
                                "Attorney Address": "Unavailable", "Court ID": "Unavailable",
                                "Defendant Name": "Unavailable", "Defendant Address": "Unavailable", "Defendant Party": "Unavailable"}
        self.fileString = None
        self.readPath = builder.readPath
        self.writePath = builder.writePath
        self.companyCaseKeywords = builder.companyCaseKeywords
        self.partyCaseKeywords = builder.partyCaseKeywords
        self.countyName = builder.countyName
        self.companyName = builder.companyName
        self.startDate = builder.startDate
        self.endDate = builder.endDate
        self.companyTagIndexOffsets = builder.companyTagIndexOffsets
        self.partyTagIndexOffsets = builder.partyTagIndexOffsets
        self.filterRegexes = builder.filterRegexes
        self.data = {}
        self.fileString = self.openFile()
        self.soup = BeautifulSoup(self.fileString, "html.parser")
        self.tags = self.soup.find_all()

    def __search(self, keywords):  # Prepending __ to a method name in python is equivalent to using a private method in Java
        matches = []
        for keyword in keywords:
            for i in range(len(self.tags)):
                if self.tags[i].text == keyword.keyword:
                    matches.append([keyword.key, i])
                    break  # Breaks out of the inner loop when it finds the first match
        return matches

    @staticmethod  # Using this annotation, it is possible to create methods that do not take a 'self' parameter
    def __offsetIndices(matches: list, offsets: list) -> list:
        for i in range(len(matches)):
            matches[i][1] += offsets[i]
        return matches

    def __toKeywordMatches(self, matches):
        keywordMatches = []
        for match in matches:
            keywordMatches.append(KeywordMatch(match[0], self.tags[match[1]]))
        return keywordMatches

    @staticmethod
    def __removeHTMLFormatting(keywordMatches: list) -> list:
        for i in range(len(keywordMatches)):
            keywordMatches[i].value = re.sub("<.*?>", "", str(keywordMatches[i].value))
            # Using a '?' after the '*' quantifier will tell the regex engine to work in 'lazy' mode, in which it will match as few characters as possible instead of as many
        return keywordMatches

    @staticmethod
    def __addToDict(dictionary, keywordMatches):
        for keywordMatch in keywordMatches:
            dictionary[keywordMatch.key] = keywordMatch.value

        print(dictionary)
        return dictionary

    def parseHTML(self):
        companyIndices = self.__offsetIndices(self.__search(self.companyCaseKeywords), self.companyTagIndexOffsets)
        partyIndices = self.__offsetIndices(self.__search(self.partyCaseKeywords), self.partyTagIndexOffsets)

        companyMatches = self.__removeHTMLFormatting(self.__toKeywordMatches(companyIndices))
        partyMatches = self.__removeHTMLFormatting(self.__toKeywordMatches(partyIndices))

        self.companyDictionary = self.__addToDict(self.companyDictionary, companyMatches)
        self.companyDictionary = self.__addToDict(self.partyDictionary, partyMatches)

    def openFile(self):
        with open(self.readPath, "r") as file:
            return file.read()

    def exportToExcel(self):
        dataFrame = pd.DataFrame(self.data)
        dataFrame.to_excel(str(re.sub(" ", "", self.writePath)) + " " + self.countyName + " " + self.companyName + " " + self.startDate + " to " + self.endDate + ".xlsx")
        pass


hamiltonHTMLProcessor = getBuilder() \
    .setReadPath(r"/home/geelhood/CaseScraper-main/Data/HTML/week1.html") \
    .setWritePath(r"/Hamilton/Output") \
    .setCompanyCaseKeywords([Keyword("Case Number:", "Case Number"), Keyword("Court:", "Court"), Keyword("Case Caption:", "Case Caption"), Keyword("Judge:", "Judge"),
                             Keyword("Filed Date:", "Filed Date"), Keyword("Case Type:", "Case Type"), Keyword("Amount:", "Amount")]) \
    .setPartyCaseKeywords([Keyword("Plaintiff Name:", "Plaintiff Name"), Keyword("Plaintiff Address:", "Plaintiff Address"), Keyword("Party:", "Party"),
                           Keyword("Attorney:", "Attorney"), Keyword("Attorney Address:", "Attorney Address"), Keyword("Court ID:", "Court ID"),
                           Keyword("Defendant Name:", "Defendant Name"), Keyword("Defendant Address:", "Defendant Address"),
                           Keyword("Defendant Party:", "Defendant Party")]) \
    .setCompanyTagIndexOffsets(repeat(1, 7)) \
    .setPartyTagIndexOffsets(repeat(1, 7)) \
    .build()

montgomeryHTMLProcessor = getBuilder() \
    .setReadPath(r"/home/geelhood/CaseScraper-main/Data/HTML/week2.html") \
    .setWritePath(r"/Hamilton/Output") \
    .setCompanyCaseKeywords([Keyword("Foreign Number:", "Case Number"), Keyword("Court:", "Court"), Keyword("Case Caption:", "Case Caption"), Keyword("Judge:", "Judge"),
                             Keyword("Filed Date:", "File Date"), Keyword("Amount", "Amount")]) \
    .setPartyCaseKeywords([Keyword("Plaintiff Name:", "Plaintiff Name"), Keyword("Plaintiff Address:", "Plaintiff Address"), Keyword("Party:", "Party"),
                           Keyword("Attorney:", "Attorney"), Keyword("Attorney Address:", "Attorney Address"), Keyword("Court ID:", "Court ID"),
                           Keyword("Defendant Name:", "Defendant Name"), Keyword("Defendant Address:", "Defendant Address"),
                           Keyword("Defendant Party:", "Defendant Party")]) \
    .setCompanyTagIndexOffsets(repeat(1, 2) + [7]) \
    .setPartyTagIndexOffsets(repeat(1, 7)) \
    .build()

franklinHTMLProcessor = getBuilder() \
    .setReadPath(r"/home/geelhood/CaseScraper-main/Data/HTML/week3.html") \
    .setWritePath(r"/Hamilton/Output") \
    .setCompanyCaseKeywords([Keyword("Case Number:", "Case Number"), Keyword("Court:", "Court"), Keyword("Case Caption:", "Case Caption"), Keyword("Judge:", "Judge"),
                             Keyword("Filed Date:", "Filed Date"), Keyword("Case Type:", "Case Type"), Keyword("Total Amount", "Amount")]) \
    .setPartyCaseKeywords([Keyword("Plaintiff Name:", "Plaintiff Name"), Keyword("Plaintiff Address:", "Plaintiff Address"), Keyword("Party:", "Party"),
                           Keyword("Attorney:", "Attorney"), Keyword("Attorney Address:", "Attorney Address"), Keyword("Court ID:", "Court ID"),
                           Keyword("Defendant Name:", "Defendant Name"), Keyword("Defendant Address:", "Defendant Address"),
                           Keyword("Defendant Party:", "Defendant Party")]) \
    .setCompanyTagIndexOffsets(repeat(1, 0) + [2]) \
    .setPartyTagIndexOffsets(repeat(1, 7)) \
    .build()


def main():
    htmlProcessor = franklinHTMLProcessor  # Choose whichever processor you need for the job
    htmlProcessor.parseHTML()


if __name__ == "__main__":
    main()

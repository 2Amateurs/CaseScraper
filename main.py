import enum
import re
import pandas as pd
from bs4 import BeautifulSoup
from utils.arrayUtils import *
from inspect import signature
from abc import abstractmethod


class KeywordMatch:
    def __init__(self, key: str, value: str):
        """
        :param key: The dictionary key that corresponds to the matched item
        :param value: The value of the matched item
        """
        self.key = key
        self.value = value


class MatchConverter:
    def __init__(self, convert):  # The convert function will take the inner text of the html node and return a list of KeywordMatches
        if len(signature(convert).parameters) == 1:
            self.convert = convert
        else:
            raise ValueError("The convert function must accept only 1 parameter")

    @staticmethod
    def defaultConverter(key):
        return MatchConverter(lambda value: [KeywordMatch(key, value)])


class KeywordPattern:
    def __init__(self, keyword: str, matchConverter: MatchConverter, indexOffset: int = 0):
        """
        :param keyword: The keyword to be searched for in the html string
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
        self.companyTagIndexOffsets = builder.companyTagIndexOffsets
        self.partyTagIndexOffsets = builder.partyTagIndexOffsets
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
                    if self.tags[i].text == keywordPattern.keyword:
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
    .setPartyCaseKeywords([KeywordPattern("Plaintiff Name:", MatchConverter.defaultConverter("Plaintiff Name"), 1),
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

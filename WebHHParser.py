from xmlrpc.client import Boolean
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from Input import Input
import re

class AgeFilter:
    def __init__(self, key = "", value = range(0,0)):
        self._FilterTuple = (key,value)
    def GetTuple(self):
        return self._FilterTuple
    def SetTuple(self, key, value):
        self._FilterTuple = (key, value)
    def SetFirst(self, newFirst):
        self._FilterTuple[0] = newFirst
    def SetSecond(self, newSecond):
        self._FilterTuple[1] = newSecond
    def ApplyFilter(self, param) -> bool:
        age = int(re.search('\d+', param).group())
        if (age <= self._FilterTuple[1].stop) and (age >= self._FilterTuple[1].start):
            return True
        return False

class WebHHParser:
    Filters=[]
    domen=""
    NoneValue = "Unknown"
    @staticmethod
    def VacancyesPartParseOnPage(domen, pageLink, VacancyName, count):
        WebHHParser.domen = domen
        driver = webdriver.Chrome('D:\commands\chromedriver')

        resumeLinks =[]
        resumeNames =[]
        expiriences =[]
        Olds        =[]

        main_page = driver.get(domen + pageLink)

        search_input_box = driver.find_element_by_name('text')
        search_input_box.send_keys(VacancyName)

        buttonAcceptLocation = driver.find_element_by_xpath("//button[@type='button']")
        buttonAcceptLocation.click()

        buttonFind = driver.find_element_by_xpath("//button[@type='submit']")
        buttonFind.click()

        filter = AgeFilter("age", Input.GetAgeRange())

        content = driver.page_source
        soup = BeautifulSoup(content)
        pageCounter = 0
        nextPageButton = soup.find('a', attrs={'class':'bloko-button', 'data-qa':'pager-next'})
        while (nextPageButton != None) and (pageCounter < count):
            RelativeUrl = nextPageButton.attrs['href']
            resumes = soup.findAll("div", attrs={'data-qa':"resume-serp__results-search"})
            if(resumes != None):
                for resume in resumes[0].children:
                    resumeName = WebHHParser.__GetResumeName(resume)
                    if resumeName == WebHHParser.NoneValue:
                        continue
                    age = WebHHParser.__GetAge(resume)
                    if filter.ApplyFilter(age):
                        Olds.append(age)
                        resumeNames.append(resumeName)
                        expiriences.append(WebHHParser.__GetExpireince(resume))
                        resumeLinks.append(WebHHParser.__GetLink(resume))

            WebHHParser.MoveToNextPage(driver, RelativeUrl)
            content = driver.page_source
            soup = BeautifulSoup(content)
            nextPageButton = soup.find('a', attrs={'class':'bloko-button', 'data-qa':'pager-next'})
            pageCounter+=1

        return (resumeLinks, resumeNames, expiriences, Olds)

    @staticmethod
    def VacancyesParseOnPage(domen, pageLink, VacancyName):
        WebHHParser.domen = domen
        driver = webdriver.Chrome('D:\commands\chromedriver')

        resumeLinks=[]
        resumeNames=[]
        expiriences =[]
        Olds        =[]

        main_page = driver.get(domen + pageLink)

        search_input_box = driver.find_element_by_name('text')
        search_input_box.send_keys(VacancyName)

        buttonAcceptLocation = driver.find_element_by_xpath("//button[@type='button']")
        buttonAcceptLocation.click()

        buttonFind = driver.find_element_by_xpath("//button[@type='submit']")
        buttonFind.click()

        content = driver.page_source
        soup = BeautifulSoup(content)

        nextPageButton = soup.find('a', attrs={'class':'bloko-button', 'data-qa':'pager-next'})
        while nextPageButton != None:
            RelativeUrl = nextPageButton.attrs['href']
            resumes = soup.findAll("div", attrs={'data-qa':"resume-serp__results-search"})
            if(resumes != None):
                for resume in resumes:
                    Olds.append(WebHHParser.__GetAge(resume))
                    resumeNames.append(WebHHParser.__GetResumeName(resume))
                    expiriences.append(WebHHParser.__GetExpireince(resume))
                    resumeLinks.append(WebHHParser.__GetLink(resume))

            WebHHParser.MoveToNextPage(driver, RelativeUrl)
            content = driver.page_source
            soup = BeautifulSoup(content)
            nextPageButton = soup.find('a', attrs={'class':'bloko-button', 'data-qa':'pager-next'})

        return (resumeLinks, resumeNames, expiriences, Olds)
    @staticmethod
    def __GetResumeName(vacancy):
        vacancyNameBlock = vacancy.findAll('a', attrs={'data-qa':'resume-serp__resume-title'})
        if len(vacancyNameBlock) != 0:
            return vacancyNameBlock[0].contents[0]
        return WebHHParser.NoneValue
    @staticmethod
    def __GetAge(resume):
        ManOld = resume.findAll('span', attrs={'data-qa':'resume-serp__resume-age'})
        if len(ManOld) != 0:
            return ManOld[0].contents[0].contents[0] + ' ' + ManOld[0].contents[0].contents[4]
        return WebHHParser.NoneValue        
    @staticmethod
    def __GetExpireince(resume):
        expirienceSum = resume.find('div', attrs={'data-qa':'resume-serp__resume-excpirience-sum'})
        if expirienceSum != None:
            expText = ""
            for expirience in expirienceSum.findAll('span', recursive=False):
                expText += expirience.contents[0] + ' ' + expirience.contents[4] + ' '
            return expText.rstrip(' ')
        return WebHHParser.NoneValue
    @staticmethod
    def __GetLink(resume):
        resumeNameBlock = resume.findAll('a', attrs={'data-qa':'resume-serp__resume-title'})
        if len(resumeNameBlock) != 0:
            return resumeNameBlock[0].attrs['href']
        return WebHHParser.NoneValue
    @staticmethod
    def MoveToNextPage(driver, RelativeUrl):
        driver.get(WebHHParser.domen + RelativeUrl)
    @staticmethod
    def VacancyParse(vacancyLink):
        pass
    pass
from typing import Tuple
from WebHHParser import WebHHParser
from Input import Input
import hashlib
from copy import deepcopy

class Resource:
    __itemSeparator = '\n---------------------------------------------------------------------------\n'
    __categorySeparator = '\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n'
    TupleRes = ()
    def __init__(self, *args) -> None:
        self.TupleRes = args
        pass
    def ToString(self, name = "") -> str:
        tupleStr = name + ':'
        for i in range(len(self.TupleRes[0])):
            for j in range(len(self.TupleRes[0][i])):
                tupleStr += self.TupleRes[0][i][j] + self.__itemSeparator
            tupleStr = tupleStr.rstrip(self.__itemSeparator)
            tupleStr += self.__categorySeparator

        return tupleStr


class ResourceManager:
    __Vacancyes=dict()
    __currentDomen=""
    ResumesPageLink = "/search/resume?clusters=True&area=26&ored_clusters=True&order_by=relevance&logic=normal&pos=full_text&exp_period=all_time&text="
    __resourceFilePath = 'main.txt'

    @staticmethod
    def ReleaseResources():
        with open(ResourceManager.__resourceFilePath, "w", encoding="utf-8") as f:
            for vac in ResourceManager.__Vacancyes:
                f.write(ResourceManager.__Vacancyes[vac].ToString())
    @staticmethod
    def loadPartVacancyResources(domen):
        ResourceManager.__currentDomen = domen
        VacancyName = Input.GetVacancyName()
        
        ResourceManager.__Vacancyes[VacancyName] = Resource(WebHHParser.VacancyesPartParseOnPage(ResourceManager.__currentDomen, ResourceManager.ResumesPageLink, VacancyName, Input.GetCountPageForParse()))
    @staticmethod
    def loadVacancyResources(domen):
        ResourceManager.__currentDomen = domen
        VacancyName = Input.GetVacancyName()

        ResourceManager.__Vacancyes[VacancyName] = Resource(WebHHParser.VacancyesParseOnPage(ResourceManager.__currentDomen, ResourceManager.ResumesPageLink, VacancyName))
    @staticmethod
    def GetVacancy(VacancyName):
        return ResourceManager.__Vacancyes[VacancyName]

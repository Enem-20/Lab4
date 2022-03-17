from ResourceManager import ResourceManager
from Printer import Printer


ResourceManager.loadPartVacancyResources('https://voronezh.hh.ru')

ResourceManager.ReleaseResources()

#print(ResourceManager.GetVacancy("manager").ToString())
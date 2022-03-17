from abc import abstractmethod
import re

class StateMachine():
    @abstractmethod
    def Choose():
        pass

class ChooseVacancyType(StateMachine):
    def Choose():
        
        pass

class Input:
    state = StateMachine()

    @staticmethod
    def GetCountPageForParse():
        print('Enter a count of pages for parsing')
        return int(input())
    @staticmethod
    def GetAgeRange() -> range:
        print('Enter an age range in format: <first> <second>')
        strAge = input()
        startStr = re.search('\d+', strAge).group()
        strAge = strAge.replace(startStr + ' ', '', 1)
        endStr = strAge
        start = int(startStr)
        end = int(endStr)

        return range(start, end)
    @staticmethod
    def GetVacancyName():
        print("Enter a vacancy name:")
        return input()
        
    def Init():
        state = ChooseVacancyType()
        pass    

    def Update():
        print('Choose what do you want: ')
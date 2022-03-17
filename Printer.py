class Printer:
    @staticmethod
    def ArrayPrintNamesFormated(arr):
        print('links:')
        for el in range(0, len(arr)):
            print(str(el + 1) + '. ' + arr[el])
    @staticmethod
    def ArrayPrintLinksFormated(arr):
        print('Vacancyes names:')
        for el in range(0, len(arr)):
            print(str(el + 1) + '. ' + arr[el])
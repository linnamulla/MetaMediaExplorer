from extractData import extractData
from transformData import transformData

if __name__ == "__main__":
    while True:
        print("\nPlease enter name of source folder, or type \"break\" to break:")
        sourceFolder: str = input("")
        if sourceFolder == "break":
            print("\nProgram has been broken.\n")
            break
        else:
            try:
                extractData(sourceFolder)
                transformData(sourceFolder, dropEmptyCols = True, dropFloatCols = True)
                break
            except OSError as e:
                print(str(e), "OSError. Likely causes are: (1) files are being downloaded from cloud access and can't be accessed, or (2) the .csv file is opened by the user and can't be overwritten.", sep = "\n")
            except ValueError as e:
                print(str(e), "ValueError. Please enter a valid source folder.", sep = "\n")
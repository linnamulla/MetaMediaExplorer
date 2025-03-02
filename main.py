from extractData import extractData
from transformData import transformData

if __name__ == "__main__":
    while True:
        print("\nPlease enter name of source folder:")
        sourceFolder: str = input("")
        if sourceFolder == "break":
            print("\nProgram has been broken.\n")
            break
        else:
            try:
                while True:
                    try:
                        extractData(sourceFolder)
                        transformData(sourceFolder, dropEmptyCols = True, dropFloatCols = True)
                        break
                    except OSError as e:
                        print(str(e), "OSError", "Forcing new attempt...\n", sep = "\n")
                break
            except ValueError:
                print("\nError: Please enter a valid source folder, or type \"break\" to break.")
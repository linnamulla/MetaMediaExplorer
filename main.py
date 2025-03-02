from extractData import extractData
from transformData import transformData

if __name__ == "__main__":
    print("\nPlease enter name of source folder:")
    sourceFolder: str = input("")
    extractData(sourceFolder)
    transformData(sourceFolder)
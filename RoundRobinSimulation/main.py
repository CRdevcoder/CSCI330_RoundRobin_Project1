import csv
import sys # handles command line arguements
import src.processModule

# "..\\input" + name of file in folder.

# reads csv input and returns data list.
def readFileInput( fileLocation : str) -> list[tuple[int,...]] :

    # stores processor data args.
    dataList : list[tuple[int,...]] = []

    # use with keywork to close file reader when done.
    # open the file. Then pass it to csvReader object.
    with open(fileLocation, "r") as fileObj:

        csvReader = csv.reader(fileObj)
        print("Csv file Data Input:")
        # print data and add it to list.

        # each row is a list of strings.
        for index,row in enumerate(csvReader):
            print(index,row)

            # convert strings in row list into nums.
            # each row should have length 3
            # ignore header row.
            if index > 0:
                # each row is args for constructing a processor object.
                processorArgs : list[int] = [-1,-1,-1] # negatives indicate error

                # test is string that needs to be converted to int.
                for j,text in enumerate(row[:3]):
                    num : int = int(text)
                    processorArgs[j] = num
                
                # add to data list as tuple.
                dataList.append( tuple(processorArgs))
    
    return dataList
    pass
        
def parseCommandLineArgs():
    
    if len(sys.argv) == 0:
        print("NO ARGS")
        return

    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    # PARSE INPUTS INTO INTENDED TYPES
    loc : str = str(arg1)
    quant : int = int(arg2)

    # using location arg input:
    # get args for processor objects in correct format.
    processorConstructorArgs : list[tuple[int,...]] = readFileInput(loc)

    
    print("\nProcessor Args: ",processorConstructorArgs)
    print("Quantime Time: ",quant)

    # convert process args later?.

# construct classes using args.
#def setUpSystem:

    

parseCommandLineArgs()







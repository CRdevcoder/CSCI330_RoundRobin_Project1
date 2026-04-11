import csv
import sys # handles command line arguements
from src.processModule import Process
from src.simulation import Simulator

# ".\\input" + name of file in folder.
# .\\input\sample1.csv

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

# reads csv file and returns inputs for simulation.
def parseCommandLineArgs() -> tuple[list[Process], int]:

    print("ARGS: ",sys.argv)
    
    # defualt arguements if ran with no args:
    arg1 : str = ".\\input\\sample1.csv"
    arg2 : str = "5"

    if len(sys.argv) != 3:
        print("NO ARGS ENTERED, RUNNING DEFAULT INPUTs.")
    else:
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

    # create process objects:
    processes : list[Process] = []

    #
    for args in processorConstructorArgs:
        p = Process(args[0],args[1],args[2])
        processes.append(p)
    
    # return process objects and quantum number for simulation.
    simulationInput : tuple[list[Process], int] = (processes, quant)

    return simulationInput
    pass

    # convert process args later?.
    

# construct classes using args.
input = parseCommandLineArgs()
sim = Simulator(input[0])
sim.runSimulation(input[1])

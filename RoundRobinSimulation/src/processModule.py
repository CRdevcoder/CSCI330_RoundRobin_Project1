# This script stores:
# process Module and process creator

from collections import defaultdict
from enum import Enum

# returns dictionary who uses process arrival time as keys and references to processes as values.
@staticmethod
def buildArrivalTimeDictionary( processList : list[Process]) -> defaultdict[int, list[Process]]:
    # automatically assigns an empty list value to keys that do not exist.
    d : defaultdict[int, list[Process]] = defaultdict(list[Process]) 
    for proc in processList:
        newKey : int = proc.arrivalTime # get arrival time if process
        d[newKey].append(proc) # append process to corresponding arrival time key.
        
    # return value
    return d
    pass

# process creator class.
# Responsabilities:
# stores all the processor constructor data for the given scenario.
# creates the processor and passes it to the ready queue
class ProcessHandler:

    def __init__( self, processList : list[Process]):
        # processes yet to be added to simulation
        self.processList : list[Process] = processList
        # build dictionary.
        self.arrivalDict = buildArrivalTimeDictionary(self.processList)
        pass

    # If time given is equal to arrival time of processes in dictionary.
    # Then return list of one or more processes with that arrival time.
    # If no process arrives at given time, return None
    def receiveNextArrival(self,time : int) -> list[Process] | None:
        
        if time in self.arrivalDict:
            l = self.arrivalDict.get(time)
            return l
        else: 
            return None
    
    # run tick for all processes.
    def tickAll(self, time: int):
        for p in self.processList:
            p.tick(time)
        

class processState(Enum):
    NEW = "new"
    READY = "ready"
    RUNNING = "running"
    TERMINATED = "terminated"
    

# process class.
# Responsabilities:
# represent a processes in simulation.
# keep track of how much burst time you need left before terminating.
class Process:
    # Enum states? 
    # Paramter meanings:
    # pid = processer id number of process.
    # arrive = arrival time, moment in time when process entered ready queue.
    # totalBurst = burst time, how long a process needs to run in CPU to finish and terminate.
    # The burst time (CPU run time) a process needs to finish decreases as it runs in CPU.
    def __init__( self, pid : int, arrive: int, totalBurst : int):
        self.pid = pid
        self.arrivalTime = arrive
        self.totalBurst = totalBurst # total burst time.

        # remaining burst time until termination.
        self.currBurst : int = self.totalBurst

        # waiting time = when in ready queue.
        self.waitingTime = 0

        # completion time: momment in time when process is completed.
        self.completionTime = 0

        #  turnaround time
        self.turnAroundTime = 0

        # current state. Process starts as new until it's added to 
        self.state = processState.NEW

        print("Process Created: ID:",self.pid, "\tAT:",self.arrivalTime,"\tBT:",totalBurst)
        pass
    
    # sets state.
    def setState(self, newState : processState):
        #print out change.
        print("P", self.pid,"- transitions from ", self.state.name, "to",  newState.name )
        self.state = newState

    # returns current state.
    def getState(self) -> processState:
        return self.state
    
    # use to check if current state the given one.
    # use to ask: Is process in NEW state? Running state? etc.
    def isThisState(self,givenState : processState):
        return self.state == givenState
    
    # calculate turn around time.
    def calcTAT(self):
        self.turnAroundTime = self.completionTime - self.arrivalTime
        pass



    # for one simulation tick in time.
    # process should be responsable for modifying its own data.
    # by knowing it's state it can do just that.
    # update after preemption?
    def tick(self, time : int):

        # nothing happens at time = 0, no time elapsed.

        # check if terminated.
        if self.isThisState(processState.TERMINATED):
            # calculate turnaround time.
            self.calcTAT()
            return
            pass

        # goes through each state. acts accordingly.
        if self.isThisState(processState.NEW):
            return # do nothing.
        
        # waiting in ready queue.
        elif self.isThisState(processState.READY):
            self.waitingTime += 1   
        # running on CPU.
        elif self.isThisState(processState.RUNNING):
            # state may be switched to terminated.
            #isTerminated = self.decrementBurst()
            #if isTerminated:
                # update state.
                #self.setState(processState.TERMINATED)
                # sets time of completion.
                #self.completionTime = time
            pass

# return true if terminated, false if needs more time to finish.
    def decrementBurst(self,time : int) -> bool:
        # decrement by 1.
        if(self.currBurst > 0):
            temp = self.currBurst
            self.currBurst -= 1
            print("P", self.pid," - decremented from",temp,"to",self.currBurst)
        
        # if now less than zero than terminated!
        if(self.currBurst <= 0):
            print( "P", self.pid, " - terminated")
            self.setState(processState.TERMINATED)
            self.completionTime = time
            return True
        
        return False
    
    # change state of process.
    def runProcess(self, time : int):
        # state may be switched to terminated.
        isTerminated = self.decrementBurst(time)
        if isTerminated:
            # sets time of completion.
            print("CT SET")
            self.completionTime = time

    # terminate
    def isTerminated(self) -> bool:
        return ( 0 >= self.currBurst)

    
    # data print method.
    def __str__(self):
        return (f"Process: ID:{self.pid}\tAT:{self.arrivalTime}\tBT:{self.totalBurst}"
                f"\tTAT: {self.turnAroundTime}\tWT: {self.waitingTime}\tCT: {self.completionTime}")


    pass
  

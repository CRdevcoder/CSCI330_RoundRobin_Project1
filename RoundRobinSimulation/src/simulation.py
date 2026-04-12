from src.processModule import Process, processState,ProcessHandler
from queue import Queue
from collections import deque
from src.RoundRobinScheduler import RoundRobinScheduler,Cpu

# helps keeps track of events.
# keeps track of cpu utilization. idle time and other stuff?
class Simulator:

    def __init__(self, processList : list[Process]):
        
        # ready queue
        self.readyQueue : deque[Process] = deque()
        # terminated list:
        # terminated processes are added to here
        self.terminated : list[Process] = []

        # original processes. use to construct handler.
        self.processData : list[Process] = processList

    def addArrivals(self,handler : ProcessHandler,time : int):
        arrivals : list[Process] | None = handler.receiveNextArrival(time)
        # if no arrival processes, do nothing. 
        # adding processes to ready queue.
        if (type(arrivals) is list):
            # get processes.
            for p in arrivals:
                print(f"P-{p.pid} Has arrived to readyQueue")
                self.readyQueue.append(p)
                p.setState(processState.READY)


    def runSimulation(self, quantum : int ):

        # set up:
        processCount : int = len(self.processData)
        timeCount : int = 0
        stopCondition : bool = (processCount > len(self.terminated) )
        # process handler
        processManager = ProcessHandler(self.processData)
        simCpu : Cpu = Cpu()

        scheduler : RoundRobinScheduler = RoundRobinScheduler(quantum,simCpu,self.readyQueue)
        # now scheduler adds terminated processes to this list.
        scheduler.terminatedProcesses = self.terminated

        print(self.processData)
        print(processCount)

        print("SIMULATION START")

        # enter first arrival?
        
        # SIMULATION LOOP - starts at time 0.
        while(stopCondition):

            print("# TIME =",timeCount)

            # step 1: update handler, get arriving processes
            self.addArrivals(processManager,timeCount)

            # step 2: select process to run on CPU. or do nothing.
            scheduler.tick(timeCount)

            # update all processes.
            processManager.tickAll(timeCount)

            # step 2: tick clock time,
            timeCount += 1 # add 1 sec to time.

            self.printReadyQueue()

            stopCondition = processCount > len(self.terminated) 
            pass

        print("SIMULATION END")

        self.printMetrics(self.terminated)

        pass
        
    def printReadyQueue(self):
        message = "Ready Queue:"
        for p in self.readyQueue:
            message += f"P{p.pid}, "
        print(message)
    
    def printMetrics(self,terminatedList : list[Process]):
        for p in terminatedList:
            print(p)
        

    # simulate 1 increment of time.
    def step(self):

        # is CPU empty? request scheduler for process.
        # adding process to cpu. or switching cpu.
        # Scheduler tell CPU to switch.
        # running -> ready = premted decision.
        
        pass

    pass




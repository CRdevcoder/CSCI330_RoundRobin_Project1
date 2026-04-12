from src.processModule import Process, processState,ProcessHandler
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
            # cpu wont run process at time zero.
            scheduler.tick(timeCount)

            # step 3: update all processes data according to their current state.
            processManager.tickAll(timeCount)

            # step 4: tick clock time,
            timeCount += 1 # add 1 sec to time.

            self.printReadyQueue()

            stopCondition = processCount > len(self.terminated) 
            pass

        print("SIMULATION END\n")

        excutionTime = (timeCount-1)

        self.printMetrics(self.terminated,simCpu,excutionTime, scheduler.switchCount)

        pass
        
    def printReadyQueue(self):
        message = "Ready Queue:"
        for p in self.readyQueue:
            message += f"P{p.pid}, "
        print(message)
    
    def printMetrics(self,terminatedList : list[Process], cpu : Cpu, executionTime : int, switchCount : int):

        totalProcesses = len(self.terminated)

        print("PROCESS TERMINATION METRICS:")
        for p in terminatedList:
            print(p)
        
         # idle time:
        idleTime = 1 - (switchCount/executionTime)
        print("\nCPU IDLE TIME:", idleTime)
        print("TOTAL EXECUTION TIME:", executionTime)
        print("TOTAL SWITCH COUNT:", switchCount)
 

        avgWaitingTime = 0
        # average waiting time:
        for p in self.terminated:
            # sum
            avgWaitingTime += p.waitingTime
        avgWaitingTime = avgWaitingTime/ totalProcesses

        avgTurnAroundTime = 0
        for p in self.terminated:
            avgTurnAroundTime += p.turnAroundTime
        avgTurnAroundTime = avgTurnAroundTime/ totalProcesses

        # Throughput calculation:
        throughput = totalProcesses/ executionTime

        # CPU utilization:
        cpuUtilization = ((executionTime - idleTime) / executionTime) * 100

        print("Avg. TurnAroundTime:",round(avgTurnAroundTime,2),"ms" )
        print("Avg. WaitingTime:",round(avgWaitingTime,2),"ms" )
        print("Throughput: ", round(throughput,2),"ms" )
        print("CPU Utilization:","%",round(cpuUtilization,2))

    pass




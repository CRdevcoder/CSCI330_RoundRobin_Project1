from src.processModule import Process,ProcessHandler
from enum import Enum
from queue import Queue

# helps keeps track of events.
# keeps track of cpu utilization. idle time and other stuff?
class Simulator:

    def __init__(self, processList : list):
        
        # ready queue
        self.readyQueue : Queue[Process] = Queue(0)
        # terminated list:
        # terminated processes are added to here
        self.terminated : list[Process] = []

        # original processes. use to construct handler.
        self.processData : list[Process] = processList


    def runSimulation(self, quantum : int ):

        # set up:
        processCount : int = len(self.processData)
        timeCount : int = 0
        stopCondition : bool = (processCount > len(self.terminated) )
        # process handler
        processManager = ProcessHandler(self.processData)
        simCpu : Cpu = Cpu()

        print(self.processData)
        print(processCount)

        print("SIMULATION START")
        
        # SIMULATION LOOP - starts at time 0.
        while(stopCondition and (timeCount < 20)):

            print("# TIME =",timeCount)

            # step 1: update handler, get arriving processes
            arrivals : list[Process] | None= processManager.receiveNextArrival(timeCount)
            # if no arrival processes, do nothing. 
            
            if (type(arrivals) is list):
                # get processes.
                for p in arrivals:
                    print(f"P-{p.pid} Has arrived to readyQueue")
                    self.readyQueue.put(p)

            # step 2: run scheduler.
            


            timeCount += 1 # add 1 sec to time.
            stopCondition = processCount > len(self.terminated) 
        
        print("SIMULATION END")
        

    # simulate 1 increment of time.
    def step(self):

        # is CPU empty? request scheduler for process.
        # adding process to cpu. or switching cpu.
        # Scheduler tell CPU to switch.
        # running -> ready = premted decision.
        
        pass

    pass

# states of cpu. either running or idle.
class CpuState(Enum):
    IDLE = 1
    RUNNING = 2

# CPU.
class Cpu:

    def __init__(self):
        # None when idle has pm.process inside when running.
        self.runningProcess : Process | None = None
        self.state = CpuState.IDLE

        # every clock tick increment when not running and elapses one time.
        #during context switch, do I have it take time?
        self.idleTime = 0


    def isIdle(self) -> bool:
        if (self.runningProcess is None):
            self.state = CpuState.IDLE
            return True
        else: 
            self.state = CpuState.RUNNING
            return False

    def isRunning(self) -> bool:
        b : bool= self.isIdle()
        ans : bool = not b # invert answer.
        return ans
    
    def getState(self) -> CpuState:
        return self.state

    # decrements Burst of current running process. None if nothing inside.
    def runProcess(self) -> bool | None :
        if type(self.runningProcess) is Process:
            # decrement BT
            isTerminated : bool = self.runningProcess.decrementBurst()
            # if terminated set completion time and return.
            return isTerminated  
        else:
            return None
        
    def loadProcess(self, p : Process):
        self.runningProcess = p
    
    def getRunningProcess(self):
        return self.runningProcess
    
    pass



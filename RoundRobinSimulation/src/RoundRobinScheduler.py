from src.simulation import Cpu
from src.processModule import Process
from queue import Queue

class RoundRobinScheduler:

    # pass CPU object as reference. will be observed and used by scheduler.
    def __init__(self, timeQuantum : int, cpu : Cpu, readyQueue : Queue[Process]):
        
        self.cpu = cpu

        # quantum time.
        self.timeQuantum = timeQuantum
        # tracks time quantum.
        self.quantumCount = timeQuantum

        # reference to ready Queue.
        self.readyQueue = readyQueue


    # selects next item in queue?
    def selectNextProcess(self, readyQueue : Queue[Process]) -> Process | None:

        # Does queue have processes, or is it empty?
        if readyQueue.qsize() > 0:
            return readyQueue.get()
        else:
            return None # return None if empty.
        pass
    
    # return terminated process if it is terminated.
    def runCpu(self) -> Process | None:
        # what happens when process terminates? process goes to terminate list in simulation.

        # if cpu is not running any process.
        if self.cpu.isIdle():
            # load next selected
            selectedProcess = self.selectNextProcess(self.readyQueue)

            # if processs avaialble, add new process to CPU.
            if isinstance(selectedProcess,Process):
                # reset count
                self.quantumCount = self.timeQuantum
                self.cpu.loadProcess(selectedProcess)
                pass
            else: # if no process available, add up idle time.
                # increment idle time.
                self.cpu.idleTime += 1
            return None
            
        # when CPU is running process
        elif self.cpu.isRunning():
            # run process and get bool.
            isTerminated : bool | None = self.cpu.runProcess()
            # is process terminated?
            if isinstance(isTerminated,bool) and isTerminated:
                terminatedProcess = self.cpu.getRunningProcess()
                return terminatedProcess
            # want to have simulation
            # who modifies wait time? ProcessHandler.
            # Who 

        pass

        
#from src.simulation import Cpu
from src.processModule import Process,processState
from collections import deque
from enum import Enum

class RoundRobinScheduler:

    # pass CPU object as reference. will be observed and used by scheduler.
    def __init__(self, timeQuantum : int, cpu : Cpu, readyQueue : deque[Process]):
        
        self.cpu = cpu

        # counts context switch:
        self.switchCount = 0

        # quantum time.
        self.timeQuantum = timeQuantum
        # tracks time quantum.
        self.quantumCount = timeQuantum

        # reference to simulation class ready Queue.
        self.readyQueue = readyQueue

        # stores processes that CPU terminated.
        self.terminatedProcesses : list[Process] = list()


    # move process to ready queue. set it's state to ready.
    def moveProcessToReadyQueue(self,p : Process):

        self.readyQueue.append(p)
        p.setState(processState.READY)
    
    def isReadyQueueEmpty(self):
        return len(self.readyQueue) == 0


    # selects next item in queue?
    def selectNextProcess(self, readyQueue : deque[Process]) -> Process | None:

        # Does queue have processes, or is it empty?
        if len(readyQueue) > 0:
            return readyQueue.popleft()
        else:
            return None # return None if empty.
        pass

    def preempt(self):

        old_p = self.cpu.unloadProcess()

        if isinstance(old_p,Process):
            if old_p.isThisState(processState.TERMINATED):
                self.terminatedProcesses.append(old_p)
            else:
                self.moveProcessToReadyQueue(old_p)
        
        next_p = self.selectNextProcess(self.readyQueue)

        if isinstance(next_p,Process):
            self.cpu.loadProcess(next_p)
            self.quantumCount = self.timeQuantum
            if isinstance(old_p,Process) and (next_p.pid != old_p.pid):
                print("$ CONTEXT SWITCH: P", next_p.pid, "with P",old_p.pid)
                self.switchCount += 1  

    def runQuantum(self) -> bool:
        # run quantum:
        if self.quantumCount > 0:
            print("Q:",self.quantumCount)
            self.quantumCount -= 1
            # check quantum
        if self.quantumCount <= 0: # quantum ran out then preepmt to ready queue.
                # set to idle. new process will be loaded next?
                # context switch
            print("TIME QUANTUM RAN OUT")
            return True
        return False
                
    
    def tick(self,time : int):

        # what happens when process terminates? process goes to terminate list in simulation.
        # if cpu is not running any process, load one into it from ready queue.
        # LOADING CPU
        if self.cpu.isIdle():
            
            print("@ Choosing Process to LOAD to idle CPU.")
            # load next selected
            selectedProcess = self.selectNextProcess(self.readyQueue)
            # if processs avaialble, add new process to CPU.
            if isinstance(selectedProcess,Process):
                # changes cpu state to RUNNING.
                self.cpu.loadProcess(selectedProcess)
                pass
            else: 
                print("READY QUEUE EMPTY")
        
        # no time has elapsed yet. do not tick cpu. or process handler.
        if time == 0:
            return

        # count up idle time if still idle.
        # how to count context switching?
        self.cpu.tick(time)


        # check if process terminated. if so move it to erminated list.
        # UNLOADING CPU
        if self.cpu.isProcessTerminated():
            self.preempt()
        # if cpu is running. Check time quantum
        # UNLOADING CPU if time quantum expired
        elif self.cpu.isRunning():
            if self.runQuantum():
                # if ready queue is empty we do not need to preempt the running process
                if self.isReadyQueueEmpty():
                    self.quantumCount = self.timeQuantum
                    return
                self.preempt()
                
        

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
        self.previousProcess : Process | None = None

        # every clock tick increment when not running and elapses one time.
        #during context switch, do I have it take time?
        self.idleTime = 0

    def setState(self, newState : CpuState):
        print("CPU changed from", self.state.name,"to",newState.name)
        self.state = newState


    def isRunning(self) -> bool:
        return isinstance(self.runningProcess, Process)
    
    def isIdle(self) -> bool:
        b : bool= self.isRunning()
        ans : bool = not b # invert answer.
        return ans
    
    def getState(self) -> CpuState:
        return self.state

    # decrements Burst of current running process. None if nothing inside.
    def runProcess(self,time: int) :
        if type(self.runningProcess) is Process:
            # decrement BT
            self.runningProcess.decrementBurst(time)
        else:
            return 
    
    # what clock does at a momment in time.
    # changes state to idle.
    def tick(self,time : int):
        # Idle to Idle = increment.
        if self.isIdle():
            self.idleTime += 1
            # means CPU is doing nothing within given time interval.
            #self.previousProcess = None
            print("CPU IS IDLE:", self.idleTime)
            pass
        elif self.isRunning():
            # runs cpu.
            print("CPU IS RUNNING: P",self.runningProcess.pid)
            self.runProcess(time)
    
    
    # load process to CPU. change state to running.
    # Sheduler calls this method for CPU.
    def loadProcess(self, p : Process):
        self.runningProcess = p
        # set CPU state to running.
        print("<< CPU LOADED PROCESS: P-",p.pid)
        self.setState(CpuState.RUNNING)
        p.setState(processState.RUNNING)
    
    # removes current running process and returns it.
    def unloadProcess(self) -> Process | None:
        if not isinstance(self.runningProcess,Process):
            return None
        
        p : Process = self.runningProcess # assuming its not None for now.
        self.runningProcess = None
        self.setState(CpuState.IDLE)
        # on't know if process will be placed in READY or TERMINATED.
        print(">> UNLOADED PROCESS: P-",p.pid)
        return p
    
    # is running process terminated?
    # returns false if process still has BT left or no process running in CPU.
    def isProcessTerminated(self):
        #self.isRunning()
        if isinstance(self.runningProcess, Process):
            p : Process = self.runningProcess
            return p.isTerminated()
            
        return False

    
    def getRunningProcess(self):
        return self.runningProcess
    
    pass

        
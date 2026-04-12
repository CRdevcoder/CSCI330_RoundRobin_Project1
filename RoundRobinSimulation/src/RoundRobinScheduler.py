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

        # reference to ready Queue.
        self.readyQueue = readyQueue

        # stores processes that CPU terminated.
        self.terminatedProcesses : list[Process] = list()


    # move process to ready queue. 
    def moveProcessToReadyQueue(self,p : Process):

        self.readyQueue.append(p)
        p.setState(processState.READY)


    # selects next item in queue?
    def selectNextProcess(self, readyQueue : deque[Process]) -> Process | None:

        # Does queue have processes, or is it empty?
        if len(readyQueue) > 0:
            return readyQueue.popleft()
        else:
            return None # return None if empty.
        pass

    # Preempt current running process
    # only run wjen process is in CPU!
    def contextSwitch(self):
        # get next process from ready queue.
        pSwitch = self.selectNextProcess(self.readyQueue)
        # false if no processes in queue or CPU not running.
        switchPossible = isinstance(pSwitch,Process) and self.cpu.isRunning()

        if switchPossible:
            print("SWITCH DONE")
            old = self.cpu.unloadProcess()
            if isinstance(old,Process):
                self.cpu.loadProcess(pSwitch)
                self.moveProcessToReadyQueue(old)
                #self.switchCount =+1
            else:
                print("SWITCH FAILURE")
        
        return switchPossible
    
    # check context switch. Check if switch happened in previous time interval.
    # if unloaded last tick and scheduler loaded process during this tick.
    # that means we did context switch!
    def checkContextSwitch(self):
        oldProcessExist = self.cpu.hadPreviousProcess()
        currProcessExist = self.cpu.isRunning()
        runningNewProcess = not self.cpu.isRunningPrevious()
        print("BOTH PROCESS?", oldProcessExist,currProcessExist)

        if  (oldProcessExist and currProcessExist):
            if runningNewProcess:
                return True
            else:
                return False
        else:
            # if previous process is same instance as. Then no context switch.
            return False
        


    def runQuantum(self):
        # run quantum:
            if self.quantumCount > 0:
                print("Q:",self.quantumCount)
                self.quantumCount -= 1
                #self.cpu.runProcess(time)
            # check quantum
            if self.quantumCount <= 0: # quantum ran out then preepmt to ready queue.
                # set to idle. new process will be loaded next?
                # context switch
                print("TIME QUANTUM RAN OUT")
                # UNLOAD Process
                # try context switch:
                #if self.contextSwitch():
                #    return
                # if context switch not possible just unload
                
                p = self.cpu.unloadProcess()
                if isinstance(p,Process):
                    # set to ready state.
                    self.moveProcessToReadyQueue(p)

        
    
    def tick(self,time : int):

        # what happens when process terminates? process goes to terminate list in simulation.
        # if cpu is not running any process.
        # LOADING CPU
        if self.cpu.isIdle():
            
            print("@ Choosing Process to LOAD to idle CPU.")
            # load next selected
            selectedProcess = self.selectNextProcess(self.readyQueue)
            # if processs avaialble, add new process to CPU.
            if isinstance(selectedProcess,Process):
                # reset time quantum when loading new process.
                self.quantumCount = self.timeQuantum
                # changes cpu state to RUNNING.
                self.cpu.loadProcess(selectedProcess)
                pass
            else: 
                print("READY QUEUE EMPTY")
        
        # no time has elapsed yet.
        if time == 0:
            return

        if self.checkContextSwitch():
            self.switchCount +=1
        # count up idle time if still idle.
        # how to count context switching?
        self.cpu.tick(time)

        # check if process terminated. if so move it.
        # UNLOADING CPU
        # false if cpu already idle. use for context switching?
        if self.cpu.isProcessTerminated():
            print("# UNLOAD TERMINATED PROCESS")
            p = self.cpu.unloadProcess()
            if isinstance(p,Process):
                # add to terminated list.
                # set to terminated afterwards.
                self.terminatedProcesses.append(p)
                # reset
            else:
                print("UNLOADING ERROR")



        # if cpu is running. 
        # Check time quantum
        # UNLOADING CPU if time quantum expired
        if self.cpu.isRunning():
            self.runQuantum()
                #if isinstance(p,Process):   
        
        
    # return terminated process if it is terminated.
    @DeprecationWarning
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
        self.previousProcess : Process | None = None

        # every clock tick increment when not running and elapses one time.
        #during context switch, do I have it take time?
        self.idleTime = 0

    def setState(self, newState : CpuState):
        print("CPU changed from", self.state.name,"to",newState.name)
        self.state = newState


    def isRunning(self) -> bool:
        return isinstance(self.runningProcess, Process)
    
    def hadPreviousProcess(self) -> bool:
        return isinstance(self.previousProcess,Process)
    
    def isRunningPrevious(self):
        if self.isRunning() and self.hadPreviousProcess():
            print("RUNNING SAME?",self.previousProcess.pid == self.runningProcess.pid)
            return (self.previousProcess.pid == self.runningProcess.pid)

    def isIdle(self) -> bool:
        b : bool= self.isRunning()
        ans : bool = not b # invert answer.
        return ans
    
    def getState(self) -> CpuState:
        return self.state

    # decrements Burst of current running process. None if nothing inside.
    #@DeprecationWarning
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
            print("PREVIOUS PROCESS:",self.previousProcess)
            print("CPU IS RUNNING:",self.runningProcess)
            self.runProcess(time)
    
    
    # load process to CPU. change state to running.
    # Sheduler calls this method for CPU.
    def loadProcess(self, p : Process):
        self.runningProcess = p
        # set CPU state to running.
        self.setState(CpuState.RUNNING)
        p.setState(processState.RUNNING)
    
    # removes current running process and returns it.
    def unloadProcess(self) -> Process | None:
        if not isinstance(self.runningProcess,Process):
            return None
        self.previousProcess = self.runningProcess
        # don't know if process will be placed in READY or OTHER.
        p : Process = self.runningProcess # assuming its not None for now.
        self.runningProcess = None
        self.setState(CpuState.IDLE)
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

        
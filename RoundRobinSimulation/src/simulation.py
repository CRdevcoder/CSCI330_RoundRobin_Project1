import processModule as pm
from enum import Enum

# helps keeps track of events.
# keeps track of cpu utilization. idle time and other stuff?
class Simulator:

    def __init__(self):
        self.contextSwitchCount = 0
        # ready queue
        self.readyQueue : list[object] = []
        # terminated list:
        # terminated processes are added
        self.terminated : list[object] = []

        self.simCpu : Cpu = Cpu()

        self.simClock : Clock = Clock()

        # process creator

    # simulate 1 increment of time.
    def step(self):

        # is CPU empty? request scheduler for process.
        # adding process to cpu. or switching cpu.
        # Scheduler tell CPU to switch.
        # running -> ready = premted decision.
        # 


        self.simClock.countUp()
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
        self.runningProcess : object = None
        self.state = CpuState.IDLE

        # every clock tick increment when not running and elapses one time.
        #during context switch, do I have it take time?
        self.idleTime = 0

    def isIdle(self) -> bool:
        if (self.runningProcess is type(None)):
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

    # count up idle time ??? or  who should handle that?
    def updateData(self):
        pass

    # decrements Burst of current running process. 
    def runProcess(self):
        #self.clock
        pass
    
    pass

# clock that counts. keeps track of time for simulator.
class Clock:
    def __init__(self):
        self.currTime = 0

    # count up clock.
    def countUp(self):
        self.currTime += 1

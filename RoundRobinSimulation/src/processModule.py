# This script stores:
# process Module and process creator


# process creator class.
# Responsabilities:
# stores all the processor constructor data for the given scenario.
# creates the processor and passes it to the ready queue
class processCreator:

    pass


# process class.
# Responsabilities:
# represent a processes in simulation.
# keep track of how much burst time you need left before terminating.
class process:

    # Enum states? NO.
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

        # completion time: current time when process is completed.
        self.completionTime = -1

        # 
        self.turnAroundTime = 0
        pass

    # return true if terminated, false if needs more time to finish.
    def decrementBurst(self, time:int ) -> bool:
        # decrement by 1.
        self.currBurst -= 1
        if( 0 > self.currBurst):
            print( "(Time = ",time,") - P", self.pid, " terminated")
            return True

        return False
  




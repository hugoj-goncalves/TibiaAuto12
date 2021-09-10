from threading import Event, Thread
from queue import Queue

ActivatedThreads = []
Queue = Queue(maxsize=19)
EventInstance = Event()

'''
    This Class Has Been Rewritten So That We Can Pause The Modules Enabled,
    In Original Class, Its Not Possible, There He Had To Keep Creating New Threads
    And That, Overloads The System.
    
    Example For Usage:
    
    # Import The Module Fist
    from Core.ThreadManager import ThreadManager
    
    # And Create The Instance
    ThreadManager = ThreadManager("NameOfYourThread")
    
    # For Start The New Thread
    ThreadManager.NewThread(TargetFunctionHere) [DOES NOT ACCEPT ARGUMENTS YET]
    
    # For Pause All Threads
    ThreadManager.PauseThread()
    
    # For UnPause All Threads
    ThreadManager.UnPauseThread()
    
    #
    # The Kill Threads Functions Not Ready Yet !!! Sorry
    #
'''

class AllThreads:
    def __init__(self):
        pass

    def ExistsThread(self, Name):
        for i in range(len(ActivatedThreads)):
            if ActivatedThreads[i][1] == Name:
                print('Found: ', ActivatedThreads[i][0])
                return True
        return False

    def PauseThreads(self, Name = None):
        for i in range(len(ActivatedThreads)):
            if Name is None or ActivatedThreads[i][1] == Name:
                print('Pausing: ', ActivatedThreads[i][0])
                ActivatedThreads[i][0].PauseOn()

    def UnPauseThreads(self, Name = None):
        for i in range(len(ActivatedThreads)):
            if Name is None or ActivatedThreads[i][1] == Name:
                print('UnPausing: ', ActivatedThreads[i][0])
                ActivatedThreads[i][0].PauseOff()

    def CleanupThreads(self):
        for i in range(len(ActivatedThreads)):
            print('Cleaning up: ', ActivatedThreads[i][0])
            ActivatedThreads[i][0].Cleanup()


class ThreadManager:
    def __init__(self, Name, Managed = False, Func = None):
        self.Name = Name
        self.Queue = Queue
        self.Target = None
        self.Managed = Managed
        self.Running = None

        if self.Managed:
            self.Running = Event()
            if Func == None:
                raise Exception('Func needs to be defined for Managed threads')
            self.NewThread(Func)

    # Create One New Thread And Put Them In The Pipeline
    def NewThread(self, _Target):
        # The Handle Need The 1st Arg to Work..
        def HandleTarget(PipeOBJ, wait):
            # print(f"PipeObject: {PipeOBJ}", wait)
            if wait:
                _Target(wait)
            else:
                _Target()

        self.Target = Pipeline(HandleTarget)
        self.Queue.put(self.Target)
        EventInstance.set()

        TheThread = self.ThreadHandler(Target=self.Target, Qqueue=Queue, Name=self.Name, Managed=self.Managed, RunningEvent=self.Running)
        TheThread.start()

        ActivatedThreads.append((TheThread, str(self.Name)))
        print('ActivatedThreads: ', ActivatedThreads)

    # Pause The All Threads Created From Manager Object
    def PauseThread(self):
        print('Pause - ActivatedThreads: ', ActivatedThreads)
        for i in range(len(ActivatedThreads)):
            if ActivatedThreads[i][1] == self.Name:
                print('Pausing: ', ActivatedThreads[i][0])
                ActivatedThreads[i][0].PauseOn()
        # print(self.Queue.queue)

    # UnPause The All Threads Created From Manager Object
    def UnPauseThread(self):
        print('UnPause - ActivatedThreads: ', ActivatedThreads)
        for i in range(len(ActivatedThreads)):
            if ActivatedThreads[i][1] == self.Name:
                print('UnPausing: ', ActivatedThreads[i][0])
                ActivatedThreads[i][0].PauseOff()

    # This Function Is Not Ready To Use !!!
    def KillThread(self):
        print('Killing Thread: ', self.Name, ActivatedThreads)
        for i in range(len(ActivatedThreads)):
            if ActivatedThreads[i][1] == self.Name:
                ActivatedThreads.remove(ActivatedThreads[i])
        Queue.put('Kill')
        # print(f"{self.Name} Killed")

    def __repr__(self) -> str:
        return str(self.Name)

    '''
        This Is Thread Class Rewrited, To Can Pause Them.
    '''

    class ThreadHandler(Thread):
        def __init__(self, Target, Qqueue, *, Name='Handler', Managed=False, RunningEvent=None):
            super().__init__()
            self.Name = Name
            self.Queue = Qqueue
            self._target = Target
            self._stoped = False

            self.Managed = Managed
            self.RunningEvent = RunningEvent
            self.Running = True
            self.ExitEvent = Event()
            # print(self.Name, "Created")

        def run(self):
            # EventInstance.wait()
            try:
                while not self.Queue.empty():
                    SelectedThread = self.Queue.get()
                    # print(self.Name, "Pipeline To Handle:",SelectedThread)
                    if SelectedThread == 'Kill':
                        self.Queue.put(SelectedThread)
                        self._stoped = True
                        # self.Queue.pop(-1)
                        break

                    if self.Managed and self.RunningEvent:
                        while self.Running:
                            run = self.RunningEvent.wait(3)
                            if run:
                                self._target(SelectedThread, self.ExitEvent.wait)
                    else:
                        self._target(SelectedThread)
            finally:
                print('Thread ended: ', self.Name)

        def PauseOn(self):
            if self.Managed and self.RunningEvent:
               self.RunningEvent.clear()
            else:
               self._stoped = False

        def PauseOff(self):
            if self.Managed and self.RunningEvent:
               self.RunningEvent.set()
            else:
                self._stoped = True

        def Cleanup(self):
            if self.Managed:
                self.Running = False
                self.ExitEvent.set()

        def __repr__(self) -> str:
            return str(self.Name)


def Pipeline(*funcs):
    def Inner(argument, wait = None):
        # print('argument: ', argument, ' wait: ', wait)
        state = argument
        for func in funcs:
            state = func(state, wait)
    return Inner

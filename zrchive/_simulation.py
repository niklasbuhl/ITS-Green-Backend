    # def __init__(self, intxnId, id, type, course):
    #
    #     # Threading
    #     threading.Thread.__init__(self)
    #     self.lock = threading.Lock()
    #
    #     #self.stop = threading.Event()
    #     self.keepAlive = True
    #
    #     # Cycle
    #     self.state = SignalState.RED
    #     self.redTime = 2000 # ms
    #     self.redBegin = 0
    #     self.orangeTime = 2000 # ms
    #     self.orangeBegin = 2000
    #     self.greenTime = 2000 # ms
    #     self.greenBegin = 4000
    #     self.yellowTime = 2000 # ms
    #     self.yellowBegin = 6000
    #     self.cycleTime = self.getCycleTime()
    #     self.currentCycle = 0
    #     self.ttg = 0
    #
    #     # Updating
    #     self.cycleInitOffset = 0 # ms, last time begin cycle
    #     self.lastUpdate = ms() # ms time since last update
    #     self.lastCycleDataUpdate = ms() # ms
    #
    #     # Info
    #     self.intxnId = intxnId
    #     self.id = id
    #     self.type = type
    #     self.course = course
    #
    #     if not CONFIG['data']['intxns']['realtiming']: self.setRandomCycleStart()
    #
    # def setCycleTime(red, orange, green, yellow):
    #
    #     self.redTime = red
    #     self.orangeTime = orange
    #     self.greenTime = green
    #     self.yellowTime = yellow
    #
    #     self.cycleTime = getCycleTime()
    #
    # def setState(self, state):
    #
    #     self.state = state
    #
    #     if state is SignalState.RED: self.cycleInitOffset = 0
    #     elif state is SignalState.ORANGE: self.cycleInitOffset = - self.orangeBegin
    #     elif state is SignalState.GREEN: self.cycleInitOffset = - self.greenBegin
    #     else: self.cycleInitOffset = - self.yellowBegin
    #
    #     self.lastDataUpdated = ms() # ms
    #
    # def run(self):
    #
    #     if CONFIG['debug']['signal']:
    #         print("Starting signal")
    #
    #     while self.keepAlive:
    #         self.update()
    #
    #     if CONFIG['debug']['signal']:
    #         print("Exiting signal")
    #
    # def update(self):
    #
    #     self.lock.acquire()
    #
    #     now = ms()
    #
    #     timeSinceUpdate =  now - self.lastUpdate
    #
    #     if timeSinceUpdate < 100:
    #         self.lock.release()
    #         return
    #
    #     if CONFIG['debug']['signalTiming']:
    #         print('[{0}][{1}] TTG: {2}'.format(self.intxnId, self.id, round((self.ttg / 1000), 1)))
    #         # print(f"[{self.intxnId}][{self.id}] TSU: {timeSinceUpdate} - Time to update!")
    #
    #     prevState = self.state
    #
    #     self.currentCycle = (now + self.cycleInitOffset) % self.cycleTime
    #
    #     if self.currentCycle < self.orangeBegin:
    #         self.ttg = self.currentCycle
    #     elif self.currentCycle > self.yellowBegin:
    #         self.ttg = self.currentCycle - (self.orangeTime + self.greenTime)
    #     else:
    #         self.ttg = 0
    #
    #     if self.currentCycle < self.orangeBegin: self.state = SignalState.RED
    #     elif self.currentCycle < self.greenBegin: self.state = SignalState.ORANGE
    #     elif self.currentCycle < self.yellowBegin: self.state = SignalState.GREEN
    #     else: self.state = SignalState.YELLOW
    #
    #     # if debug:
    #         # print(f"[{self.intxnId}][{self.id}] TSU: {timeSinceUpdate} - CC: {currentCycle} - State: {self.state}")
    #
    #     self.lastUpdate = now
    #
    #     if prevState != self.state:
    #         if CONFIG['debug']['signalState']: self.printState()
    #
    #     self.lock.release()
    #
    # def stop(self):
    #     if CONFIG['debug']['signal']: print("Exitting threads.")
    #     #self.stop.set()
    #     self.keepAlive = False
    #
    # def setTTG(ms):
    #     self.lastDataUpdated = ms()
    #     self.cycleInitOffset = ms - (self.redTime + self.orangeTime)
    #
    # def getCycleTime(self):
    #     self.redBegin = 0
    #     self.orangeBegin = self.redTime
    #     self.greenBegin = self.orangeBegin + self.orangeTime
    #     self.yellowBegin = self.greenBegin + self.greenTime
    #
    #     return self.redTime + self.orangeTime + self.greenTime + self.yellowTime
    #
    # def setRandomCycleStart(self):
    #     self.cycleInitOffset = random.randint(0, self.cycleTime)
    #
    # def print(self):
    #     print('\tSignal[{0}]'.format(self.id))
    #     print('\t\tType: {0}'.format(self.type))
    #     print('\t\tCourse: {0}'.format(self.course))
    #     print('\t\tCycle Init: {0}\n'.format(self.cycleInitOffset))
    #
    # def printState(self):
    #     message = "[" + str(self.intxnId) + "][" + str(self.id) + "] " + str(self.state.name)
    #     # print(f"[{self.intxnId}][{self.id}] {self.state.name}")
    #     print(message)
    #
    # def getState(self):
    #
    #     self.lock.acquire()
    #     state = self.state.name
    #     self.lock.release()
    #
    #     return state
    #
    # def getTTG(self):
    #
    #     self.lock.acquire()
    #     _ttg = self.ttg
    #     self.lock.release()
    #
    #     return _ttg
    #
    # def calculateTTGslots():
    #
    #
    #
    #     pass


    # Get the distance in meters from input latitude and longitude
    def distanceFrom(self, lat, lon):
        pass


            # print("\t[{0}]\tFrom: {1}:{2} ({5}), \tTo:{3}:{4} ({6})".format(
            #     dayProgram.program,
            #     dayProgram.fromHour,
            #     dayProgram.fromMin,
            #     dayProgram.toHour,
            #     dayProgram.toMin,
            #     dayProgram.totalMinFrom,
            #     dayProgram.totalMinTo
            # ))


                # print("Program: {0} - From: {1}:{2} ({5}) To: {3}:{4} ({6})".format(
                #     dayProgram.program,
                #     dayProgram.fromHour,
                #     dayProgram.fromMin,
                #     dayProgram.toHour,
                #     dayProgram.toMin,
                #     dayProgram.totalMinFrom,
                #     dayProgram.totalMinTo
                # ))


            # def __init__(self, intId, kkId, kkName, loc):

            # print()

            # for program in data['intxns'][intxnId]['programs']:
            #     print(program)


            #

    def start(self):

        print("--------------------\n")
        print("Starting Simulation!\n")
        print("--------------------\n")

        for intxn in self.intxns:
            self.intxns[intxn].start()

    def stop(self):
        for intxn in self.intxns:
            self.intxns[intxn].stop()


        def getIntersection(self, int):
            return self.intxns[int]

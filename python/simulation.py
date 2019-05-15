from enum import Enum
import random
import threading
import json

from world import CONFIG
from utility import ms

class Location():

    # Initialize with latitude and longitude
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    # Get the distance in meters from input latitude and longitude
    def distanceFrom(self, lat, lon):
        pass

class SignalState(Enum):
    RED = "0"
    ORANGE = "1"
    GREEN = "2"
    YELLOW = "3"

class SignalType(Enum):
    REGULAR = 0
    REGULARRIGHT = 1
    BICYCLE = 2
    BICYCLERIGHT = 3

class Signal(threading.Thread):

    # Should be timeless...

    def __init__(self, intxnId, id, type, course):

        # Threading
        threading.Thread.__init__(self)
        self.lock = threading.Lock()

        #self.stop = threading.Event()
        self.keepAlive = True

        # Cycle
        self.state = SignalState.RED
        self.redTime = 2000 # ms
        self.redBegin = 0
        self.orangeTime = 2000 # ms
        self.orangeBegin = 2000
        self.greenTime = 2000 # ms
        self.greenBegin = 4000
        self.yellowTime = 2000 # ms
        self.yellowBegin = 6000
        self.cycleTime = self.getCycleTime()
        self.currentCycle = 0
        self.ttg = 0

        # Updating
        self.cycleInitOffset = 0 # ms, last time begin cycle
        self.lastUpdate = ms() # ms time since last update
        self.lastCycleDataUpdate = ms() # ms

        # Info
        self.intxnId = intxnId
        self.id = id
        self.type = type
        self.course = course

        if not CONFIG['data']['intxns']['realtiming']: self.setRandomCycleStart()

    def setCycleTime(red, orange, green, yellow):

        self.redTime = red
        self.orangeTime = orange
        self.greenTime = green
        self.yellowTime = yellow

        self.cycleTime = getCycleTime()

    def setState(self, state):

        self.state = state

        if state is SignalState.RED: self.cycleInitOffset = 0
        elif state is SignalState.ORANGE: self.cycleInitOffset = - self.orangeBegin
        elif state is SignalState.GREEN: self.cycleInitOffset = - self.greenBegin
        else: self.cycleInitOffset = - self.yellowBegin

        self.lastDataUpdated = ms() # ms

    def run(self):

        if CONFIG['debug']['signal']: print(f"Starting signal")

        while self.keepAlive:
            self.update()

        if CONFIG['debug']['signal']: print(f"Exiting signal")

    def update(self):

        self.lock.acquire()

        now = ms()

        timeSinceUpdate =  now - self.lastUpdate

        if timeSinceUpdate < 100:
            self.lock.release()
            return

        if CONFIG['debug']['signalTiming']:
            print(f"[{self.intxnId}][{self.id}] TTG: {round((self.ttg / 1000), 1)}")
            # print(f"[{self.intxnId}][{self.id}] TSU: {timeSinceUpdate} - Time to update!")

        prevState = self.state

        self.currentCycle = (now + self.cycleInitOffset) % self.cycleTime

        if self.currentCycle < self.orangeBegin:
            self.ttg = self.currentCycle
        elif self.currentCycle > self.yellowBegin:
            self.ttg = self.currentCycle - (self.orangeTime + self.greenTime)
        else:
            self.ttg = 0

        if self.currentCycle < self.orangeBegin: self.state = SignalState.RED
        elif self.currentCycle < self.greenBegin: self.state = SignalState.ORANGE
        elif self.currentCycle < self.yellowBegin: self.state = SignalState.GREEN
        else: self.state = SignalState.YELLOW

        # if debug:
            # print(f"[{self.intxnId}][{self.id}] TSU: {timeSinceUpdate} - CC: {currentCycle} - State: {self.state}")

        self.lastUpdate = now

        if prevState != self.state:
            if CONFIG['debug']['signalState']: self.printState()

        self.lock.release()

    def stop(self):
        if CONFIG['debug']['signal']: print("Exitting threads.")
        #self.stop.set()
        self.keepAlive = False

    def setTTG(ms):
        self.lastDataUpdated = ms()
        self.cycleInitOffset = ms - (self.redTime + self.orangeTime)

    def getCycleTime(self):
        self.redBegin = 0
        self.orangeBegin = self.redTime
        self.greenBegin = self.orangeBegin + self.orangeTime
        self.yellowBegin = self.greenBegin + self.greenTime

        return self.redTime + self.orangeTime + self.greenTime + self.yellowTime

    def setRandomCycleStart(self):
        self.cycleInitOffset = random.randint(0, self.cycleTime)

    def print(self):
        print(f"\tSignal[{self.id}]")
        print(f"\t\tType: {self.type}")
        print(f"\t\tCourse: {self.course}")
        print(f"\t\tCycle Init: {self.cycleInitOffset}\n")

    def printState(self):
        print(f"[{self.intxnId}][{self.id}] {self.state.name}")

    def getState(self):

        self.lock.acquire()
        _state = self.state.name
        self.lock.release()

        return _state

    def getTTG(self):

        self.lock.acquire()
        _ttg = self.ttg
        self.lock.release()

        return _ttg

class Intersection:

    def __init__(self, id, name, loc):
        self.name = name
        self.id = id
        self.loc = loc
        self.signals = {}
        self.sigCnt = 0

    def addSignal(self, sig):
        self.signals[sig.id] = sig
        self.sigCnt += 1

    def start(self):
        for sig in self.signals:
            self.signals[sig].start()

    def run(self):
        pass

    def stop(self):
        for sig in self.signals:
            self.signals[sig].stop()

    def print(self):
        print(f"\nIntersection[{self.id}] - {self.name}\n")
        print(f"\tLoc: [{self.loc.lat}, {self.loc.lat}]\n")

        for sig in self.signals:
            self.signals[sig].print()

        print(f"\n")

    def getLocation(self):
        return self.loc


# Thread
class Simulation():

    def __init__(self):

        # threading.Thread.__init__(self)

        self.intxns = {}
        self.intxnCount = 0
        self.loadedIntersections = False

    def loadIntersections(self, data):

        if self.loadedIntersections: return

        for intxn in data['intxns']:
            # if CONFIG['debug']['intersection']: print(intxn)

            # Extract Data
            id = intxn
            name = data['intxns'][intxn]['name']
            lat = data['intxns'][intxn]['loc']['lat']
            lon = data['intxns'][intxn]['loc']['lon']

            # Location
            newLoc = Location(lat, lon)

            # Intersection
            newIntersection = Intersection(id, name, newLoc)

            # Signal
            for sig in data['intxns'][intxn]['sigs']:
                # if CONFIG['debug']['signal']: print(sig)

                id = sig
                type = data['intxns'][intxn]['sigs'][sig]['type']
                crs = data['intxns'][intxn]['sigs'][sig]['course']

                newSig = Signal(intxn, id, type, crs)
                # newSig.print()

                newIntersection.addSignal(newSig)

            # Add Intersection
            if CONFIG['debug']['intersection']: newIntersection.print()

            self.addIntersection(newIntersection)

        self.loadedIntersections = True

    def addIntersection(self, intxn):
        self.intxns[intxn.id] = intxn
        self.intxnCount += 1

    def start(self):

        print(f"--------------------\n")
        print(f"Starting Simulation!\n")
        print(f"--------------------\n")

        for intxn in self.intxns:
            self.intxns[intxn].start()

    def stop(self):
        for intxn in self.intxns:
            self.intxns[intxn].stop()

    def getIntxnsAndSignals(self):

        json_data = {}

        for int in self.intxns:

            intersection = {}

            intersection['lat'] = self.intxns[int].loc.lat
            intersection['lon'] = self.intxns[int].loc.lon

            signals = {}

            for sig in self.intxns[int].signals:

                signal = {}

                signal['course']  = self.intxns[int].signals[sig].course

                signals[sig] = signal

            intersection['signals'] = signals

            json_data[int] = intersection


        if CONFIG['debug']['intersectionGetData']: print(json)

        return json_data

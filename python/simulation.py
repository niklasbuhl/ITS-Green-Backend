from enum import Enum
import random
import threading
import json
import datetime

from world import CONFIG
from utility import ms

class Location():

    # Initialize with latitude and longitude
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class SignalState(Enum):
    RED = "RED"
    ORANGE = "ORANGE"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class SignalType(Enum):
    REGULAR = "REGULAR"
    REGULARRIGHT = "REGULARRIGHT"
    BICYCLE = "BICYCLE"
    BICYCLERIGHT = "BICYCLERIGHT"

# class Signal(threading.Thread):
class Signal():

    # Should be timeless...

    def __init__(self, real, kkId, intxnId, sigId, type, course):

        self.real = real
        self.kkId = kkId
        self.intxnId = intxnId
        self.sigId = sigId
        self.type = type
        self.course = course
        self.state = SignalState.INACTIVE

        self.programs = {}

    def print(self):
        print('\tSignal [{0}]\n'.format(self.sigId))
        print('\t\tReal Data: {0}'.format(self.real))
        print('\t\tKK Id: {0}'.format(self.kkId))
        print('\t\tIntxnId: {0}'.format(self.intxnId))
        print('\t\tType: {0}'.format(self.type))
        print('\t\tCourse: {0}'.format(self.course))
        print('\t\tState: {0}'.format(self.state))
        print('\t\tPrograms:')

        for program in self.programs:
            self.programs[program].print()

        print("\n")

    def getState(self): return self.state

    def addProgram(self, program): self.programs[program.program] = program

    def getProgram(self, program): return program.get(program)

    def calcSignalStateAndTTG(self, program, realCurrentCycle, revolution, printBoolean):

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean: print("\n\t\tCalculating Signal:\n")

        ttg = None
        greenTimespan = None
        state = None

        programSignalTimer = self.programs[program]

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean: programSignalTimer.print()

        offset = programSignalTimer.offset
        redTimespan = programSignalTimer.RED
        orangeTimespan = programSignalTimer.ORANGE
        greenTimespan = programSignalTimer.GREEN
        yellowTimespan = programSignalTimer.YELLOW

        orangeTimeChange = redTimespan
        greenTimeChange = orangeTimeChange + orangeTimespan
        yellowTimeChange = greenTimeChange + greenTimespan

        timespanBetweenGreen = redTimespan + orangeTimespan + yellowTimespan

        internalSignalTime = (revolution - offset + realCurrentCycle) % revolution

        ttg = redTimespan + orangeTimespan - internalSignalTime

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean:
            print("\t\tInternal Signal Time: {0}".format(internalSignalTime))
            print("\t\tOrignal Time Till Next Green: {0}".format(ttg))

        # If for some reason the calculations turned out to be less than the magnitude of green time.
        if abs(ttg) > greenTimespan: ttg = ttg + revolution

        # If the TTG is negative, means it is green and the -7 is seconds since it turned green

        # If the time is greater than a revolution, it should not be
        if ttg > revolution: ttg = ttg % revolution

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean: print("\t\tReal Time Till Next Green: {0}".format(ttg))

        # Calculate Signal State
        if internalSignalTime < orangeTimeChange: state = SignalState.RED
        elif internalSignalTime < greenTimeChange: state = SignalState.ORANGE
        elif internalSignalTime < yellowTimeChange: state = SignalState.GREEN
        else: state = SignalState.YELLOW

        signalStateAndTTG = SignalStateAndTTG()

        signalStateAndTTG.state = state
        signalStateAndTTG.ttg = ttg
        signalStateAndTTG.gts = greenTimespan
        signalStateAndTTG.revolution = revolution

        return signalStateAndTTG

        # return {
        #     'state' : state,
        #     'ttg' : ttg,
        #     'greenTimespan' : greenTimespan
        # }

class ProgramSignalTimer:

    def __init__(self, program, offset, RED, ORANGE, GREEN, YELLOW):
        self.program = program
        self.offset = offset
        self.RED = RED
        self.ORANGE = ORANGE
        self.GREEN = GREEN
        self.YELLOW = YELLOW

    def print(self):

        print('\t\t[{0}]\tOffset: {1}\tR: {2},\tO: {3},\tG: {4},\tY: {5}'.format(
            self.program,
            self.offset,
            self.RED,
            self.ORANGE,
            self.GREEN,
            self.YELLOW
        ))

class ProgramDayTimer:

    def __init__(self, program, revolution, offset, fromHour, fromMin, toHour, toMin, totalMinFrom, totalMinTo):

        self.program = program
        self.revolution = revolution
        self.offset = offset
        self.fromHour = fromHour
        self.fromMin = fromMin
        self.toHour = toHour
        self.toMin = toMin
        self.totalMinFrom = totalMinFrom
        self.totalMinTo = totalMinTo

    def print(self):

        print("\t[{0}] {7}\" (+ {8})\tFrom: {1}:{2} ({5}), \tTo:{3}:{4} ({6})".format(
            self.program,
            self.fromHour,
            self.fromMin,
            self.toHour,
            self.toMin,
            self.totalMinFrom,
            self.totalMinTo,
            self.revolution,
            self.offset
        ))

class Intersection:

    def __init__(self, intxnId, kkId, kkName, loc):

        # ID
        self.intxnId = intxnId

        # KK Information
        self.kkName = kkName
        self.kkId = kkId
        self.loc = loc

        # Signal
        self.signals = {}

        # Program Map
        self.dayPrograms = []

        # Program Offets
        self.programOffsets = {}

    def setDayPrograms(self, programs, programRevolution, programOffsets):

        for program in programs:

            # print(program)
            #
            # print("Adding Program: {0},{1},{2},{3},{4}".format(
            #     program['program'],
            #     program['from']['h'],
            #     program['from']['m'],
            #     program['to']['h'],
            #     program['to']['m']
            # ))

            tempProgramDayTimer = ProgramDayTimer(
                program['program'],
                programRevolution[program['program']], # Revolution
                programOffsets[program['program']], # Offset
                program['from']['h'],
                program['from']['m'],
                program['to']['h'],
                program['to']['m'],
                (program['from']['h'] * 60 + program['from']['m']),
                (program['to']['h'] * 60 + program['to']['m'])
            )

            self.dayPrograms.append(tempProgramDayTimer)

    def setProgramOffsets(array):
        pass

    def addSignal(self, signal):
        self.signals[signal.sigId] = signal

    def getSignal(self, sigId):
        return self.signals[sigId]

    def print(self):
        # print(f"\nIntersection[{self.id}] - {self.name}\n")
        message = "# Intersection [" + str(self.intxnId) + "] - " + str(self.kkName)

        print("# ------------------------------------------------")
        print(message)
        print("# ------------------------------------------------\n")

        print("\tKK Id: {0}".format(self.kkId))

        # print(f"\tLoc: [{self.loc.lat}, {self.loc.lat}]\n")
        message = "\tLoc: [" + str(self.loc.lat) + ", " + str(self.loc.lat) + "]\n"
        print(message)

        print("Day Programs:\n")
        # print(self.dayPrograms)
        for dayProgram in self.dayPrograms:

            dayProgram.print()

        print("\nSignals:\n")

        for sig in self.signals:
            self.signals[sig].print()

        print("\n")

    def getLocation(self):
        return self.loc

    def calcSignalStateAndTTG(self, sigId, printBoolean):

        # Intersection Info
        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean:
            print("\n\t{0}".format(self.kkName))
            print("\tCourse from North: {0}\n".format(self.signals[sigId].course))

        # Return Data
        state = None
        ttg = None
        greenTimespan = None
        revolution = None

        signalStateAndTTG = SignalStateAndTTG()

        # Now
        now = datetime.datetime.now()

        # Print now.year, now.month, now.day, now.hour, now.minute, now.second
        nowInMin = now.hour * 60 + now.minute

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean:
            print("\tNow: Day[{0}/7] {1}:{2} (Total Min: {3})\n".format(now.isoweekday(), now.hour, now.minute, nowInMin))

        # Find the program
        program = None

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean:
            print("\tFinding program:\n")

        for dayProgram in self.dayPrograms:
            if nowInMin > dayProgram.totalMinFrom and nowInMin < dayProgram.totalMinTo:

                if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean: dayProgram.print()

                program = dayProgram

                break

        # Get revolution
        signalStateAndTTG.revolution = dayProgram.revolution

        # Get seconds since the program started
        secondsSinceProgramStart = (nowInMin - dayProgram.totalMinFrom) * 60 + now.second

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean: print("\n\tSeconds since program start: {0}".format(secondsSinceProgramStart))

        # Get the seconds of current cycle by modular the revolution
        currentCycle = secondsSinceProgramStart % signalStateAndTTG.revolution;

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean: print("\n\tSeconds in current cycle: {0}".format(currentCycle))

        # Take the offset into account
        realCurrentCycle = currentCycle - program.offset

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean: print("\n\tReal Current Cycle: {0}, Offset: {1}".format(realCurrentCycle, program.offset))

        # The the specific signal state and ttg
        signalStateAndTTG = self.signals[sigId].calcSignalStateAndTTG(dayProgram.program, realCurrentCycle, signalStateAndTTG.revolution, printBoolean)

        # signalStateAndTTG.ttg = signalStateAndTTG['ttg']
        # signalStateAndTTG.greenTimespan = signalStateAndTTG['greenTimespan']
        # signalStateAndTTG.state = signalStateAndTTG['state']

        # state = self.calcSignalState(sigId)

        if CONFIG['debug']['simulation']['calcSignalStateAndTTG'] or printBoolean:
            print("\n\tReturn:\n")
            print("\tProgram: {0}".format(program.program))
            print("\tState: {0}".format(signalStateAndTTG.state))
            print("\tTTG: {0}".format(signalStateAndTTG.ttg))
            print("\tGreen Time: {0}".format(signalStateAndTTG.gts))
            print("\tRevolution: {0}".format(signalStateAndTTG.revolution))

        return signalStateAndTTG

        # return {
        #     'state' : signalStateAndTTG.state,
        #     'ttg' : signalStateAndTTG.ttg,
        #     'greenTimespan' : signalStateAndTTG.gts,
        #     'revolution' : signalStateAndTTG.revolution
        # }


# The Thread
# class SimulationUpdate(threading.Thread):
class SimulationUpdate():

    def __init__(self):
        pass


class SignalStateAndTTG():

    def __init__(self):

        # State
        self.state = None

        # Time To Green
        self.ttg = None

        # Green Time Span
        self.gts = None

        # Signal Revolution
        self.revolution = None

class Simulation():

    def __init__(self):

        self.intxns = {}
        self.intxnCount = 0
        self.loadedIntersections = False

    def loadIntersections(self, data):

        if self.loadedIntersections: return

        print("\n\n")
        print("# ------------------------------------------------")
        print("# Simulation Intersection and Signals")
        print("# ------------------------------------------------\n")

        for intxn in data['intxns']:
            # if CONFIG['debug']['intersection']: print(intxn)

            # Extract Data
            intxnId = intxn
            kkId = data['intxns'][intxnId]['kkId']
            kkName = data['intxns'][intxnId]['kkName']
            lat = data['intxns'][intxnId]['loc']['lat']
            lon = data['intxns'][intxnId]['loc']['lon']

            # Location
            newLoc = Location(lat, lon)

            # Intersection
            newIntersection = Intersection(intxnId, kkId, kkName, newLoc)

            # Set dayprogram
            newIntersection.setDayPrograms(
                data['intxns'][intxnId]['programs'],
                data['intxns'][intxnId]['programRevolution'],
                data['intxns'][intxnId]['programOffsets'],
            )

            # Signal
            for signal in data['intxns'][intxnId]['signals']:
                # if CONFIG['debug']['signal']: print(sig)

                sigId = signal
                real = data['intxns'][intxnId]['signals'][sigId]['real']
                kkId = data['intxns'][intxnId]['signals'][sigId]['kkId']
                type = data['intxns'][intxnId]['signals'][sigId]['type']
                course = data['intxns'][intxnId]['signals'][sigId]['course']

                newSig = Signal(real, kkId, intxnId, sigId, type, course)
                # def __init__(self, real, kkId, intxnId, sigId, type, course):
                # newSig.print()

                for program in data['intxns'][intxnId]['signals'][sigId]['programs']:

                    offset = data['intxns'][intxnId]['signals'][sigId]['programs'][program]['offset']
                    RED = data['intxns'][intxnId]['signals'][sigId]['programs'][program]['RED']
                    ORANGE = data['intxns'][intxnId]['signals'][sigId]['programs'][program]['ORANGE']
                    GREEN = data['intxns'][intxnId]['signals'][sigId]['programs'][program]['GREEN']
                    YELLOW = data['intxns'][intxnId]['signals'][sigId]['programs'][program]['YELLOW']

                    # print("{0} offset: {1}, R: {2}, O: {3}, G: {4}, Y: {5}".format(program, offset, RED, ORANGE, GREEN, YELLOW))

                    newProgram = ProgramSignalTimer(program, offset, RED, ORANGE, GREEN, YELLOW)

                    newSig.addProgram(newProgram)

                newIntersection.addSignal(newSig)

            # Add Intersection
            if CONFIG['debug']['intersection']: newIntersection.print()

            self.addIntersection(newIntersection)

        self.loadedIntersections = True

    def addIntersection(self, intxn): self.intxns[intxn.intxnId] = intxn

    def getIntersection(self, intxnId): return self.intxns.get(intxnId)

    def getSignal(self, intId, sigId):
        if CONFIG['debug']['simulation']['getSignal']: print("Getting Signal: [{0}][{1}]".format(intId, sigId))
        return self.intxns[intId].signals[sigId]

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


        # if CONFIG['debug']['intersectionGetData']: print(json)

        return json_data

    def calcSignalStateAndTTG(self, intxnId, sigId, printBoolean):

        if printBoolean:
            print("\n# ----------------------------------------")
            print("# Calculating Signal State and TTG!")
            print("# ----------------------------------------\n")

        return self.intxns[intxnId].calcSignalStateAndTTG(sigId, printBoolean)

    def calcRouteSignalStateAndTTG(intxnsAndSignalsArray, self):

        signalStateAndTTGs = []

        for intxnsAndSignal in intxnsAndSignalsArray:

            intxnId = intxnsAndSignal[0]
            sigId = intxnsAndSignal[1]

            signalStateAndTTG = self.intxns[intxnId].calcSignalStateAndTTG(sigId, False)

            signalStateAndTTGs.append(signalStateAndTTG)

        return signalStateAndTTGs

    def getAllSignalStatesAndTTG(self):
        # Used for testing purposes

        signalArray = [
         ['i02', 's02'],
         ['i02', 's04'],
         ['i03', 's02'],
         ['i03', 's03'],
         ['i04', 's02'],
         ['i04', 's04'],
         ['i05', 's02'],
         ['i05', 's04']
        ]

        ## Add the rest!

        signalStateData = []

        for signal in signalArray:
            newSignalStateData = self.intxns[signal[0]].calcSignalStateAndTTG(signal[1], False)
            signalStateData.append([signal[0], signal[1], newSignalStateData])

        message = ""

        # [i02][s02]    STATE   TTG GTS REV
        message = message + "[INT][SIG]\tSTATE\t\t\tTTG \tGTS \tREV\n"
        for signal in signalStateData:
            message = message + "[{0}][{1}]\t{2} \t{3}\t{4}\t{5}\n".format(
                signal[0],
                signal[1],
                signal[2].state,
                signal[2].ttg,
                signal[2].gts,
                signal[2].revolution
            )

        return message

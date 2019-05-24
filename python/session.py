from world import CONFIG
from utility import *
from simulation import *
from world import CONFIG

import gpxpy
import math
import gpxpy.gpx
import threading
from operator import itemgetter, attrgetter, methodcaller

class SessionSignal:

    def __init__(self, n, int, sig, nextInt, nextSig, prevInt, prevSig, nextDist, lastDist, course, nextCourse, lastCourse):

        self.n= n
        self.int = int
        self.sig = sig
        self.nextInt = nextInt
        self.nextSig = nextSig
        self.prevInt = prevInt
        self.prevSig = prevSig
        self.nextDist = nextDist
        self.lastDist = lastDist
        self.course = course
        self.nextCourse = nextCourse
        self.lastCourse = lastCourse
        self.passed = False
        self.state = None
        self.signalStateAndTTG = None

    def __repr__(self):
        return((
            self.n,
            self.int,
            self.sig,
            self.nextInt,
            self.nextSig,
            self.nextDist,
            self.lastDist,
            self.course,
            self.nextCourse,
            self.lastCourse
        ))

    def print(self):

        n = self.n
        int = self.int
        sig = self.sig
        nextInt = self.nextInt
        nextSig = self.nextSig
        nextDist = round(self.nextDist, 2)
        lastDist = round(self.lastDist, 2)
        course = self.course
        nextCourse = self.nextCourse
        lastCourse = self.lastCourse
        passed = self.passed
        state = self.state

        print("S {0}\t{11}\tPassed: {10}\t [{12}][{13}] -> <[{1}][{2}]> -> [{3}][{4}]\tnD: {5}m\tlD: {6}m\tC: {7}   \tnC: {8}   \tlC: {9}".format(
            self.n,
            self.int,
            self.sig,
            self.nextInt,
            self.nextSig,
            round(self.nextDist, 2),
            round(self.lastDist, 2),
            self.course,
            self.nextCourse,
            self.lastCourse,
            self.passed,
            self.state,
            self.prevInt,
            self.prevSig
        ))


class SessionSpeed:

    def __init__(self, beginMs, endMs, beginKmt, endKmt, beginS, endS):

        # [None, reachThisLightSpeed, None, reachThisLightSpeedKmT, 0, timeOfGreenLight]
        if CONFIG['debug']['session']['SessionSpeed']:
            print("\t\tCreating new Session Speed: {}, {}, {}, {}, {}, {}".format(
                beginMs, endMs, beginKmt, endKmt, beginS, endS
            ))

        # Begin/End
        self.beginMs = beginMs
        self.endMs = endMs
        self.beginKmt = beginKmt
        self.endKmt = endKmt
        self.beginS = beginS
        self.endS = endS

        # Averages Speed
        try:
            self.avgMs = (beginMs + endMs) / 2
            self.avgKmt = (beginKmt + endKmt) / 2

        except:
            self.avgMs = endMs
            self.avgKmt = endKmt

        # Changes in speed

        # Possitive is increase speed, negative is decrease speed
        self.beginSpeedChange = None
        self.endSpeedChange = None
        self.bikeSpeed = None

        self.beginSpeedChangeMs = None
        self.endSpeedChangeMs = None

        self.beginSpeedChangeKmt = None
        self.endSpeedChangeKmt = None

        self.speedChange = None
        self.relativeSpeedChange = None

        self.targetSpeed = None
        self.timespanAvgTargetSpeed = None

    def setSpeedChanges(self, beginSpeedChange, endSpeedChange):

        # Ms
        self.beginSpeedChangeMs = beginSpeedChange
        self.endSpeedChangeMs = endSpeedChange

        # Kmt
        self.beginSpeedChangeKmt = msToKmt(beginSpeedChange)
        self.endSpeedChangeKmt = msToKmt(endSpeedChange)

    def setBikeSpeed(self, speed):
        self.bikeSpeed = speed

    def info(self):

        bikeSpeed = None
        beginSpeedChangeMsKmt = None
        beginKmt = None
        endKmt = None
        endSpeedChangeMsKmt = None
        speedChange = None
        relativeSpeedChange = None

        try: bikeSpeed = round(self.bikeSpeed, 1)
        except: bikeSpeed = None
        try: beginSpeedChangeMsKmt = round(self.beginSpeedChangeKmt, 1)
        except: beginSpeedChangeMsKmt = None
        try: beginKmt = round(self.beginKmt, 1)
        except: beginKmt = None
        try: endKmt = round(self.endKmt, 1)
        except: endKmt = None
        try: endSpeedChangeMsKmt = round(self.endSpeedChangeKmt, 1)
        except: endSpeedChangeMsKmt = None
        try: speedChange = round(self.speedChange, 1)
        except: speedChange = None
        try: relativeSpeedChange = round(self.relativeSpeedChange, 1)
        except: relativeSpeedChange = None
        try: targetSpeed = round(self.targetSpeed, 1)
        except: targetSpeed = None


        # SessionSpeed: [BikeSpeed] [ToBegin] []-[] [ToEnd]
        info = "SessionSpeed:\t[{0}]\t{1}\t[{2}]-[{3}]\t{4}\t[{5}]\t({6})\tT[{7}]".format(
            bikeSpeed,
            beginSpeedChangeMsKmt,
            beginKmt,
            endKmt,
            endSpeedChangeMsKmt,
            speedChange,
            relativeSpeedChange,
            targetSpeed
        )

        # print(info)

        return info

    def calcSpeedChange(self):

        if CONFIG['debug']['session']['SessionSpeed']:
            print("\tCalculate Speed Change and Target.")
            print("\tBeginKmt: {0}, BeginSpeedChangeKmt: {1}, EndSpeedChangeKmt: {2}".format(self.beginKmt, self.beginSpeedChangeKmt, self.endSpeedChangeKmt))

        if self.beginKmt is None:
            if CONFIG['debug']['session']['SessionSpeed']: print("\tFirst Speed")

            self.speedChange = self.endSpeedChangeKmt

        elif self.beginSpeedChangeKmt > 0 and self.endSpeedChangeKmt > 0:
            if CONFIG['debug']['session']['SessionSpeed']: print("\tIncrease Speed")

            self.speedChange = min(self.beginSpeedChangeKmt, self.endSpeedChangeKmt)

        elif self.beginSpeedChangeKmt < 0 and self.endSpeedChangeKmt < 0:
            if CONFIG['debug']['session']['SessionSpeed']: print("\tDecrease Speed")

            self.speedChange = max(self.beginSpeedChangeKmt, self.endSpeedChangeKmt)

        else:
            self.speedChange = 0

        if CONFIG['debug']['session']['SessionSpeed']:print("\n\n")

        self.targetSpeed = self.bikeSpeed + self.speedChange

        self.relativeSpeedChange = abs(self.speedChange)


class Session:

    def __init__(self, id, bicycle, route):

        self.id = id
        self.route = route
        self.bicycle = bicycle

        # [i][SessionSignal]
        self.routeIntAndSignalsCalculated = False
        self.routeIntAndSignals = []

        # All Signals
        self.routeSignalStates = []

        # [int1, int2, ...]
        self.routeIntxns = []

        # [i][int, sig]
        self.routeSignals = []

        # [tntId, sigId, state, lastUpdated, # in route]
        # self.nextSignal = []

        # [targetSpeed, speedDifference, color]
        self.SpeedTarget = None
        self.speedDifference = None
        self.speedColor = None

        # Signal
        self.lastSignal = None
        self.nextSignal = None
        # self.nextSignalStateAndTTG = None


        # Route
        self.routeBegun = False
        self.routeFinished = False
        self.routeSignalStatesAndTTG = None


    def loadRouteGPX(self, gpx):
        self.route.loadGPX(gpx)

    def getRoute(self): return self.route.getRouteArray()

    def calcRouteIntxnsAndSignals(self, sim):

        # print("\n\n")
        # print("# ------------------------------------------------")
        # print("# Calculate Route Intersection and Signals")
        # print("# ------------------------------------------------\n")

        # self.routeIntAndSignals = self.route.getRouteSignalsAndIntersections(sim.intxns)
        # self.routeSignals = self.route.getRouteSignalsArray()

        tempIntAndSigArray = self.route.getRouteSignalsAndIntersections(sim.intxns)

        print("\n\n")
        print("# ------------------------------------------------")
        print("# Route Intersection and Signals")
        print("# ------------------------------------------------\n")

        arrayLength = len(tempIntAndSigArray)

        print(tempIntAndSigArray)

        print("Intersection Count: {0}".format(arrayLength))

        # print(arrayLength)
        # firstSignal = True
        # lastSignal = False

        print(sim.intxns)

        lastSignal = tempIntAndSigArray[arrayLength - 1]
        lastInt = lastSignal[0]
        lastSig = lastSignal[1]

        print("Last Signal: {0}".format(lastSignal))

        lastIntLocation = sim.getIntersection(lastInt).loc
        lastSigCourse = sim.getSignal(lastInt, lastSig).course

        for i in range(arrayLength):

            signal = tempIntAndSigArray[i]
            int = signal[0]
            sig = signal[1]

            intLocation = sim.getIntersection(int).loc

            lastDist = getDistanceFromLatLonInM(
                intLocation.lat,
                intLocation.lon,
                lastIntLocation.lat,
                lastIntLocation.lon
            )

            tempIntAndSigArray[i].append(lastDist)

        # print(tempIntAndSigArray)

        tempIntAndSigArray = sorted(tempIntAndSigArray, key = itemgetter(2), reverse = True)

        # print(tempIntAndSigArray)

        for i in range(arrayLength):

            signal = tempIntAndSigArray[i]

            int = signal[0]
            sig = signal[1]

            nextInt = None
            nextSig = None
            nextCourse = None
            nextDist = 0

            prevInt = None
            prevSig = None

            dist = 0

            intLocation = sim.getIntersection(int).loc

            course = sim.getSignal(int, sig).course

            try:

                if (i - 1) >= 0: prevSignal = tempIntAndSigArray[i - 1]
                prevInt = prevSignal[0]
                prevSig = prevSignal[1]

            except:
                pass

            try:

                nextSignal = tempIntAndSigArray[i + 1]
                nextInt = nextSignal[0]
                nextSig = nextSignal[1]

                nextCourse = sim.getSignal(nextInt, nextSig).course - course

                nextIntLocation = sim.getIntersection(nextInt).loc

                nextDist = getDistanceFromLatLonInM(
                    intLocation.lat,
                    intLocation.lon,
                    nextIntLocation.lat,
                    nextIntLocation.lon
                )

            except:
                pass

                # nextSig = None
                # nextInt = None
                # pass

            lastDist = getDistanceFromLatLonInM(
                intLocation.lat,
                intLocation.lon,
                lastIntLocation.lat,
                lastIntLocation.lon
            )

            # print(nextDist)

            # print(lastDist)

            lastCourse = course - lastSigCourse

            tempSessionSignal = SessionSignal(i, int, sig, nextInt, nextSig, prevInt, prevSig, nextDist, lastDist, course, nextCourse, lastCourse)

            self.routeIntAndSignals.append(tempSessionSignal)

            # print("tSignal {3}\t[{0}][{1}]\tnDist: {2}\tlDist: {4}\tCor: {5}\tNext Cor: {6}".format(int, sig, dist, i, lastDist, course, nextCourse))


        # print(self.routeIntxns)
        # print(self.routeSignals)

        for signal in tempIntAndSigArray: self.routeIntxns.append(signal[0])
        for signal in tempIntAndSigArray: self.routeSignals.append([signal[0], signal[1]])

        for signal in self.routeIntAndSignals: signal.print()

        print("\n")

        self.nextSignal = self.routeIntAndSignals[0]
        self.lastSignal = self.routeIntAndSignals[-1]

        self.routeIntAndSignalsCalculated = True

    def getRouteIntxns(self): return self.routeIntxns

    def getRouteSignals(self): return self.routeSignals

    def calcNextSignal(self, sim):

        if CONFIG['debug']['session']['calcNextSignal']:

            print("\n# ------------------------------------------------------")
            print("# Calculating Next Signal")
            print("# ------------------------------------------------------\n")

        self.couldFindNextSignal = False

        # Get bicycle location
        bicycleLoc = self.bicycle.loc

        # Get current next signal
        testNextSignal = self.nextSignal

        while(not self.couldFindNextSignal):

            firstSignal = False
            nextSignalInfront = False
            nextSignalCloserThanNextAndPrevious = False

            closestSignal = None
            secondClosestSignal = None

            # Get the current next signal location from sim
            nextSignalLoc = sim.getIntersection(testNextSignal.int).loc

            # Distance and angle between the bicycle and current next signal
            dist = getDistanceFromLatLonInM(
                bicycleLoc.lat,
                bicycleLoc.lon,
                nextSignalLoc.lat,
                nextSignalLoc.lon
            )

            # Angle between the bicycle and current next signal
            angle = getCourseFromLatLonInDegrees(
                bicycleLoc.lat,
                bicycleLoc.lon,
                nextSignalLoc.lat,
                nextSignalLoc.lon
            )

            # Bicycle angle
            bicycleAngle = self.bicycle.course

            # Get the absolute angle difference between the current next signal and the bicycle
            # angleDifference = abs(angle - self.bicycle.course) % 360

            # Shouldn't be able to be more than 180 degrees
            angleDifference = abs(angle - self.bicycle.course) % 360

            if angleDifference > 180: angleDifference = 180 - (angleDifference % 180)

            # Print everything
            if CONFIG['debug']['session']['calcNextSignal']:
                print("Distance: {0}\tAngle: {1}, Bicycle Angle: {2}, Angle Differnce: {3}".format(dist, angle, bicycleAngle, angleDifference))

            # Check if the current next signal is still in front of the bicyclist
            # Check if the next signal is in front of the bicyclist


            # ------------------------------------------------------------------
            # Test 1, see if the next signal is in front
            # ------------------------------------------------------------------
            if angleDifference < 90:

                if CONFIG['debug']['session']['calcNextSignal']:
                    print("Signal is in front.")

                # Check if the signal is less meters away than between the signals


                nextSignalInfront = True

            else:
                if CONFIG['debug']['session']['calcNextSignal']:
                    print("Signal is in the back.")

                nextSignalInfront = False

            # ------------------------------------------------------------------
            # Test 2, try to get the distance between the next signal and previous signal
            # ------------------------------------------------------------------
            # Check if it makes sense the intersection is that one

            try:
                if CONFIG['debug']['session']['calcNextSignal']:
                    print("Previous signal.")

                prevSignalLoc = sim.getIntersection(testNextSignal.prevInt).loc

                prevDist = getDistanceFromLatLonInM(
                    prevSignalLoc.lat,
                    prevSignalLoc.lon,
                    nextSignalLoc.lat,
                    nextSignalLoc.lon
                )

                if CONFIG['debug']['session']['calcNextSignal']:
                    print("Distance between next and previous signals: {0}".format(round(prevDist, 2)))

                if prevDist > dist:
                    if CONFIG['debug']['session']['calcNextSignal']:
                        print("Distance bicycle to next signal is less than the distance between next signal and previous signal.")

                    nextSignalCloserThanNextAndPrevious = True

            except:
                if CONFIG['debug']['session']['calcNextSignal']:
                    print("This is the first signal")

                firstSignal = True

            # ------------------------------------------------------------------
            # Result, return if next signal is really the next signal
            # ------------------------------------------------------------------

            if nextSignalInfront and (nextSignalCloserThanNextAndPrevious or firstSignal):

                if CONFIG['debug']['session']['calcNextSignal']:
                    print("Found signal!")

                self.nextSignal = testNextSignal

                return

            else:

                # Test the next signal
                try:
                    testNextSignal = self.routeIntAndSignals[testNextSignal.n + 1]

                except:

                    # Last signal
                    if CONFIG['debug']['session']['calcNextSignal']:
                        print("Couldn't find a next signal, possible something is very wrong or the route is finished.")

                    self.couldFindNextSignal = True


        # If there is no signals in front of the bicyclist do something...

        # Fint the two closest signals
        # Check if which route AB the bicyclist is on

        # If the first one is closest continue
        # If the closest is the last one and the second closest if further away from the last one, route is finished, else the
        return

    def calcNextSignalStateAndTTG(self, sim):

        if CONFIG['debug']['session']['calcNextSignalStateAndTTG']:
            print("\n# -------------------------------------------")
            print("# Calculating Next Signal State And TTG")
            print("# -------------------------------------------\n")

        self.nextSignal.signalStateAndTTG = sim.calcSignalStateAndTTG(self.nextSignal.int, self.nextSignal.sig, False)

    def getNextSignalStateAndTTG(self): return self.nextSignalStateAndTTG

    def getNextSignal(self): return [self.nextSignal.int, self.nextSignal.sig]

    def calcBicycleTargetSpeedAndColor(self, sim):

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\n# -------------------------------------------")
            print("# Calculating Bicycle Target Speed And Color")
            print("# -------------------------------------------\n")

        # Current speed

        # Get bicycle location
        bikeLat = self.bicycle.loc.lat
        bikeLon = self.bicycle.loc.lon

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\tBicycle \t\tLocation: {0}, {1}".format(bikeLat, bikeLon))

        # Get next signal from sim
        intId = self.nextSignal.int
        sigId = self.nextSignal.sig

        sigLoc = sim.getIntersection(intId).loc

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\tNext Signal: [{0}][{1}] Location: {2}, {3}".format(intId, sigId, sigLoc.lat, sigLoc.lon))

        # Get distance
        distance = getDistanceFromLatLonInM(
            bikeLat, bikeLon, sigLoc.lat, sigLoc.lon
        )

        self.bicycle.distanceToNXS = distance

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\tDistance between bicycle and signal: {0}m".format(round(distance,1)))

        # Get current speed
        bikeSpeed = self.bicycle.speed

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\tCurrent bicycle speed: {0}m/s\n".format(bikeSpeed))

        # Get next signal time to green "slots"
        signalStateAndTTG = sim.calcSignalStateAndTTG(intId, sigId, False)

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\tSignal State:\n")

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\t{0}\t{1}\t{2}\t{3}".format(
                signalStateAndTTG.state,
                signalStateAndTTG.ttg,
                signalStateAndTTG.gts,
                signalStateAndTTG.revolution
            ))

        currentlyGreen = False
        timeOfGreenLight = 0


        speeds = []

        if signalStateAndTTG.ttg < 0:
            currentlyGreen = True
            timeOfGreenLight = signalStateAndTTG.gts + signalStateAndTTG.ttg

            if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                print("\tIt is currently green light for another {0} seconds.".format(timeOfGreenLight))

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\n\tCalculating Speeds:")
            print("\n\t[BEGIN m/s]\t[END m/s]\t[BEGIN km/t]\t[END km/t]\t[FROM s]\t[TO s]")

        if currentlyGreen and timeOfGreenLight != 0:

            reachThisLightSpeed = distance / timeOfGreenLight
            reachThisLightSpeedKmT = msToKmt(reachThisLightSpeed)

            if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                print("\t[~3*10^8 m/s]\t[{0} m/s]\t[Lightspeed]\t[{1} km/t]\t[Now]\t\t[{2} s]".format(
                    round(reachThisLightSpeed, 1),
                    round(reachThisLightSpeedKmT, 1),
                    timeOfGreenLight
                ))

            # possibleSpeed = [None, reachThisLightSpeed, None, reachThisLightSpeedKmT, 0, timeOfGreenLight]
            possibleSpeed = SessionSpeed(None, reachThisLightSpeed, None, reachThisLightSpeedKmT, 0, timeOfGreenLight)

            possibleSpeed.bikeSpeed = bikeSpeed

            speeds.append(possibleSpeed)

        gts = signalStateAndTTG.gts

        revolution = signalStateAndTTG.revolution
        ttgNextBegin = signalStateAndTTG.ttg
        ttgNextEnd = ttgNextBegin + gts

        if currentlyGreen:
            ttgNextBegin = ttgNextBegin + revolution
            ttgNextEnd = ttgNextEnd + revolution

        if ttgNextBegin == 0 or ttgNextEnd == 0:
            ttgNextBegin = ttgNextBegin + revolution
            ttgNextEnd = ttgNextEnd + revolution

        beginSpeedMS = distance / ttgNextBegin
        endSpeedMS = distance / ttgNextEnd

        beginSpeedKmt = msToKmt(beginSpeedMS)
        endSpeedKmt = msToKmt(endSpeedMS)

        maxMS = 100/60/60*1000 # 1000 km/t
        minMS = 1

        while(endSpeedMS > 1):

            # possibleSpeed = [beginSpeedMS, endSpeedMS, beginSpeedKmt, endSpeedKmt, ttgNextBegin, ttgNextEnd]
            possibleSpeed = SessionSpeed(beginSpeedMS, endSpeedMS, beginSpeedKmt, endSpeedKmt, ttgNextBegin, ttgNextEnd)

            possibleSpeed.bikeSpeed = bikeSpeed

            speeds.append(possibleSpeed)

            # print("\t[{0} m/s]\t[{1} m/s]\t[{2} km/t]\t[{3} km/t]\t[{4} s]\t\t[{5} s]".format(
            #     round(beginSpeedMS, 1),
            #     round(endSpeedMS, 1),
            #     round(beginSpeedKmt, 1),
            #     round(endSpeedKmt, 1),
            #     ttgNextBegin,
            #     ttgNextEnd
            # ))

            # Calculate Next Time Span
            ttgNextBegin = ttgNextBegin + revolution
            ttgNextEnd = ttgNextEnd + revolution

            # Calculate Next Speeds
            beginSpeedMS = distance / ttgNextBegin
            endSpeedMS = distance / ttgNextEnd

            # Calculate Km/t
            beginSpeedKmt = msToKmt(beginSpeedMS)
            endSpeedKmt = msToKmt(endSpeedMS)


        # Print all speeds
        # for possibleSpeed in speeds:

            # if(possibleSpeed.beginMs == None): continue

            # possibleSpeed.info()

            # print("\t[{0} m/s]\t[{1} m/s]\t[{2} km/t]\t[{3} km/t]\t[{4} s]\t\t[{5} s]".format(
            #     round(possibleSpeed[0], 1),
            #     round(possibleSpeed[1], 1),
            #     round(possibleSpeed[2], 1),
            #     round(possibleSpeed[3], 1),
            #     possibleSpeed[4],
            #     possibleSpeed[5]
            # ))

        # Find out if the current speed is between
        currentSpeedInGreenTimespan = False

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\n")

        # speedDifferences = []

        for possibleSpeed in speeds:

            possibleSpeedDifferenceA = 0
            possibleSpeedDifferenceB = 0

            # If the next signal is currently green, this is the first
            if(possibleSpeed.beginMs == None):

                possibleSpeed.beginSpeedChangeKmt = possibleSpeed.endKmt - bikeSpeed
                possibleSpeed.endSpeedChangeKmt = possibleSpeed.endKmt - bikeSpeed

                if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                    print("\t{0}".format(possibleSpeed.info()))

                # print("\tTesting:\t\t\t\t[{0}]\t{1}\t[{2}]".format(
                #     round(bikeSpeed,1),
                #     round(possibleSpeedDifferenceA, 1),
                #     round(possibleSpeed[3],1)
                # ))

                if bikeSpeed > possibleSpeed.endKmt:
                    currentSpeedInGreenTimespan = True
                    # break

                continue

            possibleSpeed.beginSpeedChangeKmt = possibleSpeed.beginKmt - bikeSpeed
            possibleSpeed.endSpeedChangeKmt = possibleSpeed.endKmt - bikeSpeed
            # avgSpeed = (possibleSpeed[2] + possibleSpeed[3]) / 2
            # possibleAvgDifference = avgSpeed - bikeSpeed

            if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                print("\t{0}".format(possibleSpeed.info()))

            # Testing next speed


            # print("\tTesting:\t[{0}]\t{1}\t\t[{2}]({3})[{4}]\t{5}\t\t{6}".format(
            #     round(bikeSpeed,1),
            #     round(possibleSpeedDifferenceA, 1),
            #     round(possibleSpeed[2],1),
            #     round(avgSpeed,1),
            #     round(possibleSpeed[3],1),
            #     round(possibleSpeedDifferenceB, 1),
            #     possibleAvgDifference
            # ))

            # possibleSpeed.append()

            if bikeSpeed < possibleSpeed.beginKmt and bikeSpeed > possibleSpeed.endKmt:
                currentSpeedInGreenTimespan = True
                # break



        # if currentSpeedInGreenTimespan:
        #     if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
        #         print("\n\tThis is a green speed!")
        #
        #     self.bicycle.speedChange = 0
        #     self.bicycle.targetSpeed = bikeSpeed
        #     self.bicycle.deviceColor[0] = 0
        #     self.bicycle.deviceColor[1] = 255
        #     self.bicycle.deviceColor[2] = 0
        #
        #     return
        #
        # else:
        #     if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
        #         print("\n\tThis not a green speed!\n")

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\n\tCalculate Target Speed and Changes\n")

        for possibleSpeed in speeds:

            possibleSpeed.calcSpeedChange()

            # possibleSpeed.calcSpeedChangeVersion2()

            if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                print("\t{0}".format(possibleSpeed.info()))

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\n\tSorting Array\n")

        # ----------------------------------------------------------------------
        # Sort array after differences
        # ----------------------------------------------------------------------
        # speeds = sorted(speeds, key=attrgetter('relativeSpeedChange'))
        speeds = sorted(speeds, key=attrgetter('targetSpeed'), reverse=True)

        if bikeSpeed < CONFIG['session']['minSpeed']:
            if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                print("\n\tYou're moving with walking or less speed!")

            self.bicycle.speedChange = 0
            self.bicycle.targetSpeed = bikeSpeed
            self.bicycle.deviceColor[0] = 255
            self.bicycle.deviceColor[1] = 0
            self.bicycle.deviceColor[2] = 255

            return


        maxUpSpeedChange = bikeSpeed * 0.1
        targetMaxSpeed = CONFIG['session']['targetMaxSpeed']

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            for possibleSpeed in speeds:
                print("\t{0}".format(possibleSpeed.info()))

        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            print("\n\tFinding the Speed\n")

        # ----------------------------------------------------------------------
        # Finding the speed
        # ----------------------------------------------------------------------

        finalSpeed = None

        for possibleSpeed in speeds:

            if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                print("\t{0}".format(possibleSpeed.info()))

            # if possibleSpeed.speedChange > 0:

            # if possibleSpeed.speedChange < maxUpSpeedChange:
            if possibleSpeed.targetSpeed <= targetMaxSpeed:
                if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                    print("\tThis is the speed!")

                finalSpeed = possibleSpeed
                # self.bicycle.speedChange = possibleSpeed.speedChange
                # self.bicycle.targetSpeed = possibleSpeed.targetSpeed
                break
            #
            # else:
            #
            #     continue

            # if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
            #     print("\tThis is the speed!")
            #
            #
            # finalSpeed = possibleSpeed
            # # self.bicycle.speedChange = possibleSpeed.speedChange
            # # self.bicycle.targetSpeed = possibleSpeed.targetSpeed
            #
            # break

        if finalSpeed is None:
            print("SOMETHING WRONG!")
            return

        # ----------------------------------------------------------------------
        # Calculate color
        # ----------------------------------------------------------------------

        self.bicycle.speedChange = finalSpeed.speedChange
        self.bicycle.targetSpeed = finalSpeed.targetSpeed

        red = 0
        green = 0
        blue = 0

        if CONFIG['session']['colorAlgoritm'] == "sinCosColor":

            differenceFromAvg = finalSpeed.avgKmt - finalSpeed.targetSpeed

            avgOffset = (finalSpeed.beginKmt - finalSpeed.endKmt) / 2

            percentOffset = 0

            if avgOffset is not 0:
                percentOffset = abs(differenceFromAvg / avgOffset)

            if percentOffset > 1: percentOffset = 1

            piOffset = math.pi / 2 * percentOffset

            if finalSpeed.speedChange == 0:

                if differenceFromAvg == 0:
                    green = 255

                if differenceFromAvg > 0:
                    if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']: print("\tMaybe speed up?")
                    red = int(sin(piOffset) * 255 / 2)
                    green = 255 - red
                    # green = int(cos(piOffset) * 255 / 2 + 123)

                else:
                    if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']: print("\tMaybe slow down?")
                    blue = int(sin(piOffset) * 255 / 2)
                    green = 255 - blue
                    # green = int((cos(piOffset) * 255 / 2) + 123)

            if finalSpeed.speedChange > 0:

                red = 255

            elif finalSpeed.speedChange < 0:

                blue = 255

        # Print
        if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:

            cosRes = cos(piOffset)
            sinRes = sin(piOffset)

            print("\n\tBeing Speed:\t{0}".format(finalSpeed.beginKmt))
            print("\tAvg Speed:\t{0}".format(finalSpeed.avgKmt))
            print("\tEnd Speed:\t{0}\n".format(finalSpeed.endKmt))
            print("\tDifference:\t{0}".format(differenceFromAvg))
            print("\tAvg Offset:\t{0}".format(avgOffset))
            print("\tPercent Offset:\t{0}\n".format(percentOffset))
            print("\n\tCos({0}) = {1}".format(piOffset, cosRes))
            print("\tSin({0}) = {1}\n".format(piOffset, sinRes))
            print("\tRed color: {0}".format(red))
            print("\tGreen color: {0}".format(green))
            print("\tBlue color: {0}".format(blue))

        # ----------------------------------------------------------------------
        # Old Color Algorithm
        # ----------------------------------------------------------------------

        # Bicycle must increase speed
        if CONFIG['session']['colorAlgoritm'] == "threeColors":
            if self.bicycle.speedChange > 0:

                if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                    print("\tBike must increase speed by {0}!".format(self.bicycle.speedChange))

                # Red
                # red = int(translate(self.bicycle.speedChange, 0, maxUpSpeedChange, 0, 255))
                red = 255

                if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                    print("\tRed: {0}".format(red))

                self.bicycle.deviceColor[0] = red

                # Green
                self.bicycle.deviceColor[1] = 255 - red

                # Blue
                self.bicycle.deviceColor[2] = 0

            # Bicycle must decrease speed
            elif self.bicycle.speedChange < 0:

                if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                    print("\tBike must decrease speed by {0}!".format(self.bicycle.speedChange))

                if abs(self.bicycle.speedChange) > maxUpSpeedChange:

                    if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                        print("\tBike must decrease speed by more than max! (Blue)")

                    # Red
                    self.bicycle.deviceColor[0] = 0

                    # Green
                    self.bicycle.deviceColor[1] = 0

                    # Blue
                    self.bicycle.deviceColor[2] = 255

                else:

                    # Blue
                    # blue = int(translate(abs(self.bicycle.speedChange), 0, maxUpSpeedChange, 0, 255))
                    blue = 255

                    if CONFIG['debug']['session']['calcBicycleTargetSpeedAndColor']:
                        print("\tBlue: {0}".format(blue))

                    self.bicycle.deviceColor[2] = blue

                    # Green
                    self.bicycle.deviceColor[1] = 255 - blue

                    # Red
                    self.bicycle.deviceColor[0] = 0

            # No speed change
            else:

                # Red
                self.bicycle.deviceColor[0] = 0

                # Green
                self.bicycle.deviceColor[1] = 255

                # Blue
                self.bicycle.deviceColor[2] = 0


        # Target Speed
        self.bicycle.targetSpeed = bikeSpeed + self.bicycle.speedChange

        # End Speed
        self.bicycle.endSpeed = finalSpeed.endKmt

        # Begin Speed
        self.bicycle.beginSpeed = finalSpeed.beginKmt

        # Red
        self.bicycle.deviceColor[0] = red

        # Green
        self.bicycle.deviceColor[1] = green

        # Blue
        self.bicycle.deviceColor[2] = blue

        return



    def getBicycleTargetSpeedAndColor(self):

        message = ""

        #message = message + "\n# -----------------------------------------------------------\n"
        #message = message + "# Bicycle\n"
        #message = message + "# -----------------------------------------------------------\n\n"
        message = message + "\tDevice Color:\t\t\t[{0}, {1}, {2}]\n".format(self.bicycle.deviceColor[0], self.bicycle.deviceColor[1], self.bicycle.deviceColor[2])
        message = message + "\tCourse:\t\t\t\t{0} degrees\n".format(self.bicycle.course)
        message = message + "\tSpeed:\t\t\t\t{0} km/t\n".format(self.bicycle.speed)
        message = message + "\tSpeed Change:\t\t\t{0} km/t\n".format(round(self.bicycle.speedChange, 1))
        message = message + "\tTarget Speed:\t\t\t{0} km/t\n".format(round(self.bicycle.targetSpeed, 1))
        message = message + "\tGreen Begin Speed:\t\t\t{0} km/t\n".format(round(self.bicycle.beginSpeed, 1))
        message = message + "\tGreen End Speed:\t\t\t{0} km/t\n".format(round(self.bicycle.endSpeed, 1))
        message = message + "\tDistance to next signal:\t{0} m\n".format(round(self.bicycle.distanceToNXS, 1))

        return {
            "message" : message,
            "deviceColor" : self.bicycle.deviceColor,
            "course" : self.bicycle.course,
            "speed" : self.bicycle.speed,
            "beginSpeed" : self.bicycle.beginSpeed,
            "endSpeed" : self.bicycle.endSpeed,
            "speedChange" : self.bicycle.speedChange,
            "distanceToNXS" : self.bicycle.distanceToNXS
        }

    def getNextSignalStateAndTTG(self):

        message = ""

        # message = message  + "\n# -----------------------------------------------------------\n"
        # message = message  + "# Next Signal And State\n"
        # message = message  + "# -----------------------------------------------------------\n\n"
        message = message  + "\tInt: {0}\n".format(self.nextSignal.int)
        message = message  + "\tSig: {0}\n".format(self.nextSignal.sig)
        message = message  + "\tState: {0}\n".format(self.nextSignal.signalStateAndTTG.state)
        message = message  + "\tTime To Green: {0}\n".format(self.nextSignal.signalStateAndTTG.ttg)
        message = message  + "\tGreen Time Span: {0}\n".format(self.nextSignal.signalStateAndTTG.gts)
        message = message  + "\tRevolution: {0}\n\n".format(self.nextSignal.signalStateAndTTG.revolution)

        return {
            "message" : message,
            "int" : self.nextSignal.int,
            "sig" : self.nextSignal.sig,
            "state" : self.nextSignal.signalStateAndTTG.state.name,
            "ttg" : self.nextSignal.signalStateAndTTG.ttg,
            "gts" : self.nextSignal.signalStateAndTTG.gts,
            "revolution" : self.nextSignal.signalStateAndTTG.revolution
        }

    def getNextFiveSignals(self):
        array = [None, None, None, None, None]

        n = self.nextSignal.n

        array[0] = [self.nextSignal.sig, self.nextSignal.int]

        for i in range(4):
            try:
                int = self.routeIntAndSignals[i + n].nextInt
                sig = self.routeIntAndSignals[i + n].nextSig
                array[i + 1] = [int, sig]
            except:
                pass

        # print(array)

        return array

    def calcAllSignalStates(self, sim):
        for signal in self.routeIntAndSignals:
            sim.getSignal(signal.int, signal.sig).update()

    def getAllSignalStates(self, sim): return self.routeSignalStates

class SessionUpdate:

    def __init__(self):
        pass

class Motion:

    def __init__(self, loc, course, speed):
        self.loc
        self.speed
        self.course

class Bicycle:

    def __init__(self, id, loc, course, speed):

        self.id = id
        self.loc = loc
        self.speed = speed
        self.course = course
        self.updated = 0
        self.deviceColor = [0, 255, 0]
        self.targetSpeed = speed
        self.distanceToNXS = 0
        self.speedChange = 0
        self.endSpeed = 0
        self.beginSpeed = 0

    def setUpdated(self, updated): self.updated = updated
    def getUpdated(self): return self.updated

    def setLocation(self, loc): self.loc = loc
    def getLocation(self): return self.loc

    def setSpeed(self, speed): self.speed = speed
    def getSpeed(self): return self.speed

    def setCourse(self, course): self.course = course
    def getCourse(self): return self.course

    def setDeviceColor(self, r, g, b): self.deviceColor = [r, g, b]
    def getDeviceColor(self): return self.deviceColor

    def setTargetSpeed(self, speed): self.targetSpeed = speed
    def getTargetSpeed(self): return self.targetSpeed

class RouteSignal:

    def __init__(self, intxnId, sigId, loc, n):

        self.intxnId = intxnId
        self.sigId = sigId
        self.loc = loc
        self.n = n

    def distanceToPoint(self, lat, lon):
        return getDistanceFromLatLonInM(lat, lon, self.loc.lat, self.loc.lon)

class Route:

    def __init__(self, id):

        self.id = id
        self.signals = {}
        self.sigsOnRoute = []
        self.intxnsOnRoute = []

    def loadGPX(self, path):

        gpx_file = open(path, 'r')

        self.gpx = gpxpy.parse(gpx_file)

        # for track in self.gpx.tracks:
        #     for segment in track.segments:
        #         for point in segment.points:
        #             print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
        #
        # for waypoint in self.gpx.waypoints:
        #     print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))
        #
        # for route in self.gpx.routes:
        #     print('Route:')
        #
        #     firstPoint = False
        #
        #     prevPoint = []
        #
        #     for point in route.points:
        #
        #         if firstPoint:
        #             d = getDistanceFromLatLonInM(
        #                 prevPoint.latitude,
        #                 prevPoint.longitude,
        #                 point.latitude,
        #                 point.longitude,
        #             )
        #
        #             print(f"Distance {d}m.")
        #
        #         print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
        #
        #         prevPoint = point
        #         firstPoint = True
        #
        # # There are many more utility methods and functions:
        # # You can manipulate/add/remove tracks, segments, points, waypoints and routes and
        # # get the GPX XML file from the resulting object:
        #
        # print('GPX:', self.gpx.to_xml())

    def getRouteArray(self):

        array = []

        for route in self.gpx.routes:
            print('Route:')
            for point in route.points:
                print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

                array.append([point.latitude, point.longitude])

        print(array)

        return array

    def getRouteSignalsAndIntersections(self, intxns):

        for route in self.gpx.routes:

            if CONFIG['debug']['route']['findingSignals']:  print('Route:')

            firstPoint = True

            prevPoint = []

            for point in route.points:

                if not firstPoint:

                    distance = getDistanceFromLatLonInM(
                        prevPoint.latitude,
                        prevPoint.longitude,
                        point.latitude,
                        point.longitude,
                    )

                    course = getCourseFromLatLonInDegrees(
                        prevPoint.latitude,
                        prevPoint.longitude,
                        point.latitude,
                        point.longitude,
                    )

                    # if CONFIG['debug']['route']['findingSignals']: print(f"Point A [{prevPoint.latitude}, {point.longitude}] Point B [{point.latitude}, {prevPoint.longitude}], Distance {round(distance,2)}m. Courese {round(course,2)} degrees from north")
                    if CONFIG['debug']['route']['findingSignals']:
                        message = "Point A [" + str(prevPoint.latitude) + ", " + str(point.longitude) + "], Point B [" + str(point.latitude) + ", " + str(prevPoint.longitude) + "], Distance " + str(round(distance,2)) + "m. Courese " + str(round(course,2)) + " degrees from north."
                        print(message)

                    # Signals on this part of the route
                    foundSignals = []

                    # Check intersections
                    for intxn in intxns:

                        intLoc = intxns[intxn].getLocation();

                        intDistanceA = getDistanceFromLatLonInM(point.latitude, point.longitude, intLoc.lat, intLoc.lon)
                        intDistanceA = round(intDistanceA, 2)

                        intDistanceB = getDistanceFromLatLonInM(prevPoint.latitude, prevPoint.longitude, intLoc.lat, intLoc.lon)
                        intDistanceB = round(intDistanceB, 2)

                        if intDistanceA < distance and intDistanceB < distance:

                                self.intxnsOnRoute.append(intxn)

                                intxnId = intxns[intxn].intxnId

                                if CONFIG['debug']['route']['findingSignals']:
                                    # print(f"A: {intDistanceA}, B: {intDistanceA}")
                                    message = "A: " + str(intDistanceA) + ", B: " + str(intDistanceA)
                                    print(message)

                                bicycleCourse = (course - 180) % 360;

                                if CONFIG['debug']['route']['findingSignals']:
                                    # print(f"Bicycle course: {bicycleCourse}")
                                    message = "Bicycle course: " + str(bicycleCourse) + "."
                                    print(message)

                                for signal in intxns[intxn].signals:

                                    signalCourse = intxns[intxn].signals[signal].course

                                    if CONFIG['debug']['route']['findingSignals']:
                                        # print(f"Sig Course: {signalCourse}")
                                        message = "Sig Course: " + str(signalCourse)
                                        print(message)

                                    if signalCourse - bicycleCourse < 45 and bicycleCourse - signalCourse < 45:

                                        if CONFIG['debug']['route']['findingSignals']:
                                            print("This signal!")

                                        sigId = intxns[intxn].signals[signal].sigId

                                        sigIntId = intxnId+sigId

                                        if CONFIG['debug']['route']['findingSignals']:
                                            print(sigIntId)

                                        routeSignal = RouteSignal(intxnId, sigId, intxns[intxn].getLocation(), 0)

                                        self.signals[sigIntId] = routeSignal

                                        SignalDistanceFromA = round(routeSignal.distanceToPoint(point.latitude, point.longitude), 2)

                                        foundSignals.append([sigIntId, SignalDistanceFromA])

                    if CONFIG['debug']['route']['findingSignals']:
                        print(foundSignals)

                    foundSignals = sorted(foundSignals, key=itemgetter(1))

                    if CONFIG['debug']['route']['findingSignals']:
                        print(foundSignals)

                    for signal in foundSignals:
                        self.sigsOnRoute.append(signal[0])

                    # Check signals of those intersections

                if CONFIG['debug']['route']['findingSignals']:
                    print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

                prevPoint = point
                firstPoint = False

        i = 0

        for sigId in self.sigsOnRoute:

            signal = self.signals[sigId]

            signal.n = i

            #print(f"[{sigId}]: {signal.n}")

            i += 1

        array = []

        for sigId in self.sigsOnRoute:

            signal = self.signals[sigId]

            array.append([signal.intxnId, signal.sigId])

        return array

        # return self.intxnsOnRoute

    def listSignals(self):

        #i = 0

        for sigId in self.sigsOnRoute:

            signal = self.signals[sigId]

            #signal.n = i

            # print(f"[{sigId}]: {signal.intxnId}, {signal.sigId}, {signal.n}")
            message = "[" + str(sigId) + "]: " + str(signal.intxnId) + ", " + str(signal.sigId) + ", " + str(signal.n)
            print(message)

            #i += 1


            # signal = self.signals[sig]

            # print(f"[{signal.intxnId}][{signal.id}]")

    def getRouteSignalsArray(self):
        pass

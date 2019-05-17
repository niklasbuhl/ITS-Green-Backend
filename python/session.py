from world import CONFIG
from utility import *
from simulation import *
from world import CONFIG
# from math import abs
import gpxpy
import gpxpy.gpx
import threading
from operator import itemgetter, attrgetter, methodcaller
#
class SessionSignal:

    def __init__(self, n, int, sig, nextInt, nextSig, nextDist, lastDist, course, nextCourse, lastCourse):
        self.n= n
        self.int = int
        self.sig = sig
        self.nextInt = nextInt
        self.nextSig = nextSig
        self.nextDist = nextDist
        self.lastDist = lastDist
        self.course = course
        self.nextCourse = nextCourse
        self.lastCourse = lastCourse
        self.passed = False
        self.state = None

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

        print("S {0}\t{11}\tPassed: {10}\t [{1}][{2}] -> [{3}][{4}]\tnD: {5}m\tlD: {6}m\tC: {7}   \tnC: {8}   \tlC: {9}".format(
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
            self.state
        ))


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
        self.nextSignal = []

        # [targetSpeed, speedDifference, color]
        self.SpeedTarget = None
        self.speedDifference = None
        self.speedColor = None

        # Signal
        self.lastSignal = None
        self.nextSignal = None
        self.nextSignalState = None


        # Route
        self.routeBegun = False
        self.routeFinished = False


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

        # print(arrayLength)
        # firstSignal = True
        # lastSignal = False

        lastSignal = tempIntAndSigArray[arrayLength - 1]
        lastInt = lastSignal[0]
        lastSig = lastSignal[1]
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

            dist = 0

            intLocation = sim.getIntersection(int).loc

            course = sim.getSignal(int, sig).course

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

            tempSessionSignal = SessionSignal(i, int, sig, nextInt, nextSig, nextDist, lastDist, course, nextCourse, lastCourse)

            self.routeIntAndSignals.append(tempSessionSignal)

            # print("tSignal {3}\t[{0}][{1}]\tnDist: {2}\tlDist: {4}\tCor: {5}\tNext Cor: {6}".format(int, sig, dist, i, lastDist, course, nextCourse))


        # print(self.routeIntxns)
        # print(self.routeSignals)

        for signal in tempIntAndSigArray: self.routeIntxns.append(signal[0])
        for signal in tempIntAndSigArray: self.routeSignals.append([signal[0], signal[1]])

        for signal in self.routeIntAndSignals:

            # print(signal)
            signal.print()

            # n = signal.n
            # int = signal.int
            # sig = signal.sig
            # nextInt = signal.nextInt
            # nextSig = signal.nextSig
            # nextDist = round(signal.nextDist, 2)
            # lastDist = round(signal.lastDist, 2)
            # course = signal.course
            # nextCourse = signal.nextCourse
            # lastCourse = signal.lastCourse
            # passed = signal.passed
            #
            # print("S {0}\tPassed: {10}\t [{1}][{2}] -> [{3}][{4}]\tnD: {5}m\tlD: {6}m\tC: {7}   \tnC: {8}   \tlC: {9}".format(n, int, sig, nextInt, nextSig, nextDist, lastDist, course, nextCourse, lastCourse, passed))


        print("\n")

        self.nextSignal = self.routeIntAndSignals[0]
        self.lastSignal = self.routeIntAndSignals[-1]

        self.routeIntAndSignalsCalculated = True

    def getRouteIntxns(self): return self.routeIntxns

    def getRouteSignals(self): return self.routeSignals


    def calcNextSignal(self, sim):
        print("\n\nCalculating Next Signal\n")

        # Get bicycle location
        bicycleLoc = self.bicycle.loc

        # Get current next signal
        testNextSignal = self.nextSignal

        while(not self.routeFinished):

            # Get the current next signal location from sim
            nextSignalLoc = sim.getIntersection(testNextSignal.int).loc

            # Distance and angle between the bicycle and currentSignal
            dist = getDistanceFromLatLonInM(
                bicycleLoc.lat,
                bicycleLoc.lon,
                nextSignalLoc.lat,
                nextSignalLoc.lon
            )

            angle = getCourseFromLatLonInDegrees(
                bicycleLoc.lat,
                bicycleLoc.lon,
                nextSignalLoc.lat,
                nextSignalLoc.lon
            )

            print("Distance: {0}\tAngle: {1}".format(dist, angle))

            # Check if the current next signal is still in front of the bicyclist
            angleDifference = abs(angle - self.bicycle.course) % 180

            if angleDifference < 90:

                print("Signal is in front.")
                self.nextSignal = testNextSignal
                nextSignalInfront = True
                return

            else:

                try:
                    testNextSignal = self.routeIntAndSignals[testNextSignal.n + 1]
                except:
                    # Last signal
                    self.routeFinished = True
                    return

                print("Signal is in the back.")



        # Check if the next signal is in front of the bicyclist

            # If there is no signals in front of the bicyclist do something...

        # Check if which route AB the bicyclist is on

        # Check if it makes sense the intersection is that one

        # Check if (more things)

        # Get the state of the next signal

        # Return [id][state]

    def calcNextSignalState(self, sim): self.nextSignalState = sim.getSignal(self.nextSignal.int, self.nextSignal.sig).getState()

    def getNextSignalState(self): return self.nextSignalState

    def getNextSignal(self): return [self.nextSignal.int, self.nextSignal.sig]





    def calcBicycleSpeed(self, sim):
        print("\n\nCalculating Speed\n")
        # Current speed

        # Get bicycle location

        # Get next signal from sim

        # Get distance

        # Get current speed

        # Get next signal green "slots"

        # Calculate array of possible speeds

        # Get the one closest to the current speed

        # Calculate targeted speed
        self.speedTarget = 25

        # Calculate the speed difference
        self.speedDifference = 0

        # Calculate the color
        self.speedColor = [0,0,0]

    def getSpeedColor(self): return self.speedColor

    def getSpeedTarget(self): return self.speedTarget

    def getSpeedDiffernce(self): return self.speedDifference

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

            pass

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

    def setUpdated(self, updated): self.updated = updated
    def getUpdated(self): return self.updated

    def setLocation(self, loc): self.loc = loc
    def getLocation(self): return self.loc

    def setSpeed(self, speed): self.speed = speed
    def getSpeed(self): return self.speed

    def setCourse(self, course): self.course = course
    def getCourse(self): return self.course

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
                    for int in intxns:

                        intLoc = intxns[int].getLocation();

                        intDistanceA = getDistanceFromLatLonInM(point.latitude, point.longitude, intLoc.lat, intLoc.lon)
                        intDistanceA = round(intDistanceA, 2)

                        intDistanceB = getDistanceFromLatLonInM(prevPoint.latitude, prevPoint.longitude, intLoc.lat, intLoc.lon)
                        intDistanceB = round(intDistanceB, 2)

                        if intDistanceA < distance and intDistanceB < distance:

                                self.intxnsOnRoute.append(int)

                                intxnId = intxns[int].id

                                if CONFIG['debug']['route']['findingSignals']:
                                    # print(f"A: {intDistanceA}, B: {intDistanceA}")
                                    message = "A: " + str(intDistanceA) + ", B: " + str(intDistanceA)
                                    print(message)

                                bicycleCourse = (course - 180) % 360;

                                if CONFIG['debug']['route']['findingSignals']:
                                    # print(f"Bicycle course: {bicycleCourse}")
                                    message = "Bicycle course: " + str(bicycleCourse) + "."
                                    print(message)

                                for sig in intxns[int].signals:

                                    signalCourse = intxns[int].signals[sig].course

                                    if CONFIG['debug']['route']['findingSignals']:
                                        # print(f"Sig Course: {signalCourse}")
                                        message = "Sig Course: " + str(signalCourse)
                                        print(message)

                                    if signalCourse - bicycleCourse < 45 and bicycleCourse - signalCourse < 45:

                                        if CONFIG['debug']['route']['findingSignals']:
                                            print("This signal!")

                                        sigId = intxns[int].signals[sig].id

                                        sigIntId = intxnId+sigId

                                        if CONFIG['debug']['route']['findingSignals']:
                                            print(sigIntId)

                                        signal = RouteSignal(intxnId, sigId, intxns[int].getLocation(), 0)

                                        self.signals[sigIntId] = signal

                                        SignalDistanceFromA = round(signal.distanceToPoint(point.latitude, point.longitude), 2)

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

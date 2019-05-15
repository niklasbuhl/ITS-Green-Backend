from world import CONFIG
from utility import *
from simulation import *
from world import CONFIG
import gpxpy
import gpxpy.gpx
from operator import itemgetter, attrgetter, methodcaller
#
class Session:

    def __init__(self, id, bicycle, route):

        self.id = id
        self.route = route
        self.bicycle = bicycle

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

    def getRouteIntersections(self, intxns):

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

                    if CONFIG['debug']['route']['findingSignals']: print(f"Point A [{prevPoint.latitude}, {point.longitude}] Point B [{point.latitude}, {prevPoint.longitude}], Distance {round(distance,2)}m. Courese {round(course,2)} degrees from north")


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

                                if CONFIG['debug']['route']['findingSignals']: print(f"A: {intDistanceA}, B: {intDistanceA}")

                                bicycleCourse = (course - 180) % 360;

                                if CONFIG['debug']['route']['findingSignals']: print(f"Bicycle course: {bicycleCourse}")



                                for sig in intxns[int].signals:

                                    signalCourse = intxns[int].signals[sig].course

                                    if CONFIG['debug']['route']['findingSignals']: print(f"Sig Course: {signalCourse}")

                                    if signalCourse - bicycleCourse < 45 and bicycleCourse - signalCourse < 45:

                                        if CONFIG['debug']['route']['findingSignals']: print("This signal!")

                                        sigId = intxns[int].signals[sig].id

                                        sigIntId = intxnId+sigId

                                        if CONFIG['debug']['route']['findingSignals']: print(sigIntId)

                                        signal = RouteSignal(intxnId, sigId, intxns[int].getLocation(), 0)

                                        self.signals[sigIntId] = signal

                                        SignalDistanceFromA = round(signal.distanceToPoint(point.latitude, point.longitude), 2)

                                        foundSignals.append([sigIntId, SignalDistanceFromA])

                    if CONFIG['debug']['route']['findingSignals']: print(foundSignals)

                    foundSignals = sorted(foundSignals, key=itemgetter(1))

                    if CONFIG['debug']['route']['findingSignals']: print(foundSignals)

                    for signal in foundSignals:

                        self.sigsOnRoute.append(signal[0])

                    # Check signals of those intersections



                if CONFIG['debug']['route']['findingSignals']: ('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

                prevPoint = point
                firstPoint = False

        i = 0

        for sigId in self.sigsOnRoute:

            signal = self.signals[sigId]

            signal.n = i

            #print(f"[{sigId}]: {signal.n}")

            i += 1

    def listSignals(self):

        #i = 0

        for sigId in self.sigsOnRoute:

            signal = self.signals[sigId]

            #signal.n = i

            print(f"[{sigId}]: {signal.intxnId}, {signal.sigId}, {signal.n}")

            #i += 1


            # signal = self.signals[sig]

            # print(f"[{signal.intxnId}][{signal.id}]")

    def getRouteSignalsArray(self):

        array = []

        for sigId in self.sigsOnRoute:

            signal = self.signals[sigId]

            array.append([signal.intxnId, signal.sigId])

        return array

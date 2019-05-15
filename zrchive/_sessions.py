from utility import *

class Bicyclist:

    # Location,
    # Motion: Motion, Speed, Direction, Acceleration

    def __init__(self, id):

        # ID
        self.id = id

        # Current Motion
        self.currentSpeed = 0
        self.currentCourse = 0
        self.currentAcceleration = 0

        # Instructions
        self.instructedSpeed = 0
        self.instructedCourse = 0

        # Location
        self.latitude = 0
        self.longitude = 0

    def setLocation(lat, lon):
        self.latitude = lat
        self.longitude = lon

    def setSpeed(speed):
        self.speed = speed

    def setCourse(course):
        self.course = course

class Session:

    # Setup
    def __init__(self):

        #self.bicyclist = Bicyclist()

        # Bicyclist
        # GPX Route

        self.id
        self.bicyclist = Bicyclist()

    # End, kill
    def stop():
        pass

    # Thread Run ???
    def run():
        pass

    def setRoute():
        pass

    def getRoute():
        pass

    def addIntersection():
        pass

    def addSignal():
        pass

    def getRouteIntersections():
        pass

    def getRouteSignals():
        pass

    def getBicyclistLocation():
        pass

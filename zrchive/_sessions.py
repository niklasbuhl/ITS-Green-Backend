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


                # print("\tTesting:\t\t\t\t[{0}]\t{1}\t[{2}]".format(
                #     round(bikeSpeed,1),
                #     round(possibleSpeedDifferenceA, 1),
                #     round(possibleSpeed[3],1)
                # ))


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


            # print("\t[{0} m/s]\t[{1} m/s]\t[{2} km/t]\t[{3} km/t]\t[{4} s]\t\t[{5} s]".format(
            #     round(beginSpeedMS, 1),
            #     round(endSpeedMS, 1),
            #     round(beginSpeedKmt, 1),
            #     round(endSpeedKmt, 1),
            #     ttgNextBegin,
            #     ttgNextEnd
            # ))

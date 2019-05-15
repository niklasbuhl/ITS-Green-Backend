import time
from math import sin, cos, sqrt, atan2, radians, degrees
# from datetime import datetime

'''
ABRREVATIONS

intxn : intersection
intxns : intersections
loc : location
lat : latitude
lon : longitude
sigs : signals
typ : type
crs : course
ssn : session
ssns : sessions

iXX : intersection id
sXX : signal id

'''

# debug = True
# runApp = True
# testSimulation = True
# testRunSimulation = False
# debugSignalUpdateTiming = False



ms = lambda: int(round(time.time() * 1000))

sessionFilepath = ""

sessionStarted = False

def startSession():
    global sessionFilepath, sessionStarted

    # now = datetime.now()

    timestr = time.strftime("%Y-%m-%d_%H-%M-%S")

    sessionFilepath = "./log/SESSION_" + timestr + ".log"

    print(sessionFilepath)

    file = open(sessionFilepath, "w+")
    file.close()

    sessionStarted = True

    sessionLog("Session started...")

def sessionLog(message):
    global sessionFilepath, sessionStarted

    if not sessionStarted: startSession()

    timestr = time.strftime("%Y:%m:%d %H:%M:%S\t")

    message = timestr + message + "\n"

    print(message)

    file = open(sessionFilepath, "w+")

    file.write(message)

    file.close()



# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/27943#27943
def getDistanceFromLatLonInM(lat1,lon1,lat2,lon2):
    R = 6371 # Radius of the earth in km
    dLat = radians(lat2-lat1)
    dLon = radians(lon2-lon1)
    rLat1 = radians(lat1)
    rLat2 = radians(lat2)
    a = sin(dLat/2) * sin(dLat/2) + cos(rLat1) * cos(rLat2) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c # Distance in km
    distance = d * 1000 # Distance in meters
    return distance

def getCourseFromLatLonInDegrees(lat1, lon1, lat2, lon2):
    course = atan2(sin(lon2-lon1)*cos(lat2), cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))
    course = degrees(course)
    course = (course + 360) % 360
    return course

def calc_velocity(dist_km, time_start, time_end):
    """Return 0 if time_start == time_end, avoid dividing by 0"""
    return dist_km / (time_end - time_start).seconds if time_end > time_start else 0

'''

degs = [0,45,90,135,180,225,270,315,360]

for deg in degs:

    res = (deg - 180) % 360
    print(f"{deg} opposite is {res}")


'''

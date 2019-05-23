from flask import Flask, request, render_template, jsonify
import threading
import time
import json
import sys
import gpxpy
import gpxpy.gpx

sys.path.insert(0, './python')

from world import CONFIG
from utility import ms, startSessionLog, sessionLog
from simulation import Simulation, Intersection, Signal, Location
from session import Session, Bicycle, Route

# startSessionLog()
# sessionLog("Session started...")

# ------------------------------------------------------------------------------
# Flask Application
# ------------------------------------------------------------------------------

app = Flask(__name__)

# ------------------------------------------------------------------------------
# Load API Documentation
# ------------------------------------------------------------------------------

API = None

with open("./json/api.json", "r") as read_file:
    API = json.load(read_file)

if CONFIG['debug']['loadingJSON']: print(json.dumps(API, indent=4, sort_keys=True))

# ------------------------------------------------------------------------------
# Hello World
# ------------------------------------------------------------------------------

helloWorldMessage = "Hello, World Version 2.0.3"

print("\n" + helloWorldMessage)

@app.route(API['pages']['hello'])
def helloWorld():
    return render_template(
        "index.html",
        message = helloWorldMessage,
        mapUrl = API['pages']['map'],
        controlUrl = API['pages']['control']
    )

# ------------------------------------------------------------------------------
# Pages
# ------------------------------------------------------------------------------

# Control
@app.route(API['pages']['control'])
def controlPage():
    return render_template(
        "control.html",
        start = API['sim']['start']['url'],
        stop = API['sim']['stop']['url']
    )

# Map
@app.route(API['pages']['map'])
def mapPage():
    return render_template("map.html")

# Session
@app.route(API['pages']['session'])
def sessionPage():
    pass
    # return render_template("color.html")

# Route Intersections
@app.route(API['pages']['routeIntxns'])
def routeIntxnsPage():
    pass

# ------------------------------------------------------------------------------
# API: Browser Simulation Visualization
# ------------------------------------------------------------------------------

# Get a list of all intersections
@app.route(API['sim']['getIntxns']['url'])
def simulationGetIntersections():
    # intersections: id, location, signals: type, id, course

    # Return json with intersection data from all Intersections
    # id, location, signal

    # Create a JSON array
    json_data = sim.getIntxnsAndSignals()

    return jsonify(json_data)

# ------------------------------------------------------------------------------
# API: Session
# ------------------------------------------------------------------------------

@app.route(API['session']['setBicycle']['url'], methods=['GET', 'POST'])
def sessionSetBicycle():

    # Set bicycle location

    # Get the HTTP POST Body Content
    content = request.get_json()

    if CONFIG['debug']['setbicycle']:

        print("\nSet Bicycle HTTP GET Request Received.\n")
        print(content)
        print("\n")

        print("\nBicycle Update!\n")
        print("\tTime: " + str(content['time']))
        print("\tLat: " + str(content['latitude']))
        print("\tLon: " + str(content['longitude']))
        print("\tSpeed: " + str(content['speed']))
        print("\tCourse: " + str(content['course']))
        print("\n")

    # Time
    sesh.bicycle.setUpdated(int(content['time']))

    # Location
    sesh.bicycle.setLocation(Location(
        float(content['latitude']), float(content['longitude'])
    ))

    # Speed
    if content['speed'] != -1:
        speed = msToKmt(float(content['speed']))
        sesh.bicycle.setSpeed(speed)

    # Course
    sesh.bicycle.setCourse(float(content['course']))

    # Set Calculate Thread Flag
    # ???

    # Return nothing, except accepted
    return ('', 204)

@app.route(API['session']['getBicycle']['url'])
def sessionGetBicycle():
    # Location, Course, Speed

    return jsonify(
        time = sesh.bicycle.updated,
        latitude = sesh.bicycle.loc.lat,
        longitude = sesh.bicycle.loc.lon,
        speed = sesh.bicycle.speed,
        course = sesh.bicycle.course
    )

# The Grand API Request that calculated everything...

@app.route(API['session']['getDeviceColor']['url'])
def sessionGetDeviceColor():
    global sim, sesh

    # Calculate Next Signal on Route
    sesh.calcNextSignal(sim)

    # Calculate Next Signal State and TTG
    sesh.calcNextSignalStateAndTTG(sim)

    # Calculate Bicycle Target Speed And Color
    sesh.calcBicycleTargetSpeedAndColor(sim)

    # Get Bicycle Target Speed and Color
    #sesh.getBicycleTargetSpeedAndColor()

    # Get Next Signal State And TTG
    #sesh.getNextSignalStateAndTTG()

    # Location, Course
    # [target speed, speed difference, color]
    return jsonify(
        r = sesh.bicycle.deviceColor[0],
        g = sesh.bicycle.deviceColor[1],
        b = sesh.bicycle.deviceColor[2]
    )


# Get Next Signal State And TTG
@app.route(API['session']['getNextSignalStateAndTTG']['url'])
def sessionGetNextSignalStateAndTTG():
    global sesh, sim

    # Calculate Next Signal on Route
    sesh.calcNextSignal(sim)

    # Calculate Next Signal State and TTG
    sesh.calcNextSignalStateAndTTG(sim)

    # Calculate Bicycle Target Speed And Color
    sesh.calcBicycleTargetSpeedAndColor(sim)

    data = sesh.getNextSignalStateAndTTG()

    # Do something with the data...

    return ('', 204)

@app.route(API['session']['getBicycleTargetSpeedAndColor']['url'])
def sessionGetBicycleTargetSpeedAndColor():
    global sesh, sim

    # Calculate Next Signal on Route
    sesh.calcNextSignal(sim)

    # Calculate Next Signal State and TTG
    sesh.calcNextSignalStateAndTTG(sim)

    # Calculate Bicycle Target Speed And Color
    sesh.calcBicycleTargetSpeedAndColor(sim)

    data = sesh.getBicycleTargetSpeedAndColor()

    # Do something with the data...

    return ('', 204)

@app.route(API['session']['getRoute']['url'])
def sessionGetRoute():
    # GPX route as point
    return jsonify(sesh.getRoute())

@app.route(API['session']['getSignals']['url'])
def sessionGetSignals():
    # Signals on the route
    return jsonify(sesh.getRouteSignals())

@app.route(API['session']['getIntxns']['url'])
def sessionGetIntersections():
    # Route Specific Intersections
    return jsonify(sesh.getRouteIntxns())

# @app.route(API['session']['getTargetSpeedAndColor']['url'])
# def sessionGetTargetSpeedAndColor():
#     pass

@app.route(API['session']['getAllSignalStates']['url'])
def sessionAllSignalStates():
    pass

@app.route(API['session']['startWestGoingNoerrebrogade']['url'])
def sessionStartWestGoingNoerrebrogade():
    global sesh

    # Clear the data somehow...

    sesh = Session('Noerrebrogade Going West', Bicycle('b01', Location(0,0), 0, 0), Route('r01'))

    sesh.loadRouteGPX('./gpx/dronninglouisesbro-frederikssundvej.gpx')

    sesh.calcRouteIntxnsAndSignals(sim)

    # Return nothing
    return ('', 204)

# ------------------------------------------------------------------------------
# Load Intersections from JSON
# ------------------------------------------------------------------------------

if CONFIG['debug']['application']: print("\nLoading intersections")

data = json.load(open(CONFIG['data']['intxns']['jsonpath'], 'r'))

if CONFIG['debug']['loadingJSON']: print(json.dumps(data, indent=4, sort_keys=True))

# ------------------------------------------------------------------------------
# Setup Simulation
# ------------------------------------------------------------------------------

sim = Simulation()

sim.loadIntersections(data)

# ------------------------------------------------------------------------------
# Setup Initial 'Noerrebrogade Going West' Session
# ------------------------------------------------------------------------------

sesh = Session('Noerrebrogade Going West', Bicycle('b01', Location(0,0), 0, 0), Route('r01'))

sesh.loadRouteGPX('./gpx/dronninglouisesbro-frederikssundvej.gpx')

sesh.calcRouteIntxnsAndSignals(sim)

# ------------------------------------------------------------------------------
# Run a few tests...
# ------------------------------------------------------------------------------

now = ms()

print("\n# ---------------------------------------------------------------")
print("# Run a few tests...")
print("# ---------------------------------------------------------------")

# Set Bicycle Position to Nørreport
sesh.bicycle.setUpdated(0)
sesh.bicycle.setLocation(Location(55.683634, 12.571796))
sesh.bicycle.setSpeed(20)
sesh.bicycle.setCourse(300)

# Calculate Next Signal on Route
sesh.calcNextSignal(sim)

# Calculate Next Signal State and TTG
sesh.calcNextSignalStateAndTTG(sim)

# Calculate Bicycle Target Speed And Color
sesh.calcBicycleTargetSpeedAndColor(sim)

# Get Bicycle Target Speed and Color
sesh.getBicycleTargetSpeedAndColor()

# Get Next Signal State And TTG
sesh.getNextSignalStateAndTTG()

# Peace
print("Peace out! {0} ms\n\n".format(ms() - now))

# ------------------------------------------------------------------------------
# Web Application
# ------------------------------------------------------------------------------

if CONFIG['web']['run']:
    if __name__ == "__main__":
        app.run(host = '0.0.0.0', port = 80)

from flask import Flask, request, render_template, jsonify
import threading
import time
import json
import sys
import gpxpy
import gpxpy.gpx

sys.path.insert(0, './python')

from world import CONFIG
from utility import ms, startSession, sessionLog
from simulation import Simulation, Intersection, Signal, Location
from session import Session, Bicycle, Route

startSession()

# ------------------------------------------------------------------------------
# Flask Application
# ------------------------------------------------------------------------------

app = Flask(__name__)

# ------------------------------------------------------------------------------
# Load API Documentation
# ------------------------------------------------------------------------------

API = ""

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
# Browser Control Page
# ------------------------------------------------------------------------------

@app.route(API['pages']['control'])
def controlPage():
    return render_template(
        "control.html",
        start = API['sim']['start']['url'],
        stop = API['sim']['stop']['url']
    )

# ------------------------------------------------------------------------------
# Simulation View Page
# ------------------------------------------------------------------------------

@app.route(API['pages']['map'])
def simulationPage():
    return render_template("map.html")

# ------------------------------------------------------------------------------
# Color Page
# ------------------------------------------------------------------------------

@app.route(API['pages']['color'])
def color():
    return render_template("color.html")

# ------------------------------------------------------------------------------
# API Browser Simulation Visualization Data
# ------------------------------------------------------------------------------

# Get a list of all intersections
@app.route(API['sim']['getIntxns']['url'])
def simulationGetIntersections():
    # intersections: id, location, signals: type, id, course

    # Return json with intersection data from all Intersections
    # id, location, signal

    # Create a JSON array
    json_data = sim.getIntxnsAndSignals()



    # for intersection in Intersections:
    #     id = Intersections[intersection].id
    #     lat = Intersections[intersection].latitude
    #     lon = Intersections[intersection].longitude
    #
    #     json.append({"id" : id, "lat": lat, "lon": lon})


    #testJSON = [{"S01" : "Niklas", "S02" : "Sine"}]


    return jsonify(json_data)

# Get a specific signal state
@app.route(API['sim']['getSignalState']['url'])
def simulationGetSignalState():
    # Signal state: RED, ORANGE, GREEN, YELLOW

    intxnId = request.args.get('intxnid')
    sigId = request.args.get('sigid')

    return jsonify(
        state = sim.intxns[intxnId].signals[sigId].getState(),
        intId = intxnId,
        sigId = sigId
    )

# Get a specific ttg
@app.route(API['sim']['getSignalTTG']['url'])
def simulationGetTTG():
    # Signal TTG: 1.2 s

    intxnId = request.args.get('intxnid')
    sigId = request.args.get('sigid')

    return sim.intxns[intxnId].signals[sigId].getTTG()

@app.route(API['sim']['start']['url'])
def startSimulation():
    # Start simulation (signal threads)
    sim.start()

    return ('', 204)

@app.route(API['sim']['stop']['url'])
def stopSimulation():
    # Stop simulation (signal threads)
    sim.stop()

    return ('', 204)

# ------------------------------------------------------------------------------
# API Browser Session Visualization Data
# ------------------------------------------------------------------------------

@app.route(API['session']['setBicycle']['url'], methods=['GET', 'POST'])
def sessionSetBicycleLocation():
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
    sesh.bicycle.setUpdated(content['time'])

    # Location
    sesh.bicycle.setLocation(Location(content['latitude'], content['longitude']))

    # Speed
    if content['speed'] != -1: sesh.bicycle.setSpeed(content['speed'])

    # Course
    sesh.bicycle.setCourse(content['course'])

    return ('', 204)

@app.route(API['session']['getBicycle']['url'])
def sessionGetBicycle():
    # Location, Course

    return jsonify(
        time = sesh.bicycle.updated,
        latitude = sesh.bicycle.loc.lat,
        longitude = sesh.bicycle.loc.lon,
        speed = sesh.bicycle.speed,
        course = sesh.bicycle.course
    )

@app.route(API['session']['getColor']['url'])
def sessionGetColor():
    # Location, Course
    # [target speed, speed difference, color]
    return jsonift(sesh.getSessionSpeed())

@app.route(API['session']['setRoute']['url'])
def sessionSetRoute():
    # GPX route
    pass

@app.route(API['session']['getRoute']['url'])
def sessionGetRoute():
    # GPX route
    return jsonify(sesh.getRoute())

@app.route(API['session']['getSignals']['url'])
def sessionGetSignals():
    # Signals on the route
    return jsonify(sesh.getRouteSignals())

@app.route(API['session']['getIntxns']['url'])
def sessionIntersections():
    # Route Specific Intersections
    return jsonift(sesh.getRouteIntxns())

@app.route(API['session']['getNextSignal']['url'])
def sessionNextSignal():
    # Route Specific Next Intersections
    # [id, state]
    return jsonify(sesh.getNextSignal())

@app.route(API['session']['getNextFiveSignals']['url'])
def sessionNextFiveSignals():
    pass

@app.route(API['session']['getAllSignalStates']['url'])
def sessionAllSignalStates():
    pass

# ------------------------------------------------------------------------------
# API Application Control
# ------------------------------------------------------------------------------



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
# Setup Session
# ------------------------------------------------------------------------------

# sesh = Session()

# bike =

sesh = Session('norrebrogade', Bicycle('b01', Location(0,0), 0, 0), Route('r01'))

sesh.loadRouteGPX('./gpx/dronninglouisesbro-frederikssundvej.gpx')
# sesh.route.loadGPX('./gpx/dronninglouisesbro-frederikssundvej.gpx')

sesh.calcRouteIntxnsAndSignals(sim)
# sesh.route.getRouteIntersections(sim.intxns)

# sesh.calcNextSignal()

# sesh.setRoute(route)

# ------------------------------------------------------------------------------
# Test Next Signal
# ------------------------------------------------------------------------------

sesh.calcNextSignal(sim)
print(sesh.getNextSignal())
sesh.calcNextSignalState(sim)
print(sesh.getNextSignalState())
print(sesh.getNextFiveSignals())

# sesh.calcAllSignalStates()

# print(sesh.getAllSignalStates())

# 55.689490
# 12.556548

sesh.bicycle.setUpdated(0)
sesh.bicycle.setLocation(Location(55.689490, 12.556548))
sesh.bicycle.setSpeed(20)
sesh.bicycle.setCourse(140)

sesh.calcNextSignal(sim)
print(sesh.getNextSignal())
sesh.calcNextSignalState(sim)
print(sesh.getNextSignalState())
print(sesh.getNextFiveSignals())

# ------------------------------------------------------------------------------
# Test Run Simulation
# ------------------------------------------------------------------------------

# Start Simulation Signal Threads
if CONFIG['test']['simulation']: sim.start()

# Timer
if CONFIG['test']['simulation']: time.sleep(10)

# Stop Simulation Signal Threads
if CONFIG['test']['simulation']:  sim.stop()

# ------------------------------------------------------------------------------
# Testing Functionsx
# ------------------------------------------------------------------------------

sim.getIntxnsAndSignals()

# ------------------------------------------------------------------------------
# Web Application
# ------------------------------------------------------------------------------

# if CONFIG['web']['run']:
#     if __name__ == "__main__":
#         app.run(host = '0.0.0.0', port = 80)

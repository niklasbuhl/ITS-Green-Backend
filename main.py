from flask import Flask, request, render_template
import threading
import time

from utility import *
from simulation import *
from sessions import *

app = Flask(__name__)

# ------------------------------------------------------------------------------
# Hello World
# ------------------------------------------------------------------------------
helloWorldMessage = "Hello, World Version 2.0.3"

print(helloWorldMessage)

@app.route("/")
def helloWorld():
    return render_template("index.html", message = helloWorldMessage)

# ------------------------------------------------------------------------------
# Browser Simulation Visualization Page
# ------------------------------------------------------------------------------

@app.route("/simulation/")
def simulation():
    return render_template("simulation.html")

# ------------------------------------------------------------------------------
# Browser Control Page
# ------------------------------------------------------------------------------

@app.route("/control/")
def controlPage():
    return render_template("control.html")

# ------------------------------------------------------------------------------
# Simulation View Page
# ------------------------------------------------------------------------------

@app.route("/map/")
def simulationPage():
    return render_template("map.html")

# ------------------------------------------------------------------------------
# Browser Simulation Visualization Data
# ------------------------------------------------------------------------------

# Get a list of all intersections
@app.route("/sim/intxns")
def simulationGetIntersections():
    # intersections: id, location, signals: type, id, course

    pass

# Get a specific signal state
@app.route("/sim/signal/ss")
def simulationGetSignalState():
    # Signal state: RED, ORANGE, GREEN, YELLOW

    intxnId = request.args.get('intxnid')
    sigId = request.args.get('sigid')

    return sim.intxns[intxnId].signals[sigId].getState()

# Get a specific ttg
@app.route("/sim/signal/ttg")
def simulationGetTTG():
    # Signal TTG: 1.2 s

    intxnId = request.args.get('intxnid')
    sigId = request.args.get('sigid')

    return sim.intxns[intxnId].signals[sigId].getTTG()

@app.route("/sim/start/")
def startSimulation():
    # Start simulation (signal threads)
    sim.start()

    return ('', 204)

@app.route("/sim/stop/")
def stopSimulation():
    # Stop simulation (signal threads)
    sim.stop()

    return ('', 204)

# ------------------------------------------------------------------------------
# Browser Session Visualization Data
# ------------------------------------------------------------------------------

@app.route("/session/getbicycle/")
def sessionGetBicycle():
    # Location, Course

    pass

@app.route("/session/getroute/")
def sessionGetRoute():
    # GPX route

    pass

@app.route("/session/getinterections/")
def sessionIntersections():
    # Route Specific Intersections

    pass

@app.route("/session/getnextintersection/")
def sessionNextIntersection():
    # Route Specific Next Intersections

    pass

@app.route("/sessions/setbicyclelocation/")
def sessionSetBicycleLocation():
    # Set bicycle location

    pass


# ------------------------------------------------------------------------------
# Load Intersections from JSON
# ------------------------------------------------------------------------------

path = "noerrebrogade-frederikssundvej-intersections.json"
if debug: print("Loading intersections")
data = json.load(open(path, 'r'))
if debug: print(json.dumps(data, indent=4, sort_keys=True))

# ------------------------------------------------------------------------------
# Setup Simulation
# ------------------------------------------------------------------------------

sim = Simulation()

sim.loadIntersections(data)

# ------------------------------------------------------------------------------
# Setup Session
# ------------------------------------------------------------------------------

# sesh = Session()

# ------------------------------------------------------------------------------
# Test Run Simulation
# ------------------------------------------------------------------------------now = ms()

# Start Simulation Signal Threads
if testRunSimulation: sim.start()

# Timer
if testRunSimulation: time.sleep(10)

# Stop Simulation Signal Threads
if testRunSimulation:  sim.stop()

# ------------------------------------------------------------------------------
# Web Application
# ------------------------------------------------------------------------------

if runApp:
    if __name__ == "__main__":
        app.run()

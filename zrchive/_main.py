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





    # for intersection in Intersections:
    #     id = Intersections[intersection].id
    #     lat = Intersections[intersection].latitude
    #     lon = Intersections[intersection].longitude
    #
    #     json.append({"id" : id, "lat": lat, "lon": lon})


@app.route(API['session']['getNextSignal']['url'])
def sessionNextSignal():
    # Route Specific Next Intersections
    # [id, state]
    return jsonify(sesh.getNextSignal())

@app.route(API['session']['getNextSignalState']['url'])
def sessionNextSignalState():
    return sesh.getNextSignalState()

@app.route(API['session']['getNextFiveSignals']['url'])
def sessionNextFiveSignals():
    pass


@app.route(API['session']['setRoute']['url'])
def sessionSetRoute():
    # GPX route
    # Not developed
    pass

# ------------------------------------------------------------------------------
# Test Run Simulation
# ------------------------------------------------------------------------------

# Start Simulation Signal Threads
if CONFIG['test']['simulation']: sim.start()

# Timer
if CONFIG['test']['simulation']: time.sleep(10)

# Stop Simulation Signal Threads
if CONFIG['test']['simulation']:  sim.stop()


# Dronning Dronninglouises Bro
# sesh.bicycle.setUpdated(0)
# sesh.bicycle.setLocation(Location(55.686465, 12.564398))
# sesh.bicycle.setSpeed(20)
# sesh.bicycle.setCourse(300)

# sesh.calcNextSignal(sim)
# print(sesh.getNextSignal())
# sesh.calcNextSignalState(sim)
# print(sesh.getNextSignalState())
# print(sesh.getNextFiveSignals())

# sesh.calcAllSignalStates()

# print(sesh.getAllSignalStates())

# 55.689490
# 12.556548

# sesh.bicycle.setUpdated(0)
# sesh.bicycle.setLocation(Location(55.689490, 12.556548))
# sesh.bicycle.setSpeed(20)
# sesh.bicycle.setCourse(320)
#
# sesh.calcNextSignal(sim)
# print(sesh.getNextSignal())
# sesh.calcNextSignalState(sim)
# print(sesh.getNextSignalState())
# print(sesh.getNextFiveSignals())
#
# sim.calcSignalStateAndTTG(sesh.getNextSignal()[0], sesh.getNextSignal()[1])

# ------------------------------------------------------------------------------
# Testing Functionsx
# ------------------------------------------------------------------------------

# sim.getIntxnsAndSignals()

# Dronning Dronninglouises Bro
# (Too close xD)
# sesh.bicycle.setUpdated(0)
# sesh.bicycle.setLocation(Location(55.686465, 12.564398))
# sesh.bicycle.setSpeed(20)
# sesh.bicycle.setCourse(300)

# Nørre Port
# sesh.bicycle.setUpdated(0)
# sesh.bicycle.setLocation(Location(55.683634, 12.571796))
# sesh.bicycle.setSpeed(20)
# sesh.bicycle.setCourse(300)
#
# sim.calcSignalStateAndTTG(sesh.getNextSignal()[0], sesh.getNextSignal()[1], True)
#
# sesh.calcNextSignal(sim)
# print(sesh.getNextSignal())
# # sesh.calcNextSignalState(sim)
# # print(sesh.getNextSignalState())
# # print(sesh.getNextFiveSignals())
#
# sesh.calcBicycleSpeed(sim)

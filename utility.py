import time

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

debug = True
runApp = True
testSimulation = True
testRunSimulation = False

debugSignalUpdateTiming = False

ms = lambda: int(round(time.time() * 1000))


'''
Basic URLs

http://0.0.0.0:5000/sim/

http://0.0.0.0:5000/sim/start

http://0.0.0.0:5000/sim/signal/ss?intxnid=i01&sigid=s02

http://0.0.0.0:5000/sim/signal/ttg?intxnid=i01&sigid=s02

http://0.0.0.0:5000/sim/stop



'''

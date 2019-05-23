const Intersection = require('./intersection.js');
// const Visualization = require('./javascript/visualization.js');

// -----------------------------------------------------------------------------
// Simulation
// -----------------------------------------------------------------------------

class Simulation {

  constructor() {

    if(CONFIG.debug.simulation) console.log("Creating new Simulation");

    // Intersection
    this.intxns = new Map()

    this.intxnsLoaded = false;

    this.intersectionsLoaded = false;

  }

  loadIntersectionsAndSignals(data) {

    if(CONFIG.debug.simulation) console.log("Getting new simulation data");

    if(CONFIG.debug.Simulation) console.log(data);

    for(var intxn in data) {

      // Id
      if(CONFIG.debug.simulation) console.log("id: "+intxn+".");

      // Lat
      var lat = data[intxn]['lat'];
      if(CONFIG.debug.simulation) console.log("lat: "+lat+".");

      // Lon
      var lon = data[intxn]['lon'];
      if(CONFIG.debug.simulation) console.log("lon: "+lon+".");

      var tempIntxn = new Intersection(intxn, lat, lon);

      for(var signal in data[intxn]['signals']) {

        // Id
        if(CONFIG.debug.simulation) console.log("\tid:"+signal+".");

        // Course
        var course = data[intxn]['signals'][signal]['course'];
        if(CONFIG.debug.simulation) console.log("\tcourse: "+course+".");

        // Add signal to intersection
        tempIntxn.addSignal(signal, course);

      }

      this.intxns.set(intxn, tempIntxn);

    }

    this.intersectionsLoaded = true;

  }

  listAllIntersectionsAndSignals() {

    if (!this.intersectionsLoaded) return;

    console.log("\nListing all intersections.\n\n");
    // if (CONFIG.debug.simulation) console.log(this.intxns);

    for (var int of this.intxns.values()) {
      // if (CONFIG.debug.simulation) console.log(int);
      console.log("\tIntersection["+int.id+"]");
      console.log("\tLat: "+int.loc.lat+".");
      console.log("\tLon: "+int.loc.lon+".\n\n");


      for (var sig of int.signals.values()) {
        // if (CONFIG.debug.simulation) console.log(sig);
        console.log("\t\tSignal["+sig.id+"]");
        console.log("\t\tCourse: "+sig.course+".\n\n");

      }
    }

  }

  displayAllIntxns(map) {

    if (!this.intersectionsLoaded) return;

    if(CONFIG.debug.simulation) console.log("Displaying all intersections.\n\n");

    for (var int of this.intxns.values()) {

      int.displayIntersection(map);

    }

  }

  displayAllSignals(map) {

    if (!this.intersectionsLoaded) return;

    if(CONFIG.debug.simulation) console.log("Displaying all signals.\n\n");

    for (var int of this.intxns.values()) {

      int.displaySignals(map);

    }
  }

  setSignalState(intxnId, sigId, state, opacity) {

    // console.log(this.intxns.get(intxnId));

    this.intxns.get(intxnId).setSignalState(sigId, state, opacity);

  }

  displaySignal(intId, sigId, map) {

    this.intxns.get(intId).displaySignal(sigId, map);

  }


  // displaySignal() {
  //
  //   console.log("Display the state");
  //
  // }

  activateSignals(signalsArray) {

    var n = signalsArray.length;

    for (var i = 0; i < n; i ++) {

      this.setSignalState(signalsArray[i][0], signalsArray[i][1], STATE.ACTIVE, 0.5);

      // this.display();

    }

    // this.displayAllSignals();

  }
};


module.exports = Simulation;

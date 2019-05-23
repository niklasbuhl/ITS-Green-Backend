const Route = require('./route.js');
const Bicycle = require('./bicycle.js');

// -----------------------------------------------------------------------------
// Session
// -----------------------------------------------------------------------------

class Session {

  constructor(id) {

    console.log("Starting new Session.");
    // this.id = id;

    this.intxns = [];
    this.intxnCircles = new Map();

    // Next Signal
    this.nextIntxn = '';
    this.nextSignal = '';
    this.nextSignalSet = false;
    this.nextSignalNew = false;

    // Next Signal State
    this.nextSignalState = '';
    this.nextSignalStateNew = false;

    // Previous signal
    this.prevIntxn = '';
    this.prevSignal = '';
    this.prevSignalSet = false;

  }

  addRoute(id, pointArray, map) {

    this.route = new Route(id, pointArray);
    this.route.display(map);

  }

  addBicycle(bikeId, lat, lon, course, map) {

    this.bicycle = new Bicycle(bikeId, lat, lon, course);
    this.bicycle.display(map);

  }

  addSignals(signalsArray) {

    this.signals = signalsArray;

    var n = this.signals.length;

    for(var i = 0; i < n; i++) {

      console.log(this.signals[i]);

      this.intxns.push(this.signals[i][0]);

    }

  }

  listSignals() {

    console.log("Signals in this session.");

    var n = this.signals.length;

    for(var i = 0; i < n; i++) {

      console.log("Intersection["+this.signals[i][0]+"] Signal["+this.signals[i][1]+"]");

      console.log(this.signals[i]);

    }

  }

  displayIntersections(sim, map) {

    var n = this.intxns.length;

    for(var i = 0; i < n; i++) {

      var id = this.intxns[i];
      console.log(id);

      // console.log(sim.intxns.get(this.intxns[i]));

      var lat = sim.intxns.get(this.intxns[i]).loc.lat;
      var lon = sim.intxns.get(this.intxns[i]).loc.lon;

      console.log(lat);
      console.log(lon);

      // this.intxnCircles.push(L.circle([lat, lon], {
      //   opacity: 0.5,
      //   radius: 40
      // }).addTo(map));

      this.intxnCircles.set(id, (L.circle([lat, lon], {
        color: '#3388ff',
        opacity: 0.5,
        fillOpacity: 0.0,
        radius: 40
      }).addTo(map)));

    }
  }

  displayNextIntxn() {

    // if (!this.nextIntSet) this.nextInt = int;

    // Check if next is set
    if (!this.nextSignalSet) {
      console.log("No next signal set...");
      return;

    }

    // Update Displays
    if (this.nextSignalNew) {

      if (this.prevSignalSet) {
        // Reset previous
        this.intxnCircles.get(this.prevIntxn).setStyle({
          opacity: 0.5,
          fillOpacity: 0.0,
          color: '#3388ff'
        });
      }

      // Update next
      this.intxnCircles.get(this.nextIntxn).setStyle({
        opacity: 1,
        fillOpacity : 0.2,
        color: '#00FF00'
      });

      this.nextSignalNew = false;

    }

    // console.log(int);

    // console.log(this.intxnCircles.get(this.nextInt));


    // Update next int variable
    // this.nextInt = int;

    // Set next


    // this.nextIntSet = true;


  }

  setNextSignal(int, sig) {

    if (this.nextSignal != sig && this.nextInt != int) {

      // Store previous signal
      if (this.nextSignalSet) {
        this.prevIntxn = this.nextIntxn
        this.prevSignal = this.nextSignal
        this.prevSignalSet = true
      }

      // Set new next signal
      this.nextIntxn = int;
      this.nextSignal = sig;

      // Set flags
      this.nextSignalNew = true;
      this.nextSignalSet = true;

    } else {

      this.nextSignalNew = false;

    }

  }

};

module.exports = Session;

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
    this.nextInt = '';
    this.nextIntSet = false;

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

  displayNextIntxn(int) {

    if (!this.nextIntSet) this.nextInt = int;

    console.log(this.nextInt);
    console.log(int);

    console.log(this.intxnCircles.get(this.nextInt));

    // Reset previous
    this.intxnCircles.get(this.nextInt).setStyle({
      opacity: 0.5,
      fillOpacity: 0.0,
      color: '#3388ff'
    });

    // Update next int variable
    this.nextInt = int;

    // Set next
    this.intxnCircles.get(this.nextInt).setStyle({
      opacity: 1,
      fillOpacity : 0.2,
      color: '#00FF00'
    });

    this.nextIntSet = true;


  }

};

module.exports = Session;

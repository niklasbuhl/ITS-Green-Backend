const Signal = require('./signal.js');
// const Visualization = require('./javascript/visualization.js');

// -----------------------------------------------------------------------------
// Intersection
// -----------------------------------------------------------------------------

class Intersection {

  constructor(id, lat, lon) {

    if(CONFIG.debug.intersection) console.log("Creating new Intersection ["+id+"].");

    // Input variables
    this.id = id;
    this.loc = {lat: lat, lon: lon};
    this.marker = L.marker([this.loc.lat, this.loc.lon], {
      rotationAngle: 0,
      draggable: false
    });

    // Signals
    this.signals = new Map();

  }

  addSignal(id, course) {

    if (CONFIG.debug.intersection) console.log("Adding new signal to intersection.");

    this.signals.set(id, new Signal(this.id, id, course, this.loc));

  }

  displayIntersection(map) {

    this.marker.addTo(map);

  }

  displaySignals(map) {

    for (var sig of this.signals.values()) {

      sig.display(map);

    }
  }

  setSignalState(sigId, state, opacity) {

    // console.log(this.signals.get(sigId));

    this.signals.get(sigId).setState(state, opacity);


  }
};

module.exports = Intersection;

// const Visualization = require('./javascript/visualization.js');

// -----------------------------------------------------------------------------
// Signal
// -----------------------------------------------------------------------------

class Signal {

  constructor(intxnId, id, course, loc) {

    if(CONFIG.debug.signal) console.log("Creating new Signal ["+id+"].");

    // Input variables
    this.intxnId = intxnId;
    this.id = id;
    this.course = course;
    this.loc = loc;
    this.type = TYPE.CAR_S;
    this.color = STATE.INACTIVE;
    this.active = false;

    // Icon Marker
    this.marker = new L.marker([loc.lat, loc.lon], {
      icon : ICON.get(this.type).get(this.color),
      rotationAngle : this.course,
      opacity: 0.5
    });

  }

  setIcon(type) {

    this.type = type;

  }

  setState(state, opacity) {

    // console.log("name");

    // let param = {'intxnid' : this.intxnId, 'sigid' : this.id};
    //
    // $.get(API.sim.getSignalState, param, function(data) {
    //   console.log(data);
    // });

    this.marker.setOpacity(opacity);

    this.marker.setIcon(ICON.get(this.type).get(state));

  }

  display(map) {

    this.marker.addTo(map);

  }

};

module.exports = Signal;

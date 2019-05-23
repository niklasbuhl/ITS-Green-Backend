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
    this.state = STATE.INACTIVE;
    this.stateUpdate = true;
    this.active = false;
    this.opacity = 0.5;

    // Icon Marker
    this.marker = new L.marker([loc.lat, loc.lon], {
      icon : ICON.get(this.type).get(this.state),
      rotationAngle : this.course,
      opacity: this.opacity
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

    if (this.state != state) {

      this.stateUpdate = true
      this.state = state;
      this.opacity = opacity;

    }
  }

  display(map) {

    if (this.stateUpdate == true) {

      this.marker.setIcon(ICON.get(this.type).get(this.state));
      this.marker.setOpacity(this.opacity);
      this.marker.addTo(map);

      this.stateUpdate = false

    }
  }
};

module.exports = Signal;

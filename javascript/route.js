// -----------------------------------------------------------------------------
// Route
// -----------------------------------------------------------------------------

class Route {

  constructor(id, array) {

    // Input Variables
    console.log("Creating new Route ["+id+"].");
    this.id = id;

    // Route Variables
    this.route = array;
    // something to mark the route...
    // this.routeLoaded = false;
    // this.routeDisplayed = false;
    // this.routeUpdate = false;

    this.polyline = L.polyline(this.route, {color: 'blue'});

  }

  display(map) {

    this.polyline.addTo(map);

  }


};

module.exports = Route;

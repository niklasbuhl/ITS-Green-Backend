// -----------------------------------------------------------------------------
// Route
// -----------------------------------------------------------------------------

class Route {

  constructor(id, array) {

    // Input Variables
    console.log("Creating new Route ["+id+"]...");

    this.id = id;

    // Route Variables
    this.route = array;
    // something to mark the route...
    // this.routeLoaded = false;
    // this.routeDisplayed = false;
    // this.routeUpdate = false;

    this.polyline = L.polyline(this.route, {color: 'blue'});

    console.log("Created Route ["+id+"].");

  }

  display(map) {

    console.log("Displaying Route ["+this.id+"]...");

    this.polyline.addTo(map);

    console.log("Displayed Route ["+this.id+"].");

  }


};

module.exports = Route;

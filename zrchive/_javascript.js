require('leaflet-rotatedmarker') // https://github.com/bbecquet/Leaflet.RotatedMarker
var $ = require('jquery')

console.log("Hello, World! Version 5");

// Getting the base URL, for further use in the application
var protocol = window.location.protocol;
var host = window.location.host;
var baseURL = protocol + "//" + host;
// console.log(baseURL);

// DTU Ballerup 55.7315600, 12.3957664
var map = L.map('map-container').setView([55.73, 12.39], 13);

// Load the map
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibmlidWgiLCJhIjoiY2p1OXZ4ajdmMHZhZjN6cGR4NTZpajZzMiJ9.6dzIOnRPtBwMpYR7s29W9A'
}).addTo(map);

// The Application
var run;
var fps = 6;
var updateTimer = 1000 / fps; // 60 fps

// Intersection Variables
var intersections = [];
var intersectionsLoaded = false;
var intersectionsDisplayed = false;
var intersectionsUpdate = false;

class Intersection {
  constructor(id, lat, lon) {
    this.id = id;
    this.marker = L.marker([lat, lon], { rotationAngle: 0 });
  }
}

// Bicycle Variables
var bicycle = [];
var bicycleMarker = L.marker([55.73, 12.39], { rotationAngle: 0 }).addTo(map);
var bicycleCourse = 45;
var bicycleLoaded = false;
var bicycleDisplayed = false;
var bicycleUpdate = false;

class Bicycle {
  constructor(id) {
    this.marker = L.marker([55.73, 12.39], { rotationAngle: 0 }).addTo(map);
  }
}

// Route Variables
var route = [];
// something to mark the route...
var routeLoaded = false;
var routeDisplayed = false;
var routeUpdate = false;

// Signal Variables
var signals = [];
var signalMarkers = [];
var signalsLoaded = false;
var signalsDisplayed = false;
var signalsUpdate = false;

// The main setup function
function setup() {

  console.log("Starting setup...");

  loadIntersections();

  console.log("Starting Done!");

}

// The main run function
function loop() {

  // console.log("Running...");

  var d = new Date();
  var millis = d.getMilliseconds();

  // Update the intersections
  if(intersectionsLoaded) {
    if(!intersectionsDisplayed || intersectionsUpdate) {
      displayIntersections();
    }
  }

  // Update the signals
  if(signalsLoaded) {
    if(!signalsDisplayed || signalsUpdate) {
      displaySignals();
    }
  }

  // Update the bicycle with course and location
  updateBicycle();

  // Recursive
  run = setTimeout(loop, updateTimer);

}

function updateBicycle() {

  var d = new Date();
  var millis = d.getMilliseconds();

  bicycleCourse = millis % 360;
  // console.log(bicycleCourse);

  bicycleMarker.setRotationAngle(bicycleCourse);

}
// Update Intersection Signals

function updateSignals() {

}

function loadIntersections() {

  console.log("Getting intersection information...")

  intersectionsLoaded = false;

  try {

    getIntersections(function(data) {

      //console.log(data)

      intersectionsLoaded = true;

      // console.log("Hep");

      console.log("Got intersection information!")

      for(var intersection in data) {
        var id = data[intersection]['id']
        var lat = data[intersection]['lat']
        var lon = data[intersection]['lon']

        console.log("id: " + id + ". Lat: " + lat + ". Lon: " + lon + ".");

        var newIntersection = new Intersection(id, lat, lon);

        intersections.push(newIntersection);


      }



    });



  } catch(err) {
    console.log(err.message);
  }

}

function getIntersections(callback) {

  $.getJSON(baseURL + "/simulation/intersections/all", function(response) {
    // console.log("Response:" + response);
    callback(response);
  });

}

function displayIntersections() {

  console.log("Displaying signals")

  // console.log(intersections)

  for(var intersection in intersections) {
    console.log(intersections[intersection]['id'])
    intersections[intersection].marker.addTo(map);
  }

  intersectionsDisplayed = true;

}

// Signals
function getSignals() {}

function updateSignals() {}

function displaySignals() {}

// Route
function displayRoute() {}

// Utilities


// Setup and loop
setup();

loop();

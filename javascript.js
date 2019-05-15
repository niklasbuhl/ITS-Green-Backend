// Modules
require('leaflet-rotatedmarker'); // https://github.com/bbecquet/Leaflet.RotatedMarker

// jQuery
var $ = require('jquery');

var name = "Niklas";

// Get configuration
CONFIG = require('./json/frontendconfig.json');
API = require('./json/api.json');

// Simulation
const Signal = require('./javascript/signal.js');
const Intersection = require('./javascript/intersection.js');
const Simulation = require('./javascript/simulation.js');

// Session
const Bicycle = require('./javascript/bicycle.js');
const Route = require('./javascript/route.js');
const Session = require('./javascript/session.js');

// const Visualization = require('./javascript/visualization.js');

// -----------------------------------------------------------------------------
// Hello World
// -----------------------------------------------------------------------------

console.log("Hello, World! V0.0.1");

// -----------------------------------------------------------------------------
// Getting the base URL, for further use in the application
// -----------------------------------------------------------------------------

var protocol = window.location.protocol;
var host = window.location.host;
var baseURL = protocol + "//" + host;
if (CONFIG.debug.url) console.log(baseURL);

// -----------------------------------------------------------------------------
// Load the map
// -----------------------------------------------------------------------------

var map = L.map('map-container').setView([CONFIG.startLat, CONFIG.startLon], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: CONFIG.accessToken
}).addTo(map);

// -----------------------------------------------------------------------------
// Signal Icons
// -----------------------------------------------------------------------------

// var vis = new Visualization();

// if (CONFIG.debug.intersectioncolors) vis.displayIntersectionColors(map);

displayIntersectionColors(map);

// -----------------------------------------------------------------------------
// Bicycle Icons
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
// Intersection Icons
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
// Get data from backend
// -----------------------------------------------------------------------------

// function getJSON(path, callback) {
//
//   $.getJSON(path, function(response) {
//     // console.log("Response:" + response);
//     callback(response);
//   });
//
// }
//
// function get(path, callback) {
//
//   $.get(
//       path,
//       // {paramOne : 1, paramX : 'abc'},
//       {},
//       function(data) {
//          console.log('Data: ' + data);
//          callback(data);
//       }
//   );
//
// }


// -----------------------------------------------------------------------------
// Simulation
// -----------------------------------------------------------------------------

var sim = new Simulation();

var sesh = new Session();

// -----------------------------------------------------------------------------
// Setup
// -----------------------------------------------------------------------------

// Variables
// var runLoop;
// var updateTimer = 1000 / CONFIG.fps;
var setupDone = false;

function setup() {

  console.log("Starting setup...");

  var path = baseURL + API.sim.getIntxns.url;

  console.log("Intersections path: "+path+".")

  // get(path, function(data) {console.log(data);});

  $.get(path, function(data) {

    sim.loadIntersectionsAndSignals(data);

    // console.log(data);

    // sim.listAllIntersectionsAndSignals();

    // sim.displayAllIntxns(map);

    sim.displayAllSignals(map);

  });

  path = baseURL + API.session.getRoute.url;

  $.get(path, function(data) {

    console.log(data);

    sesh.addRoute('r01', data, map);

    // var polyline = L.polyline(data, {color: 'red'}).addTo(map);

  });

  path = baseURL + API.session.getSignals.url;

  $.get(path, function(data) {

    console.log(data);

    sesh.addSignals(data, map);

    sesh.listSignals();

    // Color all the signals blue
    sim.activateSignals(sesh.signals);

    sesh.displayIntersections(sim, map);

    sesh.displayNextIntxn('i09');

  });

  sesh.addBicycle('b01', 55.686584, 12.564102, 300, map);



  // get();
  // getJSON(baseURL + API.sim.getIntxns.url);

  console.log("Starting Done!");

}

// -----------------------------------------------------------------------------
// Get Data Loops
// -----------------------------------------------------------------------------

var getDataAllIntxnsLooper;
var getDataSessionSignalsLooper;
var getDataNextSignalLooper;
var getDataBicycleLooper;

function getAllIntxnsData() {

  console.log("Getting All Intersections Data");

  // // Update All Signals
  // if (sim.intersectionsLoaded) {
  //
  //   // sim.updateAllSignals();
  //
  //   for (var int of sim.intxns.values()) {
  //
  //     for (var sig of int.signals.values()) {
  //
  //       $.get(
  //         API.sim.getSignalState,
  //         {'intxnid' : int.id, 'sigid' : sig.id},
  //         function(data) {
  //
  //           sim.setSignalState(data.intId, data.sigId, data.state);
  //
  //       });
  //     }
  //   }
  // }

  getDataAllIntxnsLooper = setTimeout(getAllIntxnsData, CONFIG.loop.allIntxns.dataTimer);

}

// Update Session Signals Loop

function getSessionSignalsData() {

  console.log("Getting Session Signals Data");

  getDataSessionSignalsLooper = setTimeout(getSessionSignalsData, CONFIG.loop.sessionSignals.dataTimer);

}

// Update Next Signal Loop
function getNextSignalData() {

  console.log("Getting Next Signal Data");

  getDataNextSignalLooper = setTimeout(getNextSignalData, CONFIG.loop.bicycle.dataTimer);
}

// Bicycle Loop
function getBicycleData() {

  console.log("Getting Bicycle Data");

  $.get(
    API.session.getBicycle,
    // {'intxnid' : int.id, 'sigid' : sig.id},
    function(data) {

      console.log(data);
      // sim.setSignalState(data.intId, data.sigId, data.state);
      var time = data.time;
      var lat = data.latitude;
      var lon = data.longitude;
      var speed = data.speed;
      var course = data.course;

      sesh.bicycle.setData(time, lat, lon, course, speed);

  });

  getDataBicycleLooper = setTimeout(getBicycleData, CONFIG.loop.bicycle.dataTimer);

  setupDone = true;

}

// -----------------------------------------------------------------------------
// Display Loops
// -----------------------------------------------------------------------------

var updateBicycleLooper;

function updateBicycleLoop() {

  sesh.bicycle.update();

  updateBicycleLooper = setTimeout(updateBicycleLoop, CONFIG.loop.bicycle.updateTimer);

}


// -----------------------------------------------------------------------------
// Start Loops
// -----------------------------------------------------------------------------

function startLoops() {

  if (CONFIG.loop.allIntxns.run) {
    console.log("Starting All Intersections Loop");
    getAllIntxnsData();
  }

  if (CONFIG.loop.sessionSignals.run) {
    console.log("Starting Session Signals Loop");
    getSessionSignalsData();
  }

  if (CONFIG.loop.nextSignal.run) {
    console.log("Starting Next Signal Loop");
    getNextSignalData();
  }

  if (CONFIG.loop.bicycle.run) {
    console.log("Starting Bicycle Loop");
    getBicycleData();
    updateBicycleLoop();

  }

  // Looping
  // if (CONFIG.debug.looping) console.log("Looping'");
  // runLoop = setTimeout(loop, updateTimer);

}

// -----------------------------------------------------------------------------
// Execute
// -----------------------------------------------------------------------------

$(document).ready(setup());

while(!setupDone) {
  $(document).ready(startLoops());
}

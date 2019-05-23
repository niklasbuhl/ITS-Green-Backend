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

console.log("Creating Simulation and Session");

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

  console.log("S0.0 Starting setup...");

  var path = baseURL + API.sim.getIntxns.url;

  console.log("S1.0 Intersections path: "+path+".")

  // get(path, function(data) {console.log(data);});

  console.log("S1.2 Get intersections...")

  $.get(path, function(data) {

    console.log("S1.2 Got intersections!")

    sim.loadIntersectionsAndSignals(data);

    // console.log(data);

    // sim.listAllIntersectionsAndSignals();

    // sim.displayAllIntxns(map);

    console.log("S1.3 Display all signals (inactice).")

    sim.displayAllSignals(map);

  });

  path = baseURL + API.session.getRoute.url;

  console.log("S2.0 Session Route path: "+path+".")

  $.get(path, function(data) {

    console.log(data);

    sesh.addRoute('r01', data, map);

    // var polyline = L.polyline(data, {color: 'red'}).addTo(map);

  });

  path = baseURL + API.session.getSignals.url;

  console.log("S3.0 Session Signals path: "+path+".")

  $.get(path, function(data) {

    console.log("S3.1 - Get session signals...");

    // console.log(data);

    console.log("S3.2 - Add session signals...");

    sesh.addSignals(data, map);

    console.log("S3.3 - List session signals...");
    sesh.listSignals();

    console.log("S3.4 - Color all signals blue...");
    sim.activateSignals(sesh.signals);
    sim.displayAllSignals(map);

    console.log("S3.5 - Color all intersections blue...");
    sesh.displayIntersections(sim, map);

    // sesh.displayNextIntxn('i09');

    console.log("S3.6 - Got session signals!");

  });

  sesh.addBicycle('b01', 55.686584, 12.564102, 300, map);



  // get();
  // getJSON(baseURL + API.sim.getIntxns.url);

  console.log("Starting Done!");

  setupDone = true;

}

// -----------------------------------------------------------------------------
// Get Data Loops
// -----------------------------------------------------------------------------

var getDataSessionSignalsLooper;
var getNextSignalLooper;
var getNextSignalStateLooper;

var getDataBicycleLooper;

// Update Session Signals Loop
function getSessionSignalStates() {

  console.log("Getting Session Signals Data");

  getDataSessionSignalsLooper = setTimeout(getSessionSignalStates, CONFIG.loop.sessionSignals.dataTimer);

}

// Update Next Signal Loop
function getNextSignal() {

  $.get(
    API.session.getNextSignal,
    // ,
    function(data) {

      // console.log(data)

      // console.log("Next Signal Data")
      console.log("Get Next Signal");
      console.log(data[0]) // Int
      console.log(data[1]) // Sig

      sesh.setNextSignal(data[0], data[1]);

      sesh.displayNextIntxn();

  });

  getNextSignalLooper = setTimeout(getNextSignal, CONFIG.loop.nextSignal.dataTimer);

}

// Get next intersection data
function getNextSignalState() {

  $.get(
    API.session.getNextSignalState,
    // ,
    function(data) {

      console.log("Get Next Signal State");
      console.log(data);

      // sim.setSignalState(sesh.nextIntxn, sesh.nextSignal, data, 1);
      sim.setSignalState(sesh.nextIntxn, sesh.nextSignal, STATE.RED, 1);

      // console.log("Next Signal Data")
      // sim.intxns.get(sesh.nextIntxn).signals.get(sesh.nextSignal).setState(data, 1);

  });

  getNextSignalStateLooper = setTimeout(getNextSignalState, CONFIG.loop.nextSignal.dataTimer);

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
var displayNextSignalLooper;

function updateBicycleLoop() {

  sesh.bicycle.update();

  updateBicycleLooper = setTimeout(updateBicycleLoop, CONFIG.loop.bicycle.updateTimer);

}

function displayNextSignal() {

  console.log("Display Next Signal ["+sesh.nextIntxn+"]["+sesh.nextSignal+"]");

  // console.log(sim.intxns.get(sesh.nextIntxn))

  // sim.intxns.get(sesh.nextIntxn).signals.get(sesh.nextSignal).display(map);

  if (sesh.nextSignalSet) {
      sim.displaySignal(sesh.nextIntxn, sesh.nextSignal, map);
  }



  displayNextSignalLooper = setTimeout(displayNextSignal, CONFIG.loop.nextSignal.displayTimer);

}


// -----------------------------------------------------------------------------
// Start Loops
// -----------------------------------------------------------------------------

function startLoops() {

  console.log("Start Loops...")

  // if (CONFIG.loop.allIntxns.run) {
  //   console.log("Starting All Intersections Loop");
  //   getAllIntxnsData();
  // }
  //
  // if (CONFIG.loop.sessionSignals.run) {
  //   console.log("Starting Session Signals Loop");
  //   getSessionSignalsData();
  // }

  if (CONFIG.loop.nextSignal.run) {
    console.log("Starting Next Signal Loop");

    getNextSignal();
    getNextSignalState();

    displayNextSignal();

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

$(document).ready(startLoops());

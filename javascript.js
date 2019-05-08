require('leaflet-rotatedmarker') // https://github.com/bbecquet/Leaflet.RotatedMarker
var $ = require('jquery')

// Get configuration
CONFIG = require('./frontendconfig.json')

// Getting the base URL, for further use in the application
var protocol = window.location.protocol;
var host = window.location.host;
var baseURL = protocol + "//" + host;
// console.log(baseURL);

// DTU Ballerup 55.7315600, 12.3957664
var map = L.map('map-container').setView([CONFIG.startLat, CONFIG.startLon], 13);

// Load the map
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: CONFIG.accessToken
}).addTo(map);

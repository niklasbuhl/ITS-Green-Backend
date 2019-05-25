var $ = require('jquery');

API = require('./../json/api.json');

var getBicycleTargetSpeedAndColorLooper;
var getNextSignalStateAndTTGLooper;
var getAllSignalStatesAndTTGLooper;

function getBicycleTargetSpeedAndColor() {

  // console.log(API.session.getBicycleTargetSpeedAndColor.url);

  $.get(
    API.session.getBicycleTargetSpeedAndColor.url,
    // ,
    function(data) {

      // console.log(data);
      var red = data.deviceColor[0]
      if (red > 0) red = 127 + red

      var green = data.deviceColor[1];
      if (green > 0) green = 127 + data.deviceColor[1]/2;

      var blue = data.deviceColor[2]
      if (blue > 0) blue = 127 + blue

      console.log("["+red+", "+green+", "+blue+"]");



      // Replace newlines
      data.message = data.message.replace(/\n/g, '<br />');

      document.getElementById('color').style.backgroundColor = "rgb("+red+", "+green+", "+blue+")";

      document.getElementById('bicycle').innerHTML = data.message;

  });

  getNextSignalLooper = setTimeout(getBicycleTargetSpeedAndColor, 1000);

}

function getNextSignalStateAndTTG() {

  // console.log(API.session.getNextSignalStateAndTTG.url);

  $.get(
    API.session.getNextSignalStateAndTTG.url,
    // ,
    function(data) {

      // console.log(data);

      // Replace newlines
      data.message = data.message.replace(/\n/g, '<br />');

      document.getElementById('signal').innerHTML = data.message;

  });

  getNextSignalStateAndTTGLooper = setTimeout(getNextSignalStateAndTTG, 1000);

}

function getAllSignalStatesAndTTG() {

  console.log(API.sim.getAllSignalStatesAndTTG.url);

  $.get(
    API.sim.getAllSignalStatesAndTTG.url,
    // ,
    function(data) {

      // console.log(data);

      // Replace newlines
      data.message = data.message.replace(/\n/g, '<tr><th>');

      // Replace tabs
      data.message = data.message.replace(/\t/g, '</th><th>');

      table = "<table>" + data.message + "</table>"

      document.getElementById('all').innerHTML = table;

  });

  getAllSignalStatesAndTTGLooper = setTimeout(getAllSignalStatesAndTTG, 1000);

}

getBicycleTargetSpeedAndColor();
getNextSignalStateAndTTG();
getAllSignalStatesAndTTG();

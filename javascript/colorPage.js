var $ = require('jquery');

API = require('./../json/api.json');

var getBicycleTargetSpeedAndColorLooper;

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


      var speed = data.speed;

      speed = speed.toFixed(1);

      document.getElementById('speed').innerHTML = speed;

      var change = data.speedChange;

      change = change.toFixed(1);

      document.getElementById('speed-change').innerHTML = change;

  });

  getNextSignalLooper = setTimeout(getBicycleTargetSpeedAndColor, 1000);

}

getBicycleTargetSpeedAndColor();

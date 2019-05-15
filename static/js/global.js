// -----------------------------------------------------------------------------
// jQuery
// -----------------------------------------------------------------------------

// var $ = require('jquery');

// -----------------------------------------------------------------------------
// Icons
// -----------------------------------------------------------------------------

// var carRedStraightPNG = new Image();
// var carOrangeStraightPNG = new Image();
// var carGreenStraightPNG = new Image();
// var carYellowStraightPNG = new Image();
// var carGreyStraightPNG = new Image();
//
// carRedStraightPNG.src = "./static/media/car-red-straight.png";
// carOrangeStraightPNG.src = "./static/media/car-orange-straight.png";
// carGreenStraightPNG.src = "./static/media/car-green-straight.png";
// carYellowStraightPNG.src = "./static/media/car-yellow-straight.png";
// carGreyStraightPNG.src = "./static/media/car-grey-straight.png";

// -----------------------------------------------------------------------------
// Icons
// -----------------------------------------------------------------------------

var BicycleIcon = L.Icon.extend({
  options: {
    iconSize:   [40, 40],
    iconAnchor: [20, 20]
  }
}),
  bicycleIcon = new BicycleIcon({
    iconUrl:    './static/media/bicycle-icon.png'
  });

var CarStraightIcon = L.Icon.extend({
      options: {
        iconSize:     [100, 100],
        iconAnchor:   [72, 120]
      }
    }),

    carStraightIconRed = new CarStraightIcon({ iconUrl: './static/media/car-red-straight.png'}),
    carStraightIconOrange = new CarStraightIcon({ iconUrl: './static/media/car-orange-straight.png'}),
    carStraightIconGreen = new CarStraightIcon({ iconUrl: './static/media/car-green-straight.png'}),
    carStraightIconYellow = new CarStraightIcon({ iconUrl: './static/media/car-yellow-straight.png'}),
    carStraightIconGrey = new CarStraightIcon({ iconUrl: './static/media/car-grey-straight.png'}),
    carStraightIconBlue = new CarStraightIcon({ iconUrl: './static/media/car-blue-straight.png'}),

    CarRightIcon = L.Icon.extend({
      options: {
        iconSize:     [100, 100],
        iconAnchor:   [72, 120]
      }
    }),

    carRightIconRed = new CarRightIcon({ iconUrl: './static/media/car-red-right.png'}),
    carRightIconOrange = new CarRightIcon({ iconUrl: './static/media/car-orange-right.png'}),
    carRightIconGreen = new CarRightIcon({ iconUrl: './static/media/car-green-right.png'}),
    carRightIconYellow = new CarRightIcon({ iconUrl: './static/media/car-yellow-right.png'}),
    carRightIconGrey = new CarRightIcon({ iconUrl: './static/media/car-grey-right.png'}),
    carRightIconBlue = new CarRightIcon({ iconUrl: './static/media/car-blue-right.png'}),

    BicycleStraightIcon = L.Icon.extend({
      options: {
        iconSize:     [100, 100],
        iconAnchor:   [72, 120]
      }
    }),

    bicycleStraightIconRed = new BicycleStraightIcon({ iconUrl: './static/media/bicycle-red-straight.png'}),
    bicycleStraightIconOrange = new BicycleStraightIcon({ iconUrl: './static/media/bicycle-orange-straight.png'}),
    bicycleStraightIconGreen = new BicycleStraightIcon({ iconUrl: './static/media/bicycle-green-straight.png'}),
    bicycleStraightIconYellow = new BicycleStraightIcon({ iconUrl: './static/media/bicycle-yellow-straight.png'}),
    bicycleStraightIconGrey = new BicycleStraightIcon({ iconUrl: './static/media/bicycle-grey-straight.png'}),
    bicycleStraightIconBlue = new BicycleStraightIcon({ iconUrl: './static/media/bicycle-blue-straight.png'}),

    BicycleRightIcon = L.Icon.extend({
      options: {
        iconSize:     [100, 100],
        iconAnchor:   [72, 120]
      }
    }),

    bicycleRightIconRed = new BicycleRightIcon({ iconUrl: './static/media/bicycle-red-right.png'}),
    bicycleRightIconOrange = new BicycleRightIcon({ iconUrl: './static/media/bicycle-orange-right.png'}),
    bicycleRightIconGreen = new BicycleRightIcon({ iconUrl: './static/media/bicycle-green-right.png'}),
    bicycleRightIconYellow = new BicycleRightIcon({ iconUrl: './static/media/bicycle-yellow-right.png'}),
    bicycleRightIconGrey = new BicycleRightIcon({ iconUrl: './static/media/bicycle-grey-right.png'});
    bicycleRightIconBlue = new BicycleRightIcon({ iconUrl: './static/media/bicycle-blue-right.png'});

const TYPE = {
  CAR_S : 'CAR_S',
  CAR_R : 'CAR_R',
  BIKE_S : 'BIKE_S',
  BIKE_R : 'BIKE_R'
};

// STATE, STATE
const STATE = {
  RED: 'RED',
  ORANGE: 'ORANGE',
  GREEN: 'GREEN',
  YELLOW: 'YELLOW',
  INACTIVE: 'INACTIVE',
  ACTIVE: 'ACTIVE'
};

var CAR_S = new Map();

CAR_S.set(STATE.RED,    carStraightIconRed);
CAR_S.set(STATE.ORANGE, carStraightIconOrange);
CAR_S.set(STATE.GREEN,  carStraightIconGreen);
CAR_S.set(STATE.YELLOW, carStraightIconYellow);
CAR_S.set(STATE.INACTIVE,   carStraightIconGrey);
CAR_S.set(STATE.ACTIVE,   carStraightIconBlue);

var CAR_R = new Map();

CAR_R.set(STATE.RED,    carRightIconRed);
CAR_R.set(STATE.ORANGE, carRightIconOrange);
CAR_R.set(STATE.GREEN,  carRightIconGreen);
CAR_R.set(STATE.YELLOW, carRightIconYellow);
CAR_R.set(STATE.INACTIVE,   carRightIconGrey);
CAR_R.set(STATE.ACTIVE,   carRightIconBlue);

var BIKE_S = new Map();

BIKE_S.set(STATE.RED,     bicycleStraightIconRed);
BIKE_S.set(STATE.ORANGE,  bicycleStraightIconOrange);
BIKE_S.set(STATE.GREEN,   bicycleStraightIconGreen);
BIKE_S.set(STATE.YELLOW,  bicycleStraightIconYellow);
BIKE_S.set(STATE.INACTIVE,    bicycleStraightIconGrey);
BIKE_S.set(STATE.ACTIVE,    bicycleStraightIconBlue);

var BIKE_R = new Map();

BIKE_R.set(STATE.RED,     bicycleRightIconRed);
BIKE_R.set(STATE.ORANGE,  bicycleRightIconOrange);
BIKE_R.set(STATE.GREEN,   bicycleRightIconGreen);
BIKE_R.set(STATE.YELLOW,  bicycleRightIconYellow);
BIKE_R.set(STATE.INACTIVE,    bicycleRightIconGrey);
BIKE_R.set(STATE.ACTIVE,    bicycleRightIconBlue);

var ICON = new Map();

ICON.set(TYPE.CAR_S, CAR_S);
ICON.set(TYPE.CAR_R, CAR_R);
ICON.set(TYPE.BIKE_S, BIKE_S);
ICON.set(TYPE.BIKE_R, BIKE_R);

// -----------------------------------------------------------------------------
//
// -----------------------------------------------------------------------------

function displayIntersectionColors(map) {

  var carStraightRed = new L.marker([55.73, 12.39], {icon: carStraightIconRed, rotationAngle: 0}).addTo(map);
  var carStraightOrange = new L.marker([55.73, 12.39], {icon: carStraightIconOrange, rotationAngle: 60}).addTo(map);
  var carStraightGreen = new L.marker([55.73, 12.39], {icon: carStraightIconGreen, rotationAngle: 120}).addTo(map);
  var carStraightYellow = new L.marker([55.73, 12.39], {icon: carStraightIconYellow, rotationAngle: 180}).addTo(map);
  var carStraightGrey = new L.marker([55.73, 12.39], {icon: carStraightIconGrey, rotationAngle: 240}).addTo(map);
  var carStraightBlue = new L.marker([55.73, 12.39], {icon: carStraightIconBlue, rotationAngle: 300}).addTo(map);

  var carRightRed = new L.marker([55.73, 12.39], {icon: carRightIconRed, rotationAngle: 0}).addTo(map);
  var carRightOrange = new L.marker([55.73, 12.39], {icon: carRightIconOrange, rotationAngle: 60}).addTo(map);
  var carRightGreen = new L.marker([55.73, 12.39], {icon: carRightIconGreen, rotationAngle: 120}).addTo(map);
  var carRightYellow = new L.marker([55.73, 12.39], {icon: carRightIconYellow, rotationAngle: 180}).addTo(map);
  var carRightGrey = new L.marker([55.73, 12.39], {icon: carRightIconGrey, rotationAngle: 240}).addTo(map);
  var carRightBlue = new L.marker([55.73, 12.39], {icon: carRightIconBlue, rotationAngle: 300}).addTo(map);

  var bicycleStraightRed = new L.marker([55.73, 12.39], {icon: bicycleStraightIconRed, rotationAngle: 0}).addTo(map);
  var bicycleStraightOrange = new L.marker([55.73, 12.39], {icon: bicycleStraightIconOrange, rotationAngle: 60}).addTo(map);
  var bicycleStraightGreen = new L.marker([55.73, 12.39], {icon: bicycleStraightIconGreen, rotationAngle: 120}).addTo(map);
  var bicycleStraightYellow = new L.marker([55.73, 12.39], {icon: bicycleStraightIconYellow, rotationAngle: 180}).addTo(map);
  var bicycleStraightGrey = new L.marker([55.73, 12.39], {icon: bicycleStraightIconGrey, rotationAngle: 240}).addTo(map);
  var bicycleStraightBlue = new L.marker([55.73, 12.39], {icon: bicycleStraightIconBlue, rotationAngle: 300}).addTo(map);

  var bicycleRightRed = new L.marker([55.73, 12.39], {icon: bicycleRightIconRed, rotationAngle: 0}).addTo(map);
  var bicycleRightOrange = new L.marker([55.73, 12.39], {icon: bicycleRightIconOrange, rotationAngle: 60}).addTo(map);
  var bicycleRightGreen = new L.marker([55.73, 12.39], {icon: bicycleRightIconGreen, rotationAngle: 120}).addTo(map);
  var bicycleRightYellow = new L.marker([55.73, 12.39], {icon: bicycleRightIconYellow, rotationAngle: 180}).addTo(map);
  var bicycleRightGrey = new L.marker([55.73, 12.39], {icon: bicycleRightIconGrey, rotationAngle: 240}).addTo(map);
  var bicycleRightBlue = new L.marker([55.73, 12.39], {icon: bicycleRightIconBlue, rotationAngle: 300}).addTo(map);

}

// -----------------------------------------------------------------------------
// Get Data from Backend
// -----------------------------------------------------------------------------
//
// function getJSON(path, callback) {
//
//   $.getJSON(path,
//     param,
//     function(response) {
//     // console.log("Response:" + response);
//     callback(response);
//   });
//
// }
//
// function get(path, param, callback) {
//
//   $.get(
//       path,
//       // {paramOne : 1, paramX : 'abc'},
//       param,
//       function(data) {
//          console.log('Data: ' + data);
//          callback(data);
//       }
//   );
//}

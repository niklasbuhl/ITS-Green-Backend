// -----------------------------------------------------------------------------
// Visualization
// -----------------------------------------------------------------------------

class Visualization {

  constructor() {

    console.log("Starting new Visualization.");

    this.signalType = {
      "CAR_REG" : 0,
      "CAR_R" : 1,
      "BIKE_REG" : 2,
      "BIKE_R" : 3
    };

    this.signalColor = {
      "RED" : 0,
      "ORANGE" : 1,
      "GREEN" : 2,
      "YELLOW" : 3
    };

    this.CarStraightIcon = L.Icon.extend({
      options: {
        iconSize:     [100, 100],
        iconAnchor:   [72, 120]
      }
    });

    this.carStraightIconRed = new this.CarStraightIcon({ iconUrl: './static/media/car-red-straight.png'}),
    this.carStraightIconOrange = new this.CarStraightIcon({ iconUrl: './static/media/car-orange-straight.png'}),
    this.carStraightIconGreen = new this.CarStraightIcon({ iconUrl: './static/media/car-green-straight.png'}),
    this.carStraightIconYellow = new this.CarStraightIcon({ iconUrl: './static/media/car-yellow-straight.png'});


    this.CarRightIcon = L.Icon.extend({
      options: {
        iconSize:     [100, 100],
        iconAnchor:   [72, 120]
      }
    });

    this.carRightIconRed = new this.CarRightIcon({ iconUrl: './static/media/car-red-right.png'}),
    this.carRightIconOrange = new this.CarRightIcon({ iconUrl: './static/media/car-orange-right.png'}),
    this.carRightIconGreen = new this.CarRightIcon({ iconUrl: './static/media/car-green-right.png'}),
    this.carRightIconYellow = new this.CarRightIcon({ iconUrl: './static/media/car-yellow-right.png'});

    this.BicycleStraightIcon = L.Icon.extend({
      options: {
        iconSize:     [100, 100],
        iconAnchor:   [72, 120]
      }
    });

    this.bicycleStraightIconRed = new this.BicycleStraightIcon({ iconUrl: './static/media/bicycle-red-straight.png'}),
    this.bicycleStraightIconOrange = new this.BicycleStraightIcon({ iconUrl: './static/media/bicycle-orange-straight.png'}),
    this.bicycleStraightIconGreen = new this.BicycleStraightIcon({ iconUrl: './static/media/bicycle-green-straight.png'}),
    this.bicycleStraightIconYellow = new this.BicycleStraightIcon({ iconUrl: './static/media/bicycle-yellow-straight.png'});

    this.BicycleRightIcon = L.Icon.extend({
      options: {
        iconSize:     [100, 100],
        iconAnchor:   [72, 120]
      }
    });

    this.bicycleRightIconRed = new this.BicycleRightIcon({ iconUrl: './static/media/bicycle-red-right.png'}),
    this.bicycleRightIconOrange = new this.BicycleRightIcon({ iconUrl: './static/media/bicycle-orange-right.png'}),
    this.bicycleRightIconGreen = new this.BicycleRightIcon({ iconUrl: './static/media/bicycle-green-right.png'}),
    this.bicycleRightIconYellow = new this.BicycleRightIcon({ iconUrl: './static/media/bicycle-yellow-right.png'});

  }

  displayIntersectionColors(map) {

    var carStraightRed = L.marker([55.73, 12.39], {icon: this.carStraightIconRed, rotationAngle: 0}).addTo(map);
    var carStraightOrange = L.marker([55.73, 12.39], {icon: this.carStraightIconOrange, rotationAngle: 90}).addTo(map);
    var carStraightGreen = L.marker([55.73, 12.39], {icon: this.carStraightIconGreen, rotationAngle: 180}).addTo(map);
    var carStraightYellow = L.marker([55.73, 12.39], {icon: this.carStraightIconYellow, rotationAngle: 270}).addTo(map);

    var carRightRed = L.marker([55.73, 12.39], {icon: this.carRightIconRed, rotationAngle: 0}).addTo(map);
    var carRightOrange = L.marker([55.73, 12.39], {icon: this.carRightIconOrange, rotationAngle: 90}).addTo(map);
    var carRightGreen = L.marker([55.73, 12.39], {icon: this.carRightIconGreen, rotationAngle: 180}).addTo(map);
    var carRightYellow = L.marker([55.73, 12.39], {icon: this.carRightIconYellow, rotationAngle: 270}).addTo(map);

    var bicycleStraightRed = L.marker([55.73, 12.39], {icon: this.bicycleStraightIconRed, rotationAngle: 0}).addTo(map);
    var bicycleStraightOrange = L.marker([55.73, 12.39], {icon: this.bicycleStraightIconOrange, rotationAngle: 90}).addTo(map);
    var bicycleStraightGreen = L.marker([55.73, 12.39], {icon: this.bicycleStraightIconGreen, rotationAngle: 180}).addTo(map);
    var bicycleStraightYellow = L.marker([55.73, 12.39], {icon: this.bicycleStraightIconYellow, rotationAngle: 270}).addTo(map);

    var bicycleRightRed = L.marker([55.73, 12.39], {icon: this.bicycleRightIconRed, rotationAngle: 0}).addTo(map);
    var bicycleRightOrange = L.marker([55.73, 12.39], {icon: this.bicycleRightIconOrange, rotationAngle: 90}).addTo(map);
    var bicycleRightGreen = L.marker([55.73, 12.39], {icon: this.bicycleRightIconGreen, rotationAngle: 180}).addTo(map);
    var bicycleRightYellow = L.marker([55.73, 12.39], {icon: this.bicycleRightIconYellow, rotationAngle: 270}).addTo(map);

  }
};

module.exports = Visualization;

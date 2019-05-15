// -----------------------------------------------------------------------------
// Bicycle
// -----------------------------------------------------------------------------

class Bicycle {

  constructor(id, lat, lon, course, speed) {

    console.log("Creating new Bicycle.");

    // Input Variables
    this.id = id;

    this.lat = lat;
    this.nextLat = lat;
    this.incLat = 0;
    this.difLat = 0;

    this.lon = lon;
    this.nextLon = lon;
    this.incLon = 0;
    this.difLon = 0;

    this.cor = course;
    this.nextCor = course;
    this.incCor = 0;
    this.difCor = 0;

    this.speed = speed;
    this.lastUpdate = 0;

    // this.centerMarker = L.marker([lat, lon], {
    //   rotationAngle: course
    // });

    this.marker = L.marker([lat, lon], {
      icon: bicycleIcon,
      rotationAngle: course
    });

    console.log("Placing bicycle["+id+"]: ["+lat+", "+lon+"] heading "+course+".");

  }

  display(map) {
    console.log("Displaying Bicycle["+this.id+"].");
    this.marker.addTo(map);
    // this.centerMarker.addTo(map);
  }

  update() {

    // Get difference
    this.difLat = this.lat - this.nextLat;
    this.difLon = this.lon - this.nextLon;
    this.difCor = this.cor - this.nextCourse;

    // Continue
    var c = true;

    if (this.difLat == 0) { this.incLat = 0; } else { c = false; }
    if (this.difLon == 0) { this.incLon = 0; } else { c = false; }
    if (this.difCor == 0) { this.incCor = 0; } else { c = false; }

    if (c) { return; }

    // Update numbers
    this.cor = (this.cor + this.incCor) % 360;
    this.lat = this.lat + this.incLat;
    this.lon = this.lon + this.incLon;

    // Update Marker
    this.marker.setLatLng([this.lat, this.lon]);
    this.marker.setRotationAngle(this.course);

    // Make sure it does not go out of bounds.
    if (Math.abs(this.difLat) < Math.abs(this.incLat)) { this.incLat = this.difLab; }
    if (Math.abs(this.difLon) < Math.abs(this.incLon)) { this.incLon = this.difLon; }
    if (Math.abs(this.difCor) < Math.abs(this.incCor)) { this.incCor = this.difCor; }

  }

  setData(time, lat, lon, course, speed) {

    console.log("Updating bicycle!");
    var incrementCount = Math.ceil(CONFIG.loop.bicycle.dataTimer / CONFIG.loop.bicycle.updateTimer) - 1;
    if (incrementCount < 1) { incrementCount = 1; }
    console.log("incrementCount: " + incrementCount);

    this.lastUpdate = time;

    // Latitude
    this.nextLat = lat;
    this.difLat = this.nextLat - this.lat;
    this.incLat = this.difLat / incrementCount;

    console.log("Lat Now: " + this.lat);
    console.log("Lat Next: " + this.nextLat);
    console.log("Lat Dif: " + this.difLat);
    console.log("Lat Inc: " + this.incLat);

    // Longitude
    this.nextLon = lon;
    this.difLon = this.nextLon - this.lon;
    this.incLon = this.difLon / incrementCount;

    console.log("Lon Now: " + this.lon);
    console.log("Lon Next: " + this.nextLon);
    console.log("Lon Dif: " + this.difLon);
    console.log("Lon Inc: " + this.incLon);

    // Speed
    this.speed = speed;

    // Course
    this.nextCor = course;
    this.difCor = this.nextCor - this.cor;

    console.log("Cor Now: " + this.cor);
    console.log("Cor Next: " + this.nextCor);
    console.log("Cor Dif1: " + this.difCor);

    // If the change is more than 180, go the other way.
    if (this.difCor > 180) { this.difCor = 360 - this.difCor; }

    // If the change is less than -180, go the other way.
    if (this.difCor < -180) { this.difCor = -360 - this.difCor; }

    this.incCor = this.difCor / incrementCount;

    console.log("Cor Dif2: " + this.difCor);
    console.log("Cor Inc: " + this.incLon);


  }
};

module.exports = Bicycle;

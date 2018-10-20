var map;
var fireCircles = new Array();

function setMapOnLocation(location) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: location.latitude, lng: location.longitude },
        zoom: 20
    });

    createCircle(map, {lat: location.latitude, lng: location.longitude }, 50);
    createCircle(map, {lat: 42, lng: 23 }, 10000);

}

function initMap() {
    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      };
      
      var longt = 0, lat = 0;
      function success(pos) {
        setMapOnLocation(pos.coords);
        
        fireCircles.forEach(circle => {
            circle.addListener('click', function() {confirmFire(circle)});
        })
      }
      
      function error(err) {
        allert('There was an error while tyring to locate you. Check if you browser can give your location.');
        setMapOnLocation({'longtitude': 0, 'lattitude': 0});
      }
      
      navigator.geolocation.getCurrentPosition(success, error, options);
}


function confirmFire(circle) {
    console.log(circle.center.lat(), circle.center.lng());
    $("#confirmFireForm").modal();
}

/*
 * map -> GMap obj
 * center -> long and lat
 * raius -> IN METERS
 */
function createCircle(map, center, radius) {
    var circle  = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        center: center,
        radius: radius
    });
    fireCircles.push(circle);
}
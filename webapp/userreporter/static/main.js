var map;
var fireCircles = new Array();
var marker;

function setMapOnLocation(location) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: location.latitude, lng: location.longitude },
        zoom: 20,
        mapTypeId: 'satellite' 
    });

    $.ajax({
        type: "GET",
        url: '/get_fire',
        async: false,
        success: function(data) {
            console.log(data);
            data = JSON.parse(data)["data"];
            console.log(data);
            console.log(map)
            data.forEach(el => {
            createCircle(map, {lat: parseFloat(el[0]), lng: parseFloat(el[1])},
                         parseFloat(el[2]));
            });
        }
      });
    fireCircles.forEach(circle => {
        circle.addListener('click', function() {confirmFireModal(circle.center)});
    })
    enableMarkers();
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
      }
      
      function error(err) {
        allert('There was an error while tyring to locate you. Check if you browser can give your location.');
        setMapOnLocation({'longtitude': 0, 'latitude': 0});
      }
      navigator.geolocation.getCurrentPosition(success, error, options);
}


function confirmFireModal(position) {
    $("#position").val(position.lat() + "," + position.lng())
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

function enableMarkers() {
    google.maps.event.addListener(map, 'click', function(event) {
        placeMarker(event.latLng);
     });    
}

function placeMarker(location) {
    if(marker != undefined) {
        marker.setMap(null);
    }

    marker = new google.maps.Marker({
        position: location,
        map: map
    });
    marker.addListener('click', function(event) {
        reportFireModal(this.position);
    });
}

function removeCircle(position) {
    fireCircles.forEach(element => {
        if(element.center.lat() == position.latitude && element.center.lng() == position.longitude) {
            element.setMap(null);
        }
    })
}

function reportFireModal(position) {
    $("#position").val(position.lat() + "," + position.lng())
    $("#reportFire").modal();
}

function reportFire() {
    position = getLongLatOfClick();
    data = {
        'confermed': true,
        'lat': position.latitude,
        'lng': position.longitude
    } 
    
    postData("/fire_confirm", data, function() {})

    $("#reportFire").modal('hide');
}

function confirmFire(confermed) {
    position = getLongLatOfClick();
    data = {
        'confermed': confermed,
        'lat': position.latitude,
        'lng': position.longitude
    }

    if(!confermed) {
        removeCircle(position);
    }

    postData("/fire_confirm", data, function() {   })
    $("#confirmFireForm").modal('hide');
}

function getLongLatOfClick() {
    var res =  $("#position").val().split(",");
    return {'latitude': res[0], 'longitude': res[1] }
}

function postData(url, data, callback_func) {
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: callback_func
      });
}
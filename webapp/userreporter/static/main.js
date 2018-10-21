var map;
var fireCircles = new Array();
var activeMarkers = new Array();
var marker;

function setMapOnLocation(location) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: location.latitude, lng: location.longitude },
        zoom: 7,
        mapTypeId: 'satellite' 
    });
    console.log("Set map on location")
    $.ajax({
        type: "GET",
        url: '/get_fire',
        async: false,
        success: function(data) {
            data = JSON.parse(data)["data"];
            data.forEach(el => {
                if(parseFloat(el[4]) >= 0.3) {
                    createCircle(map, {lat: parseFloat(el[0]), lng: parseFloat(el[1])},
                         parseFloat(el[2]), el[3], parseFloat(el[4]));
                }
            });
        }
      });
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


function confirmFireModal(position, probability, area) {
    $("#position").val(position.lat() + "," + position.lng())
    $("#probability").html("Probability: " + parseInt(probability * 100) + "% Area: " + parseInt(area) + " meters square.")
    $("#confirmFireForm").modal();
}

/*
 * map -> GMap obj
 * center -> long and lat
 * raius -> IN METERS
 */
function createCircle(map, center, radius, active, probability) {
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
    console.log(active == "True")
    if(active == "True") {
        addActiveFireAnimation({latitude: center.lat, longitude: center.lng})
    }
    circle.addListener('click', function() {confirmFireModal(circle.center, probability, radius)});
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
    
    postData("/predict_fire", data, function(data) {
        positions = JSON.parse(data)["data"];
        console.log(positions)
        createCircle(map, {lat: parseFloat(positions[0]), lng: parseFloat(positions[1]),},
            parseFloat(positions[2]), "True",parseFloat(positions[3]));
    })

    $("#reportFire").modal('hide');
    marker.setMap(null); // remove temp marker
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
        removeActiveMarker(position);
    } else {
        addActiveFireAnimation(position)
    }

    postData("/fire_confirm", data, function() {   })
    $("#confirmFireForm").modal('hide');
}

function getLongLatOfClick() {
    var res =  $("#position").val().split(",");
    return {'latitude': res[0], 'longitude': res[1] }
}

function removeActiveMarker(position) {
    activeMarkers.forEach(element => {
        if(element.position.lat() == position.latitude && element.position.lng() == position.longitude) {
            element.setMap(null);
        }
    })
}

function addActiveFireAnimation(position) {
    console.log(position)
    var infowindow = new google.maps.InfoWindow({
        content: "<h3>Active fire reported by user!</h3>"
      });
    active_marker = new google.maps.Marker({
        map: map,
        draggable: true,
        animation: google.maps.Animation.DROP,
        position: {lat: parseFloat(position.latitude), lng: parseFloat(position.longitude)}
    });

    active_marker.setAnimation(google.maps.Animation.BOUNCE);
    active_marker.addListener('click', function() {
        infowindow.open(map, active_marker);
    });

    activeMarkers.push(active_marker);
}

function postData(url, data, callback_func) {
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: callback_func
      });
}
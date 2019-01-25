var map;
var fireCircles = new Array();
var activeMarkers = new Array();
var marker;


function setMapOnLocation(location) {
    console.log("Set map on location")
    map = new google.maps.Map(document.getElementById("map"), {
        center: {lat: location.latitude, lng: location.longitude },
        zoom: 7,
        mapTypeId: "satellite" 
    });

    $.ajax({
        type: "GET",
        url: "/get_fire",
        async: false,
        success: function(data) {
            data = JSON.parse(data)["data"];
            data.forEach(el => {
                createCircle(map, {lat: parseFloat(el[0]), lng: parseFloat(el[1])},
                parseFloat(el[2]), el[3], parseFloat(el[4]));
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

    function success(pos) {
        setMapOnLocation(pos.coords);
    }

    function error(err) {
        alert("There was an error while tyring to locate you. Check if you browser can give your location.");
        setMapOnLocation({"longitude": 0.0, "latitude": 0.0});
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
    color = "#FF0000";
    if (probability <= 0.3) {
        color = "#707070";
    }

    var circle  = new google.maps.Circle({
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.35,
        map: map,
        center: center,
        radius: radius
    });

    if (active == "True") {
        addActiveFireAnimation({latitude: center.lat, longitude: center.lng})
    }
    circle.addListener("click", function() {confirmFireModal(circle.center, probability, radius)});
    fireCircles.push(circle);
}

function enableMarkers() {
    google.maps.event.addListener(map, "click", function(event) {
        placeMarker(event.latLng);
    });    
}

function placeMarker(location) {
    if (marker != undefined) {
        marker.setMap(null);
    }

    marker = new google.maps.Marker({
        position: location,
        map: map
    });
    marker.addListener("click", function(event) {
        reportFireModal(this.position);
    });
}

function removeCircle(position) {
    fireCircles.forEach(element => {
        if(element.center.lat() == position.latitude && element.center.lng() == position.longitude) {
            element.setMap(null);
        }
    });
}

function reportFireModal(position) {
    $("#position").val(position.lat() + "," + position.lng());
    $("#reportFire").modal();
}

function reportFire() {
    position = getLongLatOfClick();
    data = {
        "confirmed": true,
        "lat": position.latitude,
        "lng": position.longitude
    };

    postData("/predict_fire", data, function(data) {
        positions = JSON.parse(data)["data"];
        createCircle(map, {lat: parseFloat(positions[0]), lng: parseFloat(positions[1]),},
            parseFloat(positions[2]), "True",parseFloat(positions[3]));
    });

    $("#reportFire").modal("hide");
    marker.setMap(null); // remove temp marker
}

function confirmFire(confirmed) {
    position = getLongLatOfClick();
    data = {
        "confirmed": confirmed,
        "lat": position.latitude,
        "lng": position.longitude
    };

    if (!confirmed) {
        removeCircle(position);
        removeActiveMarker(position);
    }else {
        addActiveFireAnimation(position);
    }

    postData("/fire_confirm", data, function() {   });
    $("#confirmFireForm").modal("hide");
}

function getLongLatOfClick() {
    var res =  $("#position").val().split(",");
    return {"latitude": res[0], "longitude": res[1]};
}

function removeActiveMarker(position) {
    activeMarkers.forEach(element => {
        if(element.position.lat() == position.latitude && element.position.lng() == position.longitude) {
            element.setMap(null);
        }
    });
}

function addActiveFireAnimation(position) {
    var infoWindow = new google.maps.InfoWindow({
        content: "<h3>Active fire reported by user!</h3>"
    });

    activeMarker = new google.maps.Marker({
        map: map,
        draggable: true,
        animation: google.maps.Animation.DROP,
        position: {lat: parseFloat(position.latitude), lng: parseFloat(position.longitude)}
    });

    activeMarker.setAnimation(google.maps.Animation.BOUNCE);
    activeMarker.addListener("click", function() {
        infoWindows.open(map, activeMarker);
    });

    activeMarkers.push(activeMarker);
}

function postData(url, data, callbackFunc) {
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: callbackFunc
      });
}

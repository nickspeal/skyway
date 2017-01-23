var map;
var marker = null;
var tracker = null;
var home = null;

function askForUserLocation(){
  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    function geoLocationSuccess(position){
      //console.log("lat: position.coords.latitude, ", lat: position.coords.latitude);
      //console.log("lng: position.coords.longitude, ", lng: position.coords.longitude);
      //var pos = {
      //  lat: position.coords.latitude,
      //  lng: position.coords.longitude
      //};
      var pos = {
          lat: -35.3400000,
          lng: 149.1640000
      };

      map.setCenter(pos)
      var homeImage = '/static/homeicon.png';
      var droneImage = '/static/droneicon.png';
      //console.log("home icon")
      //console.log("image.heigh: ", image.height, " & image.width: ", image.width)
      home = new google.maps.Marker({
          position: {lat: pos.lat, lng: pos.lng},
          map: map,
          icon: homeImage
      });
      tracker = new google.maps.Marker({
          position: {lat: pos.lat, lng: pos.lng},
          map: map,
          icon: droneImage
      });
      //console.log("here 5")
    }
    function geoLocationFailed(){
      console.error("Could not get user's location");
    }
    const options = {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    }
    navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationFailed, options );
  } else {
    console.error("Broweser does not support geolocation");
  }
}

function addListeners(){

  // On Click, remove all pins, add a pin, save location
  map.addListener('click', function(event) {
    //clear any existing marker
 
    if (marker !== null){
      marker.setMap(null);
    }
    //console.log("map clicked. Current pos: ", event.latLng);
    //console.log( "lat long: ", event.latLng.lat(), event.latLng.lng() );
    var targetImage = '/static/targeticon.png';
    marker = new google.maps.Marker({
      position: event.latLng,
      map: map,
      icon: targetImage
    });

    window.destination = [event.latLng.lng(), event.latLng.lat()];
    document.getElementById('goButton').disabled = false;
    document.getElementById('form').elements["latitude"].value=event.latLng.lat()
    document.getElementById('form').elements["longitude"].value=event.latLng.lng()
  })

}
function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 18
  });
  //onsole.log("here 3")
  askForUserLocation()
  addListeners()
}
function refreshData()
{
  x = 1;
  setTimeout(refreshData, x*1000);
  console.log("refreshing now");
  $.ajax({
    url: '/coordinates/',
    type: 'get',
    //dataType : 'json'
    success: function(data){
      var pos = jQuery.parseJSON(data)
      tracker.setMap(null);
      //console.log("pos: ", pos);
      //console.log("map.js: pos.lat: ", pos.lat, "pos.lon: ", pos.lon)
      //var pos = jQuery.parseJSON()
      tracker = new google.maps.Marker({
        position: {lat: pos.lat,lng: pos.lon},
        map: map
      });
    },
    failure: function(data){
      //alert('Got an error dude');
    }
  })
}
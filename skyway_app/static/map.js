var map;
var marker = null;

function askForUserLocation(){
  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    function geoLocationSuccess(position){
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      map.setCenter(pos)
      var image = '/static/homeicon.png';
      console.log("home icon")
      console.log("image.heigh: ", image.height, " & image.width: ", image.width)
      var homeIcon = new google.maps.Marker({
          position: {lat: pos.lat, lng: pos.lng},
          map: map,
          icon: image
      });
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
    console.log("map clicked. Current pos: ", event.latLng);
    console.log( "lat long: ", event.latLng.lat(), event.latLng.lng() );

    marker = new google.maps.Marker({
      position: event.latLng,
      map: map
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
  askForUserLocation()
  addListeners()
}
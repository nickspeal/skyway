var map;

function askForUserLocation(){
  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    function geoLocationSuccess(position){
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      map.setCenter(pos)
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
    //TODO remove all pins
    console.log("map clicked. Current pos: ", event.latLng);
    console.log( "lat long: ", event.latLng.lat(), event.latLng.lng() );
    
    const marker = new google.maps.Marker({
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
  askForUserLocation()
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 18
  });
  addListeners()
}
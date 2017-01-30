var map;
var marker = null;
var tracker = null;
var home = null;
var droneImage = null;

function addListeners(){

  // On Click, remove all pins, add a pin, save location
  map.addListener('click', function(event) {
    //clear any existing marker
 
    if (marker !== null){
      marker.setMap(null);
    }
    //console.log("map clicked. Current pos: ", event.latLng);
    //console.log( "lat long: ", event.latLng.lat(), event.latLng.lng() );
    var targetImage = 'skyway_app/static/targeticon.png';
    marker = new google.maps.Marker({
      position: event.latLng,
      map: map,
      icon: targetImage
    });

    map.setCenter(marker.getPosition().lat(), marker.getPostiion().lng());

  })
}


function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 18
  });
  //onsole.log("here 3")
  //askForUserLocation()
  addListeners()
}
var map;
var marker = null;
var tracker = null;
var home = null;

function askForUserLocation(){
  // Try HTML5 geolocation.
  /*if (navigator.geolocation) {
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
  */
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

    var bound = new google.maps.LatLngBounds();

    bound.extend(new google.maps.LatLng(home.getPosition().lat(),home.getPosition().lng()));
    bound.extend(new google.maps.LatLng(marker.getPosition().lat(),marker.getPosition().lng()));

    map.setCenter(bound.getCenter());

    window.destination = [event.latLng.lng(), event.latLng.lat()];
    document.getElementById('goButton').disabled = false;
    document.getElementById('form').elements["latitude"].value=event.latLng.lat()
    document.getElementById('form').elements["longitude"].value=event.latLng.lng()
  })
}

function getHomeCoordinates(){
  console.log("getting home coordinates");
  $.ajax({
    url: '/homecoordinates/',
    type: 'get',
    //dataType : 'json'
    success: function(data){
      var pos = jQuery.parseJSON(data)
      //console.log("pos: ", pos);
      //console.log("map.js: pos.lat: ", pos.lat, "pos.lon: ", pos.lon)
      //var pos = jQuery.parseJSON()

      var homeImage = '/static/homeicon.png';
      var droneImage = '/static/droneicon.png';
      home = new google.maps.Marker({
          position: {lat: pos.lat, lng: pos.lon},
          map: map,
          icon: homeImage
      });
      tracker = new google.maps.Marker({
          position: {lat: pos.lat, lng: pos.lon},
          map: map,
          icon: droneImage
      });
      var pos2 = {
        lat: pos.lat,
        lng: pos.lon
      };
      map.setCenter(pos2)

      //tracker.setMap(map);      
      //tracker.setPosition({lat: pos.lat,lng: pos.lon});
      //home.setMap(map);

      //home.setPosition({lat: pos.lat,lng: pos.lon});
    },
    failure: function(data){
      //alert('Got an error dude');
    }
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
  getHomeCoordinates()
}

function refreshData(){
  x = 2;
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
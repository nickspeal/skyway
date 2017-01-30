var map;
var marker = null;
var tracker = null;
var droneImage = null;
var pinger = null;
var home = null;

// On Click, remove all pins, add a pin, zoom map, save location
function newDestination(event){
  const destination = {
    lat: event.latLng.lat(),
    lng: event.latLng.lng()
  };
  
  // Create or move marker
  if (marker !== null){
    marker.setMap(null);
  }
  const targetImage = '/static/targeticon.png';
  marker = new google.maps.Marker({
    position: destination,
    map: map,
    icon: targetImage
  });

  // Update map zoom/center
  if (home){
    const bounds = new google.maps.LatLngBounds();
    bounds.extend(new google.maps.LatLng(home.getPosition().lat(),home.getPosition().lng()));
    bounds.extend(new google.maps.LatLng( destination.lat, destination.lng ));
    map.setCenter(bounds.getCenter());
  }
  // Save latlng to form for future submission
  document.getElementById('form').elements["latitude"].value=event.latLng.lat()
  document.getElementById('form').elements["longitude"].value=event.latLng.lng()
  // Enable Fly Button
  document.getElementById('FlyButton').disabled = false;
}

function getHomeCoordinates(){
  $.ajax({
    url: '/homecoordinates/',
    type: 'get',
    success: function(data){
      const homeLocation = jQuery.parseJSON(data)
      const homeImage = '/static/homeicon.png';
      const droneImage = '/static/droneicon.png';
      if (home !== null){
        home.setMap(null);
      }
      // Put home marker on the map:
      home = new google.maps.Marker({
          position: {lat: homeLocation.lat, lng: homeLocation.lng},
          map: map,
          icon: homeImage
      });
      map.setCenter(homeLocation)

    },
    error: function(data){
      //alert('Got an error dude');
    }
  })
}

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 18
  });
  // addListeners()
  map.addListener('click', newDestination);
}

function refreshData(){
  console.log(home.getPosition())
  console.log(home.getPosition().lat())
  if (home.getPosition().lat()===0){
    console.log("Nick is a douche")
    getHomeCoordinates();
  }
  droneImage = '/static/droneicon.png';
  $.ajax({
    url: '/coordinates/',
    type: 'get',
    //dataType : 'json'
    success: function(data){
      const telemetry = jQuery.parseJSON(data);
      // Update the drone marker on the map:
      if (tracker !== null){
        tracker.setMap(null);
      }
      tracker = new google.maps.Marker({
        position: {lat: telemetry.lat,lng: telemetry.lon},
        map: map,
        icon: droneImage
      });
      document.getElementById('elevation').innerHTML = telemetry.elevation ? telemetry.elevation.toFixed(1) : "Unknown";
      document.getElementById('speed').innerHTML = telemetry.speed ? telemetry.speed.toFixed(1) : "Unknown";
      document.getElementById('eta').innerHTML = telemetry.eta ? telemetry.eta.toFixed(1) : "Unknown";
      document.getElementById('mode').innerHTML = telemetry.mode
      document.getElementById('armable').innerHTML = telemetry.armable
    },
    error: function(data){
      clearInterval(pinger);
      console.error("error pinging coordinates")
      alert('Failure to get coordinates. Not trying anymore until you connect again.');
    }
  })
}

function connectDrone(){
    $.ajax({
    url: '/connect/',
    type: 'get',
    success: function(data){
      document.getElementById('connected').innerHTML = "Connected"
      getHomeCoordinates()
      const TELEMETRY_REFRESH_INTERVAL = .1; // Query interval in seconds
      pinger = setInterval(refreshData, TELEMETRY_REFRESH_INTERVAL*1000);
    },
    error: function(data){
      console.log("couldn't connect")
    }
  })
}
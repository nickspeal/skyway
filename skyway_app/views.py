from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.templatetags.static import static
import drone
import json

solo = drone.drone()
soloconnected = False

def index(request):  
  #print "here 1"
  context = {'time_estimate': '5', 'GOOGLE_API_KEY': 'AIzaSyBN-Q9c7O40j-z3TRcc3KFHRRcpP290s-8'}     
  #print "here 2"
  return render(request, 'skyway_app/index.html', context)

def connect(request):
  global soloconnected
  if soloconnected == False:
    solo.connectToDrone()
    soloconnected = True
  resp = None
  return HttpResponse(resp)

def go(request):
  lat = request.GET.get('latitude', None)
  lng = request.GET.get('longitude', None)
  alt = 20 # TODO would be nice to specify this in the UI
  speed = 15
  if lat == "" or lng == "":
    print "ERROR: BAD URL PARAMETERS"
  
  # takeoff returns after takeoff success
  if not solo.getArmed():
    solo.takeoff(alt)

  # flyTo returns after landing success.
  solo.flyTo(lat, lng, alt, speed)
  resp = "Arrived and landed."
  # resp = "Arrived and landed. <br> <a href=/rtl>Return Home</a>"   # Return home button for later
  return HttpResponse(resp)

def coordinates(request):
  #print solo
  lat = solo.getLat()
  lon = solo.getLng()
  elevation = solo.getElevation()
  speed = solo.getSpeed()
  eta = solo.getETA()
  mode = solo.getMode()
  armable = solo.isArmable()
  #print "home location, lat: ", lat, ". lon: ", lon, ". elevation: ", elevation, ". speed: ", speed, ". eta: ", eta
  data = {'lat':lat,'lon':lon,'elevation':elevation,'speed':speed,'eta':eta,'mode':mode, 'armable':armable}

  return HttpResponse(json.dumps(data))

def homecoordinates(request):
  lat = solo.getHomeLat()
  lng = solo.getHomeLng()

  data = {'lat':lat,'lng':lng}
  return HttpResponse(json.dumps(data))